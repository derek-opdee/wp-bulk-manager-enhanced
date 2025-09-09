<?php
/**
 * Security Handler for WP Bulk Manager
 * 
 * @package WPBulkManager
 */

if (!defined('ABSPATH')) {
    exit;
}

class WPBM_Security {
    
    private $rate_limits = [
        'content' => ['limit' => 100, 'window' => 3600],
        'bulk' => ['limit' => 10, 'window' => 3600],
        'search-replace' => ['limit' => 5, 'window' => 3600]
    ];
    
    /**
     * Verify API request
     */
    public function verify_request($request) {
        // Check API key
        if (!$this->verify_api_key($request)) {
            return false;
        }
        
        // Check IP whitelist
        if (!$this->verify_ip_whitelist()) {
            return false;
        }
        
        // Check rate limits
        if (!$this->check_rate_limit($request)) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Verify API key
     */
    private function verify_api_key($request) {
        $provided_key = $request->get_header('X-API-Key');
        
        if (empty($provided_key)) {
            return false;
        }
        
        $stored_key = get_option('wpbm_api_key');
        
        if (empty($stored_key)) {
            return false;
        }
        
        return hash_equals($stored_key, $provided_key);
    }
    
    /**
     * Verify IP whitelist
     */
    private function verify_ip_whitelist() {
        $allowed_ips = get_option('wpbm_allowed_ips', '');
        
        // If no IPs configured, allow all
        if (empty($allowed_ips)) {
            return true;
        }
        
        $client_ip = $this->get_client_ip();
        $allowed = array_map('trim', explode("\n", $allowed_ips));
        
        // Check exact match or CIDR range
        foreach ($allowed as $allowed_ip) {
            if ($this->ip_in_range($client_ip, $allowed_ip)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Check rate limiting
     */
    private function check_rate_limit($request) {
        $route = $request->get_route();
        $client_ip = $this->get_client_ip();
        
        // Determine rate limit key
        $limit_key = 'content';
        if (strpos($route, 'search-replace') !== false) {
            $limit_key = 'search-replace';
        } elseif (strpos($route, 'bulk') !== false) {
            $limit_key = 'bulk';
        }
        
        $limits = $this->rate_limits[$limit_key];
        $transient_key = 'wpbm_rate_' . md5($client_ip . $limit_key);
        
        // Get current count
        $current = get_transient($transient_key);
        
        if ($current === false) {
            // First request
            set_transient($transient_key, 1, $limits['window']);
            return true;
        }
        
        if ($current >= $limits['limit']) {
            // Rate limit exceeded
            return false;
        }
        
        // Increment counter
        set_transient($transient_key, $current + 1, $limits['window']);
        return true;
    }
    
    /**
     * Generate secure API key
     */
    public function generate_api_key() {
        return wp_generate_password(32, false);
    }
    
    /**
     * Get client IP address
     */
    private function get_client_ip() {
        $ip_keys = ['HTTP_CF_CONNECTING_IP', 'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];
        
        foreach ($ip_keys as $key) {
            if (isset($_SERVER[$key]) && filter_var($_SERVER[$key], FILTER_VALIDATE_IP)) {
                return $_SERVER[$key];
            }
        }
        
        return '0.0.0.0';
    }
    
    /**
     * Check if IP is in range
     */
    private function ip_in_range($ip, $range) {
        if (strpos($range, '/') === false) {
            // Single IP
            return $ip === $range;
        }
        
        // CIDR notation
        list($subnet, $bits) = explode('/', $range);
        $ip_decimal = ip2long($ip);
        $subnet_decimal = ip2long($subnet);
        $mask = -1 << (32 - $bits);
        $subnet_decimal &= $mask;
        
        return ($ip_decimal & $mask) == $subnet_decimal;
    }
    
    /**
     * Log security events
     */
    public function log_security_event($event_type, $details = []) {
        $log_entry = [
            'timestamp' => current_time('mysql'),
            'event' => $event_type,
            'ip' => $this->get_client_ip(),
            'details' => $details
        ];
        
        // Store in options table (could be improved with custom table)
        $logs = get_option('wpbm_security_logs', []);
        
        // Keep only last 1000 entries
        if (count($logs) > 1000) {
            $logs = array_slice($logs, -1000);
        }
        
        $logs[] = $log_entry;
        update_option('wpbm_security_logs', $logs);
    }
}