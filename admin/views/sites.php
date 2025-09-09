<?php
// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Handle form submissions
if (isset($_POST['action'])) {
    if ($_POST['action'] === 'add_site' && wp_verify_nonce($_POST['_wpnonce'], 'add_site_nonce')) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        
        $site_data = [
            'site_name' => sanitize_text_field($_POST['site_name']),
            'site_url' => sanitize_url($_POST['site_url']),
            'username' => sanitize_text_field($_POST['username']),
            'app_password' => $_POST['app_password'],
            'status' => 'active'
        ];
        
        $result = $api_manager->add_site($site_data);
        
        if (is_wp_error($result)) {
            $error_message = $result->get_error_message();
        } else {
            $success_message = 'Site added successfully!';
        }
    }
    
    if ($_POST['action'] === 'delete_site' && wp_verify_nonce($_POST['_wpnonce'], 'delete_site_nonce')) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        $site_id = intval($_POST['site_id']);
        
        if ($api_manager->delete_site($site_id)) {
            $success_message = 'Site deleted successfully!';
        } else {
            $error_message = 'Failed to delete site.';
        }
    }
}

// Get all sites
$api_manager = new WP_Bulk_Manager_API_Manager();
$sites = $api_manager->get_all_sites('all');
?>

<div class="wrap">
    <h1>
        <?php echo esc_html(get_admin_page_title()); ?>
        <a href="#add-new-site" class="page-title-action">Add New Site</a>
    </h1>
    
    <?php if (isset($success_message)): ?>
        <div class="notice notice-success is-dismissible">
            <p><?php echo esc_html($success_message); ?></p>
        </div>
    <?php endif; ?>
    
    <?php if (isset($error_message)): ?>
        <div class="notice notice-error is-dismissible">
            <p><?php echo esc_html($error_message); ?></p>
        </div>
    <?php endif; ?>
    
    <!-- Sites List -->
    <div class="wp-bulk-manager-sites-list">
        <h2>Connected WordPress Sites</h2>
        
        <?php if (empty($sites)): ?>
            <div class="notice notice-info">
                <p>No sites connected yet. Add your first site below.</p>
            </div>
        <?php else: ?>
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th style="width: 30px;">ID</th>
                        <th>Site Name</th>
                        <th>Domain</th>
                        <th>Username</th>
                        <th>Status</th>
                        <th>Last Sync</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($sites as $site): ?>
                        <tr>
                            <td><?php echo esc_html($site->id); ?></td>
                            <td>
                                <strong><?php echo esc_html($site->site_name); ?></strong>
                            </td>
                            <td>
                                <a href="<?php echo esc_url($site->site_url); ?>" target="_blank">
                                    <?php echo esc_html(parse_url($site->site_url, PHP_URL_HOST)); ?>
                                    <span class="dashicons dashicons-external" style="font-size: 14px;"></span>
                                </a>
                            </td>
                            <td><?php echo esc_html($site->username); ?></td>
                            <td>
                                <span class="status-badge status-<?php echo esc_attr($site->status); ?>">
                                    <?php echo esc_html(ucfirst($site->status)); ?>
                                </span>
                            </td>
                            <td>
                                <?php echo $site->last_sync ? esc_html(human_time_diff(strtotime($site->last_sync)) . ' ago') : 'Never'; ?>
                            </td>
                            <td>
                                <div class="row-actions">
                                    <a href="#" class="test-connection" data-site-id="<?php echo esc_attr($site->id); ?>">Test</a> |
                                    <a href="?page=wp-bulk-manager&action=manage&site_id=<?php echo esc_attr($site->id); ?>">Manage</a> |
                                    <a href="#" class="edit-site" data-site-id="<?php echo esc_attr($site->id); ?>">Edit</a> |
                                    <form method="post" style="display: inline;">
                                        <?php wp_nonce_field('delete_site_nonce'); ?>
                                        <input type="hidden" name="action" value="delete_site">
                                        <input type="hidden" name="site_id" value="<?php echo esc_attr($site->id); ?>">
                                        <a href="#" class="delete-site submitdelete" style="color: #a00;">Delete</a>
                                    </form>
                                </div>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>
    
    <!-- Add New Site Form -->
    <div id="add-new-site" class="postbox" style="margin-top: 30px;">
        <h2 class="hndle">Add New WordPress Site</h2>
        <div class="inside">
            <form method="post" id="add-site-form">
                <?php wp_nonce_field('add_site_nonce'); ?>
                <input type="hidden" name="action" value="add_site">
                
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="site_name">Site Name</label>
                        </th>
                        <td>
                            <input type="text" name="site_name" id="site_name" class="regular-text" required>
                            <p class="description">A friendly name to identify this site</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="site_url">Site URL</label>
                        </th>
                        <td>
                            <input type="url" name="site_url" id="site_url" class="regular-text" placeholder="https://example.com" required>
                            <p class="description">The full URL of your WordPress site</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="username">Username</label>
                        </th>
                        <td>
                            <input type="text" name="username" id="username" class="regular-text" required>
                            <p class="description">WordPress username or email</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="app_password">Application Password</label>
                        </th>
                        <td>
                            <input type="password" name="app_password" id="app_password" class="regular-text" required>
                            <p class="description">
                                Generate in WordPress Admin → Users → Profile → Application Passwords
                                <a href="#" id="show-password" style="margin-left: 10px;">Show</a>
                            </p>
                        </td>
                    </tr>
                </table>
                
                <p class="submit">
                    <button type="button" id="test-connection-btn" class="button">Test Connection</button>
                    <button type="submit" class="button button-primary">Add Site</button>
                </p>
                
                <div id="connection-test-result" style="display: none; margin-top: 10px;"></div>
            </form>
        </div>
    </div>
    
    <!-- Quick Actions Section -->
    <div class="postbox" style="margin-top: 30px;">
        <h2 class="hndle">Quick Actions</h2>
        <div class="inside">
            <p>Select sites and perform bulk actions:</p>
            
            <form method="post" id="bulk-actions-form">
                <?php wp_nonce_field('bulk_action_nonce'); ?>
                
                <div class="site-selector" style="margin-bottom: 15px;">
                    <label>
                        <input type="checkbox" id="select-all-sites"> Select All Sites
                    </label>
                    
                    <div class="sites-checkboxes" style="margin-top: 10px; margin-left: 20px;">
                        <?php foreach ($sites as $site): ?>
                            <label style="display: block; margin-bottom: 5px;">
                                <input type="checkbox" name="selected_sites[]" value="<?php echo esc_attr($site->id); ?>" class="site-checkbox">
                                <?php echo esc_html($site->site_name); ?> 
                                <span style="color: #666;">(<?php echo esc_html(parse_url($site->site_url, PHP_URL_HOST)); ?>)</span>
                            </label>
                        <?php endforeach; ?>
                    </div>
                </div>
                
                <div class="bulk-actions">
                    <select name="bulk_action" id="bulk-action-selector">
                        <option value="">-- Select Action --</option>
                        <option value="create_content">Create Content</option>
                        <option value="update_plugins">Update Plugins</option>
                        <option value="update_themes">Update Themes</option>
                        <option value="clear_cache">Clear Cache</option>
                        <option value="backup">Create Backup</option>
                    </select>
                    
                    <button type="submit" class="button button-primary" disabled>Apply to Selected Sites</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
