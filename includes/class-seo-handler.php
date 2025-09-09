<?php
/**
 * SEO Handler - Manages SEO meta titles and descriptions
 */
class WP_Bulk_Manager_SEO_Handler {
    
    private $content_processor;
    private $supported_plugins = [
        'yoast' => 'wordpress-seo/wp-seo.php',
        'rank_math' => 'seo-by-rank-math/rank-math.php',
        'all_in_one' => 'all-in-one-seo-pack/all_in_one_seo_pack.php',
        'seo_generator' => 'seo-generator/seo-generator.php'
    ];
    
    public function __construct() {
        require_once WP_BULK_MANAGER_PATH . 'includes/class-content-processor.php';
        $this->content_processor = new WP_Bulk_Manager_Content_Processor();
    }
    
    /**
     * Detect active SEO plugin on remote site
     */
    public function detect_seo_plugin($site_plugins) {
        foreach ($this->supported_plugins as $name => $plugin_file) {
            foreach ($site_plugins as $plugin) {
                if (strpos($plugin['plugin'], $plugin_file) !== false && $plugin['status'] === 'active') {
                    return $name;
                }
            }
        }
        return 'none';
    }
    
    /**
     * Generate SEO data based on template
     */
    public function generate_seo_data($template, $replacements = [], $use_spintax = true) {
        $seo_data = [
            'title' => '',
            'description' => '',
            'focus_keyword' => '',
            'og_title' => '',
            'og_description' => '',
            'twitter_title' => '',
            'twitter_description' => ''
        ];
        
        // Process each field
        foreach ($template as $field => $value) {
            if (isset($seo_data[$field])) {
                $seo_data[$field] = $this->content_processor->process_content(
                    $value,
                    $replacements,
                    $use_spintax
                );
            }
        }
        
        // Apply length limits
        $seo_data['title'] = $this->truncate_text($seo_data['title'], 60);
        $seo_data['description'] = $this->truncate_text($seo_data['description'], 160);
        $seo_data['og_title'] = $this->truncate_text($seo_data['og_title'], 60);
        $seo_data['og_description'] = $this->truncate_text($seo_data['og_description'], 160);
        
        return $seo_data;
    }
    
    /**
     * Format SEO data for specific plugin
     */
    public function format_for_plugin($seo_data, $plugin_type) {
        switch ($plugin_type) {
            case 'yoast':
                return $this->format_for_yoast($seo_data);
                
            case 'rank_math':
                return $this->format_for_rank_math($seo_data);
                
            case 'all_in_one':
                return $this->format_for_aioseo($seo_data);
                
            case 'seo_generator':
                return $this->format_for_seo_generator($seo_data);
                
            default:
                return $this->format_generic($seo_data);
        }
    }
    
    /**
     * Format for Yoast SEO
     */
    private function format_for_yoast($seo_data) {
        return [
            'yoast_meta' => [
                '_yoast_wpseo_title' => $seo_data['title'],
                '_yoast_wpseo_metadesc' => $seo_data['description'],
                '_yoast_wpseo_focuskw' => $seo_data['focus_keyword'],
                '_yoast_wpseo_opengraph-title' => $seo_data['og_title'],
                '_yoast_wpseo_opengraph-description' => $seo_data['og_description'],
                '_yoast_wpseo_twitter-title' => $seo_data['twitter_title'],
                '_yoast_wpseo_twitter-description' => $seo_data['twitter_description']
            ]
        ];
    }
    
    /**
     * Format for Rank Math
     */
    private function format_for_rank_math($seo_data) {
        return [
            'rank_math_meta' => [
                'rank_math_title' => $seo_data['title'],
                'rank_math_description' => $seo_data['description'],
                'rank_math_focus_keyword' => $seo_data['focus_keyword'],
                'rank_math_facebook_title' => $seo_data['og_title'],
                'rank_math_facebook_description' => $seo_data['og_description'],
                'rank_math_twitter_title' => $seo_data['twitter_title'],
                'rank_math_twitter_description' => $seo_data['twitter_description']
            ]
        ];
    }
    
    /**
     * Format for All in One SEO
     */
    private function format_for_aioseo($seo_data) {
        return [
            'aioseo_meta' => [
                '_aioseo_title' => $seo_data['title'],
                '_aioseo_description' => $seo_data['description'],
                '_aioseo_keywords' => $seo_data['focus_keyword'],
                '_aioseo_og_title' => $seo_data['og_title'],
                '_aioseo_og_description' => $seo_data['og_description'],
                '_aioseo_twitter_title' => $seo_data['twitter_title'],
                '_aioseo_twitter_description' => $seo_data['twitter_description']
            ]
        ];
    }
    
