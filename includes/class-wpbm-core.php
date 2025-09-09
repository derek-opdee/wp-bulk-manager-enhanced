<?php
namespace WPBM;

/**
 * Core plugin class
 */
class WPBM_Core {
    
    /**
     * Plugin instance
     */
    private static $instance = null;
    
    /**
     * Loader instance
     */
    private $loader;
    
    /**
     * Plugin version
     */
    private $version;
    
    /**
     * Constructor
     */
    public function __construct() {
        $this->version = WPBM_VERSION;
        $this->load_dependencies();
        $this->set_locale();
        $this->define_admin_hooks();
        $this->define_public_hooks();
        $this->define_api_hooks();
    }
    
    /**
     * Load required dependencies
     */
    private function load_dependencies() {
        // Core classes
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-loader.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-i18n.php';
        
        // Admin classes
        require_once WPBM_PLUGIN_DIR . 'admin/class-wpbm-admin.php';
        require_once WPBM_PLUGIN_DIR . 'admin/class-wpbm-sites-manager.php';
        require_once WPBM_PLUGIN_DIR . 'admin/class-wpbm-templates-manager.php';
        
        // Functionality classes
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-content-processor.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-gutenberg-handler.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-seo-manager.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-spintax-processor.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-queue-manager.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-logger.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-wpbm-multi-site-connector.php';
        
        // API classes
        require_once WPBM_PLUGIN_DIR . 'api/class-wpbm-rest-api.php';
        
        $this->loader = new WPBM_Loader();
    }
    
    /**
     * Set plugin locale
     */
    private function set_locale() {
        $plugin_i18n = new WPBM_i18n();
        $this->loader->add_action('plugins_loaded', $plugin_i18n, 'load_plugin_textdomain');
    }
    
    /**
     * Register admin hooks
     */
    private function define_admin_hooks() {
        $plugin_admin = new WPBM_Admin($this->get_plugin_name(), $this->get_version());
        
        $this->loader->add_action('admin_enqueue_scripts', $plugin_admin, 'enqueue_styles');
        $this->loader->add_action('admin_enqueue_scripts', $plugin_admin, 'enqueue_scripts');
        $this->loader->add_action('admin_menu', $plugin_admin, 'add_plugin_admin_menu');
        $this->loader->add_action('admin_init', $plugin_admin, 'register_settings');
        
        // AJAX handlers
        $this->loader->add_action('wp_ajax_wpbm_test_connection', $plugin_admin, 'ajax_test_connection');
        $this->loader->add_action('wp_ajax_wpbm_process_bulk_action', $plugin_admin, 'ajax_process_bulk_action');
        $this->loader->add_action('wp_ajax_wpbm_get_queue_status', $plugin_admin, 'ajax_get_queue_status');
    }
    
    /**
     * Register public hooks
     */
    private function define_public_hooks() {
        // Public functionality can be added here if needed
    }
    
    /**
     * Register API hooks
     */
    private function define_api_hooks() {
        $rest_api = new WPBM_REST_API();
        $this->loader->add_action('rest_api_init', $rest_api, 'register_routes');
    }
    
    /**
     * Run the plugin
     */
    public function run() {
        $this->loader->run();
    }
    
    /**
     * Get plugin name
     */
    public function get_plugin_name() {
        return 'wp-bulk-manager';
    }
    
    /**
     * Get plugin version
     */
    public function get_version() {
        return $this->version;
    }
    
    /**
     * Get singleton instance
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
}