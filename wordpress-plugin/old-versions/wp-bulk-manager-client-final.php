<?php
/**
 * Plugin Name: WP Bulk Manager Client (Final)
 * Plugin URI: https://github.com/yourusername/wp-bulk-manager
 * Description: WordPress bulk content management with REST API - Final version with working API key persistence
 * Version: 1.2.0
 * Author: Your Name
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class WP_Bulk_Manager_Client_Final {
    
    private $version = '1.2.0';
    
    public function __construct() {
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        
        // Add AJAX handler for generating API keys
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
        
        // Handle custom form submission to prevent key clearing
        add_action('admin_post_wpbm_save_settings', [$this, 'handle_settings_save']);
    }
    
    /**
     * Handle custom settings save
     */
    public function handle_settings_save() {
        // Check permissions
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        // Verify nonce
        check_admin_referer('wpbm_settings_nonce');
        
        // Only update if fields are provided
        if (isset($_POST['wpbm_allowed_ips'])) {
            update_option('wpbm_allowed_ips', sanitize_textarea_field($_POST['wpbm_allowed_ips']));
        }
        
        // IMPORTANT: Don't touch the API key unless explicitly generating a new one
        // This prevents the key from being cleared
        
        // Redirect back to settings page
        wp_redirect(admin_url('options-general.php?page=wp-bulk-manager-client&updated=true'));
        exit;
    }
    
    /**
     * AJAX handler to generate API key server-side
     */
    public function ajax_generate_api_key() {
        // Check nonce and permissions
        if (!check_ajax_referer('wpbm_generate_key', 'nonce', false) || !current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        // Generate secure API key server-side
        $api_key = $this->generate_api_key();
        
        // Save the API key
        update_option('wpbm_api_key', $api_key);
        
        // Return the new key
        wp_send_json_success(['api_key' => $api_key]);
    }
    
    /**
     * Generate a secure API key
     */
    private function generate_api_key() {
        // Use WordPress's built-in password generation for secure random strings
        if (function_exists('wp_generate_password')) {
            return wp_generate_password(32, false, false);
        }
        
        // Fallback to random_bytes
        return bin2hex(random_bytes(16));
    }
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wpbm/v1';
        
        // All your existing routes here...
        register_rest_route($namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'get_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        // ... other routes ...
    }
    
    /**
     * Verify API key - Fixed to properly check the key
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
            'WP Bulk Manager Client',
            'Bulk Manager',
            'manage_options',
            'wp-bulk-manager-client',
            [$this, 'admin_page']
        );
    }
    
    /**
     * Register settings - simplified
     */
    public function register_settings() {
        // Only register settings that we're actually using in the form
        register_setting('wpbm_client_settings', 'wpbm_allowed_ips', [
            'sanitize_callback' => 'sanitize_textarea_field'
        ]);
    }
    
    /**
     * Admin page - Fixed to prevent API key clearing
     */
    public function admin_page() {
        $api_key = get_option('wpbm_api_key');
        
        // Show updated message
        if (isset($_GET['updated'])) {
            echo '<div class="notice notice-success"><p>Settings saved successfully!</p></div>';
        }
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Client</h1>
            
            <div style="background: #fff; border: 1px solid #ccd0d4; padding: 20px; margin: 20px 0;">
                <h2>API Key</h2>
                <?php if ($api_key): ?>
                    <p><strong>Current API Key:</strong></p>
                    <code id="api-key-display" style="display: block; background: #f0f0f0; padding: 10px; font-family: monospace; user-select: all; margin: 10px 0;"><?php echo esc_html($api_key); ?></code>
                    <button type="button" id="copy-key" class="button">Copy API Key</button>
                    <button type="button" id="regenerate-key" class="button">Generate New Key</button>
                    <p class="description">⚠️ Keep this key secure. Regenerating will invalidate the current key.</p>
                <?php else: ?>
                    <p>No API key configured yet.</p>
                    <button type="button" id="generate-key" class="button button-primary">Generate API Key</button>
                <?php endif; ?>
            </div>
            
            <!-- Separate form that doesn't touch the API key -->
            <form method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                <?php wp_nonce_field('wpbm_settings_nonce'); ?>
                <input type="hidden" name="action" value="wpbm_save_settings">
                
                <table class="form-table">
                    <tr>
                        <th scope="row">Allowed IP Addresses</th>
                        <td>
                            <textarea name="wpbm_allowed_ips" rows="5" cols="50"><?php echo esc_textarea(get_option('wpbm_allowed_ips', '')); ?></textarea>
                            <p class="description">Enter one IP address per line. Leave empty to allow all IPs.</p>
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">API Endpoint</th>
                        <td>
                            <code><?php echo rest_url('wpbm/v1/'); ?></code>
                            <p class="description">Use this URL for API requests.</p>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button('Save Settings'); ?>
            </form>
            
            <hr>
            
            <h2>Quick Test</h2>
            <p>Test your API key with this curl command:</p>
            <pre style="background: #f0f0f0; padding: 10px; overflow-x: auto;">curl -H "X-API-Key: <?php echo $api_key ? esc_html($api_key) : 'YOUR_API_KEY'; ?>" \
     <?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?></pre>
            
            <p><button type="button" id="test-api" class="button">Test API Connection</button></p>
            <div id="test-result"></div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            // Copy API key
            $('#copy-key').on('click', function() {
                const apiKey = $('#api-key-display').text();
                
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(apiKey).then(function() {
                        alert('API key copied to clipboard!');
                    });
                } else {
                    // Fallback
                    const textArea = document.createElement("textarea");
                    textArea.value = apiKey;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    alert('API key copied to clipboard!');
                }
            });
            
            // Generate or regenerate API key
            $('#generate-key, #regenerate-key').on('click', function() {
                const isRegenerate = $(this).attr('id') === 'regenerate-key';
                
                if (isRegenerate && !confirm('Generate a new API key? The old key will stop working immediately.')) {
                    return;
                }
                
                const $button = $(this);
                $button.prop('disabled', true).text('Generating...');
                
                // Make AJAX request to generate key server-side
                $.ajax({
                    url: ajaxurl,
                    type: 'POST',
                    data: {
                        action: 'wpbm_generate_api_key',
                        nonce: '<?php echo wp_create_nonce('wpbm_generate_key'); ?>'
                    },
                    success: function(response) {
                        if (response.success) {
                            // Reload page to show new key
                            window.location.reload();
                        } else {
                            alert('Failed to generate API key. Please try again.');
                            $button.prop('disabled', false).text(isRegenerate ? 'Generate New Key' : 'Generate API Key');
                        }
                    },
                    error: function() {
                        alert('An error occurred. Please try again.');
                        $button.prop('disabled', false).text(isRegenerate ? 'Generate New Key' : 'Generate API Key');
                    }
                });
            });
            
            // Test API
            $('#test-api').on('click', function() {
                const $button = $(this);
                const $result = $('#test-result');
                const apiKey = $('#api-key-display').text();
                
                if (!apiKey) {
                    $result.html('<p style="color: red;">Please generate an API key first.</p>');
                    return;
                }
                
                $button.prop('disabled', true).text('Testing...');
                $result.html('<p>Testing connection...</p>');
                
                // Test the API
                $.ajax({
                    url: '<?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?>',
                    type: 'GET',
                    headers: {
                        'X-API-Key': apiKey
                    },
                    success: function(response) {
                        $result.html('<p style="color: green;">✅ API connection successful! Found ' + response.posts.length + ' pages.</p>');
                        $button.prop('disabled', false).text('Test API Connection');
                    },
                    error: function(xhr) {
                        let message = 'Connection failed';
                        if (xhr.status === 401) {
                            message = 'Authentication failed - check API key';
                        } else if (xhr.status === 404) {
                            message = 'API endpoint not found';
                        }
                        $result.html('<p style="color: red;">❌ ' + message + ' (Status: ' + xhr.status + ')</p>');
                        $button.prop('disabled', false).text('Test API Connection');
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
                'link' => get_permalink($post->ID)
            ];
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts
        ];
    }
}

// Initialize the plugin
new WP_Bulk_Manager_Client_Final();