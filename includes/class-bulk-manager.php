<?php
/**
 * Main plugin class
 */
class WP_Bulk_Manager {
    
    protected $loader;
    protected $plugin_name;
    protected $version;
    
    public function __construct() {
        $this->version = WP_BULK_MANAGER_VERSION;
        $this->plugin_name = 'wp-bulk-manager';
        
        $this->load_dependencies();
        $this->set_locale();
        $this->define_admin_hooks();
        $this->define_public_hooks();
        $this->define_api_hooks();
    }
    
    private function load_dependencies() {
        // Core classes
        require_once WP_BULK_MANAGER_PATH . 'includes/class-loader.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-i18n.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-api-manager.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-content-processor.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-gutenberg-handler.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-seo-handler.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-template-engine.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-queue-processor.php';
        require_once WP_BULK_MANAGER_PATH . 'includes/class-spintax-processor.php';
        
        // Admin classes
        require_once WP_BULK_MANAGER_PATH . 'admin/class-admin.php';
        
        // API classes
        require_once WP_BULK_MANAGER_PATH . 'api/class-rest-api.php';
        
        $this->loader = new WP_Bulk_Manager_Loader();
    }
    
    private function set_locale() {
        $plugin_i18n = new WP_Bulk_Manager_i18n();
        $this->loader->add_action('plugins_loaded', $plugin_i18n, 'load_plugin_textdomain');
    }
    
    private function define_admin_hooks() {
        $plugin_admin = new WP_Bulk_Manager_Admin($this->get_plugin_name(), $this->get_version());
        
        $this->loader->add_action('admin_enqueue_scripts', $plugin_admin, 'enqueue_styles');
        $this->loader->add_action('admin_enqueue_scripts', $plugin_admin, 'enqueue_scripts');
        
        // AJAX handlers
        $this->loader->add_action('wp_ajax_wp_bulk_manager_test_connection', $plugin_admin, 'ajax_test_connection');
        $this->loader->add_action('wp_ajax_wp_bulk_manager_process_template', $plugin_admin, 'ajax_process_template');
        $this->loader->add_action('wp_ajax_wp_bulk_manager_bulk_update', $plugin_admin, 'ajax_bulk_update');
    }
    
    private function define_public_hooks() {
        // Add any public-facing functionality here
    }
    
    private function define_api_hooks() {
        $plugin_api = new WP_Bulk_Manager_REST_API();
        $this->loader->add_action('rest_api_init', $plugin_api, 'register_routes');
    }
    
    public function run() {
        $this->loader->run();
        
        // Schedule cron jobs
        if (!wp_next_scheduled('wp_bulk_manager_process_queue')) {
            wp_schedule_event(time(), 'every_five_minutes', 'wp_bulk_manager_process_queue');
        }
        
        if (!wp_next_scheduled('wp_bulk_manager_cleanup_logs')) {
            wp_schedule_event(time(), 'daily', 'wp_bulk_manager_cleanup_logs');
        }
    }
    
    public function get_plugin_name() {
        return $this->plugin_name;
    }
    
    public function get_loader() {
        return $this->loader;
    }
    
    public function get_version() {
        return $this->version;
    }
}

// Loader class
class WP_Bulk_Manager_Loader {
    
    protected $actions;
    protected $filters;
    
    public function __construct() {
        $this->actions = array();
        $this->filters = array();
    }
    
    public function add_action($hook, $component, $callback, $priority = 10, $accepted_args = 1) {
        $this->actions = $this->add($this->actions, $hook, $component, $callback, $priority, $accepted_args);
    }
    
    public function add_filter($hook, $component, $callback, $priority = 10, $accepted_args = 1) {
        $this->filters = $this->add($this->filters, $hook, $component, $callback, $priority, $accepted_args);
    }
    
    private function add($hooks, $hook, $component, $callback, $priority, $accepted_args) {
        $hooks[] = array(
            'hook'          => $hook,
            'component'     => $component,
            'callback'      => $callback,
            'priority'      => $priority,
            'accepted_args' => $accepted_args
        );
        return $hooks;
    }
    
    public function run() {
        foreach ($this->filters as $hook) {
            add_filter($hook['hook'], array($hook['component'], $hook['callback']), $hook['priority'], $hook['accepted_args']);
        }
        
        foreach ($this->actions as $hook) {
            add_action($hook['hook'], array($hook['component'], $hook['callback']), $hook['priority'], $hook['accepted_args']);
        }
    }
}

// i18n class
class WP_Bulk_Manager_i18n {
    
    public function load_plugin_textdomain() {
        load_plugin_textdomain(
            'wp-bulk-manager',
            false,
            dirname(dirname(plugin_basename(__FILE__))) . '/languages/'
        );
    }
}