<?php
/**
 * Plugin deactivation class
 */
class WP_Bulk_Manager_Deactivator {
    
    public static function deactivate() {
        // Clear scheduled events
        wp_clear_scheduled_hook('wp_bulk_manager_process_queue');
        wp_clear_scheduled_hook('wp_bulk_manager_cleanup_logs');
        
        // Flush rewrite rules
        flush_rewrite_rules();
    }
}