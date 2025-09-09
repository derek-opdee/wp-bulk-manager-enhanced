<?php
/**
 * Admin functionality
 */
class WP_Bulk_Manager_Admin {
    
    private $plugin_name;
    private $version;
    private $api_manager;
    
    public function __construct($plugin_name, $version) {
        $this->plugin_name = $plugin_name;
        $this->version = $version;
        
        require_once WP_BULK_MANAGER_PATH . 'includes/class-api-manager.php';
        $this->api_manager = new WP_Bulk_Manager_API_Manager();
    }
    
    /**
     * Register admin styles
     */
    public function enqueue_styles() {
        wp_enqueue_style(
            $this->plugin_name,
            WP_BULK_MANAGER_URL . 'admin/css/admin.css',
            [],
            $this->version
        );
    }
    
    /**
     * Register admin scripts
     */
    public function enqueue_scripts() {
        wp_enqueue_script(
            $this->plugin_name,
            WP_BULK_MANAGER_URL . 'admin/js/admin.js',
            ['jquery'],
            $this->version,
            true
        );
        
        wp_localize_script($this->plugin_name, 'wp_bulk_manager', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('wp_bulk_manager_nonce'),
            'strings' => [
                'confirm_delete' => __('Are you sure you want to delete this site?', 'wp-bulk-manager'),
                'testing_connection' => __('Testing connection...', 'wp-bulk-manager'),
                'connection_success' => __('Connection successful!', 'wp-bulk-manager'),
                'connection_failed' => __('Connection failed:', 'wp-bulk-manager')
            ]
        ]);
    }
    
    /**
     * AJAX handler for testing connection
     */
    public function ajax_test_connection() {
        check_ajax_referer('wp_bulk_manager_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die(__('Insufficient permissions', 'wp-bulk-manager'));
        }
        
        $site_url = sanitize_url($_POST['site_url']);
        $username = sanitize_text_field($_POST['username']);
        $password = $_POST['app_password']; // Don't sanitize passwords
        
        $result = $this->api_manager->test_connection($site_url, $username, $password);
        
        wp_send_json($result);
    }
    
    /**
     * AJAX handler for processing templates
     */
    public function ajax_process_template() {
        check_ajax_referer('wp_bulk_manager_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die(__('Insufficient permissions', 'wp-bulk-manager'));
        }
        
        // Process template logic here
        wp_send_json_success(['message' => 'Template processed']);
    }
    
    /**
     * AJAX handler for bulk updates
     */
    public function ajax_bulk_update() {
        check_ajax_referer('wp_bulk_manager_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die(__('Insufficient permissions', 'wp-bulk-manager'));
        }
        
        // Bulk update logic here
        wp_send_json_success(['message' => 'Bulk update completed']);
    }
}

// Dashboard page
function wp_bulk_manager_dashboard_page() {
    require_once WP_BULK_MANAGER_PATH . 'admin/views/dashboard.php';
}

// Sites management page
function wp_bulk_manager_sites_page() {
    require_once WP_BULK_MANAGER_PATH . 'admin/views/sites.php';
}

// Templates page
function wp_bulk_manager_templates_page() {
    require_once WP_BULK_MANAGER_PATH . 'admin/views/templates.php';
}

// Variables page
function wp_bulk_manager_variables_page() {
    require_once WP_BULK_MANAGER_PATH . 'admin/views/variables.php';
}

// Queue page
function wp_bulk_manager_queue_page() {
    require_once WP_BULK_MANAGER_PATH . 'admin/views/queue.php';
}