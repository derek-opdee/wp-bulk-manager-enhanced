<?php
/**
 * Content Processor - Handles dynamic content replacement and spintax
 */
class WP_Bulk_Manager_Content_Processor {
    
    private $variables = [];
    private $current_replacements = [];
    
    public function __construct() {
        $this->load_variables();
    }
    
    /**
     * Load variables from database
     */
    private function load_variables() {
        global $wpdb;
        $table_name = $wpdb->prefix . 'bm_variables';
        $results = $wpdb->get_results("SELECT * FROM $table_name");
        
        foreach ($results as $variable) {
            $this->variables[$variable->variable_name] = json_decode($variable->values, true);
        }
    }
    
    /**
     * Process content with variable replacements and spintax
     */
    public function process_content($content, $replacements = [], $use_spintax = true) {
        $this->current_replacements = $replacements;
        
        // Process spintax first if enabled
        if ($use_spintax) {
            $content = $this->process_spintax($content);
        }
        
        // Process variables
        $content = $this->replace_variables($content);
        
        // Process conditional logic
        $content = $this->process_conditionals($content);
        
        // Process modifiers
        $content = $this->process_modifiers($content);
        
        return $content;
    }
    
    /**
     * Process spintax variations
     */
    private function process_spintax($content) {
        // Match nested spintax patterns
        while (preg_match('/\{([^{}]*)\}/m', $content, $matches)) {
            $full_match = $matches[0];
            $options = explode('|', $matches[1]);
            
            // Skip if it's a variable placeholder
            if (count($options) == 1 && !strpos($options[0], ' ')) {
                // Check if it's a variable we should preserve
                $var_name = trim($options[0]);
                if (array_key_exists($var_name, $this->current_replacements) || 
                    array_key_exists($var_name, $this->variables)) {
                    continue;
                }
            }
            
            // Choose random option for spintax
            $replacement = trim($options[array_rand($options)]);
            $content = str_replace($full_match, $replacement, $content);
        }
        
        return $content;
    }
    
    /**
     * Replace variables with actual values
     */
    private function replace_variables($content) {
        // Replace custom replacements first
        foreach ($this->current_replacements as $key => $value) {
            $content = str_replace('{' . $key . '}', $value, $content);
        }
        
        // Replace predefined variables
        foreach ($this->variables as $var_name => $var_values) {
            if (isset($this->current_replacements[$var_name])) {
                continue; // Already replaced
            }
            
            // Handle different variable types
            if ($var_name == 'service' && is_array($var_values)) {
                // Services have singular/plural forms
                if (isset($this->current_replacements['service_key'])) {
                    $service_key = $this->current_replacements['service_key'];
                    if (isset($var_values[$service_key])) {
                        $content = str_replace('{service}', $var_values[$service_key]['singular'], $content);
                        $content = str_replace('{service_plural}', $var_values[$service_key]['plural'], $content);
                    }
                }
            } elseif (is_array($var_values)) {
                // Location type - pick random if not specified
                $value = $var_values[array_rand($var_values)];
                $content = str_replace('{' . $var_name . '}', $value, $content);
            }
        }
        
        return $content;
    }
    
    /**
     * Process conditional statements
     */
    private function process_conditionals($content) {
        // Pattern: {if:variable}content{/if}
        $pattern = '/\{if:(\w+)\}(.*?)\{\/if\}/s';
        
        $content = preg_replace_callback($pattern, function($matches) {
            $variable = $matches[1];
            $conditional_content = $matches[2];
            
            if (isset($this->current_replacements[$variable]) && !empty($this->current_replacements[$variable])) {
                return $conditional_content;
            }
            
            return '';
        }, $content);
        
        return $content;
    }
    
    /**
     * Process variable modifiers
     */
    private function process_modifiers($content) {
        // Pattern: {variable|modifier}
        $pattern = '/\{(\w+)\|(\w+)\}/';
        
        $content = preg_replace_callback($pattern, function($matches) {
            $variable = $matches[1];
            $modifier = $matches[2];
            
            $value = isset($this->current_replacements[$variable]) ? 
                     $this->current_replacements[$variable] : 
                     $variable;
            
            switch ($modifier) {
                case 'upper':
                case 'uppercase':
                    return strtoupper($value);
                    
                case 'lower':
                case 'lowercase':
                    return strtolower($value);
                    
                case 'capitalize':
                case 'title':
                    return ucwords(strtolower($value));
                    
                case 'first':
                    return ucfirst(strtolower($value));
                    
                default:
                    return $value;
            }
        }, $content);
        
        return $content;
    }
    
    /**
     * Generate multiple variations of content
     */
    public function generate_variations($template, $variable_sets, $count = 1) {
        $variations = [];
        
        for ($i = 0; $i < $count; $i++) {
            $replacements = [];
            
            // Pick random values for each variable
            foreach ($variable_sets as $var_name => $var_options) {
                if (is_array($var_options)) {
                    $replacements[$var_name] = $var_options[array_rand($var_options)];
                } else {
                    $replacements[$var_name] = $var_options;
                }
            }
            
            $variations[] = [
                'content' => $this->process_content($template, $replacements),
                'replacements' => $replacements
            ];
        }
        
        return $variations;
    }
    
    /**
     * Extract variables from template
     */
    public function extract_variables($content) {
        $variables = [];
        
        // Match all {variable} patterns, excluding spintax
        preg_match_all('/\{([a-zA-Z_]\w*)\}/', $content, $matches);
        
        foreach ($matches[1] as $variable) {
            if (!in_array($variable, $variables)) {
                $variables[] = $variable;
            }
        }
        
        return $variables;
    }
}