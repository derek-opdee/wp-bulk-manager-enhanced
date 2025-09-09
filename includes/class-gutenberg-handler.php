<?php
/**
 * Gutenberg Handler - Manages Gutenberg blocks
 */
class WP_Bulk_Manager_Gutenberg_Handler {
    
    private $content_processor;
    
    public function __construct() {
        require_once WP_BULK_MANAGER_PATH . 'includes/class-content-processor.php';
        $this->content_processor = new WP_Bulk_Manager_Content_Processor();
    }
    
    /**
     * Parse Gutenberg content into blocks
     */
    public function parse_blocks($content) {
        return parse_blocks($content);
    }
    
    /**
     * Serialize blocks back to content
     */
    public function serialize_blocks($blocks) {
        return serialize_blocks($blocks);
    }
    
    /**
     * Process blocks with dynamic content
     */
    public function process_blocks($blocks, $replacements = [], $use_spintax = true) {
        foreach ($blocks as &$block) {
            // Process block attributes
            if (isset($block['attrs'])) {
                $block['attrs'] = $this->process_attributes($block['attrs'], $replacements, $use_spintax);
            }
            
            // Process innerHTML
            if (isset($block['innerHTML'])) {
                $block['innerHTML'] = $this->content_processor->process_content(
                    $block['innerHTML'],
                    $replacements,
                    $use_spintax
                );
            }
            
            // Process innerContent
            if (isset($block['innerContent']) && is_array($block['innerContent'])) {
                foreach ($block['innerContent'] as &$inner) {
                    if (is_string($inner)) {
                        $inner = $this->content_processor->process_content(
                            $inner,
                            $replacements,
                            $use_spintax
                        );
                    }
                }
            }
            
            // Process inner blocks recursively
            if (isset($block['innerBlocks']) && !empty($block['innerBlocks'])) {
                $block['innerBlocks'] = $this->process_blocks(
                    $block['innerBlocks'],
                    $replacements,
                    $use_spintax
                );
            }
        }
        
        return $blocks;
    }
    
    /**
     * Process block attributes
     */
    private function process_attributes($attrs, $replacements, $use_spintax) {
        foreach ($attrs as $key => &$value) {
            if (is_string($value)) {
                $value = $this->content_processor->process_content($value, $replacements, $use_spintax);
            } elseif (is_array($value)) {
                $value = $this->process_attributes($value, $replacements, $use_spintax);
            }
        }
        return $attrs;
    }
    
    /**
     * Duplicate blocks with variations
     */
    public function duplicate_blocks($blocks, $variations_count = 1, $variable_sets = []) {
        $duplicated = [];
        
        for ($i = 0; $i < $variations_count; $i++) {
            $replacements = [];
            
            // Generate random replacements for this variation
            foreach ($variable_sets as $var_name => $var_options) {
                if (is_array($var_options)) {
                    $replacements[$var_name] = $var_options[array_rand($var_options)];
                } else {
                    $replacements[$var_name] = $var_options;
                }
            }
            
            $processed_blocks = $this->process_blocks($blocks, $replacements, true);
            $duplicated[] = [
                'blocks' => $processed_blocks,
                'replacements' => $replacements
            ];
        }
        
        return $duplicated;
    }
    
    /**
     * Find and replace in specific block types
     */
    public function find_replace_in_blocks($blocks, $block_types, $find, $replace) {
        foreach ($blocks as &$block) {
            if (in_array($block['blockName'], $block_types)) {
                // Replace in innerHTML
                if (isset($block['innerHTML'])) {
                    $block['innerHTML'] = str_replace($find, $replace, $block['innerHTML']);
                }
                
                // Replace in innerContent
                if (isset($block['innerContent']) && is_array($block['innerContent'])) {
                    foreach ($block['innerContent'] as &$inner) {
                        if (is_string($inner)) {
                            $inner = str_replace($find, $replace, $inner);
                        }
                    }
                }
                
                // Replace in attributes
                if (isset($block['attrs'])) {
                    $block['attrs'] = $this->replace_in_attributes($block['attrs'], $find, $replace);
                }
            }
            
            // Process inner blocks recursively
            if (isset($block['innerBlocks']) && !empty($block['innerBlocks'])) {
                $block['innerBlocks'] = $this->find_replace_in_blocks(
                    $block['innerBlocks'],
                    $block_types,
                    $find,
                    $replace
                );
            }
        }
        
        return $blocks;
    }
    
