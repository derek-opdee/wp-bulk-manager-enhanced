<?php
/**
 * Queue Processor - Handles background job processing
 */
class WP_Bulk_Manager_Queue_Processor {
    
    /**
     * Process queue items
     */
    public function process_queue() {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_operations';
        
        // Get pending operations
        $operations = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM $table_name WHERE status = %s LIMIT 5",
            'pending'
        ));
        
        foreach ($operations as $operation) {
            $this->process_operation($operation);
        }
    }
    
    /**
     * Process single operation
     */
    private function process_operation($operation) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_operations';
        
        // Update status to processing
        $wpdb->update($table_name, ['status' => 'processing'], ['id' => $operation->id]);
        
        $data = json_decode($operation->data, true);
        $result = false;
        $error = null;
        
        try {
            switch ($operation->operation_type) {
                case 'create_content':
                    $result = $this->handle_create_content($operation->site_id, $data);
                    break;
                    
                case 'update_content':
                    $result = $this->handle_update_content($operation->site_id, $data);
                    break;
                    
                case 'update_plugins':
                    $result = $this->handle_update_plugins($operation->site_id, $data);
                    break;
                    
                default:
                    throw new Exception('Unknown operation type: ' . $operation->operation_type);
            }
            
            // Update status to completed
            $wpdb->update($table_name, [
                'status' => 'completed',
                'completed_at' => current_time('mysql')
            ], ['id' => $operation->id]);
            
        } catch (Exception $e) {
            $error = $e->getMessage();
            
            // Update status to failed
            $wpdb->update($table_name, [
                'status' => 'failed',
                'error_message' => $error,
                'completed_at' => current_time('mysql')
            ], ['id' => $operation->id]);
        }
        
        return $result;
    }
    
    /**
     * Add operation to queue
     */
    public function add_to_queue($operation_type, $site_id, $data) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_operations';
        
        return $wpdb->insert($table_name, [
            'operation_type' => $operation_type,
            'site_id' => $site_id,
            'data' => json_encode($data),
            'status' => 'pending'
        ]);
    }
    
    /**
     * Handle create content operation
     */
    private function handle_create_content($site_id, $data) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        return $api_manager->create_content($site_id, $data['type'], $data['content']);
    }
    
    /**
     * Handle update content operation
     */
    private function handle_update_content($site_id, $data) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        return $api_manager->update_content($site_id, $data['type'], $data['id'], $data['content']);
    }
    
    /**
     * Handle update plugins operation
     */
    private function handle_update_plugins($site_id, $data) {
        $api_manager = new WP_Bulk_Manager_API_Manager();
        $results = [];
        
        foreach ($data['plugins'] as $plugin) {
            $results[$plugin] = $api_manager->update_plugin($site_id, $plugin, 'update');
        }
        
        return $results;
    }
}