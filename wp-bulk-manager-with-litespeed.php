<?php
/**
 * Plugin Name: WP Bulk Manager Enhanced with LiteSpeed
 * Plugin URI: https://github.com/derek-opdee/wp-bulk-manager-enhanced
 * Description: Complete WordPress management system with SEO, Schema.org, and LiteSpeed Cache management
 * Version: 2.1.0
 * Author: Derek Zar - Opdee Digital
 * Author URI: https://opdee.com
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('WPBM_VERSION', '2.1.0');
define('WPBM_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WPBM_PLUGIN_URL', plugin_dir_url(__FILE__));

/**
 * Main plugin class with LiteSpeed Cache support
 */
class WP_Bulk_Manager_Enhanced {
    
    private static $instance = null;
    private $api_key = null;
    private $litespeed_available = false;
    
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
    }
    
    /**
     * Initialize hooks
     */
    private function init_hooks() {
        add_action('init', [$this, 'init']);
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('wp_head', [$this, 'output_seo_meta_tags']);
        
        // Activation/deactivation hooks
        register_activation_hook(__FILE__, [$this, 'activate']);
        register_deactivation_hook(__FILE__, [$this, 'deactivate']);
    }
    
    /**
     * Plugin initialization
     */
    public function init() {
        // Initialize API key
        $this->api_key = get_option('wpbm_api_key');
        if (!$this->api_key) {
            $this->api_key = wp_generate_password(32, false);
            update_option('wpbm_api_key', $this->api_key);
        }
        
        // Check if LiteSpeed Cache is available
        $this->litespeed_available = defined('LSCWP_V') || class_exists('LiteSpeed\Core');
    }
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wpbm/v1';
        
        // Authentication endpoint
        register_rest_route($namespace, '/auth', [
            'methods' => 'GET',
            'callback' => [$this, 'check_auth'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        // Content endpoints
        register_rest_route($namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'get_content'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/content', [
            'methods' => 'POST',
            'callback' => [$this, 'create_content'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_single_content'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_content'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'DELETE',
            'callback' => [$this, 'delete_content'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        // SEO endpoints
        register_rest_route($namespace, '/seo/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_seo'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/seo/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_seo'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        // Plugin management endpoints
        register_rest_route($namespace, '/plugins', [
            'methods' => 'GET',
            'callback' => [$this, 'get_plugins'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        // LiteSpeed Cache endpoints
        register_rest_route($namespace, '/litespeed/status', [
            'methods' => 'GET',
            'callback' => [$this, 'get_litespeed_status'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/litespeed/settings', [
            'methods' => 'GET',
            'callback' => [$this, 'get_litespeed_settings'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/litespeed/cache/purge', [
            'methods' => 'POST',
            'callback' => [$this, 'purge_litespeed_cache'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/litespeed/cache/purge-all', [
            'methods' => 'POST',
            'callback' => [$this, 'purge_all_litespeed_cache'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        register_rest_route($namespace, '/litespeed/optimize', [
            'methods' => 'POST',
            'callback' => [$this, 'optimize_litespeed_settings'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
        
        // System info endpoint
        register_rest_route($namespace, '/system', [
            'methods' => 'GET',
            'callback' => [$this, 'get_system_info'],
            'permission_callback' => [$this, 'check_api_permission']
        ]);
    }
    
    /**
     * Check API permissions
     */
    public function check_api_permission($request) {
        $provided_key = $request->get_header('X-API-Key');
        
        if (!$provided_key) {
            // Check for Bearer token
            $auth_header = $request->get_header('Authorization');
            if ($auth_header && preg_match('/Bearer\s+(.+)/i', $auth_header, $matches)) {
                $provided_key = $matches[1];
            }
        }
        
        return $provided_key && $provided_key === $this->api_key;
    }
    
    /**
     * Auth check endpoint
     */
    public function check_auth($request) {
        return new WP_REST_Response([
            'success' => true,
            'message' => 'Authentication successful',
            'version' => WPBM_VERSION,
            'litespeed_available' => $this->litespeed_available
        ], 200);
    }
    
    /**
     * Get LiteSpeed Cache status
     */
    public function get_litespeed_status($request) {
        if (!$this->litespeed_available) {
            return new WP_Error('litespeed_not_available', 'LiteSpeed Cache plugin not installed or active', ['status' => 404]);
        }
        
        $status = [
            'plugin_active' => true,
            'version' => defined('LSCWP_V') ? LSCWP_V : 'Unknown',
            'cache_enabled' => false,
            'object_cache_enabled' => false,
            'css_minify' => false,
            'js_minify' => false,
            'image_optimization' => false,
            'webp_enabled' => false
        ];
        
        // Get LiteSpeed options
        if (function_exists('get_option')) {
            $ls_options = get_option('litespeed.conf', []);
            
            if (!empty($ls_options)) {
                $status['cache_enabled'] = !empty($ls_options['cache-browser']) ? $ls_options['cache-browser'] : false;
                $status['object_cache_enabled'] = !empty($ls_options['object-kind']) ? ($ls_options['object-kind'] != 0) : false;
                $status['css_minify'] = !empty($ls_options['css_minify']) ? $ls_options['css_minify'] : false;
                $status['js_minify'] = !empty($ls_options['js_minify']) ? $ls_options['js_minify'] : false;
                $status['webp_enabled'] = !empty($ls_options['media-webp_replace']) ? $ls_options['media-webp_replace'] : false;
            }
        }
        
        return new WP_REST_Response($status, 200);
    }
    
    /**
     * Get LiteSpeed Cache settings
     */
    public function get_litespeed_settings($request) {
        if (!$this->litespeed_available) {
            return new WP_Error('litespeed_not_available', 'LiteSpeed Cache plugin not installed or active', ['status' => 404]);
        }
        
        $settings = get_option('litespeed.conf', []);
        
        // Return sanitized settings (remove sensitive data)
        $safe_settings = [];
        $allowed_keys = [
            'cache-browser', 'cache-mobile', 'cache-login_cookie',
            'css_minify', 'css_combine', 'js_minify', 'js_combine',
            'object-kind', 'object-host', 'object-port',
            'media-webp_replace', 'media-webp_attribute',
            'optm-css_async', 'optm-js_defer', 'optm-emoji_remove',
            'cdn-mapping', 'crawler', 'heartbeat'
        ];
        
        foreach ($allowed_keys as $key) {
            if (isset($settings[$key])) {
                $safe_settings[$key] = $settings[$key];
            }
        }
        
        return new WP_REST_Response($safe_settings, 200);
    }
    
    /**
     * Purge LiteSpeed Cache for specific URL
     */
    public function purge_litespeed_cache($request) {
        if (!$this->litespeed_available) {
            return new WP_Error('litespeed_not_available', 'LiteSpeed Cache plugin not installed or active', ['status' => 404]);
        }
        
        $url = $request->get_param('url');
        
        // Use LiteSpeed purge functions if available
        if (function_exists('litespeed_purge_url')) {
            litespeed_purge_url($url);
        } elseif (class_exists('LiteSpeed\Purge')) {
            LiteSpeed\Purge::purge_url($url);
        } elseif (function_exists('do_action')) {
            do_action('litespeed_purge_url', $url);
        }
        
        return new WP_REST_Response([
            'message' => 'Cache purged successfully',
            'url' => $url
        ], 200);
    }
    
    /**
     * Purge all LiteSpeed Cache
     */
    public function purge_all_litespeed_cache($request) {
        if (!$this->litespeed_available) {
            return new WP_Error('litespeed_not_available', 'LiteSpeed Cache plugin not installed or active', ['status' => 404]);
        }
        
        // Use LiteSpeed purge all functions
        if (function_exists('litespeed_purge_all')) {
            litespeed_purge_all();
        } elseif (class_exists('LiteSpeed\Purge')) {
            LiteSpeed\Purge::purge_all();
        } elseif (function_exists('do_action')) {
            do_action('litespeed_purge_all');
        }
        
        return new WP_REST_Response([
            'message' => 'All cache purged successfully'
        ], 200);
    }
    
    /**
     * Optimize LiteSpeed settings
     */
    public function optimize_litespeed_settings($request) {
        if (!$this->litespeed_available) {
            return new WP_Error('litespeed_not_available', 'LiteSpeed Cache plugin not installed or active', ['status' => 404]);
        }
        
        $optimizations = $request->get_param('optimizations') ?: 'standard';
        
        $settings = get_option('litespeed.conf', []);
        
        // Apply optimizations based on level
        switch ($optimizations) {
            case 'aggressive':
                $settings['cache-browser'] = 1;
                $settings['cache-mobile'] = 1;
                $settings['css_minify'] = 1;
                $settings['css_combine'] = 1;
                $settings['js_minify'] = 1;
                $settings['js_combine'] = 1;
                $settings['media-webp_replace'] = 1;
                $settings['optm-css_async'] = 1;
                $settings['optm-js_defer'] = 1;
                break;
                
            case 'conservative':
                $settings['cache-browser'] = 1;
                $settings['css_minify'] = 1;
                $settings['js_minify'] = 1;
                $settings['media-webp_replace'] = 1;
                break;
                
            default: // standard
                $settings['cache-browser'] = 1;
                $settings['css_minify'] = 1;
                $settings['js_minify'] = 1;
                break;
        }
        
        update_option('litespeed.conf', $settings);
        
        return new WP_REST_Response([
            'message' => 'LiteSpeed settings optimized successfully',
            'level' => $optimizations
        ], 200);
    }
    
    // ... [Previous methods remain the same] ...
    
    /**
     * Get content endpoint
     */
    public function get_content($request) {
        $post_type = $request->get_param('post_type') ?: 'any';
        $per_page = $request->get_param('per_page') ?: 100;
        $page = $request->get_param('page') ?: 1;
        
        $args = [
            'post_type' => $post_type,
            'posts_per_page' => $per_page,
            'paged' => $page,
            'post_status' => 'any'
        ];
        
        $query = new WP_Query($args);
        
        $posts = [];
        foreach ($query->posts as $post) {
            $posts[] = [
                'id' => $post->ID,
                'title' => $post->post_title,
                'content' => $post->post_content,
                'excerpt' => $post->post_excerpt,
                'status' => $post->post_status,
                'type' => $post->post_type,
                'slug' => $post->post_name,
                'date' => $post->post_date,
                'modified' => $post->post_modified,
                'link' => get_permalink($post->ID),
                'meta' => get_post_meta($post->ID)
            ];
        }
        
        return new WP_REST_Response([
            'posts' => $posts,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages
        ], 200);
    }
    
    /**
     * Get single content
     */
    public function get_single_content($request) {
        $id = $request->get_param('id');
        $post = get_post($id);
        
        if (!$post) {
            return new WP_Error('not_found', 'Content not found', ['status' => 404]);
        }
        
        return new WP_REST_Response([
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'status' => $post->post_status,
            'type' => $post->post_type,
            'slug' => $post->post_name,
            'date' => $post->post_date,
            'modified' => $post->post_modified,
            'link' => get_permalink($post->ID),
            'meta' => get_post_meta($post->ID)
        ], 200);
    }
    
    /**
     * Create content
     */
    public function create_content($request) {
        $title = sanitize_text_field($request->get_param('title'));
        $content = wp_kses_post($request->get_param('content'));
        $status = $request->get_param('status') ?: 'draft';
        $type = $request->get_param('type') ?: 'post';
        
        $post_data = [
            'post_title' => $title,
            'post_content' => $content,
            'post_status' => $status,
            'post_type' => $type
        ];
        
        $post_id = wp_insert_post($post_data);
        
        if (is_wp_error($post_id)) {
            return new WP_Error('creation_failed', 'Failed to create content', ['status' => 500]);
        }
        
        return new WP_REST_Response([
            'id' => $post_id,
            'message' => 'Content created successfully',
            'link' => get_permalink($post_id)
        ], 201);
    }
    
    /**
     * Update content
     */
    public function update_content($request) {
        $id = $request->get_param('id');
        
        $post_data = [
            'ID' => $id
        ];
        
        if ($request->get_param('title')) {
            $post_data['post_title'] = sanitize_text_field($request->get_param('title'));
        }
        
        if ($request->get_param('content')) {
            $post_data['post_content'] = wp_kses_post($request->get_param('content'));
        }
        
        if ($request->get_param('status')) {
            $post_data['post_status'] = $request->get_param('status');
        }
        
        $result = wp_update_post($post_data);
        
        if (is_wp_error($result)) {
            return new WP_Error('update_failed', 'Failed to update content', ['status' => 500]);
        }
        
        return new WP_REST_Response([
            'id' => $id,
            'message' => 'Content updated successfully'
        ], 200);
    }
    
    /**
     * Delete content
     */
    public function delete_content($request) {
        $id = $request->get_param('id');
        $force = $request->get_param('force') ?: false;
        
        $result = wp_delete_post($id, $force);
        
        if (!$result) {
            return new WP_Error('deletion_failed', 'Failed to delete content', ['status' => 500]);
        }
        
        return new WP_REST_Response([
            'message' => 'Content deleted successfully'
        ], 200);
    }
    
    /**
     * Get SEO data
     */
    public function get_seo($request) {
        $id = $request->get_param('id');
        
        $seo_data = [
            'title' => get_post_meta($id, '_wpbm_seo_title', true),
            'description' => get_post_meta($id, '_wpbm_seo_description', true),
            'keywords' => get_post_meta($id, '_wpbm_seo_keywords', true),
            'og_title' => get_post_meta($id, '_wpbm_og_title', true),
            'og_description' => get_post_meta($id, '_wpbm_og_description', true),
            'og_image' => get_post_meta($id, '_wpbm_og_image', true),
            'twitter_title' => get_post_meta($id, '_wpbm_twitter_title', true),
            'twitter_description' => get_post_meta($id, '_wpbm_twitter_description', true),
            'twitter_image' => get_post_meta($id, '_wpbm_twitter_image', true)
        ];
        
        return new WP_REST_Response($seo_data, 200);
    }
    
    /**
     * Update SEO data
     */
    public function update_seo($request) {
        $id = $request->get_param('id');
        
        $seo_fields = [
            'title' => '_wpbm_seo_title',
            'description' => '_wpbm_seo_description',
            'keywords' => '_wpbm_seo_keywords',
            'og_title' => '_wpbm_og_title',
            'og_description' => '_wpbm_og_description',
            'og_image' => '_wpbm_og_image',
            'twitter_title' => '_wpbm_twitter_title',
            'twitter_description' => '_wpbm_twitter_description',
            'twitter_image' => '_wpbm_twitter_image'
        ];
        
        foreach ($seo_fields as $field => $meta_key) {
            if ($request->get_param($field) !== null) {
                update_post_meta($id, $meta_key, sanitize_text_field($request->get_param($field)));
            }
        }
        
        return new WP_REST_Response([
            'message' => 'SEO data updated successfully'
        ], 200);
    }
    
    /**
     * Get plugins list
     */
    public function get_plugins($request) {
        if (!function_exists('get_plugins')) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        
        $all_plugins = get_plugins();
        $active_plugins = get_option('active_plugins', []);
        
        $plugins = [];
        foreach ($all_plugins as $plugin_file => $plugin_data) {
            $plugins[] = [
                'file' => $plugin_file,
                'name' => $plugin_data['Name'],
                'version' => $plugin_data['Version'],
                'author' => $plugin_data['Author'],
                'active' => in_array($plugin_file, $active_plugins)
            ];
        }
        
        return new WP_REST_Response($plugins, 200);
    }
    
    /**
     * Get system information
     */
    public function get_system_info($request) {
        global $wp_version;
        
        return new WP_REST_Response([
            'wordpress_version' => $wp_version,
            'php_version' => phpversion(),
            'plugin_version' => WPBM_VERSION,
            'site_url' => get_site_url(),
            'home_url' => get_home_url(),
            'timezone' => get_option('timezone_string'),
            'language' => get_locale(),
            'multisite' => is_multisite(),
            'memory_limit' => WP_MEMORY_LIMIT,
            'debug_mode' => WP_DEBUG,
            'litespeed_available' => $this->litespeed_available,
            'litespeed_version' => defined('LSCWP_V') ? LSCWP_V : null
        ], 200);
    }
    
    /**
     * Output SEO meta tags in wp_head
     */
    public function output_seo_meta_tags() {
        if (!is_singular()) {
            return;
        }
        
        global $post;
        
        // Get SEO data
        $seo_title = get_post_meta($post->ID, '_wpbm_seo_title', true);
        $seo_description = get_post_meta($post->ID, '_wpbm_seo_description', true);
        $og_title = get_post_meta($post->ID, '_wpbm_og_title', true);
        $og_description = get_post_meta($post->ID, '_wpbm_og_description', true);
        $og_image = get_post_meta($post->ID, '_wpbm_og_image', true);
        
        // Output meta tags
        if ($seo_title) {
            echo '<meta name="title" content="' . esc_attr($seo_title) . '">' . "\n";
        }
        
        if ($seo_description) {
            echo '<meta name="description" content="' . esc_attr($seo_description) . '">' . "\n";
        }
        
        // Open Graph tags
        if ($og_title) {
            echo '<meta property="og:title" content="' . esc_attr($og_title) . '">' . "\n";
        }
        
        if ($og_description) {
            echo '<meta property="og:description" content="' . esc_attr($og_description) . '">' . "\n";
        }
        
        if ($og_image) {
            echo '<meta property="og:image" content="' . esc_url($og_image) . '">' . "\n";
        }
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
            'dashicons-admin-generic',
            30
        );
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Enhanced</h1>
            
            <div class="card">
                <h2>API Configuration</h2>
                <p><strong>Your API Key:</strong></p>
                <code style="background: #f0f0f0; padding: 10px; display: block; margin: 10px 0;">
                    <?php echo esc_html($this->api_key); ?>
                </code>
                <p>Use this API key to authenticate requests from the management application.</p>
            </div>
            
            <div class="card">
                <h2>LiteSpeed Cache Status</h2>
                <?php if ($this->litespeed_available): ?>
                    <p>✅ <strong>LiteSpeed Cache is available</strong></p>
                    <p>Version: <?php echo defined('LSCWP_V') ? esc_html(LSCWP_V) : 'Unknown'; ?></p>
                <?php else: ?>
                    <p>❌ <strong>LiteSpeed Cache not detected</strong></p>
                    <p>Install and activate the LiteSpeed Cache plugin to enable cache management features.</p>
                <?php endif; ?>
            </div>
            
            <div class="card">
                <h2>API Endpoints</h2>
                <p>Base URL: <code><?php echo esc_url(get_rest_url(null, 'wpbm/v1')); ?></code></p>
                <ul>
                    <li><code>GET /auth</code> - Check authentication</li>
                    <li><code>GET /content</code> - List content</li>
                    <li><code>POST /content</code> - Create content</li>
                    <li><code>GET /content/{id}</code> - Get single content</li>
                    <li><code>PUT /content/{id}</code> - Update content</li>
                    <li><code>DELETE /content/{id}</code> - Delete content</li>
                    <li><code>GET /seo/{id}</code> - Get SEO data</li>
                    <li><code>PUT /seo/{id}</code> - Update SEO data</li>
                    <li><code>GET /plugins</code> - List plugins</li>
                    <li><code>GET /system</code> - System information</li>
                    <?php if ($this->litespeed_available): ?>
                    <li><strong>LiteSpeed Cache Endpoints:</strong></li>
                    <li><code>GET /litespeed/status</code> - Cache status</li>
                    <li><code>GET /litespeed/settings</code> - Cache settings</li>
                    <li><code>POST /litespeed/cache/purge</code> - Purge specific URL</li>
                    <li><code>POST /litespeed/cache/purge-all</code> - Purge all cache</li>
                    <li><code>POST /litespeed/optimize</code> - Optimize settings</li>
                    <?php endif; ?>
                </ul>
            </div>
            
            <div class="card">
                <h2>Quick Test</h2>
                <p>Test your API connection with this curl command:</p>
                <code style="background: #f0f0f0; padding: 10px; display: block; margin: 10px 0;">
                    curl -H "X-API-Key: <?php echo esc_html($this->api_key); ?>" <?php echo esc_url(get_rest_url(null, 'wpbm/v1/auth')); ?>
                </code>
                
                <?php if ($this->litespeed_available): ?>
                <p>Test LiteSpeed Cache status:</p>
                <code style="background: #f0f0f0; padding: 10px; display: block; margin: 10px 0;">
                    curl -H "X-API-Key: <?php echo esc_html($this->api_key); ?>" <?php echo esc_url(get_rest_url(null, 'wpbm/v1/litespeed/status')); ?>
                </code>
                <?php endif; ?>
            </div>
        </div>
        <?php
    }
    
    /**
     * Plugin activation
     */
    public function activate() {
        // Generate API key if not exists
        if (!get_option('wpbm_api_key')) {
            update_option('wpbm_api_key', wp_generate_password(32, false));
        }
        
        // Flush rewrite rules for REST API
        flush_rewrite_rules();
    }
    
    /**
     * Plugin deactivation
     */
    public function deactivate() {
        // Flush rewrite rules
        flush_rewrite_rules();
    }
}

// Initialize plugin
add_action('plugins_loaded', function() {
    WP_Bulk_Manager_Enhanced::get_instance();
});