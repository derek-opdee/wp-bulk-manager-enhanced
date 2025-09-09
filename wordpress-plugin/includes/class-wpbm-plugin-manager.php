<?php
/**
 * Plugin Manager for WP Bulk Manager
 * 
 * @package WPBulkManager
 */

if (!defined('ABSPATH')) {
    exit;
}

class WPBM_Plugin_Manager {
    
    /**
     * Check if current request has plugin management permissions
     * For API requests, this is already verified by API key authentication
     */
    private function has_plugin_permissions() {
        // If this is a REST API request with valid API key, grant permissions
        if (defined('REST_REQUEST') && REST_REQUEST) {
            return true; // API key was already verified to reach this point
        }
        
        // For regular WordPress admin, check user capabilities
        return current_user_can('install_plugins');
    }
    
    /**
     * Create upgrader skin dynamically after classes are loaded
     */
    private function create_upgrader_skin() {
        // Ensure all classes are loaded first
        $this->load_wp_upgrader_classes();
        
        // Create anonymous class that extends WP_Upgrader_Skin
        return new class extends WP_Upgrader_Skin {
            private $messages = [];
            
            public function feedback($string, ...$args) {
                if (isset($args[0])) {
                    $string = vsprintf($string, $args);
                }
                $this->messages[] = $string;
            }
            
            public function header() {
                // No output
            }
            
            public function footer() {
                // No output
            }
            
            public function error($errors) {
                if (is_string($errors)) {
                    $this->messages[] = 'Error: ' . $errors;
                } elseif (is_wp_error($errors)) {
                    $this->messages[] = 'Error: ' . $errors->get_error_message();
                }
            }
            
            public function get_messages() {
                return $this->messages;
            }
        };
    }
    
    /**
     * Load WordPress upgrader classes when needed
     */
    private function load_wp_upgrader_classes() {
        // Load core files first
        if (!function_exists('request_filesystem_credentials')) {
            require_once ABSPATH . 'wp-admin/includes/file.php';
        }
        if (!function_exists('get_plugin_data')) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        if (!function_exists('plugins_api')) {
            require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
        }
        
        // Load upgrader classes in correct order
        if (!class_exists('WP_Upgrader_Skin')) {
            require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader-skin.php';
        }
        if (!class_exists('WP_Upgrader')) {
            require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
        }
        if (!class_exists('Plugin_Upgrader')) {
            require_once ABSPATH . 'wp-admin/includes/class-plugin-upgrader.php';
        }
        if (!class_exists('Plugin_Installer_Skin')) {
            require_once ABSPATH . 'wp-admin/includes/class-plugin-installer-skin.php';
        }
        
        // Load additional dependencies
        if (!function_exists('wp_tempnam')) {
            require_once ABSPATH . 'wp-admin/includes/file.php';
        }
        if (!function_exists('download_url')) {
            require_once ABSPATH . 'wp-admin/includes/file.php';
        }
    }
    
    /**
     * Handle plugin upload and installation
     */
    public function handle_plugin_upload($request) {
        // For API requests, permission is handled by API key verification
        // We simulate admin capabilities for valid API requests
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to install plugins', ['status' => 403]);
        }
        
        // Get the uploaded file from the request
        $files = $request->get_file_params();
        
        if (empty($files['plugin_file'])) {
            return new WP_Error('no_file', 'No plugin file uploaded', ['status' => 400]);
        }
        
        $uploaded_file = $files['plugin_file'];
        
        // Verify it's a zip file
        if ($uploaded_file['type'] !== 'application/zip' && !preg_match('/\.zip$/i', $uploaded_file['name'])) {
            return new WP_Error('invalid_file_type', 'Plugin must be a ZIP file', ['status' => 400]);
        }
        
        // Load WordPress upgrader classes
        $this->load_wp_upgrader_classes();
        
        // Load additional required files
        if (!function_exists('get_plugin_data')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin.php');
        }
        if (!function_exists('plugins_api')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin-install.php');
        }
        
        // Create custom upgrader skin to capture output
        $skin = $this->create_upgrader_skin();
        
        // Create plugin upgrader
        $upgrader = new Plugin_Upgrader($skin);
        
