<?php
/**
 * Plugin Name: WP Bulk Manager Client (Fixed)
 * Plugin URI: https://github.com/yourusername/wp-bulk-manager
 * Description: WordPress bulk content management with REST API - Fixed version with proper API key handling
 * Version: 1.1.0
 * Author: Your Name
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class WP_Bulk_Manager_Client_Fixed {
    
    private $version = '1.1.0';
    
    public function __construct() {
        add_action('rest_api_init', [$this, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        
        // Add AJAX handler for generating API keys
        add_action('wp_ajax_wpbm_generate_api_key', [$this, 'ajax_generate_api_key']);
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
        
        // Content endpoints
        register_rest_route($namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'get_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content', [
            'methods' => 'POST',
            'callback' => [$this, 'create_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_single_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_content'],
            'permission_callback' => [$this, 'verify_api_key']
        ]);
        
        register_rest_route($namespace, '/content/(?P<id>\d+)', [
            'methods' => 'DELETE',
            'callback' => [$this, 'delete_content'],
            'permission_callback' => [$this, 'verify_api_key']
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
        
        // Use timing-safe comparison
        return hash_equals($stored_key, $provided_key);
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
        register_setting('wpbm_client_settings', 'wpbm_api_key', [
            'sanitize_callback' => 'sanitize_text_field'
        ]);
        register_setting('wpbm_client_settings', 'wpbm_allowed_ips', [
            'sanitize_callback' => 'sanitize_textarea_field'
        ]);
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        $api_key = get_option('wpbm_api_key');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Client</h1>
            
            <form method="post" action="options.php">
                <?php settings_fields('wpbm_client_settings'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">API Key</th>
                        <td>
                            <?php if ($api_key): ?>
                                <code id="api-key-display" style="background: #f0f0f0; padding: 8px 12px; font-family: monospace; user-select: all;"><?php echo esc_html($api_key); ?></code>
                                <button type="button" id="copy-key" class="button">Copy</button>
                                <button type="button" id="regenerate-key" class="button">Regenerate</button>
                                <p class="description">Keep this key secure. It provides full access to your content.</p>
                            <?php else: ?>
                                <button type="button" id="generate-key" class="button button-primary">Generate API Key</button>
                                <p class="description">Click to generate your first API key.</p>
                            <?php endif; ?>
                            <input type="hidden" name="wpbm_api_key" id="wpbm_api_key" value="<?php echo esc_attr($api_key); ?>" />
                        </td>
                    </tr>
                    
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
                
                <?php submit_button(); ?>
            </form>
            
            <hr>
            
            <h2>Quick Test</h2>
            <p>Test your API key with this curl command:</p>
            <pre style="background: #f0f0f0; padding: 10px; overflow-x: auto;">curl -H "X-API-Key: <?php echo $api_key ? esc_html($api_key) : 'YOUR_API_KEY'; ?>" \
     <?php echo rest_url('wpbm/v1/content?type=page&limit=1'); ?></pre>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            // Copy API key
            $('#copy-key').on('click', function() {
                const apiKey = $('#api-key-display').text();
                
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(apiKey).then(function() {
                        alert('API key copied to clipboard!');
                    }).catch(function() {
                        fallbackCopy(apiKey);
                    });
                } else {
                    fallbackCopy(apiKey);
                }
            });
            
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
                            // Update the hidden input
                            $('#wpbm_api_key').val(response.data.api_key);
                            
                            // Submit the form to save
                            $('form').submit();
                        } else {
                            alert('Failed to generate API key. Please try again.');
                            $button.prop('disabled', false).text(isRegenerate ? 'Regenerate' : 'Generate API Key');
                        }
                    },
                    error: function() {
                        alert('An error occurred. Please try again.');
                        $button.prop('disabled', false).text(isRegenerate ? 'Regenerate' : 'Generate API Key');
                    }
                });
            });
        });
        </script>
        <?php
    }
    
    // REST API callbacks (simplified for this example)
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
                'content' => $post->post_content,
                'status' => $post->post_status,
                'type' => $post->post_type,
                'link' => get_permalink($post->ID)
            ];
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts
        ];
    }
    
    // Other endpoint implementations...
}

// Initialize the plugin
new WP_Bulk_Manager_Client_Fixed();