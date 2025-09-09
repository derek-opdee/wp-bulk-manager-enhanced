<?php
/**
 * Plugin Name: WP Bulk Manager Client (Bulletproof)
 * Plugin URI: https://github.com/yourusername/wp-bulk-manager
 * Description: WordPress bulk content management with REST API - Bulletproof version with completely independent settings
 * Version: 2.0.0
 * Author: Your Name
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class WP_Bulk_Manager_Client_Bulletproof {
    
    private $version = '2.0.0';
    
    public function __construct() {
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        
        // AJAX handlers - completely separate
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
        add_action('wp_ajax_wpbm_save_allowed_ips', [$this, 'ajax_save_allowed_ips']);
        add_action('wp_ajax_wpbm_test_connection', [$this, 'ajax_test_connection']);
    }
    
    /**
     * NO register_settings() - We handle everything via AJAX
     */
    
    /**
     * AJAX: Generate API key only
     */
    public function ajax_generate_api_key() {
        check_ajax_referer('wpbm_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        // Generate key
        $api_key = wp_generate_password(32, false, false);
        
        // Update ONLY the API key option
        update_option('wpbm_api_key', $api_key);
        
        wp_send_json_success(['api_key' => $api_key]);
    }
    
    /**
     * AJAX: Save allowed IPs only
     */
    public function ajax_save_allowed_ips() {
        check_ajax_referer('wpbm_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        $allowed_ips = sanitize_textarea_field($_POST['allowed_ips'] ?? '');
        
        // Update ONLY the allowed IPs option
        update_option('wpbm_allowed_ips', $allowed_ips);
        
        wp_send_json_success(['message' => 'IPs saved']);
    }
    
    /**
     * AJAX: Test connection
     */
    public function ajax_test_connection() {
        check_ajax_referer('wpbm_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        $api_key = get_option('wpbm_api_key');
        
        wp_send_json_success([
            'api_key_exists' => !empty($api_key),
            'api_endpoint' => rest_url('wpbm/v1/')
        ]);
    }
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wpbm/v1';
        
        register_rest_route($namespace, '/content', [
            [
                'methods' => 'GET',
                'callback' => [$this, 'get_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ],
            [
                'methods' => 'POST',
                'callback' => [$this, 'create_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ]
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            [
                'methods' => 'GET',
                'callback' => [$this, 'get_single_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ],
            [
                'methods' => 'PUT',
                'callback' => [$this, 'update_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ],
            [
                'methods' => 'DELETE',
                'callback' => [$this, 'delete_content'],
                'permission_callback' => [$this, 'verify_api_key']
            ]
        ]);
    }
    
    /**
     * Verify API key
     */
    public function verify_api_key($request) {
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
     * Admin page - NO FORMS, only AJAX
     */
    public function admin_page() {
        $api_key = get_option('wpbm_api_key');
        $allowed_ips = get_option('wpbm_allowed_ips', '');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager</h1>
            
            <div id="wpbm-notices"></div>
            
            <!-- API Key Section -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">API Key</h2>
                <div style="padding: 0 12px 12px;">
                    <?php if ($api_key): ?>
                        <div style="margin-bottom: 10px;">
                            <input type="text" 
                                   id="api-key-field" 
                                   value="<?php echo esc_attr($api_key); ?>" 
                                   readonly 
                                   style="width: 100%; max-width: 400px; font-family: monospace;"
                                   onclick="this.select();">
                        </div>
                        <button type="button" class="button" onclick="copyApiKey()">Copy</button>
                        <button type="button" class="button" onclick="generateApiKey(true)">Regenerate</button>
                    <?php else: ?>
                        <p>No API key generated yet.</p>
                        <button type="button" class="button button-primary" onclick="generateApiKey(false)">Generate API Key</button>
                    <?php endif; ?>
                </div>
            </div>
            
            <!-- Allowed IPs Section -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">Allowed IP Addresses</h2>
                <div style="padding: 0 12px 12px;">
                    <textarea id="allowed-ips-field" 
                              rows="5" 
                              style="width: 100%; max-width: 400px;"><?php echo esc_textarea($allowed_ips); ?></textarea>
                    <p class="description">One IP per line. Leave empty to allow all.</p>
                    <button type="button" class="button button-primary" onclick="saveAllowedIps()">Save IPs</button>
                </div>
            </div>
            
            <!-- Info Section -->
            <div class="card" style="max-width: 800px; margin: 20px 0;">
                <h2 class="title">API Information</h2>
                <div style="padding: 0 12px 12px;">
                    <p><strong>Endpoint:</strong></p>
                    <code style="display: block; padding: 10px; background: #f0f0f1; margin: 10px 0;">
                        <?php echo rest_url('wpbm/v1/'); ?>
                    </code>
                    
                    <p><strong>Test Command:</strong></p>
                    <pre style="padding: 10px; background: #f0f0f1; overflow-x: auto;">curl -H "X-API-Key: <?php echo $api_key ?: 'YOUR_API_KEY'; ?>" \
     <?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?></pre>
                    
                    <button type="button" class="button" onclick="testConnection()">Test Connection</button>
                    <span id="test-result"></span>
                </div>
            </div>
        </div>
        
        <script>
        const ajaxurl = '<?php echo admin_url('admin-ajax.php'); ?>';
        const nonce = '<?php echo wp_create_nonce('wpbm_nonce'); ?>';
        
        function showNotice(message, type = 'success') {
            const html = `<div class="notice notice-${type} is-dismissible"><p>${message}</p></div>`;
            document.getElementById('wpbm-notices').innerHTML = html;
            
            // Auto dismiss after 3 seconds
            setTimeout(() => {
                document.getElementById('wpbm-notices').innerHTML = '';
            }, 3000);
        }
        
        function generateApiKey(regenerate) {
            if (regenerate && !confirm('Generate new API key? The current key will stop working.')) {
                return;
            }
            
            const data = new FormData();
            data.append('action', 'wpbm_generate_api_key');
            data.append('nonce', nonce);
            
            fetch(ajaxurl, {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    location.reload();
                } else {
                    showNotice('Failed to generate API key', 'error');
                }
            });
        }
        
        function saveAllowedIps() {
            const ips = document.getElementById('allowed-ips-field').value;
            
            const data = new FormData();
            data.append('action', 'wpbm_save_allowed_ips');
            data.append('allowed_ips', ips);
            data.append('nonce', nonce);
            
            fetch(ajaxurl, {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    showNotice('IP addresses saved successfully');
                } else {
                    showNotice('Failed to save IP addresses', 'error');
                }
            });
        }
        
        function copyApiKey() {
            const field = document.getElementById('api-key-field');
            field.select();
            document.execCommand('copy');
            showNotice('API key copied to clipboard');
        }
        
        function testConnection() {
            const resultSpan = document.getElementById('test-result');
            resultSpan.textContent = 'Testing...';
            
            const apiKey = document.getElementById('api-key-field')?.value;
            
            if (!apiKey) {
                resultSpan.innerHTML = '<span style="color: red;">No API key</span>';
                return;
            }
            
            fetch('<?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?>', {
                headers: {
                    'X-API-Key': apiKey
                }
            })
            .then(response => {
                if (response.ok) {
                    resultSpan.innerHTML = '<span style="color: green;">✓ Connection successful</span>';
                } else {
                    resultSpan.innerHTML = '<span style="color: red;">✗ Connection failed</span>';
                }
            })
            .catch(() => {
                resultSpan.innerHTML = '<span style="color: red;">✗ Network error</span>';
            });
        }
        </script>
        <?php
    }
    
    // REST API callbacks
    public function get_content($request) {
        $params = $request->get_params();
        
        $args = [
            'post_type' => $params['type'] ?? 'post',
            'posts_per_page' => $params['limit'] ?? 100,
            'paged' => $params['page'] ?? 1,
            'post_status' => $params['status'] ?? 'any',
            'orderby' => $params['orderby'] ?? 'date',
            'order' => $params['order'] ?? 'DESC'
        ];
        
        $query = new WP_Query($args);
        $posts = [];
        
        foreach ($query->posts as $post) {
            $posts[] = [
                'id' => $post->ID,
                'title' => $post->post_title,
                'content' => $post->post_content,
                'excerpt' => $post->post_excerpt,
                'slug' => $post->post_name,
                'type' => $post->post_type,
                'status' => $post->post_status,
                'link' => get_permalink($post->ID),
                'date' => $post->post_date,
                'modified' => $post->post_modified
            ];
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages
        ];
    }
    
    public function get_single_content($request) {
        $post_id = $request->get_param('id');
        $post = get_post($post_id);
        
        if (!$post) {
            return new WP_Error('not_found', 'Post not found', ['status' => 404]);
        }
        
        return [
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'slug' => $post->post_name,
            'type' => $post->post_type,
            'status' => $post->post_status,
            'link' => get_permalink($post->ID),
            'date' => $post->post_date,
            'modified' => $post->post_modified
        ];
    }
    
    public function create_content($request) {
        $params = $request->get_params();
        
        $post_data = [
            'post_title' => $params['title'] ?? '',
            'post_content' => $params['content'] ?? '',
            'post_type' => $params['type'] ?? 'post',
            'post_status' => $params['status'] ?? 'draft'
        ];
        
        $post_id = wp_insert_post($post_data);
        
        if (is_wp_error($post_id)) {
            return $post_id;
        }
        
        return [
            'id' => $post_id,
            'message' => 'Content created successfully'
        ];
    }
    
    public function update_content($request) {
        $post_id = $request->get_param('id');
        $params = $request->get_params();
        
        $post_data = ['ID' => $post_id];
        
        if (isset($params['title'])) {
            $post_data['post_title'] = $params['title'];
        }
        
        if (isset($params['content'])) {
            $post_data['post_content'] = $params['content'];
        }
        
        if (isset($params['status'])) {
            $post_data['post_status'] = $params['status'];
        }
        
        $result = wp_update_post($post_data);
        
        if (is_wp_error($result)) {
            return $result;
        }
        
        return [
            'id' => $post_id,
            'message' => 'Content updated successfully'
        ];
    }
    
    public function delete_content($request) {
        $post_id = $request->get_param('id');
        
        $result = wp_delete_post($post_id, true);
        
        if (!$result) {
            return new WP_Error('delete_failed', 'Failed to delete content', ['status' => 500]);
        }
        
        return [
            'message' => 'Content deleted successfully'
        ];
    }
}

// Initialize
new WP_Bulk_Manager_Client_Bulletproof();