    /**
     * Format for SEO Generator plugin
     */
    private function format_for_seo_generator($seo_data) {
        return [
            'seo_generator_meta' => [
                'seo_title' => $seo_data['title'],
                'seo_description' => $seo_data['description'],
                'seo_keywords' => $seo_data['focus_keyword'],
                'dynamic_variables' => json_encode([
                    'location' => $seo_data['location'] ?? '',
                    'service' => $seo_data['service'] ?? ''
                ])
            ]
        ];
    }
    
    /**
     * Generic format for custom meta
     */
    private function format_generic($seo_data) {
        return [
            'meta' => [
                '_wp_page_title' => $seo_data['title'],
                '_wp_meta_description' => $seo_data['description'],
                '_wp_focus_keyword' => $seo_data['focus_keyword']
            ]
        ];
    }
    
    /**
     * Analyze SEO score
     */
    public function analyze_seo($content, $seo_data) {
        $score = 100;
        $issues = [];
        
        // Check title length
        $title_length = strlen($seo_data['title']);
        if ($title_length < 30) {
            $score -= 10;
            $issues[] = 'Title is too short (recommended: 30-60 characters)';
        } elseif ($title_length > 60) {
            $score -= 5;
            $issues[] = 'Title is too long (recommended: 30-60 characters)';
        }
        
        // Check description length
        $desc_length = strlen($seo_data['description']);
        if ($desc_length < 120) {
            $score -= 10;
            $issues[] = 'Description is too short (recommended: 120-160 characters)';
        } elseif ($desc_length > 160) {
            $score -= 5;
            $issues[] = 'Description is too long (recommended: 120-160 characters)';
        }
        
        // Check keyword presence
        if (!empty($seo_data['focus_keyword'])) {
            $keyword = strtolower($seo_data['focus_keyword']);
            $content_lower = strtolower($content);
            $title_lower = strtolower($seo_data['title']);
            $desc_lower = strtolower($seo_data['description']);
            
            // Keyword in title
            if (strpos($title_lower, $keyword) === false) {
                $score -= 15;
                $issues[] = 'Focus keyword not found in title';
            }
            
            // Keyword in description
            if (strpos($desc_lower, $keyword) === false) {
                $score -= 10;
                $issues[] = 'Focus keyword not found in description';
            }
            
            // Keyword density in content
            $keyword_count = substr_count($content_lower, $keyword);
            $word_count = str_word_count($content);
            $density = ($keyword_count / $word_count) * 100;
            
            if ($density < 0.5) {
                $score -= 10;
                $issues[] = 'Keyword density is too low';
            } elseif ($density > 3) {
                $score -= 15;
                $issues[] = 'Keyword density is too high (keyword stuffing)';
            }
        }
        
        return [
            'score' => max(0, $score),
            'issues' => $issues,
            'stats' => [
                'title_length' => $title_length,
                'description_length' => $desc_length,
                'keyword_density' => isset($density) ? round($density, 2) : 0
            ]
        ];
    }
    
    /**
     * Generate variations of SEO data
     */
    public function generate_seo_variations($template, $variable_sets, $count = 5) {
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
                'seo_data' => $this->generate_seo_data($template, $replacements),
                'replacements' => $replacements
            ];
        }
        
        return $variations;
    }
    
    /**
     * Truncate text to character limit
     */
    private function truncate_text($text, $limit) {
        if (strlen($text) <= $limit) {
            return $text;
        }
        
        $truncated = substr($text, 0, $limit);
        $last_space = strrpos($truncated, ' ');
        
        if ($last_space !== false) {
            $truncated = substr($truncated, 0, $last_space) . '...';
        }
        
        return $truncated;
    }
    
    /**
     * Get SEO templates
     */
    public function get_seo_templates() {
        return [
            'service_location' => [
                'title' => '{service|capitalize} in {location} - Professional {service}',
                'description' => 'Looking for {service} in {location}? We offer professional {service} with experienced technicians. Call now for a free quote!',
                'focus_keyword' => '{service} {location}',
                'og_title' => '{service|capitalize} in {location} | Your Local Experts',
                'og_description' => 'Professional {service} in {location}. Experienced, reliable, and affordable. Get your free quote today!'
            ],
            'emergency_service' => [
                'title' => '24/7 Emergency {service|capitalize} in {location}',
                'description' => 'Need emergency {service} in {location}? Available 24/7 with fast response times. Call our emergency hotline now!',
                'focus_keyword' => 'emergency {service} {location}',
                'og_title' => 'Emergency {service|capitalize} {location} - 24/7 Service',
                'og_description' => '24/7 emergency {service} in {location}. Fast response, professional service. Call now!'
            ],
            'best_service' => [
                'title' => 'Best {service|capitalize} in {location} - Top Rated Local {service}',
                'description' => 'Discover the best {service} in {location}. Top-rated professionals with excellent reviews. Quality service guaranteed!',
                'focus_keyword' => 'best {service} {location}',
                'og_title' => 'Top Rated {service|capitalize} in {location}',
                'og_description' => 'Looking for the best {service} in {location}? Check our reviews and see why we\'re the top choice!'
            ]
        ];
    }
}