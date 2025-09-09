<?php
/**
 * Plugin Name: WP Bulk Manager Client (Separated)
 * Plugin URI: https://github.com/yourusername/wp-bulk-manager
 * Description: WordPress bulk content management with REST API - Properly separated API key management
 * Version: 1.3.0
 * Author: Your Name
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class WP_Bulk_Manager_Client_Separated {
    
    private $version = '1.3.0';
    
    public function __construct() {
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        
        // AJAX handlers
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
        add_action('wp_ajax_wpbm_test_api_key', [$this, 'ajax_test_api_key']);
    }
    
    /**
     * Register settings - ONLY for non-API key settings
     */
    public function register_settings() {
        // IMPORTANT: We do NOT register wpbm_api_key here
        // This prevents it from being touched by the settings form
        register_setting('wpbm_client_settings', 'wpbm_allowed_ips', [
            'sanitize_callback' => 'sanitize_textarea_field'
        ]);
    }
    
    /**
     * AJAX handler to generate API key
     */
    public function ajax_generate_api_key() {
        // Check nonce and permissions
        if (!check_ajax_referer('wpbm_ajax_nonce', 'nonce', false) || !current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        // Generate secure API key
        $api_key = wp_generate_password(32, false, false);
        
        // Save directly (not through settings API)
        update_option('wpbm_api_key', $api_key, false);
        
        wp_send_json_success(['api_key' => $api_key]);
    }
    
    /**
     * AJAX handler to test API key
     */
    public function ajax_test_api_key() {
        // Check nonce and permissions
        if (!check_ajax_referer('wpbm_ajax_nonce', 'nonce', false) || !current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        $api_key = get_option('wpbm_api_key');
        
        if (empty($api_key)) {
            wp_send_json_error('No API key configured');
        }
        
        // Test by making a simple query
        $test_url = rest_url('wpbm/v1/content?type=page&limit=1');
        
        wp_send_json_success([
            'api_key' => $api_key,
            'test_url' => $test_url
        ]);
    }
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wpbm/v1';
        
        register_rest_route($namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'get_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_single_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // Add other routes as needed...
    }
    
    /**
     * Verify API key
     */
    public function verify_api_key($request) {
        $provided_key = $request->get_header('X-API-Key');
        
        if (empty($provided_key)) {
            return new WP_Error('missing_api_key', 'API key is required', ['status' => 401]);
        }
        
        $stored_key = get_option('wpbm_api_key');
        
        if (empty($stored_key)) {
            return new WP_Error('no_api_key_configured', 'No API key configured', ['status' => 401]);
        }
        
        // Use timing-safe comparison
        if (!hash_equals($stored_key, $provided_key)) {
            return new WP_Error('invalid_api_key', 'Invalid API key', ['status' => 401]);
        }
        
        return true;
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
        $api_key = get_option('wpbm_api_key');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager</h1>
            
            <?php if (isset($_GET['settings-updated'])): ?>
                <div class="notice notice-success is-dismissible">
                    <p>Settings saved successfully!</p>
                </div>
            <?php endif; ?>
            
            <!-- API Key Section (Completely Separate) -->
            <div class="card" style="max-width: 800px; margin-top: 20px;">
                <h2 class="title">API Key Management</h2>
                <div style="padding: 0 12px 12px;">
                    <?php if ($api_key): ?>
                        <p><strong>Current API Key:</strong></p>
                        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 10px;">
                            <input type="text" 
                                   id="api-key-display" 
                                   value="<?php echo esc_attr($api_key); ?>" 
                                   readonly 
                                   style="font-family: monospace; width: 350px;"
                                   onclick="this.select();">
                            <button type="button" class="button" id="copy-api-key">Copy</button>
                            <button type="button" class="button" id="regenerate-api-key">Regenerate</button>
                        </div>
                        <p class="description">
                            ⚠️ Keep this key secure. It provides full API access to your content.
                        </p>
                    <?php else: ?>
                        <p>No API key configured yet.</p>
                        <button type="button" class="button button-primary" id="generate-api-key">Generate API Key</button>
                    <?php endif; ?>
                    
                    <hr style="margin: 20px 0;">
                    
                    <p><strong>API Endpoint:</strong></p>
                    <code style="background: #f0f0f1; padding: 5px; display: block; margin: 10px 0;">
                        <?php echo rest_url('wpbm/v1/'); ?>
                    </code>
                    
                    <button type="button" class="button" id="test-connection">Test Connection</button>
                    <span id="test-result" style="margin-left: 10px;"></span>
                </div>
            </div>
            
            <!-- Settings Form (Separate from API Key) -->
            <form method="post" action="options.php" style="margin-top: 20px;">
                <?php settings_fields('wpbm_client_settings'); ?>
                
                <div class="card" style="max-width: 800px;">
                    <h2 class="title">Security Settings</h2>
                    <table class="form-table" role="presentation">
                        <tr>
                            <th scope="row">Allowed IP Addresses</th>
                            <td>
                                <textarea name="wpbm_allowed_ips" 
                                          rows="5" 
                                          cols="50"
                                          class="large-text"><?php echo esc_textarea(get_option('wpbm_allowed_ips', '')); ?></textarea>
                                <p class="description">
                                    Enter one IP address per line. Leave empty to allow all IPs.<br>
                                    Supports CIDR notation (e.g., 192.168.1.0/24)
                                </p>
                            </td>
                        </tr>
                    </table>
                    
                    <?php submit_button('Save Settings'); ?>
                </div>
            </form>
            
            <!-- Quick Test Section -->
            <div class="card" style="max-width: 800px; margin-top: 20px;">
                <h2 class="title">Quick Test</h2>
                <div style="padding: 0 12px 12px;">
                    <p>Test your API with this curl command:</p>
                    <pre style="background: #f0f0f1; padding: 10px; overflow-x: auto;">curl -H "X-API-Key: <?php echo $api_key ?: 'YOUR_API_KEY'; ?>" \
     <?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?></pre>
                </div>
            </div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            const ajaxUrl = '<?php echo admin_url('admin-ajax.php'); ?>';
            const nonce = '<?php echo wp_create_nonce('wpbm_ajax_nonce'); ?>';
            
            // Copy API key
            $('#copy-api-key').on('click', function() {
                const input = document.getElementById('api-key-display');
                input.select();
                
                try {
                    document.execCommand('copy');
                    $(this).text('Copied!');
                    setTimeout(() => $(this).text('Copy'), 2000);
                } catch (err) {
                    alert('Please copy manually');
                }
            });
            
            // Generate/Regenerate API key
            $('#generate-api-key, #regenerate-api-key').on('click', function() {
                if ($(this).attr('id') === 'regenerate-api-key') {
                    if (!confirm('Generate a new API key? The current key will stop working immediately.')) {
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
                        location.reload();
                    } else {
                        alert('Failed to generate API key');
                        $button.prop('disabled', false).text('Generate API Key');
                    }
                });
            });
            
            // Test connection
            $('#test-connection').on('click', function() {
                const $button = $(this);
                const $result = $('#test-result');
                const apiKey = $('#api-key-display').val();
                
                if (!apiKey) {
                    $result.html('<span style="color: red;">No API key configured</span>');
                    return;
                }
                
                $button.prop('disabled', true).text('Testing...');
                $result.html('<span style="color: #666;">Testing...</span>');
                
                // Test the API directly
                $.ajax({
                    url: '<?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?>',
                    method: 'GET',
                    headers: {
                        'X-API-Key': apiKey
                    },
                    success: function(data) {
                        $result.html('<span style="color: green;">✓ Connection successful!</span>');
                        $button.prop('disabled', false).text('Test Connection');
                    },
                    error: function(xhr) {
                        const msg = xhr.status === 401 ? 'Invalid API key' : 'Connection failed';
                        $result.html('<span style="color: red;">✗ ' + msg + '</span>');
                        $button.prop('disabled', false).text('Test Connection');
                    }
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
            'post_type' => $params['type'] ?? 'post',
            'posts_per_page' => $params['limit'] ?? 100,
            'paged' => $params['page'] ?? 1,
            'post_status' => $params['status'] ?? 'any'
        ];
        
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
                'edit_link' => get_edit_post_link($post->ID, 'raw')
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
            return new WP_Error('post_not_found', 'Post not found', ['status' => 404]);
        }
        
        return [
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'slug' => $post->post_name,
            'type' => $post->post_type,
            'status' => $post->post_status,
            'date' => $post->post_date,
            'modified' => $post->post_modified,
            'permalink' => get_permalink($post->ID)
        ];
    }
}

// Initialize plugin
new WP_Bulk_Manager_Client_Separated();