        // Install the plugin
        $result = $upgrader->install($uploaded_file['tmp_name']);
        
        if (is_wp_error($result)) {
            return new WP_Error('installation_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        // Get plugin info
        $plugin_info = $upgrader->plugin_info();
        
        if (!$plugin_info) {
            return new WP_Error('plugin_info_not_found', 'Could not retrieve plugin information', ['status' => 500]);
        }
        
        // Get plugin data
        $plugin_data = get_plugin_data(WP_PLUGIN_DIR . '/' . $plugin_info);
        
        return [
            'success' => true,
            'plugin_file' => $plugin_info,
            'plugin_data' => [
                'name' => $plugin_data['Name'],
                'version' => $plugin_data['Version'],
                'author' => $plugin_data['Author'],
                'description' => $plugin_data['Description']
            ],
            'messages' => $skin->get_messages(),
            'installed' => true,
            'activated' => false
        ];
    }
    
    /**
     * Install plugin from URL
     */
    public function handle_plugin_install_from_url($request) {
        // Check permissions
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to install plugins', ['status' => 403]);
        }
        
        $params = $request->get_json_params();
        $plugin_url = $params['url'] ?? '';
        
        if (empty($plugin_url)) {
            return new WP_Error('no_url', 'Plugin URL is required', ['status' => 400]);
        }
        
        // Validate URL
        if (!filter_var($plugin_url, FILTER_VALIDATE_URL)) {
            return new WP_Error('invalid_url', 'Invalid plugin URL', ['status' => 400]);
        }
        
        // Load WordPress upgrader classes
        $this->load_wp_upgrader_classes();
        
        // Load additional required files
        if (!function_exists('get_plugin_data')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin.php');
        }
        if (!function_exists('plugins_api')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin-install.php');
        };
        
        // Create custom upgrader skin
        $skin = $this->create_upgrader_skin();
        
        // Create plugin upgrader
        $upgrader = new Plugin_Upgrader($skin);
        
        // Install from URL
        $result = $upgrader->install($plugin_url);
        
        if (is_wp_error($result)) {
            return new WP_Error('installation_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        // Get plugin info
        $plugin_info = $upgrader->plugin_info();
        
        if (!$plugin_info) {
            return new WP_Error('plugin_info_not_found', 'Could not retrieve plugin information', ['status' => 500]);
        }
        
        // Get plugin data
        $plugin_data = get_plugin_data(WP_PLUGIN_DIR . '/' . $plugin_info);
        
        return [
            'success' => true,
            'plugin_file' => $plugin_info,
            'plugin_data' => [
                'name' => $plugin_data['Name'],
                'version' => $plugin_data['Version'],
                'author' => $plugin_data['Author'],
                'description' => $plugin_data['Description']
            ],
            'messages' => $skin->get_messages(),
            'installed' => true,
            'activated' => false
        ];
    }
    
    /**
     * Activate plugin
     */
    public function handle_plugin_activate($request) {
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to activate plugins', ['status' => 403]);
        }
        
        $params = $request->get_json_params();
        $plugin_file = $params['plugin_file'] ?? '';
        
        if (empty($plugin_file)) {
            return new WP_Error('no_plugin', 'Plugin file is required', ['status' => 400]);
        }
        
        // Activate the plugin
        $result = activate_plugin($plugin_file);
        
        if (is_wp_error($result)) {
            return new WP_Error('activation_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        return [
            'success' => true,
            'plugin_file' => $plugin_file,
            'activated' => true,
            'message' => 'Plugin activated successfully'
        ];
    }
    
    /**
     * Deactivate plugin
     */
    public function handle_plugin_deactivate($request) {
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to deactivate plugins', ['status' => 403]);
        }
        
        $params = $request->get_json_params();
        $plugin_file = $params['plugin_file'] ?? '';
        
        if (empty($plugin_file)) {
            return new WP_Error('no_plugin', 'Plugin file is required', ['status' => 400]);
        }
        
        // Deactivate the plugin
        deactivate_plugins($plugin_file);
        
        return [
            'success' => true,
            'plugin_file' => $plugin_file,
            'activated' => false,
            'message' => 'Plugin deactivated successfully'
        ];
    }
    
    /**
     * Delete plugin
     */
    public function handle_plugin_delete($request) {
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to delete plugins', ['status' => 403]);
        }
        
        $params = $request->get_json_params();
        $plugin_file = $params['plugin_file'] ?? '';
        
        if (empty($plugin_file)) {
            return new WP_Error('no_plugin', 'Plugin file is required', ['status' => 400]);
        }
        
        // Delete the plugin
        $result = delete_plugins([$plugin_file]);
        
        if (is_wp_error($result)) {
            return new WP_Error('deletion_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        return [
            'success' => true,
            'plugin_file' => $plugin_file,
            'deleted' => true,
            'message' => 'Plugin deleted successfully'
        ];
    }
    
    /**
     * Get list of all plugins
     */
    public function handle_list_plugins($request) {
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to view plugins', ['status' => 403]);
        }
        
        // Force check for plugin updates if requested
        $force_check = $request->get_param('force_update_check');
        if ($force_check) {
            // Clear the update transient to force a fresh check
            delete_site_transient('update_plugins');
            
            // Load necessary functions for update check
            if (!function_exists('wp_update_plugins')) {
                require_once ABSPATH . 'wp-includes/update.php';
            }
            
            // Safely trigger update check
            try {
                wp_update_plugins();
            } catch (Exception $e) {
                // If update check fails, continue without it
                error_log('WPBM: Plugin update check failed: ' . $e->getMessage());
            }
        }
        
        // Get all plugins
        $all_plugins = get_plugins();
        $active_plugins = get_option('active_plugins', []);
        $update_plugins = get_site_transient('update_plugins');
        
        $plugins = [];
        
        foreach ($all_plugins as $plugin_file => $plugin_data) {
            $is_active = in_array($plugin_file, $active_plugins);
            
            // Check if update is available
            $update_available = false;
            $update_version = null;
            
            if (isset($update_plugins->response[$plugin_file])) {
                $update_available = true;
                $update_version = $update_plugins->response[$plugin_file]->new_version;
            }
            
            $plugins[] = [
                'plugin_file' => $plugin_file,
                'name' => $plugin_data['Name'],
                'version' => $plugin_data['Version'],
                'author' => $plugin_data['Author'],
                'description' => $plugin_data['Description'],
                'active' => $is_active,
                'update_available' => $update_available,
                'update_version' => $update_version,
                'network' => $plugin_data['Network'],
                'requires_wp' => $plugin_data['RequiresWP'],
                'requires_php' => $plugin_data['RequiresPHP']
            ];
        }
        
        return [
            'plugins' => $plugins,
            'total' => count($plugins),
            'active_count' => count($active_plugins)
        ];
    }
    
