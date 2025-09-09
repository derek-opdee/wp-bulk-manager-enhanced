<?php
/**
 * Plugin Name: WP Bulk Manager Client
 * Plugin URI: https://github.com/opdee/wp-bulk-manager
 * Description: WordPress bulk content management with REST API and plugin management
 * Version: 3.0.0
 * Author: Derek Zar
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class WP_Bulk_Manager_Client_Robust {
    
    private $version = '3.0.0';
    private $option_api_key = 'wpbm_api_key';
    private $option_allowed_ips = 'wpbm_allowed_ips';
    private $option_settings = 'wpbm_settings';
    private $plugin_manager;
    
    public function __construct() {
        // Plugin manager will be loaded on-demand when needed
        
        // Core hooks
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_enqueue_scripts', [$this, 'enqueue_admin_scripts']);
        
        // AJAX handlers
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
        add_action('wp_ajax_wpbm_save_allowed_ips', [$this, 'ajax_save_allowed_ips']);
        add_action('wp_ajax_wpbm_test_connection', [$this, 'ajax_test_connection']);
        add_action('wp_ajax_wpbm_get_current_settings', [$this, 'ajax_get_current_settings']);
        
        // Add custom REST API headers
        add_filter('rest_pre_serve_request', [$this, 'add_custom_headers'], 10, 3);
    }
    
    /**
     * Get plugin manager instance (loaded on-demand)
     */
    private function get_plugin_manager() {
        if ($this->plugin_manager === null) {
            $plugin_manager_file = plugin_dir_path(__FILE__) . 'includes/class-wpbm-plugin-manager.php';
            if (file_exists($plugin_manager_file)) {
                try {
                    require_once $plugin_manager_file;
                    if (class_exists('WPBM_Plugin_Manager')) {
                        $this->plugin_manager = new WPBM_Plugin_Manager();
                    }
                } catch (Exception $e) {
                    error_log('WPBM: Failed to load plugin manager: ' . $e->getMessage());
                    return false;
                }
            } else {
                return false;
            }
        }
        return $this->plugin_manager;
    }
    
    /**
     * Enqueue admin scripts with better error handling
     */
    public function enqueue_admin_scripts($hook) {
        if ('settings_page_wp-bulk-manager' !== $hook) {
            return;
        }
        
        wp_enqueue_script('wpbm-admin', plugin_dir_url(__FILE__) . 'assets/js/wpbm-admin.js', ['jquery'], $this->version, true);
        wp_localize_script('wpbm-admin', 'wpbm', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('wpbm_nonce'),
            'api_endpoint' => rest_url('wpbm/v1/'),
            'plugin_version' => $this->version
        ]);
    }
    
    /**
     * Add custom headers to REST responses
     */
    public function add_custom_headers($served, $result, $request) {
        if (strpos($request->get_route(), '/wpbm/v1') === 0) {
            header('X-WPBM-Version: ' . $this->version);
        }
        return $served;
    }
    
    /**
     * AJAX: Generate API key with validation
     */
    public function ajax_generate_api_key() {
        try {
            // Verify nonce
            if (!check_ajax_referer('wpbm_nonce', 'nonce', false)) {
                throw new Exception('Security check failed');
            }
            
            // Check permissions
            if (!current_user_can('manage_options')) {
                throw new Exception('Insufficient permissions');
            }
            
            // Get current values to preserve them
            $current_ips = get_option($this->option_allowed_ips, '');
            $current_settings = get_option($this->option_settings, []);
            
            // Generate new API key
            $api_key = $this->generate_secure_api_key();
            
            // Save ONLY the API key
            $saved = update_option($this->option_api_key, $api_key, false);
            
            if (!$saved) {
                throw new Exception('Failed to save API key');
            }
            
            // Verify other settings weren't affected
            if (get_option($this->option_allowed_ips, '') !== $current_ips) {
                update_option($this->option_allowed_ips, $current_ips);
            }
            
            // Log the action
            $this->log_action('api_key_generated', [
                'user_id' => get_current_user_id(),
                'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
            ]);
            
            wp_send_json_success([
                'api_key' => $api_key,
                'message' => 'API key generated successfully'
            ]);
            
        } catch (Exception $e) {
            wp_send_json_error([
                'message' => $e->getMessage()
            ]);
        }
    }
    
    /**
     * AJAX: Save allowed IPs with validation
     */
    public function ajax_save_allowed_ips() {
        try {
            // Verify nonce
            if (!check_ajax_referer('wpbm_nonce', 'nonce', false)) {
                throw new Exception('Security check failed');
            }
            
            // Check permissions
            if (!current_user_can('manage_options')) {
                throw new Exception('Insufficient permissions');
            }
            
            // Get and validate IPs
            $raw_ips = $_POST['allowed_ips'] ?? '';
            $validated_ips = $this->validate_ip_list($raw_ips);
            
            // Get current API key to preserve it
            $current_api_key = get_option($this->option_api_key, '');
            
            // Save ONLY the IPs
            $saved = update_option($this->option_allowed_ips, $validated_ips, false);
            
            if (!$saved && get_option($this->option_allowed_ips) !== $validated_ips) {
                throw new Exception('Failed to save IP addresses');
            }
            
            // Verify API key wasn't affected
            if (get_option($this->option_api_key, '') !== $current_api_key) {
                update_option($this->option_api_key, $current_api_key);
            }
            
            // Parse IPs for response
            $ip_list = array_filter(array_map('trim', explode("\n", $validated_ips)));
            
            wp_send_json_success([
                'message' => 'IP addresses saved successfully',
                'ip_count' => count($ip_list),
                'ips' => $ip_list
            ]);
            
        } catch (Exception $e) {
            wp_send_json_error([
                'message' => $e->getMessage()
            ]);
        }
    }
    
    /**
     * AJAX: Test connection
     */
    public function ajax_test_connection() {
        try {
            if (!check_ajax_referer('wpbm_nonce', 'nonce', false)) {
                throw new Exception('Security check failed');
            }
            
            if (!current_user_can('manage_options')) {
                throw new Exception('Insufficient permissions');
            }
            
            $api_key = get_option($this->option_api_key);
            
            if (empty($api_key)) {
                throw new Exception('No API key configured');
            }
            
            // Test the API internally
            $test_request = new WP_REST_Request('GET', '/wpbm/v1/content');
            $test_request->set_header('X-API-Key', $api_key);
            $test_request->set_query_params(['type' => 'page', 'limit' => 1]);
            
            $response = rest_do_request($test_request);
            
            if (is_wp_error($response)) {
                throw new Exception('API test failed: ' . $response->get_error_message());
            }
            
            $data = $response->get_data();
            
            wp_send_json_success([
                'message' => 'Connection successful',
                'posts_found' => count($data['posts'] ?? []),
                'api_version' => $this->version
            ]);
            
        } catch (Exception $e) {
            wp_send_json_error([
                'message' => $e->getMessage()
            ]);
        }
    }
    
    /**
     * AJAX: Get current settings
     */
    public function ajax_get_current_settings() {
        try {
            if (!check_ajax_referer('wpbm_nonce', 'nonce', false)) {
                throw new Exception('Security check failed');
            }
            
            if (!current_user_can('manage_options')) {
                throw new Exception('Insufficient permissions');
            }
            
            $api_key = get_option($this->option_api_key, '');
            $allowed_ips = get_option($this->option_allowed_ips, '');
            
            wp_send_json_success([
                'api_key' => $api_key,
                'allowed_ips' => $allowed_ips,
                'has_api_key' => !empty($api_key),
                'ip_count' => count(array_filter(explode("\n", $allowed_ips)))
            ]);
            
        } catch (Exception $e) {
            wp_send_json_error([
                'message' => $e->getMessage()
            ]);
        }
    }
    
    /**
     * Generate cryptographically secure API key
     */
    private function generate_secure_api_key() {
        // Try multiple methods for maximum compatibility
        if (function_exists('random_bytes')) {
            return bin2hex(random_bytes(16));
        } elseif (function_exists('openssl_random_pseudo_bytes')) {
            return bin2hex(openssl_random_pseudo_bytes(16));
        } else {
            // Fallback to WordPress password generator
            return wp_generate_password(32, false, false);
        }
    }
    
    /**
     * Validate IP address list
     */
    private function validate_ip_list($ip_string) {
        $lines = explode("\n", $ip_string);
        $valid_ips = [];
        
        foreach ($lines as $line) {
            $ip = trim($line);
            
            if (empty($ip)) {
                continue;
            }
            
            // Check for CIDR notation
            if (strpos($ip, '/') !== false) {
                list($ip_part, $cidr) = explode('/', $ip);
                if (filter_var($ip_part, FILTER_VALIDATE_IP) && is_numeric($cidr) && $cidr >= 0 && $cidr <= 32) {
                    $valid_ips[] = $ip;
                }
            } else {
                // Regular IP
                if (filter_var($ip, FILTER_VALIDATE_IP)) {
                    $valid_ips[] = $ip;
                }
            }
        }
        
        return implode("\n", $valid_ips);
    }
    
    /**
     * Log actions for debugging
     */
    private function log_action($action, $data = []) {
        if (defined('WP_DEBUG') && WP_DEBUG) {
            error_log(sprintf(
                '[WPBM] Action: %s | Data: %s | Time: %s',
                $action,
                json_encode($data),
                current_time('mysql')
            ));
        }
    }
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wpbm/v1';
        
        // Content endpoints
        register_rest_route($namespace, '/content', [
            [
                'methods' => WP_REST_Server::READABLE,
                'callback' => [$this, 'get_content'],
                'permission_callback' => [$this, 'verify_api_key'],
                'args' => [
                    'type' => [
                        'default' => 'post',
                        'sanitize_callback' => 'sanitize_text_field'
                    ],
                    'limit' => [
                        'default' => 100,
                        'sanitize_callback' => 'absint'
                    ],
                    'page' => [
                        'default' => 1,
                        'sanitize_callback' => 'absint'
                    ],
                    'status' => [
                        'default' => 'any',
                        'sanitize_callback' => 'sanitize_text_field'
                    ]
                ]
            ],
            [
                'methods' => WP_REST_Server::CREATABLE,
                'callback' => [$this, 'create_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ]
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            [
                'methods' => WP_REST_Server::READABLE,
                'callback' => [$this, 'get_single_content'],
                'permission_callback' => [$this, 'verify_api_key'],
                'args' => [
                    'id' => [
                        'validate_callback' => function($param) {
                            return is_numeric($param);
                        }
                    ]
                ]
            ],
            [
                'methods' => WP_REST_Server::EDITABLE,
                'callback' => [$this, 'update_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ],
            [
                'methods' => WP_REST_Server::DELETABLE,
                'callback' => [$this, 'delete_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ]
        ]);
        
        // Health check endpoint (no auth required)
        register_rest_route($namespace, '/health', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'health_check'],
            'permission_callback' => '__return_true'
        ]);
        
        // Plugin management endpoints (loaded on-demand)
        register_rest_route($namespace, '/plugins', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'handle_list_plugins_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/upload', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_upload_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/install-url', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_install_url_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/activate', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_activate_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/deactivate', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_deactivate_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/delete', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_delete_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/plugins/update', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handle_plugin_update_endpoint'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
    }
    
    /**
     * Verify API key with IP whitelist support
     */
    public function verify_api_key($request) {
        // Check API key
        $provided_key = $request->get_header('X-API-Key');
        
        if (empty($provided_key)) {
            return new WP_Error(
                'missing_api_key',
                'API key is required',
                ['status' => 401]
            );
        }
        
        $stored_key = get_option($this->option_api_key);
        
        if (empty($stored_key)) {
            return new WP_Error(
                'no_api_key_configured',
                'No API key configured in WordPress',
                ['status' => 401]
            );
        }
        
        // Timing-safe comparison
        if (!hash_equals($stored_key, $provided_key)) {
            return new WP_Error(
                'invalid_api_key',
                'Invalid API key',
                ['status' => 401]
            );
        }
        
        // Check IP whitelist
        $allowed_ips = get_option($this->option_allowed_ips, '');
        
        if (!empty($allowed_ips)) {
            $client_ip = $this->get_client_ip();
            
            if (!$this->is_ip_allowed($client_ip, $allowed_ips)) {
                return new WP_Error(
                    'ip_not_allowed',
                    'Your IP address is not allowed',
                    ['status' => 403]
                );
            }
        }
        
        return true;
    }
    
    /**
     * Get client IP address
     */
    private function get_client_ip() {
        $ip_keys = ['HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];
        
        foreach ($ip_keys as $key) {
            if (!empty($_SERVER[$key])) {
                $ips = explode(',', $_SERVER[$key]);
                $ip = trim($ips[0]);
                
                if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
                    return $ip;
                }
            }
        }
        
        return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    }
    
    /**
     * Check if IP is in allowed list
     */
    private function is_ip_allowed($client_ip, $allowed_ips_string) {
        $allowed_ips = array_filter(array_map('trim', explode("\n", $allowed_ips_string)));
        
        foreach ($allowed_ips as $allowed_ip) {
            if ($this->ip_in_range($client_ip, $allowed_ip)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Check if IP is in range (supports CIDR)
     */
    private function ip_in_range($ip, $range) {
        if (strpos($range, '/') === false) {
            return $ip === $range;
        }
        
        list($subnet, $bits) = explode('/', $range);
        $ip_decimal = ip2long($ip);
        $subnet_decimal = ip2long($subnet);
        $mask = -1 << (32 - $bits);
        
        return ($ip_decimal & $mask) === ($subnet_decimal & $mask);
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_options_page(
            'WP Bulk Manager',
            'Bulk Manager',
            'manage_options',
            'wp-bulk-manager',
            [$this, 'admin_page']
        );
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        $api_key = get_option($this->option_api_key, '');
        $allowed_ips = get_option($this->option_allowed_ips, '');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager</h1>
            
            <div id="wpbm-notices"></div>
            
            <!-- Status Overview -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">Status</h2>
                <div style="padding: 0 12px 12px;">
                    <p>
                        <strong>Plugin Version:</strong> <?php echo esc_html($this->version); ?><br>
                        <strong>API Status:</strong> 
                        <span id="api-status">
                            <?php echo $api_key ? '✅ Configured' : '❌ Not configured'; ?>
                        </span><br>
                        <strong>IP Restrictions:</strong> 
                        <span id="ip-status">
                            <?php 
                            $ip_count = count(array_filter(explode("\n", $allowed_ips)));
                            echo $ip_count > 0 ? "✅ {$ip_count} IPs allowed" : '⚠️ All IPs allowed';
                            ?>
                        </span>
                    </p>
                </div>
            </div>
            
            <!-- API Key Management -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">API Key Management</h2>
                <div style="padding: 0 12px 12px;">
                    <?php if ($api_key): ?>
                        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 15px;">
                            <input type="text" 
                                   id="api-key-field" 
                                   value="<?php echo esc_attr(substr($api_key, 0, 8) . '••••••••••••••••••••••••'); ?>" 
                                   data-full-key="<?php echo esc_attr($api_key); ?>"
                                   readonly 
                                   style="font-family: monospace; flex: 1; max-width: 400px;"
                                   title="Click to reveal full key">
                            <button type="button" class="button" id="reveal-api-key">👁️ Show</button>
                            <button type="button" class="button" id="copy-api-key">Copy</button>
                            <button type="button" class="button" id="regenerate-api-key">Regenerate</button>
                        </div>
                        <p class="description">
                            ⚠️ Keep this key secure. Regenerating will invalidate the current key immediately.
                        </p>
                    <?php else: ?>
                        <p>No API key has been generated yet.</p>
                        <button type="button" class="button button-primary" id="generate-api-key">
                            Generate API Key
                        </button>
                    <?php endif; ?>
                </div>
            </div>
            
            <!-- IP Whitelist -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">IP Address Whitelist</h2>
                <div style="padding: 0 12px 12px;">
                    <textarea id="allowed-ips-field" 
                              rows="5" 
                              style="width: 100%; max-width: 400px; font-family: monospace;"
                              placeholder="192.168.1.1&#10;10.0.0.0/24"><?php echo esc_textarea($allowed_ips); ?></textarea>
                    <p class="description">
                        Enter one IP address per line. Supports CIDR notation (e.g., 192.168.1.0/24).<br>
                        Leave empty to allow all IP addresses.
                    </p>
                    <button type="button" class="button button-primary" id="save-allowed-ips">
                        Save IP Addresses
                    </button>
                    <span id="ip-save-status" style="margin-left: 10px;"></span>
                </div>
            </div>
            
            <!-- Connection Test -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">Connection Test</h2>
                <div style="padding: 0 12px 12px;">
                    <p class="description">
                        Test the API connection to ensure everything is working correctly.
                    </p>
                    <p>
                        <button type="button" class="button button-primary" id="test-connection">Test Connection</button>
                        <span id="test-result" style="margin-left: 10px;"></span>
                    </p>
                </div>
            </div>
            
            <!-- Debug Information -->
            <?php if (defined('WP_DEBUG') && WP_DEBUG): ?>
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">Debug Information</h2>
                <div style="padding: 0 12px 12px;">
                    <p>
                        <strong>Your IP:</strong> <?php echo esc_html($this->get_client_ip()); ?><br>
                        <strong>PHP Version:</strong> <?php echo PHP_VERSION; ?><br>
                        <strong>WordPress Version:</strong> <?php echo get_bloginfo('version'); ?>
                    </p>
                </div>
            </div>
            <?php endif; ?>
        </div>
        
        <!-- Inline JavaScript (more reliable than separate file) -->
        <script>
        jQuery(document).ready(function($) {
            const ajaxUrl = '<?php echo admin_url('admin-ajax.php'); ?>';
            const nonce = '<?php echo wp_create_nonce('wpbm_nonce'); ?>';
            
            // Show notice
            function showNotice(message, type = 'success') {
                const $notices = $('#wpbm-notices');
                const noticeClass = type === 'error' ? 'notice-error' : 'notice-success';
                
                $notices.html(
                    `<div class="notice ${noticeClass} is-dismissible">
                        <p>${message}</p>
                        <button type="button" class="notice-dismiss"></button>
                    </div>`
                );
                
                // Handle dismiss button
                $notices.find('.notice-dismiss').on('click', function() {
                    $(this).parent().fadeOut();
                });
                
                // Auto dismiss success after 3 seconds
                if (type === 'success') {
                    setTimeout(() => {
                        $notices.find('.notice').fadeOut();
                    }, 3000);
                }
            }
            
            // Reveal/Hide API key
            let keyRevealed = false;
            $('#reveal-api-key').on('click', function() {
                const $button = $(this);
                const $field = $('#api-key-field');
                const fullKey = $field.data('full-key');
                const maskedKey = fullKey.substring(0, 8) + '••••••••••••••••••••••••';
                
                if (keyRevealed) {
                    // Hide key
                    $field.val(maskedKey);
                    $button.text('👁️ Show');
                    keyRevealed = false;
                } else {
                    // Show key
                    $field.val(fullKey);
                    $button.text('🙈 Hide');
                    keyRevealed = true;
                    
                    // Auto-hide after 10 seconds for security
                    setTimeout(() => {
                        if (keyRevealed) {
                            $field.val(maskedKey);
                            $button.text('👁️ Show');
                            keyRevealed = false;
                        }
                    }, 10000);
                }
            });
            
            // Copy API key
            $('#copy-api-key').on('click', function() {
                const $field = $('#api-key-field');
                const fullKey = $field.data('full-key');
                
                // Temporarily show full key for copying
                const currentValue = $field.val();
                $field.val(fullKey);
                $field.select();
                
                try {
                    document.execCommand('copy');
                    showNotice('API key copied to clipboard');
                } catch (err) {
                    showNotice('Please copy the API key manually', 'error');
                }
                
                // Restore masked view
                $field.val(currentValue);
            });
            
            // Generate/Regenerate API key
            $('#generate-api-key, #regenerate-api-key').on('click', function() {
                const isRegenerate = $(this).attr('id') === 'regenerate-api-key';
                
                if (isRegenerate) {
                    if (!confirm('Are you sure? The current API key will stop working immediately.')) {
                        return;
                    }
                }
                
                const $button = $(this);
                $button.prop('disabled', true).text('Generating...');
                
                $.post(ajaxUrl, {
                    action: 'wpbm_generate_api_key',
                    nonce: nonce
                }, function(response) {
                    if (response.success) {
                        // Show success message and reload to display masked key
                        showNotice('API key generated successfully! Page will reload to show the new key.');
                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showNotice(response.data.message || 'Failed to generate API key', 'error');
                        $button.prop('disabled', false).text(isRegenerate ? 'Regenerate' : 'Generate API Key');
                    }
                }).fail(function() {
                    showNotice('Network error. Please try again.', 'error');
                    $button.prop('disabled', false).text(isRegenerate ? 'Regenerate' : 'Generate API Key');
                });
            });
            
            // Save allowed IPs
            $('#save-allowed-ips').on('click', function() {
                const $button = $(this);
                const $status = $('#ip-save-status');
                const ips = $('#allowed-ips-field').val();
                
                $button.prop('disabled', true).text('Saving...');
                $status.text('');
                
                $.post(ajaxUrl, {
                    action: 'wpbm_save_allowed_ips',
                    allowed_ips: ips,
                    nonce: nonce
                }, function(response) {
                    if (response.success) {
                        showNotice(response.data.message);
                        $status.html('<span style="color: green;">✓ Saved</span>');
                        
                        // Update status display
                        const ipCount = response.data.ip_count;
                        $('#ip-status').html(
                            ipCount > 0 
                                ? `✅ ${ipCount} IPs allowed` 
                                : '⚠️ All IPs allowed'
                        );
                    } else {
                        showNotice(response.data.message || 'Failed to save IPs', 'error');
                        $status.html('<span style="color: red;">✗ Failed</span>');
                    }
                    
                    $button.prop('disabled', false).text('Save IP Addresses');
                }).fail(function() {
                    showNotice('Network error. Please try again.', 'error');
                    $status.html('<span style="color: red;">✗ Network error</span>');
                    $button.prop('disabled', false).text('Save IP Addresses');
                });
            });
            
            // Test connection
            $('#test-connection').on('click', function() {
                const $button = $(this);
                const $result = $('#test-result');
                
                $button.prop('disabled', true).text('Testing...');
                $result.text('');
                
                $.post(ajaxUrl, {
                    action: 'wpbm_test_connection',
                    nonce: nonce
                }, function(response) {
                    if (response.success) {
                        $result.html('<span style="color: green;">✓ ' + response.data.message + '</span>');
                    } else {
                        $result.html('<span style="color: red;">✗ ' + (response.data.message || 'Test failed') + '</span>');
                    }
                    
                    $button.prop('disabled', false).text('Test Connection');
                }).fail(function() {
                    $result.html('<span style="color: red;">✗ Network error</span>');
                    $button.prop('disabled', false).text('Test Connection');
                });
            });
        });
        </script>
        <?php
    }
    
    // REST API callbacks
    public function get_content($request) {
        $params = $request->get_params();
        
        $args = [
            'post_type' => $params['type'],
            'posts_per_page' => min($params['limit'], 500), // Cap at 500
            'paged' => $params['page'],
            'post_status' => $params['status']
        ];
        
        $query = new WP_Query($args);
        $posts = [];
        
        foreach ($query->posts as $post) {
            $posts[] = $this->format_post($post);
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages,
            'page' => $params['page'],
            'limit' => $params['limit']
        ];
    }
    
    public function get_single_content($request) {
        $post_id = $request->get_param('id');
        $post = get_post($post_id);
        
        if (!$post) {
            return new WP_Error('not_found', 'Content not found', ['status' => 404]);
        }
        
        return $this->format_post($post, true);
    }
    
    public function create_content($request) {
        $params = $request->get_json_params();
        
        if (empty($params['title']) && empty($params['content'])) {
            return new WP_Error('invalid_data', 'Title or content is required', ['status' => 400]);
        }
        
        $post_data = [
            'post_title' => sanitize_text_field($params['title'] ?? ''),
            'post_content' => wp_kses_post($params['content'] ?? ''),
            'post_type' => sanitize_key($params['type'] ?? 'post'),
            'post_status' => sanitize_key($params['status'] ?? 'draft')
        ];
        
        $post_id = wp_insert_post($post_data, true);
        
        if (is_wp_error($post_id)) {
            return new WP_Error('create_failed', $post_id->get_error_message(), ['status' => 500]);
        }
        
        return [
            'id' => $post_id,
            'message' => 'Content created successfully',
            'link' => get_permalink($post_id)
        ];
    }
    
    public function update_content($request) {
        $post_id = $request->get_param('id');
        $params = $request->get_json_params();
        
        if (!get_post($post_id)) {
            return new WP_Error('not_found', 'Content not found', ['status' => 404]);
        }
        
        $post_data = ['ID' => $post_id];
        
        if (isset($params['title'])) {
            $post_data['post_title'] = sanitize_text_field($params['title']);
        }
        
        if (isset($params['content'])) {
            $post_data['post_content'] = wp_kses_post($params['content']);
        }
        
        if (isset($params['status'])) {
            $post_data['post_status'] = sanitize_key($params['status']);
        }
        
        $result = wp_update_post($post_data, true);
        
        if (is_wp_error($result)) {
            return new WP_Error('update_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        return [
            'id' => $post_id,
            'message' => 'Content updated successfully',
            'link' => get_permalink($post_id)
        ];
    }
    
    public function delete_content($request) {
        $post_id = $request->get_param('id');
        
        if (!get_post($post_id)) {
            return new WP_Error('not_found', 'Content not found', ['status' => 404]);
        }
        
        $result = wp_delete_post($post_id, true);
        
        if (!$result) {
            return new WP_Error('delete_failed', 'Failed to delete content', ['status' => 500]);
        }
        
        return [
            'message' => 'Content deleted successfully'
        ];
    }
    
    public function health_check($request) {
        return [
            'status' => 'healthy',
            'version' => $this->version,
            'time' => current_time('mysql'),
            'php_version' => PHP_VERSION,
            'wp_version' => get_bloginfo('version')
        ];
    }
    
    private function format_post($post, $full = false) {
        $data = [
            'id' => $post->ID,
            'title' => $post->post_title,
            'slug' => $post->post_name,
            'type' => $post->post_type,
            'status' => $post->post_status,
            'date' => $post->post_date,
            'modified' => $post->post_modified,
            'link' => get_permalink($post->ID)
        ];
        
        if ($full) {
            $data['content'] = $post->post_content;
            $data['excerpt'] = $post->post_excerpt;
            $data['author'] = get_the_author_meta('display_name', $post->post_author);
            $data['featured_media'] = get_post_thumbnail_id($post->ID);
        }
        
        return $data;
    }
    
    // Plugin management endpoint wrappers (load plugin manager on-demand)
    
    public function handle_list_plugins_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_list_plugins($request);
    }
    
    public function handle_plugin_upload_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_upload($request);
    }
    
    public function handle_plugin_install_url_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_install_from_url($request);
    }
    
    public function handle_plugin_activate_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_activate($request);
    }
    
    public function handle_plugin_deactivate_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_deactivate($request);
    }
    
    public function handle_plugin_delete_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_delete($request);
    }
    
    public function handle_plugin_update_endpoint($request) {
        $plugin_manager = $this->get_plugin_manager();
        if (!$plugin_manager) {
            return new WP_Error('plugin_manager_unavailable', 'Plugin management is not available', ['status' => 503]);
        }
        return $plugin_manager->handle_plugin_update($request);
    }
}

// Initialize the plugin
function wpbm_init_plugin() {
    try {
        new WP_Bulk_Manager_Client_Robust();
    } catch (Exception $e) {
        error_log('WPBM: Plugin initialization failed: ' . $e->getMessage());
        add_action('admin_notices', function() use ($e) {
            echo '<div class="notice notice-error"><p>WP Bulk Manager failed to initialize: ' . esc_html($e->getMessage()) . '</p></div>';
        });
    }
}

// Plugin activation
register_activation_hook(__FILE__, function() {
    // Check PHP version
    if (version_compare(PHP_VERSION, '7.4', '<')) {
        deactivate_plugins(plugin_basename(__FILE__));
        wp_die('WP Bulk Manager requires PHP 7.4 or higher. You are running PHP ' . PHP_VERSION);
    }
    
    // Create options with defaults
    add_option('wpbm_api_key', '');
    add_option('wpbm_allowed_ips', '');
    add_option('wpbm_settings', []);
});

// Plugin deactivation
register_deactivation_hook(__FILE__, function() {
    // Clean up if needed
});

// Initialize
add_action('plugins_loaded', 'wpbm_init_plugin');