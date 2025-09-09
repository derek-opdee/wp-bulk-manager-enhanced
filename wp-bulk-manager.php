<?php
/**
 * Plugin Name: WP Bulk Manager
 * Plugin URI: https://derekzar.com/wp-bulk-manager
 * Description: Comprehensive bulk management for multiple WordPress sites with dynamic content injection, SEO optimization, and SEO Generator integration
 * Version: 1.0.0
 * Author: Derek
 * License: GPL v2 or later
 * Text Domain: wp-bulk-manager
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('WP_BULK_MANAGER_VERSION', '1.0.0');
define('WP_BULK_MANAGER_PATH', plugin_dir_path(__FILE__));
define('WP_BULK_MANAGER_URL', plugin_dir_url(__FILE__));
define('WP_BULK_MANAGER_BASENAME', plugin_basename(__FILE__));

// Include required files
require_once WP_BULK_MANAGER_PATH . 'includes/class-activator.php';
require_once WP_BULK_MANAGER_PATH . 'includes/class-deactivator.php';
require_once WP_BULK_MANAGER_PATH . 'includes/class-bulk-manager.php';

// Activation hook
register_activation_hook(__FILE__, ['WP_Bulk_Manager_Activator', 'activate']);

// Deactivation hook
register_deactivation_hook(__FILE__, ['WP_Bulk_Manager_Deactivator', 'deactivate']);

// Initialize plugin
function run_wp_bulk_manager() {
    $plugin = new WP_Bulk_Manager();
    $plugin->run();
}
add_action('plugins_loaded', 'run_wp_bulk_manager');

// Add admin menu
add_action('admin_menu', 'wp_bulk_manager_admin_menu');
function wp_bulk_manager_admin_menu() {
    add_menu_page(
        'WP Bulk Manager',
        'Bulk Manager',
        'manage_options',
        'wp-bulk-manager',
        'wp_bulk_manager_dashboard_page',
        'dashicons-admin-multisite',
        30
    );
    
    add_submenu_page(
        'wp-bulk-manager',
        'Connected Sites',
        'Sites',
        'manage_options',
        'wp-bulk-manager-sites',
        'wp_bulk_manager_sites_page'
    );
    
    add_submenu_page(
        'wp-bulk-manager',
        'Content Templates',
        'Templates',
        'manage_options',
        'wp-bulk-manager-templates',
        'wp_bulk_manager_templates_page'
    );
    
    add_submenu_page(
        'wp-bulk-manager',
        'Variables',
        'Variables',
        'manage_options',
        'wp-bulk-manager-variables',
        'wp_bulk_manager_variables_page'
    );
    
    add_submenu_page(
        'wp-bulk-manager',
        'Operations Queue',
        'Queue',
        'manage_options',
        'wp-bulk-manager-queue',
        'wp_bulk_manager_queue_page'
    );
}