.status-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: 500;
}
.status-active {
    background-color: #d4edda;
    color: #155724;
}
.status-inactive {
    background-color: #f8d7da;
    color: #721c24;
}
.sites-checkboxes {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    background: #f9f9f9;
}
</style>

<script>
jQuery(document).ready(function($) {
    // Show/hide password
    $('#show-password').click(function(e) {
        e.preventDefault();
        var passwordField = $('#app_password');
        if (passwordField.attr('type') === 'password') {
            passwordField.attr('type', 'text');
            $(this).text('Hide');
        } else {
            passwordField.attr('type', 'password');
            $(this).text('Show');
        }
    });
    
    // Test connection
    $('#test-connection-btn').click(function() {
        var btn = $(this);
        var resultDiv = $('#connection-test-result');
        
        btn.prop('disabled', true).text('Testing...');
        
        $.ajax({
            url: wp_bulk_manager.ajax_url,
            type: 'POST',
            data: {
                action: 'wp_bulk_manager_test_connection',
                nonce: wp_bulk_manager.nonce,
                site_url: $('#site_url').val(),
                username: $('#username').val(),
                app_password: $('#app_password').val()
            },
            success: function(response) {
                if (response.success) {
                    resultDiv.html('<div class="notice notice-success"><p>' + wp_bulk_manager.strings.connection_success + '</p></div>').show();
                } else {
                    resultDiv.html('<div class="notice notice-error"><p>' + wp_bulk_manager.strings.connection_failed + ' ' + response.message + '</p></div>').show();
                }
            },
            complete: function() {
                btn.prop('disabled', false).text('Test Connection');
            }
        });
    });
    
    // Delete site confirmation
    $('.delete-site').click(function(e) {
        e.preventDefault();
        if (confirm(wp_bulk_manager.strings.confirm_delete)) {
            $(this).closest('form').submit();
        }
    });
    
    // Select all sites
    $('#select-all-sites').change(function() {
        $('.site-checkbox').prop('checked', $(this).prop('checked'));
        updateBulkActionButton();
    });
    
    // Enable/disable bulk action button
    function updateBulkActionButton() {
        var hasSelection = $('.site-checkbox:checked').length > 0;
        var hasAction = $('#bulk-action-selector').val() !== '';
        
        $('#bulk-actions-form button[type="submit"]').prop('disabled', !(hasSelection && hasAction));
    }
    
    $('.site-checkbox, #bulk-action-selector').change(updateBulkActionButton);
});
</script>