<?php
/**
 * API Manager - Handles connections to multiple WordPress sites
 */
class WP_Bulk_Manager_API_Manager {
    
    private $encryption_key;
    private $timeout = 30;
    
    public function __construct() {
        $this->encryption_key = get_option('wp_bulk_manager_encryption_key');
        $this->timeout = get_option('wp_bulk_manager_timeout', 30);
    }
    
    /**
     * Test connection to a WordPress site
     */
    public function test_connection($site_url, $username, $password) {
        $response = $this->make_request($site_url, 'users/me', 'GET', [], $username, $password);
        
        if (is_wp_error($response)) {
            return [
                'success' => false,
                'message' => $response->get_error_message()
            ];
        }
        
        return [
            'success' => true,
            'user' => $response,
            'message' => 'Connection successful'
        ];
    }
    
    /**
     * Create content on remote site
     */
    public function create_content($site_id, $content_type, $data) {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        $endpoint = $content_type === 'post' ? 'posts' : 'pages';
        
        return $this->make_request(
            $site->site_url,
            $endpoint,
            'POST',
            $data,
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Update content on remote site
     */
    public function update_content($site_id, $content_type, $content_id, $data) {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        $endpoint = $content_type === 'post' ? "posts/$content_id" : "pages/$content_id";
        
        return $this->make_request(
            $site->site_url,
            $endpoint,
            'POST',
            $data,
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Get content from remote site
     */
    public function get_content($site_id, $content_type = 'post', $params = []) {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        $endpoint = $content_type === 'post' ? 'posts' : 'pages';
        
        return $this->make_request(
            $site->site_url,
            $endpoint,
            'GET',
            $params,
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Delete content from remote site
     */
    public function delete_content($site_id, $content_type, $content_id, $force = false) {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        $endpoint = $content_type === 'post' ? "posts/$content_id" : "pages/$content_id";
        $params = ['force' => $force];
        
        return $this->make_request(
            $site->site_url,
            $endpoint,
            'DELETE',
            $params,
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Get plugins from remote site
     */
    public function get_plugins($site_id) {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        return $this->make_request(
            $site->site_url,
            'plugins',
            'GET',
            [],
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Update plugin on remote site
     */
    public function update_plugin($site_id, $plugin, $action = 'update') {
        $site = $this->get_site($site_id);
        if (!$site) {
            return new WP_Error('site_not_found', 'Site not found');
        }
        
        $data = ['status' => $action === 'activate' ? 'active' : 'inactive'];
        
        return $this->make_request(
            $site->site_url,
            "plugins/$plugin",
            'POST',
            $data,
            $site->username,
            $this->decrypt_password($site->app_password)
        );
    }
    
    /**
     * Make API request
     */
    private function make_request($site_url, $endpoint, $method = 'GET', $data = [], $username = '', $password = '') {
        $url = trailingslashit($site_url) . 'wp-json/wp/v2/' . $endpoint;
        
        $args = [
            'method' => $method,
            'timeout' => $this->timeout,
            'headers' => [
                'Authorization' => 'Basic ' . base64_encode($username . ':' . $password),
                'Content-Type' => 'application/json'
            ]
        ];
        
        if (!empty($data) && in_array($method, ['POST', 'PUT', 'PATCH'])) {
            $args['body'] = json_encode($data);
        } elseif (!empty($data) && $method === 'GET') {
            $url = add_query_arg($data, $url);
        }
        
        $response = wp_remote_request($url, $args);
        
        if (is_wp_error($response)) {
            return $response;
        }
        
        $body = wp_remote_retrieve_body($response);
        $code = wp_remote_retrieve_response_code($response);
        
        if ($code >= 400) {
            $error_data = json_decode($body, true);
            $message = isset($error_data['message']) ? $error_data['message'] : 'Unknown error';
            return new WP_Error('api_error', $message, ['status' => $code, 'response' => $error_data]);
        }
        
        return json_decode($body, true);
    }
    
    /**
     * Get site from database
     */
    private function get_site($site_id) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_sites';
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM $table_name WHERE id = %d", $site_id));
    }
    
    /**
     * Encrypt password for storage
     */
    public function encrypt_password($password) {
        if (!$this->encryption_key) {
            return base64_encode($password);
        }
        
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
        $encrypted = openssl_encrypt($password, 'aes-256-cbc', $this->encryption_key, 0, $iv);
        return base64_encode($encrypted . '::' . $iv);
    }
    
    /**
     * Decrypt password from storage
     */
    private function decrypt_password($encrypted_password) {
        if (!$this->encryption_key) {
            return base64_decode($encrypted_password);
        }
        
        list($encrypted_data, $iv) = explode('::', base64_decode($encrypted_password), 2);
        return openssl_decrypt($encrypted_data, 'aes-256-cbc', $this->encryption_key, 0, $iv);
    }
    
    /**
     * Get all sites
     */
    public function get_all_sites($status = 'active') {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_sites';
        
        if ($status === 'all') {
            return $wpdb->get_results("SELECT * FROM $table_name ORDER BY site_name");
        }
        
        return $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM $table_name WHERE status = %s ORDER BY site_name",
            $status
        ));
    }
    
    /**
     * Add new site
     */
    public function add_site($site_data) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_sites';
        
        // Test connection first
        $test = $this->test_connection(
            $site_data['site_url'],
            $site_data['username'],
            $site_data['app_password']
        );
        
        if (!$test['success']) {
            return new WP_Error('connection_failed', $test['message']);
        }
        
        // Encrypt password
        $site_data['app_password'] = $this->encrypt_password($site_data['app_password']);
        
        $result = $wpdb->insert($table_name, $site_data);
        
        if ($result === false) {
            return new WP_Error('db_error', 'Failed to save site');
        }
        
        return $wpdb->insert_id;
    }
    
    /**
     * Update site
     */
    public function update_site($site_id, $site_data) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_sites';
        
        // If password is provided, encrypt it
        if (isset($site_data['app_password']) && !empty($site_data['app_password'])) {
            $site_data['app_password'] = $this->encrypt_password($site_data['app_password']);
        }
        
        return $wpdb->update($table_name, $site_data, ['id' => $site_id]);
    }
    
    /**
     * Delete site
     */
    public function delete_site($site_id) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_sites';
        
        return $wpdb->delete($table_name, ['id' => $site_id]);
    }
}