<?php
/**
 * Plugin activation class
 */
class WP_Bulk_Manager_Activator {
    
    public static function activate() {
        self::create_tables();
        self::set_default_options();
        self::create_upload_directories();
        
        // Flush rewrite rules for REST API endpoints
        flush_rewrite_rules();
    }
    
    private static function create_tables() {
        global $wpdb;
        $charset_collate = $wpdb->get_charset_collate();
        
        // Sites table
        $table_sites = $wpdb->prefix . 'bm_sites';
        $sql_sites = "CREATE TABLE IF NOT EXISTS $table_sites (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            site_name varchar(255) NOT NULL,
            site_url varchar(255) NOT NULL,
            username varchar(255) NOT NULL,
            app_password text NOT NULL,
            status enum('active','inactive') DEFAULT 'active',
            last_sync datetime DEFAULT NULL,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY site_url (site_url)
        ) $charset_collate;";
        
        // Templates table
        $table_templates = $wpdb->prefix . 'bm_templates';
        $sql_templates = "CREATE TABLE IF NOT EXISTS $table_templates (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            template_name varchar(255) NOT NULL,
            template_type enum('post','page','block') DEFAULT 'page',
            content longtext NOT NULL,
            variables text,
            spintax_enabled boolean DEFAULT false,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        ) $charset_collate;";
        
        // Operations table
        $table_operations = $wpdb->prefix . 'bm_operations';
        $sql_operations = "CREATE TABLE IF NOT EXISTS $table_operations (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            operation_type varchar(50) NOT NULL,
            site_id bigint(20) DEFAULT NULL,
            status enum('pending','processing','completed','failed') DEFAULT 'pending',
            data longtext,
            error_message text,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            completed_at datetime DEFAULT NULL,
            PRIMARY KEY (id),
            KEY idx_status (status),
            KEY idx_site_id (site_id)
        ) $charset_collate;";
        
        // Variables table
        $table_variables = $wpdb->prefix . 'bm_variables';
        $sql_variables = "CREATE TABLE IF NOT EXISTS $table_variables (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            variable_name varchar(100) NOT NULL,
            variable_type enum('location','service','custom') DEFAULT 'custom',
            values text NOT NULL,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY variable_name (variable_name)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql_sites);
        dbDelta($sql_templates);
        dbDelta($sql_operations);
        dbDelta($sql_variables);
        
        // Add sample data
        self::add_sample_data();
    }
    
    private static function set_default_options() {
        add_option('wp_bulk_manager_version', WP_BULK_MANAGER_VERSION);
        add_option('wp_bulk_manager_encryption_key', wp_generate_password(32, true, true));
        add_option('wp_bulk_manager_batch_size', 10);
        add_option('wp_bulk_manager_timeout', 30);
        add_option('wp_bulk_manager_enable_logging', true);
    }
    
    private static function create_upload_directories() {
        $upload_dir = wp_upload_dir();
        $plugin_upload_dir = $upload_dir['basedir'] . '/wp-bulk-manager';
        
        if (!file_exists($plugin_upload_dir)) {
            wp_mkdir_p($plugin_upload_dir);
            wp_mkdir_p($plugin_upload_dir . '/logs');
            wp_mkdir_p($plugin_upload_dir . '/templates');
            wp_mkdir_p($plugin_upload_dir . '/exports');
        }
    }
    
    private static function add_sample_data() {
        global $wpdb;
        
        // Add sample variables
        $variables_table = $wpdb->prefix . 'bm_variables';
        
        // Locations
        $wpdb->insert($variables_table, [
            'variable_name' => 'location',
            'variable_type' => 'location',
            'values' => json_encode([
                'Brisbane', 'Sydney', 'Melbourne', 'Perth', 'Adelaide',
                'Gold Coast', 'Newcastle', 'Canberra', 'Sunshine Coast',
                'Wollongong', 'Hobart', 'Geelong', 'Townsville', 'Cairns'
            ])
        ]);
        
        // Services
        $wpdb->insert($variables_table, [
            'variable_name' => 'service',
            'variable_type' => 'service',
            'values' => json_encode([
                'painting' => ['singular' => 'painting service', 'plural' => 'painting services'],
                'plumbing' => ['singular' => 'plumbing service', 'plural' => 'plumbing services'],
                'electrical' => ['singular' => 'electrical service', 'plural' => 'electrical services'],
                'cleaning' => ['singular' => 'cleaning service', 'plural' => 'cleaning services'],
                'landscaping' => ['singular' => 'landscaping service', 'plural' => 'landscaping services']
            ])
        ]);
        
        // Sample template
        $templates_table = $wpdb->prefix . 'bm_templates';
        $sample_content = '<!-- wp:heading -->
<h1>{service|capitalize} in {location}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Looking for reliable {service} in {location}? {We are|We\'re} your trusted local {service} provider{s} with {over 10|more than 10|10+} years of experience serving the {location} {area|region|community}.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Why Choose Our {service|capitalize} in {location}?</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>{Licensed|Certified|Qualified} and insured {service} professionals</li>
<li>{Fast|Quick|Rapid} response times in {location} and surrounding areas</li>
<li>{Competitive|Affordable|Fair} pricing with no hidden fees</li>
<li>{100%|Complete|Total} satisfaction guarantee</li>
</ul>
<!-- /wp:list -->

<!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/contact">Get Free {service|capitalize} Quote in {location}</a></div>
<!-- /wp:button -->';
        
        $wpdb->insert($templates_table, [
            'template_name' => 'Service Location Page Template',
            'template_type' => 'page',
            'content' => $sample_content,
            'variables' => json_encode(['location', 'service']),
            'spintax_enabled' => true
        ]);
    }
}