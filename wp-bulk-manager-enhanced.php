<?php
/**
 * Plugin Name: WP Bulk Manager Enhanced
 * Plugin URI: https://github.com/opdee/wp-bulk-manager
 * Description: Enterprise WordPress management with SEO, Schema.org, LiteSpeed optimization, and bulk operations
 * Version: 4.0.0
 * Author: Derek Zar - Opdee Digital
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 * 
 * OpenAPI Specification: /openapi-spec.yaml
 * Contract-Driven Development compliant
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('WPBM_VERSION', '4.0.0');
define('WPBM_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WPBM_PLUGIN_URL', plugin_dir_url(__FILE__));
define('WPBM_API_NAMESPACE', 'wpbm/v1');

/**
 * Main WP Bulk Manager Enhanced Class
 */
class WP_Bulk_Manager_Enhanced {
    
    private static $instance = null;
    private $api_key_option = 'wpbm_api_key';
    private $settings_option = 'wpbm_settings';
    private $seo_manager;
    private $schema_manager;
    private $litespeed_manager;
    private $performance_manager;
    
    /**
     * Get singleton instance
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    /**
     * Constructor
     */
    private function __construct() {
        $this->init_hooks();
        $this->load_dependencies();
    }
    
    /**
     * Initialize hooks
     */
    private function init_hooks() {
        // Core hooks
        add_action('init', [$this, 'init']);
        add_action('rest_api_init', [$this, 'register_rest_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_enqueue_scripts', [$this, 'enqueue_admin_assets']);
        add_action('wp_head', [$this, 'output_seo_meta_tags']);
        
        // Activation/Deactivation hooks
        register_activation_hook(__FILE__, [$this, 'activate']);
        register_deactivation_hook(__FILE__, [$this, 'deactivate']);
        
        // AJAX hooks
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
        add_action('wp_ajax_wpbm_save_settings', [$this, 'ajax_save_settings']);
        add_action('wp_ajax_wpbm_run_seo_analysis', [$this, 'ajax_run_seo_analysis']);
        add_action('wp_ajax_wpbm_generate_schema', [$this, 'ajax_generate_schema']);
        
        // Custom REST API authentication
        add_filter('rest_authentication_errors', [$this, 'rest_authentication']);
    }
    
    /**
     * Load dependencies
     */
    private function load_dependencies() {
        // Load manager classes when needed
        require_once WPBM_PLUGIN_DIR . 'includes/class-seo-manager.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-schema-manager.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-litespeed-manager.php';
        require_once WPBM_PLUGIN_DIR . 'includes/class-performance-manager.php';
        
        $this->seo_manager = new WPBM_SEO_Manager();
        $this->schema_manager = new WPBM_Schema_Manager();
        $this->litespeed_manager = new WPBM_LiteSpeed_Manager();
        $this->performance_manager = new WPBM_Performance_Manager();
    }
    
    /**
     * Plugin initialization
     */
    public function init() {
        // Load textdomain
        load_plugin_textdomain('wp-bulk-manager', false, dirname(plugin_basename(__FILE__)) . '/languages');
        
        // Register custom post meta for SEO and Schema
        $this->register_custom_meta();
    }
    
    /**
     * Register custom meta fields
     */
    private function register_custom_meta() {
        // SEO meta fields
        register_post_meta('', '_wpbm_seo_title', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        register_post_meta('', '_wpbm_seo_description', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        register_post_meta('', '_wpbm_seo_canonical', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        register_post_meta('', '_wpbm_seo_robots', [
            'type' => 'object',
            'single' => true,
            'show_in_rest' => [
                'schema' => [
                    'type' => 'object',
                    'properties' => [
                        'index' => ['type' => 'boolean'],
                        'follow' => ['type' => 'boolean'],
                        'archive' => ['type' => 'boolean'],
                    ],
                ],
            ],
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        // Open Graph meta
        register_post_meta('', '_wpbm_og_data', [
            'type' => 'object',
            'single' => true,
            'show_in_rest' => [
                'schema' => [
                    'type' => 'object',
                    'properties' => [
                        'title' => ['type' => 'string'],
                        'description' => ['type' => 'string'],
                        'image' => ['type' => 'string'],
                        'type' => ['type' => 'string'],
                    ],
                ],
            ],
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        // Twitter Card meta
        register_post_meta('', '_wpbm_twitter_data', [
            'type' => 'object',
            'single' => true,
            'show_in_rest' => [
                'schema' => [
                    'type' => 'object',
                    'properties' => [
                        'card' => ['type' => 'string'],
                        'title' => ['type' => 'string'],
                        'description' => ['type' => 'string'],
                        'image' => ['type' => 'string'],
                    ],
                ],
            ],
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        // Schema.org data
        register_post_meta('', '_wpbm_schema_type', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
        
        register_post_meta('', '_wpbm_schema_data', [
            'type' => 'object',
            'single' => true,
            'show_in_rest' => true,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ]);
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        // Authentication endpoint
        register_rest_route(WPBM_API_NAMESPACE, '/auth', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_authenticate'],
            'permission_callback' => '__return_true',
        ]);
        
        // Content endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/content', [
            [
                'methods' => 'GET',
                'callback' => [$this, 'rest_get_content'],
                'permission_callback' => [$this, 'check_api_permission'],
                'args' => $this->get_content_list_args(),
            ],
            [
                'methods' => 'POST',
                'callback' => [$this, 'rest_create_content'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/content/(?P<id>\d+)', [
            [
                'methods' => 'GET',
                'callback' => [$this, 'rest_get_single_content'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'PUT',
                'callback' => [$this, 'rest_update_content'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'DELETE',
                'callback' => [$this, 'rest_delete_content'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        // SEO endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/seo/(?P<id>\d+)', [
            [
                'methods' => 'GET',
                'callback' => [$this->seo_manager, 'get_seo_data'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'PUT',
                'callback' => [$this->seo_manager, 'update_seo_data'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/seo/bulk', [
            'methods' => 'POST',
            'callback' => [$this->seo_manager, 'bulk_update_seo'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        // Schema.org endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/schema/(?P<id>\d+)', [
            [
                'methods' => 'GET',
                'callback' => [$this->schema_manager, 'get_schema_data'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'PUT',
                'callback' => [$this->schema_manager, 'update_schema_data'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        // Plugin management endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/plugins', [
            [
                'methods' => 'GET',
                'callback' => [$this, 'rest_get_plugins'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'POST',
                'callback' => [$this, 'rest_install_plugin'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/plugins/(?P<slug>[a-z0-9\-]+)', [
            [
                'methods' => 'PUT',
                'callback' => [$this, 'rest_update_plugin'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'DELETE',
                'callback' => [$this, 'rest_delete_plugin'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/plugins/(?P<slug>[a-z0-9\-]+)/activate', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_activate_plugin'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/plugins/(?P<slug>[a-z0-9\-]+)/deactivate', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_deactivate_plugin'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        // LiteSpeed Cache endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/litespeed/settings', [
            [
                'methods' => 'GET',
                'callback' => [$this->litespeed_manager, 'get_settings'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
            [
                'methods' => 'PUT',
                'callback' => [$this->litespeed_manager, 'update_settings'],
                'permission_callback' => [$this, 'check_api_permission'],
            ],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/litespeed/purge', [
            'methods' => 'POST',
            'callback' => [$this->litespeed_manager, 'purge_cache'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        register_rest_route(WPBM_API_NAMESPACE, '/litespeed/crawler', [
            'methods' => 'POST',
            'callback' => [$this->litespeed_manager, 'run_crawler'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        // Performance endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/performance/analyze', [
            'methods' => 'POST',
            'callback' => [$this->performance_manager, 'analyze_performance'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
        
        // Bulk operations endpoints
        register_rest_route(WPBM_API_NAMESPACE, '/bulk/content', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_bulk_create_content'],
            'permission_callback' => [$this, 'check_api_permission'],
        ]);
    }
    
    /**
     * Check API permission
     */
    public function check_api_permission($request) {
        $api_key = $request->get_header('X-API-Key');
        
        if (!$api_key) {
            // Check for Bearer token
            $auth_header = $request->get_header('Authorization');
            if ($auth_header && preg_match('/Bearer\s+(.+)/', $auth_header, $matches)) {
                $api_key = $matches[1];
            }
        }
        
        if (!$api_key) {
            return new WP_Error('no_api_key', 'API key required', ['status' => 401]);
        }
        
        $stored_key = get_option($this->api_key_option);
        
        if (!$stored_key || !hash_equals($stored_key, $api_key)) {
            return new WP_Error('invalid_api_key', 'Invalid API key', ['status' => 401]);
        }
        
        return true;
    }
    
    /**
     * REST API authentication
     */
    public function rest_authentication($errors) {
        // Allow our custom authentication for our namespace
        if (isset($_SERVER['REQUEST_URI']) && strpos($_SERVER['REQUEST_URI'], '/wp-json/' . WPBM_API_NAMESPACE) !== false) {
            return true;
        }
        return $errors;
    }
    
    /**
     * REST authenticate endpoint
     */
    public function rest_authenticate($request) {
        $api_key = $request->get_param('api_key');
        
        if (!$api_key) {
            return new WP_Error('missing_api_key', 'API key is required', ['status' => 400]);
        }
        
        $stored_key = get_option($this->api_key_option);
        
        if (!$stored_key || !hash_equals($stored_key, $api_key)) {
            return new WP_Error('invalid_api_key', 'Invalid API key', ['status' => 401]);
        }
        
        return [
            'success' => true,
            'site' => [
                'name' => get_bloginfo('name'),
                'url' => get_site_url(),
                'version' => get_bloginfo('version'),
            ],
            'user' => [
                'id' => get_current_user_id(),
                'username' => wp_get_current_user()->user_login,
                'email' => wp_get_current_user()->user_email,
                'roles' => wp_get_current_user()->roles,
            ],
        ];
    }
    
    /**
     * Get content list arguments
     */
    private function get_content_list_args() {
        return [
            'post_type' => [
                'type' => 'string',
                'default' => 'any',
                'enum' => ['post', 'page', 'any'],
            ],
            'status' => [
                'type' => 'string',
                'default' => 'any',
                'enum' => ['publish', 'draft', 'private', 'trash', 'any'],
            ],
            'per_page' => [
                'type' => 'integer',
                'default' => 20,
                'minimum' => 1,
                'maximum' => 100,
            ],
            'page' => [
                'type' => 'integer',
                'default' => 1,
                'minimum' => 1,
            ],
            'search' => [
                'type' => 'string',
            ],
        ];
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            'WP Bulk Manager',
            'WP Bulk Manager',
            'manage_options',
            'wp-bulk-manager',
            [$this, 'admin_page'],
            'dashicons-admin-tools',
            30
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'SEO Management',
            'SEO Management',
            'manage_options',
            'wp-bulk-manager-seo',
            [$this, 'admin_seo_page']
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'Schema.org',
            'Schema.org',
            'manage_options',
            'wp-bulk-manager-schema',
            [$this, 'admin_schema_page']
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'LiteSpeed Cache',
            'LiteSpeed Cache',
            'manage_options',
            'wp-bulk-manager-litespeed',
            [$this, 'admin_litespeed_page']
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'Performance',
            'Performance',
            'manage_options',
            'wp-bulk-manager-performance',
            [$this, 'admin_performance_page']
        );
    }
    
    /**
     * Enqueue admin assets
     */
    public function enqueue_admin_assets($hook) {
        if (strpos($hook, 'wp-bulk-manager') === false) {
            return;
        }
        
        wp_enqueue_script(
            'wpbm-admin',
            WPBM_PLUGIN_URL . 'assets/js/wpbm-admin.js',
            ['jquery', 'wp-api', 'wp-components', 'wp-element'],
            WPBM_VERSION,
            true
        );
        
        wp_enqueue_style(
            'wpbm-admin',
            WPBM_PLUGIN_URL . 'assets/css/wpbm-admin.css',
            ['wp-components'],
            WPBM_VERSION
        );
        
        wp_localize_script('wpbm-admin', 'wpbm', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'api_url' => rest_url(WPBM_API_NAMESPACE),
            'nonce' => wp_create_nonce('wpbm_nonce'),
            'api_key' => get_option($this->api_key_option),
        ]);
    }
    
    /**
     * Plugin activation
     */
    public function activate() {
        // Create database tables if needed
        $this->create_tables();
        
        // Set default options
        add_option($this->settings_option, [
            'enable_seo' => true,
            'enable_schema' => true,
            'enable_litespeed' => true,
            'enable_performance' => true,
        ]);
        
        // Generate initial API key
        if (!get_option($this->api_key_option)) {
            update_option($this->api_key_option, wp_generate_password(32, false));
        }
        
        // Flush rewrite rules
        flush_rewrite_rules();
    }
    
    /**
     * Plugin deactivation
     */
    public function deactivate() {
        // Flush rewrite rules
        flush_rewrite_rules();
    }
    
    /**
     * Create database tables
     */
    private function create_tables() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        // SEO analysis history table
        $table_name = $wpdb->prefix . 'wpbm_seo_analysis';
        $sql = "CREATE TABLE IF NOT EXISTS $table_name (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            post_id bigint(20) NOT NULL,
            analysis_date datetime DEFAULT CURRENT_TIMESTAMP,
            score int(11) DEFAULT 0,
            issues text,
            recommendations text,
            PRIMARY KEY (id),
            KEY post_id (post_id)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
        
        // Performance metrics table
        $table_name = $wpdb->prefix . 'wpbm_performance_metrics';
        $sql = "CREATE TABLE IF NOT EXISTS $table_name (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            url varchar(255) NOT NULL,
            test_date datetime DEFAULT CURRENT_TIMESTAMP,
            ttfb float DEFAULT 0,
            fcp float DEFAULT 0,
            lcp float DEFAULT 0,
            cls float DEFAULT 0,
            fid float DEFAULT 0,
            performance_score int(11) DEFAULT 0,
            PRIMARY KEY (id),
            KEY url (url)
        ) $charset_collate;";
        
        dbDelta($sql);
    }
    
    /**
     * Output SEO meta tags in wp_head
     */
    public function output_seo_meta_tags() {
        if (!is_singular()) {
            return;
        }
        
        global $post;
        
        // Get SEO meta data
        $seo_title = get_post_meta($post->ID, '_wpbm_seo_title', true);
        $seo_description = get_post_meta($post->ID, '_wpbm_seo_description', true);
        $seo_canonical = get_post_meta($post->ID, '_wpbm_seo_canonical', true);
        $og_data = get_post_meta($post->ID, '_wpbm_og_data', true);
        $twitter_data = get_post_meta($post->ID, '_wpbm_twitter_data', true);
        
        // Output meta tags
        if ($seo_description) {
            echo '<meta name="description" content="' . esc_attr($seo_description) . '">' . "\n";
        }
        
        if ($seo_canonical) {
            echo '<link rel="canonical" href="' . esc_url($seo_canonical) . '">' . "\n";
        }
        
        // Open Graph tags
        if ($og_data && is_array($og_data)) {
            if (!empty($og_data['title'])) {
                echo '<meta property="og:title" content="' . esc_attr($og_data['title']) . '">' . "\n";
            }
            if (!empty($og_data['description'])) {
                echo '<meta property="og:description" content="' . esc_attr($og_data['description']) . '">' . "\n";
            }
            if (!empty($og_data['image'])) {
                echo '<meta property="og:image" content="' . esc_url($og_data['image']) . '">' . "\n";
            }
        }
        
        // Twitter Card tags
        if ($twitter_data && is_array($twitter_data)) {
            if (!empty($twitter_data['card'])) {
                echo '<meta name="twitter:card" content="' . esc_attr($twitter_data['card']) . '">' . "\n";
            }
            if (!empty($twitter_data['title'])) {
                echo '<meta name="twitter:title" content="' . esc_attr($twitter_data['title']) . '">' . "\n";
            }
            if (!empty($twitter_data['description'])) {
                echo '<meta name="twitter:description" content="' . esc_attr($twitter_data['description']) . '">' . "\n";
            }
        }
    }
    
    /**
     * Generate API key via AJAX
     */
    public function ajax_generate_api_key() {
        check_ajax_referer('wpbm_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $new_key = wp_generate_password(32, false);
        update_option($this->api_key_option, $new_key);
        
        wp_send_json_success(['api_key' => $new_key]);
    }
    
    /**
     * Save settings via AJAX
     */
    public function ajax_save_settings() {
        check_ajax_referer('wpbm_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $settings = [
            'enable_seo' => isset($_POST['enable_seo']),
            'enable_schema' => isset($_POST['enable_schema']),
            'enable_litespeed' => isset($_POST['enable_litespeed']),
            'enable_performance' => isset($_POST['enable_performance']),
        ];
        
        update_option($this->settings_option, $settings);
        
        wp_send_json_success(['message' => 'Settings saved']);
    }
}

// Initialize plugin
add_action('plugins_loaded', function() {
    WP_Bulk_Manager_Enhanced::get_instance();
});