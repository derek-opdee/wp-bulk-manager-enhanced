<?php
/**
 * Plugin Name: WP Bulk Manager Client v2
 * Plugin URI: https://github.com/yourusername/wp-bulk-manager
 * Description: Enhanced WordPress bulk content management with REST API - Refactored version
 * Version: 2.0.0
 * Author: Derek Zar
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('WPBM_VERSION', '2.0.0');
define('WPBM_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WPBM_PLUGIN_URL', plugin_dir_url(__FILE__));

// Autoload classes
spl_autoload_register(function ($class) {
    if (strpos($class, 'WPBM_') !== 0) {
        return;
    }
    
    $class_file = 'class-' . strtolower(str_replace('_', '-', $class)) . '.php';
    $class_path = WPBM_PLUGIN_DIR . 'includes/' . $class_file;
    
    if (file_exists($class_path)) {
        require_once $class_path;
    }
});

// Main plugin class
class WP_Bulk_Manager_Client {
    
    private static $instance = null;
    private $security;
    private $api_handler;
    private $seo_manager;
    
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
        $this->init();
    }
    
    /**
     * Initialize plugin
     */
    private function init() {
        // Initialize components
        $this->security = new WPBM_Security();
        $this->api_handler = new WPBM_API_Handler($this->security);
        $this->seo_manager = new WPBM_SEO_Manager();
        
        // Register hooks
        add_action('rest_api_init', [$this->api_handler, 'register_routes']);
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        add_action('admin_enqueue_scripts', [$this, 'enqueue_admin_scripts']);
        
        // Add custom capabilities
        add_action('init', [$this, 'add_capabilities']);
        
        // Add cron jobs for cleanup
        add_action('wpbm_cleanup_cron', [$this, 'cleanup_old_data']);
        
        // Schedule cron if not already scheduled
        if (!wp_next_scheduled('wpbm_cleanup_cron')) {
            wp_schedule_event(time(), 'daily', 'wpbm_cleanup_cron');
        }
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            'WP Bulk Manager',
            'Bulk Manager',
            'manage_options',
            'wp-bulk-manager',
            [$this, 'admin_page'],
            'dashicons-database',
            30
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'Settings',
            'Settings',
            'manage_options',
            'wp-bulk-manager-settings',
            [$this, 'settings_page']
        );
        
        add_submenu_page(
            'wp-bulk-manager',
            'Activity Log',
            'Activity Log',
            'manage_options',
            'wp-bulk-manager-logs',
            [$this, 'logs_page']
        );
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('wpbm_settings', 'wpbm_api_key');
        register_setting('wpbm_settings', 'wpbm_allowed_ips');
        register_setting('wpbm_settings', 'wpbm_enable_logging');
        register_setting('wpbm_settings', 'wpbm_rate_limits');
    }
    
    /**
     * Enqueue admin scripts
     */
    public function enqueue_admin_scripts($hook) {
        if (strpos($hook, 'wp-bulk-manager') === false) {
            return;
        }
        
        wp_enqueue_script(
            'wpbm-admin',
            WPBM_PLUGIN_URL . 'assets/js/admin.js',
            ['jquery'],
            WPBM_VERSION,
            true
        );
        
        wp_enqueue_style(
            'wpbm-admin',
            WPBM_PLUGIN_URL . 'assets/css/admin.css',
            [],
            WPBM_VERSION
        );
        
        wp_localize_script('wpbm-admin', 'wpbm_ajax', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('wpbm_ajax_nonce')
        ]);
    }
    
    /**
     * Main admin page
     */
    public function admin_page() {
        $api_key = get_option('wpbm_api_key');
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager</h1>
            
            <?php if (empty($api_key)): ?>
                <div class="notice notice-warning">
                    <p>Please configure your API key in the <a href="<?php echo admin_url('admin.php?page=wp-bulk-manager-settings'); ?>">settings</a>.</p>
                </div>
            <?php else: ?>
                <div class="wpbm-dashboard">
                    <div class="wpbm-card">
                        <h2>API Status</h2>
                        <p>API Key: <code><?php echo substr($api_key, 0, 8) . '...' . substr($api_key, -8); ?></code></p>
                        <p>Endpoint: <code><?php echo rest_url('wpbm/v1/'); ?></code></p>
                    </div>
                    
                    <div class="wpbm-card">
                        <h2>Quick Stats</h2>
                        <?php $this->display_stats(); ?>
                    </div>
                    
                    <div class="wpbm-card">
                        <h2>Recent Activity</h2>
                        <?php $this->display_recent_activity(); ?>
                    </div>
                </div>
            <?php endif; ?>
        </div>
        <?php
    }
    
    /**
     * Settings page
     */
    public function settings_page() {
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Settings</h1>
            
            <form method="post" action="options.php">
                <?php settings_fields('wpbm_settings'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">API Key</th>
                        <td>
                            <?php
                            $api_key = get_option('wpbm_api_key');
                            if (empty($api_key)): ?>
                                <input type="text" name="wpbm_api_key" value="" class="regular-text" />
                                <button type="button" class="button" id="generate-api-key">Generate New Key</button>
                            <?php else: ?>
                                <code><?php echo esc_html($api_key); ?></code>
                                <button type="button" class="button" id="regenerate-api-key">Regenerate</button>
                            <?php endif; ?>
                            <p class="description">This key is required for API authentication.</p>
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">Allowed IP Addresses</th>
                        <td>
                            <textarea name="wpbm_allowed_ips" rows="5" cols="50"><?php echo esc_textarea(get_option('wpbm_allowed_ips', '')); ?></textarea>
                            <p class="description">Enter one IP address per line. Leave empty to allow all IPs. Supports CIDR notation (e.g., 192.168.1.0/24).</p>
                        </td>
                    </tr>
                    
                    <tr>
                        <th scope="row">Enable Logging</th>
                        <td>
                            <label>
                                <input type="checkbox" name="wpbm_enable_logging" value="1" <?php checked(get_option('wpbm_enable_logging'), '1'); ?> />
                                Log API requests and responses
                            </label>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button(); ?>
            </form>
            
            <script>
            jQuery(document).ready(function($) {
                $('#generate-api-key, #regenerate-api-key').on('click', function() {
                    if (confirm('Generate a new API key? The old key will stop working immediately.')) {
                        $.post(wpbm_ajax.ajax_url, {
                            action: 'wpbm_generate_api_key',
                            nonce: wpbm_ajax.nonce
                        }, function(response) {
                            if (response.success) {
                                location.reload();
                            }
                        });
                    }
                });
            });
            </script>
        </div>
        <?php
    }
    
    /**
     * Activity logs page
     */
    public function logs_page() {
        $logs = get_option('wpbm_security_logs', []);
        $logs = array_reverse($logs); // Show newest first
        ?>
        <div class="wrap">
            <h1>WP Bulk Manager Activity Log</h1>
            
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Event</th>
                        <th>IP Address</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (empty($logs)): ?>
                        <tr>
                            <td colspan="4">No activity logged yet.</td>
                        </tr>
                    <?php else: ?>
                        <?php foreach (array_slice($logs, 0, 100) as $log): ?>
                            <tr>
                                <td><?php echo esc_html($log['timestamp']); ?></td>
                                <td><?php echo esc_html($log['event']); ?></td>
                                <td><?php echo esc_html($log['ip']); ?></td>
                                <td><?php echo esc_html(json_encode($log['details'])); ?></td>
                            </tr>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
        <?php
    }
    
    /**
     * Display stats
     */
    private function display_stats() {
        $post_count = wp_count_posts('post');
        $page_count = wp_count_posts('page');
        $media_count = wp_count_posts('attachment');
        ?>
        <ul>
            <li>Posts: <?php echo $post_count->publish; ?> published</li>
            <li>Pages: <?php echo $page_count->publish; ?> published</li>
            <li>Media: <?php echo $media_count->inherit; ?> items</li>
        </ul>
        <?php
    }
    
    /**
     * Display recent activity
     */
    private function display_recent_activity() {
        $logs = get_option('wpbm_security_logs', []);
        $recent = array_slice(array_reverse($logs), 0, 5);
        
        if (empty($recent)) {
            echo '<p>No recent activity.</p>';
            return;
        }
        
        echo '<ul>';
        foreach ($recent as $log) {
            echo '<li>' . esc_html($log['timestamp']) . ' - ' . esc_html($log['event']) . '</li>';
        }
        echo '</ul>';
    }
    
    /**
     * Add custom capabilities
     */
    public function add_capabilities() {
        $role = get_role('administrator');
        
        if ($role) {
            $role->add_cap('wpbm_manage_bulk_operations');
            $role->add_cap('wpbm_view_logs');
        }
    }
    
    /**
     * Cleanup old data
     */
    public function cleanup_old_data() {
        // Clean old logs
        $logs = get_option('wpbm_security_logs', []);
        if (count($logs) > 10000) {
            $logs = array_slice($logs, -5000);
            update_option('wpbm_security_logs', $logs);
        }
        
        // Clean old transients
        global $wpdb;
        $wpdb->query(
            "DELETE FROM {$wpdb->options} 
             WHERE option_name LIKE '_transient_wpbm_backup_%' 
             AND option_name < '_transient_wpbm_backup_" . (time() - DAY_IN_SECONDS) . "'"
        );
    }
}

// AJAX handlers
add_action('wp_ajax_wpbm_generate_api_key', function() {
    check_ajax_referer('wpbm_ajax_nonce', 'nonce');
    
    if (!current_user_can('manage_options')) {
        wp_die('Unauthorized');
    }
    
    $security = new WPBM_Security();
    $new_key = $security->generate_api_key();
    
    update_option('wpbm_api_key', $new_key);
    
    wp_send_json_success(['key' => $new_key]);
});

// Initialize plugin
add_action('plugins_loaded', function() {
    WP_Bulk_Manager_Client::get_instance();
});

// Activation hook
register_activation_hook(__FILE__, function() {
    // Create default options
    add_option('wpbm_api_key', '');
    add_option('wpbm_allowed_ips', '');
    add_option('wpbm_enable_logging', '0');
    
    // Schedule cleanup cron
    if (!wp_next_scheduled('wpbm_cleanup_cron')) {
        wp_schedule_event(time(), 'daily', 'wpbm_cleanup_cron');
    }
});

// Deactivation hook
register_deactivation_hook(__FILE__, function() {
    // Remove scheduled cron
    wp_clear_scheduled_hook('wpbm_cleanup_cron');
});