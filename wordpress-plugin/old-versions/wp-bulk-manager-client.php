<?php
/**
 * Plugin Name: WP Bulk Manager Client
 * Plugin URI: https://derekzar.com/wp-bulk-manager
 * Description: Lightweight client plugin for WP Bulk Manager - enables remote management of your WordPress site
 * Version: 1.0.0
 * Author: Derek
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager-client
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('WPBM_CLIENT_VERSION', '1.0.0');
define('WPBM_CLIENT_PATH', plugin_dir_path(__FILE__));
define('WPBM_CLIENT_URL', plugin_dir_url(__FILE__));

/**
 * Main plugin class
 */
class WP_Bulk_Manager_Client {
    
    private static $instance = null;
    
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        add_action('rest_api_init', [$this, 'register_rest_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        
        // Add support for The SEO Framework
        add_action('plugins_loaded', [$this, 'init_seo_framework_support']);
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        $namespace = 'wpbm/v1';
        
        // Authentication endpoint
        register_rest_route($namespace, '/auth', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_auth'],
            'permission_callback' => '__return_true'
        ]);
        
        // Status endpoint
        register_rest_route($namespace, '/status', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_status'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Content endpoints
        register_rest_route($namespace, '/content', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_create_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_get_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'handle_update_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // SEO endpoint
        register_rest_route($namespace, '/seo/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'handle_update_seo'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Plugins endpoint
        register_rest_route($namespace, '/plugins', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_get_plugins'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Bulk operations
        register_rest_route($namespace, '/bulk', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_bulk_operation'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // List all content
        register_rest_route($namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_list_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Duplicate content
        register_rest_route($namespace, '/content/(?P<id>\d+)/duplicate', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_duplicate_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Delete content
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'DELETE',
            'callback' => [$this, 'handle_delete_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Get all SEO data
        register_rest_route($namespace, '/seo', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_list_seo'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Update plugins
        register_rest_route($namespace, '/plugins/update', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_update_plugins'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Update themes
        register_rest_route($namespace, '/themes', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_get_themes'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/themes/update', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_update_themes'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // SEO Generator endpoints
        register_rest_route($namespace, '/seo-generator/pages', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_get_seo_generator_pages'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/seo-generator/page/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'handle_get_seo_generator_page'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/seo-generator/page/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'handle_update_seo_generator_page'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
    }
    
    /**
     * Verify API key
     */
    public function verify_api_key($request) {
        $api_key = $request->get_header('X-API-Key');
        $stored_key = get_option('wpbm_api_key');
        
        if (empty($api_key) || empty($stored_key)) {
            return false;
        }
        
        return hash_equals($stored_key, $api_key);
    }
    
    /**
     * Handle authentication
     */
    public function handle_auth($request) {
        if (!$this->verify_api_key($request)) {
            return new WP_Error('invalid_api_key', 'Invalid API key', ['status' => 401]);
        }
        
        return [
            'success' => true,
            'site' => [
                'name' => get_bloginfo('name'),
                'url' => get_site_url(),
                'version' => get_bloginfo('version'),
                'plugins' => [
                    'wpbm_client' => WPBM_CLIENT_VERSION,
                    'seo_framework' => defined('THE_SEO_FRAMEWORK_VERSION') ? THE_SEO_FRAMEWORK_VERSION : false
                ]
            ]
        ];
    }
    
    /**
     * Handle status request
     */
    public function handle_status($request) {
        global $wpdb;
        
        return [
            'site' => [
                'name' => get_bloginfo('name'),
                'url' => get_site_url(),
                'admin_email' => get_option('admin_email'),
                'wordpress_version' => get_bloginfo('version'),
                'php_version' => phpversion(),
                'timezone' => get_option('timezone_string'),
                'language' => get_locale()
            ],
            'content' => [
                'posts' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish'"),
                'pages' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'page' AND post_status = 'publish'")
            ],
            'plugins' => [
                'active' => count(get_option('active_plugins', [])),
                'seo_framework' => defined('THE_SEO_FRAMEWORK_VERSION'),
                'seo_generator' => is_plugin_active('seo-generator/seo-generator.php')
            ]
        ];
    }
    
    /**
     * Handle content creation
     */
    public function handle_create_content($request) {
        $params = $request->get_json_params();
        
        $post_data = [
            'post_title' => sanitize_text_field($params['title']),
            'post_content' => wp_kses_post($params['content']),
            'post_status' => in_array($params['status'], ['draft', 'publish', 'private']) ? $params['status'] : 'draft',
            'post_type' => in_array($params['type'], ['post', 'page']) ? $params['type'] : 'post'
        ];
        
        // Handle parent page
        if (isset($params['parent_id'])) {
            $post_data['post_parent'] = absint($params['parent_id']);
        }
        
        // Handle categories
        if (isset($params['categories'])) {
            $post_data['post_category'] = array_map('absint', $params['categories']);
        }
        
        $post_id = wp_insert_post($post_data);
        
        if (is_wp_error($post_id)) {
            return $post_id;
        }
        
        // Handle SEO data if provided
        if (isset($params['seo'])) {
            $this->update_seo_data($post_id, $params['seo']);
        }
        
        return [
            'success' => true,
            'post_id' => $post_id,
            'permalink' => get_permalink($post_id),
            'edit_link' => get_edit_post_link($post_id, 'raw')
        ];
    }
    
    /**
     * Handle content retrieval
     */
    public function handle_get_content($request) {
        $post_id = absint($request->get_param('id'));
        $post = get_post($post_id);
        
        if (!$post) {
            return new WP_Error('post_not_found', 'Post not found', ['status' => 404]);
        }
        
        $response = [
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'status' => $post->post_status,
            'type' => $post->post_type,
            'permalink' => get_permalink($post->ID),
            'seo' => $this->get_seo_data($post->ID)
        ];
        
        return $response;
    }
    
    /**
     * Handle content update
     */
    public function handle_update_content($request) {
        $post_id = absint($request->get_param('id'));
        $params = $request->get_json_params();
        
        $post_data = ['ID' => $post_id];
        
        if (isset($params['title'])) {
            $post_data['post_title'] = sanitize_text_field($params['title']);
        }
        
        if (isset($params['content'])) {
            $post_data['post_content'] = wp_kses_post($params['content']);
        }
        
        if (isset($params['status'])) {
            $post_data['post_status'] = sanitize_text_field($params['status']);
        }
        
        $result = wp_update_post($post_data);
        
        if (is_wp_error($result)) {
            return $result;
        }
        
        // Handle SEO data if provided
        if (isset($params['seo'])) {
            $this->update_seo_data($post_id, $params['seo']);
        }
        
        return [
            'success' => true,
            'post_id' => $post_id,
            'permalink' => get_permalink($post_id)
        ];
    }
    
    /**
     * Handle SEO update
     */
    public function handle_update_seo($request) {
        $post_id = absint($request->get_param('id'));
        $seo_data = $request->get_json_params();
        
        $this->update_seo_data($post_id, $seo_data);
        
        return [
            'success' => true,
            'post_id' => $post_id,
            'seo' => $this->get_seo_data($post_id)
        ];
    }
    
    /**
     * Update SEO data - supports The SEO Framework
     */
    private function update_seo_data($post_id, $seo_data) {
        // Check if The SEO Framework is active
        if (function_exists('the_seo_framework')) {
            $tsf = the_seo_framework();
            
            // Update title
            if (isset($seo_data['title'])) {
                update_post_meta($post_id, '_genesis_title', $seo_data['title']);
                // TSF also checks for _genesis_title
            }
            
            // Update description
            if (isset($seo_data['description'])) {
                update_post_meta($post_id, '_genesis_description', $seo_data['description']);
            }
            
            // Update robots meta
            if (isset($seo_data['noindex'])) {
                update_post_meta($post_id, '_genesis_noindex', $seo_data['noindex'] ? 1 : 0);
            }
            
            if (isset($seo_data['nofollow'])) {
                update_post_meta($post_id, '_genesis_nofollow', $seo_data['nofollow'] ? 1 : 0);
            }
            
            if (isset($seo_data['noarchive'])) {
                update_post_meta($post_id, '_genesis_noarchive', $seo_data['noarchive'] ? 1 : 0);
            }
            
            // Update canonical URL
            if (isset($seo_data['canonical'])) {
                update_post_meta($post_id, '_genesis_canonical_uri', $seo_data['canonical']);
            }
            
        } else {
            // Fallback for standard meta
            if (isset($seo_data['title'])) {
                update_post_meta($post_id, '_wpbm_seo_title', $seo_data['title']);
            }
            
            if (isset($seo_data['description'])) {
                update_post_meta($post_id, '_wpbm_seo_description', $seo_data['description']);
            }
        }
    }
    
    /**
     * Get SEO data
     */
    private function get_seo_data($post_id) {
        $seo_data = [];
        
        // Check if The SEO Framework is active
        if (function_exists('the_seo_framework')) {
            $tsf = the_seo_framework();
            
            $seo_data['title'] = get_post_meta($post_id, '_genesis_title', true);
            $seo_data['description'] = get_post_meta($post_id, '_genesis_description', true);
            $seo_data['canonical'] = get_post_meta($post_id, '_genesis_canonical_uri', true);
            $seo_data['noindex'] = (bool) get_post_meta($post_id, '_genesis_noindex', true);
            $seo_data['nofollow'] = (bool) get_post_meta($post_id, '_genesis_nofollow', true);
            $seo_data['noarchive'] = (bool) get_post_meta($post_id, '_genesis_noarchive', true);
            
            // Get generated title/description if custom ones aren't set
            if (empty($seo_data['title']) && method_exists($tsf, 'get_title')) {
                $seo_data['generated_title'] = $tsf->get_title(['id' => $post_id]);
            }
            
            if (empty($seo_data['description']) && method_exists($tsf, 'get_description')) {
                $seo_data['generated_description'] = $tsf->get_description(['id' => $post_id]);
            }
        } else {
            // Fallback
            $seo_data['title'] = get_post_meta($post_id, '_wpbm_seo_title', true);
            $seo_data['description'] = get_post_meta($post_id, '_wpbm_seo_description', true);
        }
        
        return $seo_data;
    }
    
    /**
     * Handle plugins list
     */
    public function handle_get_plugins($request) {
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
                'active' => in_array($plugin_file, $active_plugins),
                'update_available' => false // Would need to check for updates
            ];
        }
        
        return [
            'plugins' => $plugins,
            'count' => count($plugins),
            'active_count' => count($active_plugins)
        ];
    }
    
    /**
     * Handle bulk operations
     */
    public function handle_bulk_operation($request) {
        $params = $request->get_json_params();
        $operation = $params['operation'];
        $items = $params['items'];
        
        $results = [];
        
        switch ($operation) {
            case 'create_pages':
                foreach ($items as $item) {
                    $post_id = wp_insert_post([
                        'post_title' => $item['title'],
                        'post_content' => $item['content'],
                        'post_type' => 'page',
                        'post_status' => $item['status'] ?? 'draft'
                    ]);
                    
                    if (!is_wp_error($post_id) && isset($item['seo'])) {
                        $this->update_seo_data($post_id, $item['seo']);
                    }
                    
                    $results[] = [
                        'success' => !is_wp_error($post_id),
                        'post_id' => is_wp_error($post_id) ? null : $post_id,
                        'error' => is_wp_error($post_id) ? $post_id->get_error_message() : null
                    ];
                }
                break;
                
            case 'update_seo':
                foreach ($items as $item) {
                    $this->update_seo_data($item['post_id'], $item['seo']);
                    $results[] = [
                        'success' => true,
                        'post_id' => $item['post_id']
                    ];
                }
                break;
        }
        
        return [
            'success' => true,
            'operation' => $operation,
            'results' => $results
        ];
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_options_page(
            'WP Bulk Manager Client',
            'Bulk Manager',
            'manage_options',
            'wp-bulk-manager-client',
            [$this, 'admin_page']
        );
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('wpbm_client_settings', 'wpbm_api_key');
        register_setting('wpbm_client_settings', 'wpbm_allowed_ips');
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        $api_key = get_option('wpbm_api_key');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Client</h1>
            
            <?php if (isset($_GET['settings-updated'])): ?>
                <div class="notice notice-success is-dismissible">
                    <p>Settings saved successfully!</p>
                </div>
            <?php endif; ?>
            
            <?php if (isset($_GET['key-generated'])): ?>
                <div class="notice notice-success is-dismissible">
                    <p>API key generated successfully!</p>
                </div>
            <?php endif; ?>
            
            <form method="post" action="options.php">
                <?php settings_fields('wpbm_client_settings'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">API Key</th>
                        <td>
                            <?php if ($api_key): ?>
                                <div style="margin-bottom: 15px;">
                                    <code id="api-key-display" style="background: #f0f0f0; padding: 10px 15px; font-size: 14px; display: inline-block; font-family: monospace; border: 1px solid #ddd; border-radius: 3px;"><?php echo esc_html($api_key); ?></code>
                                </div>
                                <button type="button" onclick="copyApiKey()" class="button">Copy to Clipboard</button>
                                <button type="button" onclick="generateNewKey()" class="button">Generate New Key</button>
                                <p class="description" style="margin-top: 10px;">Use this key in your WP Bulk Manager desktop application.</p>
                                
                                <script>
                                function copyApiKey() {
                                    const apiKey = document.getElementById('api-key-display').textContent;
                                    if (navigator.clipboard && navigator.clipboard.writeText) {
                                        navigator.clipboard.writeText(apiKey).then(function() {
                                            alert('API key copied to clipboard!');
                                        }).catch(function() {
                                            fallbackCopy(apiKey);
                                        });
                                    } else {
                                        fallbackCopy(apiKey);
                                    }
                                }
                                
                                function fallbackCopy(text) {
                                    const textArea = document.createElement("textarea");
                                    textArea.value = text;
                                    textArea.style.position = "fixed";
                                    textArea.style.left = "-999999px";
                                    document.body.appendChild(textArea);
                                    textArea.select();
                                    try {
                                        document.execCommand('copy');
                                        alert('API key copied to clipboard!');
                                    } catch (err) {
                                        alert('Please copy the API key manually');
                                    }
                                    document.body.removeChild(textArea);
                                }
                                
                                function generateNewKey() {
                                    if (!confirm('Generate a new API key? The old key will stop working.')) {
                                        return;
                                    }
                                    
                                    // Generate a random key client-side
                                    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
                                    let newKey = '';
                                    for (let i = 0; i < 32; i++) {
                                        newKey += characters.charAt(Math.floor(Math.random() * characters.length));
                                    }
                                    
                                    // Save via hidden form
                                    const form = document.createElement('form');
                                    form.method = 'post';
                                    form.action = 'options.php';
                                    
                                    const action = document.createElement('input');
                                    action.type = 'hidden';
                                    action.name = 'action';
                                    action.value = 'update';
                                    
                                    const option = document.createElement('input');
                                    option.type = 'hidden';
                                    option.name = 'option_page';
                                    option.value = 'wpbm_client_settings';
                                    
                                    const nonce = document.createElement('input');
                                    nonce.type = 'hidden';
                                    nonce.name = '_wpnonce';
                                    nonce.value = '<?php echo wp_create_nonce('wpbm_client_settings-options'); ?>';
                                    
                                    const referer = document.createElement('input');
                                    referer.type = 'hidden';
                                    referer.name = '_wp_http_referer';
                                    referer.value = '<?php echo esc_attr(wp_unslash($_SERVER['REQUEST_URI'])); ?>';
                                    
                                    const keyInput = document.createElement('input');
                                    keyInput.type = 'hidden';
                                    keyInput.name = 'wpbm_api_key';
                                    keyInput.value = newKey;
                                    
                                    form.appendChild(action);
                                    form.appendChild(option);
                                    form.appendChild(nonce);
                                    form.appendChild(referer);
                                    form.appendChild(keyInput);
                                    
                                    document.body.appendChild(form);
                                    form.submit();
                                }
                                </script>
                            <?php else: ?>
                                <button type="button" onclick="generateFirstKey()" class="button button-primary">Generate API Key</button>
                                <p class="description">Click to generate your first API key.</p>
                                <script>
                                function generateFirstKey() {
                                    // Generate a random key client-side
                                    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
                                    let newKey = '';
                                    for (let i = 0; i < 32; i++) {
                                        newKey += characters.charAt(Math.floor(Math.random() * characters.length));
                                    }
                                    
                                    // Save via hidden form
                                    const form = document.createElement('form');
                                    form.method = 'post';
                                    form.action = 'options.php';
                                    
                                    const action = document.createElement('input');
                                    action.type = 'hidden';
                                    action.name = 'action';
                                    action.value = 'update';
                                    
                                    const option = document.createElement('input');
                                    option.type = 'hidden';
                                    option.name = 'option_page';
                                    option.value = 'wpbm_client_settings';
                                    
                                    const nonce = document.createElement('input');
                                    nonce.type = 'hidden';
                                    nonce.name = '_wpnonce';
                                    nonce.value = '<?php echo wp_create_nonce('wpbm_client_settings-options'); ?>';
                                    
                                    const referer = document.createElement('input');
                                    referer.type = 'hidden';
                                    referer.name = '_wp_http_referer';
                                    referer.value = '<?php echo esc_attr(wp_unslash($_SERVER['REQUEST_URI'])); ?>';
                                    
                                    const keyInput = document.createElement('input');
                                    keyInput.type = 'hidden';
                                    keyInput.name = 'wpbm_api_key';
                                    keyInput.value = newKey;
                                    
                                    form.appendChild(action);
                                    form.appendChild(option);
                                    form.appendChild(nonce);
                                    form.appendChild(referer);
                                    form.appendChild(keyInput);
                                    
                                    document.body.appendChild(form);
                                    form.submit();
                                }
                                </script>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Allowed IPs</th>
                        <td>
                            <textarea name="wpbm_allowed_ips" rows="5" cols="50"><?php echo esc_textarea(get_option('wpbm_allowed_ips')); ?></textarea>
                            <p class="description">Optional: Enter one IP address per line to restrict access.</p>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button(); ?>
            </form>
            
            <h2>Connection Info</h2>
            <table class="form-table">
                <tr>
                    <th>Site URL</th>
                    <td><code><?php echo esc_url(get_site_url()); ?></code></td>
                </tr>
                <tr>
                    <th>API Endpoint</th>
                    <td><code><?php echo esc_url(rest_url('wpbm/v1/')); ?></code></td>
                </tr>
                <tr>
                    <th>Plugin Version</th>
                    <td><?php echo WPBM_CLIENT_VERSION; ?></td>
                </tr>
                <tr>
                    <th>SEO Framework</th>
                    <td><?php echo defined('THE_SEO_FRAMEWORK_VERSION') ? '✓ Active (v' . THE_SEO_FRAMEWORK_VERSION . ')' : '✗ Not Active'; ?></td>
                </tr>
            </table>
        </div>
        <?php
    }
    
    /**
     * Handle list content
     */
    public function handle_list_content($request) {
        $params = $request->get_query_params();
        
        $args = [
            'post_type' => $params['type'] ?? ['post', 'page'],
            'posts_per_page' => isset($params['limit']) ? intval($params['limit']) : 100,
            'post_status' => $params['status'] ?? 'any',
            'orderby' => $params['orderby'] ?? 'date',
            'order' => $params['order'] ?? 'DESC'
        ];
        
        if (isset($params['search'])) {
            $args['s'] = $params['search'];
        }
        
        $query = new WP_Query($args);
        $posts = [];
        
        foreach ($query->posts as $post) {
            $posts[] = [
                'id' => $post->ID,
                'title' => $post->post_title,
                'slug' => $post->post_name,
                'type' => $post->post_type,
                'status' => $post->post_status,
                'date' => $post->post_date,
                'modified' => $post->post_modified,
                'permalink' => get_permalink($post->ID),
                'edit_link' => get_edit_post_link($post->ID, 'raw'),
                'seo' => $this->get_seo_data($post->ID)
            ];
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages
        ];
    }
    
    /**
     * Handle duplicate content
     */
    public function handle_duplicate_content($request) {
        $post_id = absint($request->get_param('id'));
        $original = get_post($post_id);
        
        if (!$original) {
            return new WP_Error('post_not_found', 'Post not found', ['status' => 404]);
        }
        
        // Create duplicate
        $new_post = [
            'post_title' => $original->post_title . ' (Copy)',
            'post_content' => $original->post_content,
            'post_status' => 'draft',
            'post_type' => $original->post_type,
            'post_author' => get_current_user_id(),
            'post_parent' => $original->post_parent,
            'menu_order' => $original->menu_order
        ];
        
        $new_id = wp_insert_post($new_post);
        
        if (is_wp_error($new_id)) {
            return $new_id;
        }
        
        // Copy metadata
        $meta_data = get_post_meta($post_id);
        foreach ($meta_data as $key => $values) {
            // Skip certain meta keys
            if (in_array($key, ['_edit_lock', '_edit_last'])) {
                continue;
            }
            
            foreach ($values as $value) {
                add_post_meta($new_id, $key, maybe_unserialize($value));
            }
        }
        
        // Copy taxonomies
        $taxonomies = get_object_taxonomies($original->post_type);
        foreach ($taxonomies as $taxonomy) {
            $terms = wp_get_object_terms($post_id, $taxonomy, ['fields' => 'ids']);
            wp_set_object_terms($new_id, $terms, $taxonomy);
        }
        
        return [
            'success' => true,
            'post_id' => $new_id,
            'permalink' => get_permalink($new_id),
            'edit_link' => get_edit_post_link($new_id, 'raw')
        ];
    }
    
    /**
     * Handle delete content
     */
    public function handle_delete_content($request) {
        $post_id = absint($request->get_param('id'));
        $force = $request->get_param('force') === 'true';
        
        $result = wp_delete_post($post_id, $force);
        
        if (!$result) {
            return new WP_Error('delete_failed', 'Failed to delete post', ['status' => 500]);
        }
        
        return [
            'success' => true,
            'message' => $force ? 'Post permanently deleted' : 'Post moved to trash'
        ];
    }
    
    /**
     * Handle list SEO data
     */
    public function handle_list_seo($request) {
        $params = $request->get_query_params();
        
        $args = [
            'post_type' => $params['type'] ?? ['post', 'page'],
            'posts_per_page' => isset($params['limit']) ? intval($params['limit']) : 100,
            'post_status' => $params['status'] ?? 'publish'
        ];
        
        $query = new WP_Query($args);
        $seo_data = [];
        
        foreach ($query->posts as $post) {
            $seo = $this->get_seo_data($post->ID);
            $seo_data[] = [
                'id' => $post->ID,
                'title' => $post->post_title,
                'url' => get_permalink($post->ID),
                'seo_title' => $seo['title'] ?? '',
                'seo_description' => $seo['description'] ?? '',
                'generated_title' => $seo['generated_title'] ?? '',
                'generated_description' => $seo['generated_description'] ?? ''
            ];
        }
        
        return [
            'posts' => $seo_data,
            'total' => $query->found_posts
        ];
    }
    
    /**
     * Handle update plugins
     */
    public function handle_update_plugins($request) {
        if (!function_exists('get_plugin_updates')) {
            require_once ABSPATH . 'wp-admin/includes/update.php';
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        
        $plugins = $request->get_param('plugins');
        $results = [];
        
        // Get available updates
        wp_update_plugins();
        $updates = get_plugin_updates();
        
        foreach ($plugins as $plugin_file) {
            if (isset($updates[$plugin_file])) {
                // Perform update
                $skin = new Automatic_Upgrader_Skin();
                $upgrader = new Plugin_Upgrader($skin);
                $result = $upgrader->upgrade($plugin_file);
                
                $results[$plugin_file] = [
                    'success' => $result !== false,
                    'message' => $result === false ? 'Update failed' : 'Updated successfully'
                ];
            } else {
                $results[$plugin_file] = [
                    'success' => false,
                    'message' => 'No update available'
                ];
            }
        }
        
        return ['results' => $results];
    }
    
    /**
     * Handle get themes
     */
    public function handle_get_themes($request) {
        $themes = wp_get_themes();
        $theme_list = [];
        
        foreach ($themes as $theme_slug => $theme) {
            $theme_list[] = [
                'slug' => $theme_slug,
                'name' => $theme->get('Name'),
                'version' => $theme->get('Version'),
                'active' => get_stylesheet() === $theme_slug,
                'parent' => $theme->parent() ? $theme->parent()->get_stylesheet() : null,
                'update_available' => false // Would need to check for updates
            ];
        }
        
        return ['themes' => $theme_list];
    }
    
    /**
     * Handle update themes
     */
    public function handle_update_themes($request) {
        if (!function_exists('get_theme_updates')) {
            require_once ABSPATH . 'wp-admin/includes/update.php';
            require_once ABSPATH . 'wp-admin/includes/theme.php';
        }
        
        $themes = $request->get_param('themes');
        $results = [];
        
        // Get available updates
        wp_update_themes();
        $updates = get_theme_updates();
        
        foreach ($themes as $theme_slug) {
            if (isset($updates[$theme_slug])) {
                // Perform update
                $skin = new Automatic_Upgrader_Skin();
                $upgrader = new Theme_Upgrader($skin);
                $result = $upgrader->upgrade($theme_slug);
                
                $results[$theme_slug] = [
                    'success' => $result !== false,
                    'message' => $result === false ? 'Update failed' : 'Updated successfully'
                ];
            } else {
                $results[$theme_slug] = [
                    'success' => false,
                    'message' => 'No update available'
                ];
            }
        }
        
        return ['results' => $results];
    }
    
    /**
     * Initialize SEO Framework support
     */
    public function init_seo_framework_support() {
        if (!function_exists('the_seo_framework')) {
            return;
        }
        
        // Add custom filters for bulk operations
        add_filter('the_seo_framework_title_from_custom_field', [$this, 'filter_tsf_title'], 10, 2);
        add_filter('the_seo_framework_description_from_custom_field', [$this, 'filter_tsf_description'], 10, 2);
    }
    
    /**
     * Filter TSF title
     */
    public function filter_tsf_title($title, $args) {
        if (empty($title) && !empty($args['id'])) {
            $custom_title = get_post_meta($args['id'], '_wpbm_seo_title', true);
            if ($custom_title) {
                return $custom_title;
            }
        }
        return $title;
    }
    
    /**
     * Filter TSF description
     */
    public function filter_tsf_description($description, $args) {
        if (empty($description) && !empty($args['id'])) {
            $custom_desc = get_post_meta($args['id'], '_wpbm_seo_description', true);
            if ($custom_desc) {
                return $custom_desc;
            }
        }
        return $description;
    }
    
    /**
     * Handle get SEO Generator pages
     */
    public function handle_get_seo_generator_pages($request) {
        global $wpdb;
        
        // Check if SEO Generator is active
        if (!is_plugin_active('seo-generator/seo-generator.php')) {
            return new WP_Error('plugin_not_active', 'SEO Generator plugin is not active', ['status' => 404]);
        }
        
        // Get all SEO Generator pages
        $seo_pages = $wpdb->get_results(
            "SELECT p.ID, p.post_title, p.post_status, p.post_name,
                    pm1.meta_value as search_terms,
                    pm2.meta_value as locations,
                    pm3.meta_value as url_structure
             FROM {$wpdb->posts} p
             LEFT JOIN {$wpdb->postmeta} pm1 ON p.ID = pm1.post_id AND pm1.meta_key = 'seo_generator_search_terms'
             LEFT JOIN {$wpdb->postmeta} pm2 ON p.ID = pm2.post_id AND pm2.meta_key = 'seo_generator_locations'
             LEFT JOIN {$wpdb->postmeta} pm3 ON p.ID = pm3.post_id AND pm3.meta_key = 'seo_generator_url_structure'
             WHERE p.post_type = 'page' 
             AND (pm1.meta_value IS NOT NULL OR pm2.meta_value IS NOT NULL)
             ORDER BY p.post_title",
            ARRAY_A
        );
        
        $pages = [];
        foreach ($seo_pages as $page) {
            $search_terms = maybe_unserialize($page['search_terms']);
            $locations = maybe_unserialize($page['locations']);
            
            $pages[] = [
                'id' => $page['ID'],
                'title' => $page['post_title'],
                'status' => $page['post_status'],
                'slug' => $page['post_name'],
                'url_structure' => $page['url_structure'],
                'search_terms_count' => is_array($search_terms) ? count($search_terms) : 0,
                'locations_count' => is_array($locations) ? count($locations) : 0,
                'total_variations' => (is_array($search_terms) ? count($search_terms) : 0) * (is_array($locations) ? count($locations) : 0)
            ];
        }
        
        return [
            'pages' => $pages,
            'total' => count($pages)
        ];
    }
    
    /**
     * Handle get SEO Generator page details
     */
    public function handle_get_seo_generator_page($request) {
        $post_id = absint($request->get_param('id'));
        $post = get_post($post_id);
        
        if (!$post || $post->post_type !== 'page') {
            return new WP_Error('post_not_found', 'Page not found', ['status' => 404]);
        }
        
        // Get SEO Generator meta data
        $search_terms = get_post_meta($post_id, 'seo_generator_search_terms', true);
        $locations = get_post_meta($post_id, 'seo_generator_locations', true);
        $url_structure = get_post_meta($post_id, 'seo_generator_url_structure', true);
        
        // Get content to show dynamic field usage
        $content = $post->post_content;
        
        // Count dynamic field occurrences
        $search_term_count = substr_count($content, '[search_term]');
        $search_terms_count = substr_count($content, '[search_terms]');
        $location_count = substr_count($content, '[location]');
        
        return [
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $content,
            'url_structure' => $url_structure ?: '',
            'search_terms' => is_array($search_terms) ? $search_terms : [],
            'locations' => is_array($locations) ? $locations : [],
            'dynamic_fields' => [
                '[search_term]' => $search_term_count,
                '[search_terms]' => $search_terms_count,
                '[location]' => $location_count
            ],
            'limits' => [
                'max_search_terms' => 20,
                'max_locations' => 300
            ]
        ];
    }
    
    /**
     * Handle update SEO Generator page
     */
    public function handle_update_seo_generator_page($request) {
        $post_id = absint($request->get_param('id'));
        $params = $request->get_json_params();
        
        $post = get_post($post_id);
        if (!$post || $post->post_type !== 'page') {
            return new WP_Error('post_not_found', 'Page not found', ['status' => 404]);
        }
        
        $updated = [];
        
        // Update search terms
        if (isset($params['search_terms'])) {
            if (!is_array($params['search_terms'])) {
                return new WP_Error('invalid_data', 'Search terms must be an array', ['status' => 400]);
            }
            if (count($params['search_terms']) > 20) {
                return new WP_Error('limit_exceeded', 'Maximum 20 search terms allowed', ['status' => 400]);
            }
            
            // Clean and validate search terms
            $clean_terms = array_map('sanitize_text_field', $params['search_terms']);
            $clean_terms = array_filter($clean_terms); // Remove empty values
            
            update_post_meta($post_id, 'seo_generator_search_terms', $clean_terms);
            $updated['search_terms'] = count($clean_terms);
        }
        
        // Update locations
        if (isset($params['locations'])) {
            if (!is_array($params['locations'])) {
                return new WP_Error('invalid_data', 'Locations must be an array', ['status' => 400]);
            }
            if (count($params['locations']) > 300) {
                return new WP_Error('limit_exceeded', 'Maximum 300 locations allowed', ['status' => 400]);
            }
            
            // Clean and validate locations
            $clean_locations = array_map('sanitize_text_field', $params['locations']);
            $clean_locations = array_filter($clean_locations); // Remove empty values
            
            update_post_meta($post_id, 'seo_generator_locations', $clean_locations);
            $updated['locations'] = count($clean_locations);
        }
        
        // Update URL structure if provided
        if (isset($params['url_structure'])) {
            $url_structure = sanitize_text_field($params['url_structure']);
            update_post_meta($post_id, 'seo_generator_url_structure', $url_structure);
            $updated['url_structure'] = $url_structure;
        }
        
        // Update content if provided (to add/modify dynamic fields)
        if (isset($params['content'])) {
            $post_data = [
                'ID' => $post_id,
                'post_content' => wp_kses_post($params['content'])
            ];
            wp_update_post($post_data);
            $updated['content'] = true;
        }
        
        return [
            'success' => true,
            'post_id' => $post_id,
            'updated' => $updated,
            'total_variations' => isset($updated['search_terms']) || isset($updated['locations']) ? 
                count(get_post_meta($post_id, 'seo_generator_search_terms', true) ?: []) * 
                count(get_post_meta($post_id, 'seo_generator_locations', true) ?: []) : null
        ];
    }
}

// Initialize plugin
WP_Bulk_Manager_Client::get_instance();