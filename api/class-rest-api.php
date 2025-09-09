<?php
/**
 * REST API endpoints
 */
class WP_Bulk_Manager_REST_API {
    
    /**
     * Register REST API routes
     */
    public function register_routes() {
        $namespace = 'wp-bulk-manager/v1';
        
        // Sites endpoints
        register_rest_route($namespace, '/sites', [
            'methods' => 'GET',
            'callback' => [$this, 'get_sites'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        register_rest_route($namespace, '/sites', [
            'methods' => 'POST',
            'callback' => [$this, 'add_site'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        register_rest_route($namespace, '/sites/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_site'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        register_rest_route($namespace, '/sites/(?P<id>\d+)', [
            'methods' => 'DELETE',
            'callback' => [$this, 'delete_site'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        // Content endpoints
        register_rest_route($namespace, '/content/create', [
            'methods' => 'POST',
            'callback' => [$this, 'create_content'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        register_rest_route($namespace, '/content/update', [
            'methods' => 'POST',
            'callback' => [$this, 'update_content'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        // Template endpoints
        register_rest_route($namespace, '/templates', [
            'methods' => 'GET',
            'callback' => [$this, 'get_templates'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        register_rest_route($namespace, '/templates', [
            'methods' => 'POST',
            'callback' => [$this, 'create_template'],
            'permission_callback' => [$this, 'check_permission']
        ]);
        
        // Process template
        register_rest_route($namespace, '/process-template', [
            'methods' => 'POST',
            'callback' => [$this, 'process_template'],
            'permission_callback' => [$this, 'check_permission']
        ]);
    }
    
    /**
     * Check permissions
     */
    public function check_permission() {
        return current_user_can('manage_options');
    }
    
    /**
     * Get all sites
     */
    public function get_sites($request) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        $sites = $api_manager->get_all_sites();
        
        return rest_ensure_response($sites);
    }
    
    /**
     * Add new site
     */
    public function add_site($request) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        
        $site_data = [
            'site_name' => sanitize_text_field($request->get_param('site_name')),
            'site_url' => sanitize_url($request->get_param('site_url')),
            'username' => sanitize_text_field($request->get_param('username')),
            'app_password' => $request->get_param('app_password')
        ];
        
        $result = $api_manager->add_site($site_data);
        
        if (is_wp_error($result)) {
            return rest_ensure_response([
                'success' => false,
                'message' => $result->get_error_message()
            ]);
        }
        
        return rest_ensure_response([
            'success' => true,
            'site_id' => $result
        ]);
    }
    
    /**
     * Update site
     */
    public function update_site($request) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        $site_id = intval($request->get_param('id'));
        
        $site_data = [];
        
        if ($request->get_param('site_name')) {
            $site_data['site_name'] = sanitize_text_field($request->get_param('site_name'));
        }
        
        if ($request->get_param('site_url')) {
            $site_data['site_url'] = sanitize_url($request->get_param('site_url'));
        }
        
        if ($request->get_param('status')) {
            $site_data['status'] = sanitize_text_field($request->get_param('status'));
        }
        
        $result = $api_manager->update_site($site_id, $site_data);
        
        return rest_ensure_response([
            'success' => $result !== false
        ]);
    }
    
    /**
     * Delete site
     */
    public function delete_site($request) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        $site_id = intval($request->get_param('id'));
        
        $result = $api_manager->delete_site($site_id);
        
        return rest_ensure_response([
            'success' => $result !== false
        ]);
    }
    
    /**
     * Create content
     */
    public function create_content($request) {
        $queue_processor = new WP_Bulk_Manager_Queue_Processor();
        
        $sites = $request->get_param('sites');
        $content_type = $request->get_param('content_type');
        $content_data = $request->get_param('content');
        
        $queued_count = 0;
        
        foreach ($sites as $site_id) {
            $result = $queue_processor->add_to_queue('create_content', $site_id, [
                'type' => $content_type,
                'content' => $content_data
            ]);
            
            if ($result) {
                $queued_count++;
            }
        }
        
        return rest_ensure_response([
            'success' => true,
            'queued' => $queued_count
        ]);
    }
    
    /**
     * Update content
     */
    public function update_content($request) {
        $queue_processor = new WP_Bulk_Manager_Queue_Processor();
        
        $sites = $request->get_param('sites');
        $content_type = $request->get_param('content_type');
        $content_id = $request->get_param('content_id');
        $content_data = $request->get_param('content');
        
        $queued_count = 0;
        
        foreach ($sites as $site_id) {
            $result = $queue_processor->add_to_queue('update_content', $site_id, [
                'type' => $content_type,
                'id' => $content_id,
                'content' => $content_data
            ]);
            
            if ($result) {
                $queued_count++;
            }
        }
        
        return rest_ensure_response([
            'success' => true,
            'queued' => $queued_count
        ]);
    }
    
    /**
     * Get templates
     */
    public function get_templates($request) {
        $template_engine = new WP_Bulk_Manager_Template_Engine();
        $templates = $template_engine->get_templates();
        
        return rest_ensure_response($templates);
    }
    
    /**
     * Create template
     */
    public function create_template($request) {
        $template_engine = new WP_Bulk_Manager_Template_Engine();
        
        $template_data = [
            'template_name' => sanitize_text_field($request->get_param('name')),
            'template_type' => sanitize_text_field($request->get_param('type')),
            'content' => $request->get_param('content'),
            'variables' => json_encode($request->get_param('variables')),
            'spintax_enabled' => (bool)$request->get_param('spintax_enabled')
        ];
        
        $result = $template_engine->save_template($template_data);
        
        return rest_ensure_response([
            'success' => $result !== false
        ]);
    }
    
    /**
     * Process template with variables
     */
    public function process_template($request) {
        $content_processor = new WP_Bulk_Manager_Content_Processor();
        
        $template = $request->get_param('template');
        $replacements = $request->get_param('replacements');
        $use_spintax = (bool)$request->get_param('use_spintax');
        
        $processed = $content_processor->process_content($template, $replacements, $use_spintax);
        
        return rest_ensure_response([
            'success' => true,
            'processed_content' => $processed
        ]);
    }
}