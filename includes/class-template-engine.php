<?php
/**
 * Template Engine - Manages content templates
 */
class WP_Bulk_Manager_Template_Engine {
    
    /**
     * Get all templates
     */
    public function get_templates($type = 'all') {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_templates';
        
        if ($type === 'all') {
            return $wpdb->get_results("SELECT * FROM $table_name ORDER BY template_name");
        }
        
        return $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM $table_name WHERE template_type = %s ORDER BY template_name",
            $type
        ));
    }
    
    /**
     * Get template by ID
     */
    public function get_template($template_id) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_templates';
        
        return $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM $table_name WHERE id = %d",
            $template_id
        ));
    }
    
    /**
     * Save template
     */
    public function save_template($data) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_templates';
        
        if (isset($data['id']) && $data['id']) {
            // Update existing
            return $wpdb->update($table_name, $data, ['id' => $data['id']]);
        } else {
            // Insert new
            unset($data['id']);
            return $wpdb->insert($table_name, $data);
        }
    }
    
    /**
     * Delete template
     */
    public function delete_template($template_id) {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_templates';
        
        return $wpdb->delete($table_name, ['id' => $template_id]);
    }
}