    /**
     * Update plugin
     */
    public function handle_plugin_update($request) {
        if (!$this->has_plugin_permissions()) {
            return new WP_Error('insufficient_permissions', 'You do not have permission to update plugins', ['status' => 403]);
        }
        
        $params = $request->get_json_params();
        $plugin_file = $params['plugin_file'] ?? '';
        
        if (empty($plugin_file)) {
            return new WP_Error('no_plugin', 'Plugin file is required', ['status' => 400]);
        }
        
        // Load WordPress upgrader classes
        $this->load_wp_upgrader_classes();
        
        // Load additional required files
        if (!function_exists('get_plugin_data')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin.php');
        }
        if (!function_exists('plugins_api')) {
            require_once(ABSPATH . 'wp-admin/includes/plugin-install.php');
        };
        
        // Create custom upgrader skin
        $skin = $this->create_upgrader_skin();
        
        // Create plugin upgrader
        $upgrader = new Plugin_Upgrader($skin);
        
        // Update the plugin
        $result = $upgrader->upgrade($plugin_file);
        
        if (is_wp_error($result)) {
            return new WP_Error('update_failed', $result->get_error_message(), ['status' => 500]);
        }
        
        return [
            'success' => true,
            'plugin_file' => $plugin_file,
            'messages' => $skin->get_messages(),
            'updated' => true
        ];
    }
}
