<?php
// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Get statistics
$api_manager = new WP_Bulk_Manager_API_Manager();
$sites = $api_manager->get_all_sites('all');
$active_sites = array_filter($sites, function($site) { return $site->status === 'active'; });

global $wpdb;
$templates_count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}bm_templates");
$operations_pending = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}bm_operations WHERE status = 'pending'");
$operations_completed = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}bm_operations WHERE status = 'completed' AND completed_at > DATE_SUB(NOW(), INTERVAL 24 HOUR)");
?>

<div class="wrap">
    <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
    
    <!-- Statistics Cards -->
    <div class="wp-bulk-manager-stats">
        <div class="stat-card">
            <h3>Connected Sites</h3>
            <div class="stat-number"><?php echo count($active_sites); ?> / <?php echo count($sites); ?></div>
            <div class="stat-label">Active / Total</div>
        </div>
        
        <div class="stat-card">
            <h3>Templates</h3>
            <div class="stat-number"><?php echo $templates_count; ?></div>
            <div class="stat-label">Available Templates</div>
        </div>
        
        <div class="stat-card">
            <h3>Operations Queue</h3>
            <div class="stat-number"><?php echo $operations_pending; ?></div>
            <div class="stat-label">Pending Tasks</div>
        </div>
        
        <div class="stat-card">
            <h3>Completed Today</h3>
            <div class="stat-number"><?php echo $operations_completed; ?></div>
            <div class="stat-label">Operations</div>
        </div>
    </div>
    
    <!-- Quick Site Access -->
    <div class="postbox" style="margin-top: 30px;">
        <h2 class="hndle">Quick Site Access</h2>
        <div class="inside">
            <div class="site-grid">
                <?php foreach ($active_sites as $site): ?>
                    <div class="site-card">
                        <h4><?php echo esc_html($site->site_name); ?></h4>
                        <div class="site-domain">
                            <a href="<?php echo esc_url($site->site_url); ?>" target="_blank">
                                <?php echo esc_html(parse_url($site->site_url, PHP_URL_HOST)); ?>
                                <span class="dashicons dashicons-external"></span>
                            </a>
                        </div>
                        <div class="site-actions">
                            <a href="?page=wp-bulk-manager&action=content&site_id=<?php echo esc_attr($site->id); ?>" class="button button-small">
                                <span class="dashicons dashicons-edit"></span> Content
                            </a>
                            <a href="?page=wp-bulk-manager&action=seo&site_id=<?php echo esc_attr($site->id); ?>" class="button button-small">
                                <span class="dashicons dashicons-search"></span> SEO
                            </a>
                            <a href="?page=wp-bulk-manager&action=plugins&site_id=<?php echo esc_attr($site->id); ?>" class="button button-small">
                                <span class="dashicons dashicons-admin-plugins"></span> Plugins
                            </a>
                        </div>
                    </div>
                <?php endforeach; ?>
                
                <?php if (empty($active_sites)): ?>
                    <div class="notice notice-info inline">
                        <p>No active sites. <a href="?page=wp-bulk-manager-sites">Add your first site</a></p>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="postbox">
        <h2 class="hndle">Quick Actions</h2>
        <div class="inside">
            <div class="quick-actions">
                <a href="?page=wp-bulk-manager&action=bulk-create" class="button button-primary button-hero">
                    <span class="dashicons dashicons-welcome-add-page"></span>
                    Bulk Create Content
                </a>
                
                <a href="?page=wp-bulk-manager&action=bulk-update-seo" class="button button-hero">
                    <span class="dashicons dashicons-search"></span>
                    Bulk Update SEO
                </a>
                
                <a href="?page=wp-bulk-manager-templates#new" class="button button-hero">
                    <span class="dashicons dashicons-admin-page"></span>
                    Create Template
                </a>
                
                <a href="?page=wp-bulk-manager&action=sync-all" class="button button-hero">
                    <span class="dashicons dashicons-update"></span>
                    Sync All Sites
                </a>
            </div>
        </div>
    </div>
    
    <!-- Recent Operations -->
    <div class="postbox">
        <h2 class="hndle">Recent Operations</h2>
        <div class="inside">
            <?php
            $recent_operations = $wpdb->get_results("
                SELECT o.*, s.site_name 
                FROM {$wpdb->prefix}bm_operations o
                LEFT JOIN {$wpdb->prefix}bm_sites s ON o.site_id = s.id
                ORDER BY o.created_at DESC
                LIMIT 10
            ");
            ?>
            
            <?php if ($recent_operations): ?>
                <table class="wp-list-table widefat">
                    <thead>
                        <tr>
                            <th>Operation</th>
                            <th>Site</th>
                            <th>Status</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($recent_operations as $op): ?>
                            <tr>
                                <td><?php echo esc_html($op->operation_type); ?></td>
                                <td><?php echo esc_html($op->site_name ?: 'All Sites'); ?></td>
                                <td>
                                    <span class="status-badge status-<?php echo esc_attr($op->status); ?>">
                                        <?php echo esc_html($op->status); ?>
                                    </span>
                                </td>
                                <td><?php echo esc_html(human_time_diff(strtotime($op->created_at)) . ' ago'); ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <p>No recent operations.</p>
            <?php endif; ?>
        </div>
    </div>
</div>

<style>
.wp-bulk-manager-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.stat-card {
    background: #fff;
    border: 1px solid #ccd0d4;
    box-shadow: 0 1px 1px rgba(0,0,0,0.04);
    padding: 20px;
    text-align: center;
}

.stat-card h3 {
    margin: 0 0 10px 0;
    color: #23282d;
    font-size: 14px;
    font-weight: 600;
}

.stat-number {
    font-size: 32px;
    font-weight: 300;
    color: #0073aa;
    margin: 10px 0;
}

.stat-label {
    color: #666;
    font-size: 12px;
}

.site-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.site-card {
    background: #f9f9f9;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 4px;
}

.site-card h4 {
    margin: 0 0 10px 0;
    font-size: 16px;
}

.site-domain {
    margin-bottom: 15px;
    font-size: 14px;
}

.site-domain a {
    text-decoration: none;
}

.site-actions {
    display: flex;
    gap: 5px;
}

.site-actions .button-small {
    font-size: 12px;
    padding: 0 8px;
    height: 26px;
    line-height: 24px;
}

.site-actions .dashicons {
    font-size: 14px;
    line-height: 26px;
    vertical-align: middle;
}

.quick-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.button-hero .dashicons {
    vertical-align: middle;
    margin-right: 5px;
}

.status-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 600;
}

.status-completed {
    background: #d4edda;
    color: #155724;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

.status-processing {
    background: #cce5ff;
    color: #004085;
}

.status-failed {
    background: #f8d7da;
    color: #721c24;
}
</style>