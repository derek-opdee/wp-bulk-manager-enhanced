<?php
/**
 * Spintax Processor - Handles spintax parsing and generation
 */
class WP_Bulk_Manager_Spintax_Processor {
    
    /**
     * Process spintax string
     */
    public function process($text) {
        // Process nested spintax
        while (preg_match('/\{([^{}]*)\}/m', $text, $matches)) {
            $full_match = $matches[0];
            $options = explode('|', $matches[1]);
            
            // Choose random option
            $replacement = trim($options[array_rand($options)]);
            $text = str_replace($full_match, $replacement, $text);
        }
        
        return $text;
    }
    
    /**
     * Generate multiple variations
     */
    public function generate_variations($text, $count = 5) {
        $variations = [];
        
        for ($i = 0; $i < $count; $i++) {
            $variations[] = $this->process($text);
        }
        
        return array_unique($variations);
    }
    
    /**
     * Count possible variations
     */
    public function count_variations($text) {
        $count = 1;
        
        // Find all spintax patterns
        preg_match_all('/\{([^{}]*)\}/m', $text, $matches);
        
        foreach ($matches[1] as $match) {
            $options = explode('|', $match);
            $count *= count($options);
        }
        
        return $count;
    }
    
    /**
     * Validate spintax syntax
     */
    public function validate($text) {
        $open_braces = substr_count($text, '{');
        $close_braces = substr_count($text, '}');
        
        if ($open_braces !== $close_braces) {
            return ['valid' => false, 'error' => 'Mismatched braces'];
        }
        
        // Check for empty options
        if (preg_match('/\{[^}]*\|\|[^}]*\}/', $text)) {
            return ['valid' => false, 'error' => 'Empty spintax options found'];
        }
        
        return ['valid' => true];
    }
}