    /**
     * Replace in attributes recursively
     */
    private function replace_in_attributes($attrs, $find, $replace) {
        foreach ($attrs as $key => &$value) {
            if (is_string($value)) {
                $value = str_replace($find, $replace, $value);
            } elseif (is_array($value)) {
                $value = $this->replace_in_attributes($value, $find, $replace);
            }
        }
        return $attrs;
    }
    
    /**
     * Extract all text content from blocks
     */
    public function extract_text_from_blocks($blocks) {
        $text = '';
        
        foreach ($blocks as $block) {
            // Extract from innerHTML
            if (isset($block['innerHTML'])) {
                $text .= strip_tags($block['innerHTML']) . "\n";
            }
            
            // Extract from inner blocks
            if (isset($block['innerBlocks']) && !empty($block['innerBlocks'])) {
                $text .= $this->extract_text_from_blocks($block['innerBlocks']);
            }
        }
        
        return $text;
    }
    
    /**
     * Get block statistics
     */
    public function get_block_stats($blocks) {
        $stats = [
            'total_blocks' => 0,
            'block_types' => []
        ];
        
        foreach ($blocks as $block) {
            $stats['total_blocks']++;
            
            if ($block['blockName']) {
                if (!isset($stats['block_types'][$block['blockName']])) {
                    $stats['block_types'][$block['blockName']] = 0;
                }
                $stats['block_types'][$block['blockName']]++;
            }
            
            // Count inner blocks
            if (isset($block['innerBlocks']) && !empty($block['innerBlocks'])) {
                $inner_stats = $this->get_block_stats($block['innerBlocks']);
                $stats['total_blocks'] += $inner_stats['total_blocks'];
                
                foreach ($inner_stats['block_types'] as $type => $count) {
                    if (!isset($stats['block_types'][$type])) {
                        $stats['block_types'][$type] = 0;
                    }
                    $stats['block_types'][$type] += $count;
                }
            }
        }
        
        return $stats;
    }
    
    /**
     * Create block template
     */
    public function create_block_template($block_type, $content, $attrs = []) {
        $block = [
            'blockName' => $block_type,
            'attrs' => $attrs,
            'innerBlocks' => [],
            'innerHTML' => '',
            'innerContent' => []
        ];
        
        switch ($block_type) {
            case 'core/paragraph':
                $block['innerHTML'] = "<!-- wp:paragraph -->\n<p>$content</p>\n<!-- /wp:paragraph -->";
                $block['innerContent'] = ["<p>$content</p>"];
                break;
                
            case 'core/heading':
                $level = isset($attrs['level']) ? $attrs['level'] : 2;
                $tag = "h$level";
                $block['innerHTML'] = "<!-- wp:heading {\"level\":$level} -->\n<$tag>$content</$tag>\n<!-- /wp:heading -->";
                $block['innerContent'] = ["<$tag>$content</$tag>"];
                break;
                
            case 'core/list':
                $items = is_array($content) ? $content : [$content];
                $list_html = "<ul>\n";
                foreach ($items as $item) {
                    $list_html .= "<li>$item</li>\n";
                }
                $list_html .= "</ul>";
                $block['innerHTML'] = "<!-- wp:list -->\n$list_html\n<!-- /wp:list -->";
                $block['innerContent'] = [$list_html];
                break;
                
            case 'core/button':
                $url = isset($attrs['url']) ? $attrs['url'] : '#';
                $block['innerHTML'] = "<!-- wp:button -->\n<div class=\"wp-block-button\"><a class=\"wp-block-button__link\" href=\"$url\">$content</a></div>\n<!-- /wp:button -->";
                $block['innerContent'] = ["<div class=\"wp-block-button\"><a class=\"wp-block-button__link\" href=\"$url\">$content</a></div>"];
                break;
        }
        
        return $block;
    }
}