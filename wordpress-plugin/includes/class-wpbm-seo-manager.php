<?php
/**
 * SEO Manager for WP Bulk Manager
 * 
 * @package WPBulkManager
 */

if (!defined('ABSPATH')) {
    exit;
}

class WPBM_SEO_Manager {
    
    /**
     * Get SEO data for a post
     */
    public function get_seo_data($post_id) {
        $seo_data = [];
        
        // Check for Yoast SEO
        if (defined('WPSEO_VERSION')) {
            $seo_data['yoast'] = $this->get_yoast_data($post_id);
        }
        
        // Check for All in One SEO
        if (defined('AIOSEO_VERSION')) {
            $seo_data['aioseo'] = $this->get_aioseo_data($post_id);
        }
        
        // Check for Rank Math
        if (class_exists('RankMath')) {
            $seo_data['rankmath'] = $this->get_rankmath_data($post_id);
        }
        
        // Check for SEO Framework
        if (defined('THE_SEO_FRAMEWORK_VERSION')) {
            $seo_data['seoframework'] = $this->get_seoframework_data($post_id);
        }
        
        // Fallback to basic meta
        if (empty($seo_data)) {
            $seo_data['basic'] = $this->get_basic_meta($post_id);
        }
        
        return $seo_data;
    }
    
    /**
     * Update SEO data for a post
     */
    public function update_seo_data($post_id, $seo_data) {
        $updated = false;
        
        // Update based on active SEO plugin
        if (defined('WPSEO_VERSION') && isset($seo_data['title'])) {
            $this->update_yoast_data($post_id, $seo_data);
            $updated = true;
        } elseif (defined('AIOSEO_VERSION') && isset($seo_data['title'])) {
            $this->update_aioseo_data($post_id, $seo_data);
            $updated = true;
        } elseif (class_exists('RankMath') && isset($seo_data['title'])) {
            $this->update_rankmath_data($post_id, $seo_data);
            $updated = true;
        } elseif (defined('THE_SEO_FRAMEWORK_VERSION') && isset($seo_data['title'])) {
            $this->update_seoframework_data($post_id, $seo_data);
            $updated = true;
        }
        
        // Always update basic meta as fallback
        $this->update_basic_meta($post_id, $seo_data);
        
        return $updated;
    }
    
    /**
     * Get Yoast SEO data
     */
    private function get_yoast_data($post_id) {
        return [
            'title' => get_post_meta($post_id, '_yoast_wpseo_title', true),
            'description' => get_post_meta($post_id, '_yoast_wpseo_metadesc', true),
            'keywords' => get_post_meta($post_id, '_yoast_wpseo_metakeywords', true),
            'canonical' => get_post_meta($post_id, '_yoast_wpseo_canonical', true),
            'og_title' => get_post_meta($post_id, '_yoast_wpseo_opengraph-title', true),
            'og_description' => get_post_meta($post_id, '_yoast_wpseo_opengraph-description', true),
            'og_image' => get_post_meta($post_id, '_yoast_wpseo_opengraph-image', true)
        ];
    }
    
    /**
     * Update Yoast SEO data
     */
    private function update_yoast_data($post_id, $data) {
        if (isset($data['title'])) {
            update_post_meta($post_id, '_yoast_wpseo_title', $data['title']);
        }
        
        if (isset($data['description'])) {
            update_post_meta($post_id, '_yoast_wpseo_metadesc', $data['description']);
        }
        
        if (isset($data['keywords'])) {
            update_post_meta($post_id, '_yoast_wpseo_metakeywords', $data['keywords']);
        }
        
        if (isset($data['canonical'])) {
            update_post_meta($post_id, '_yoast_wpseo_canonical', $data['canonical']);
        }
        
        if (isset($data['og_title'])) {
            update_post_meta($post_id, '_yoast_wpseo_opengraph-title', $data['og_title']);
        }
        
        if (isset($data['og_description'])) {
            update_post_meta($post_id, '_yoast_wpseo_opengraph-description', $data['og_description']);
        }
    }
    
    /**
     * Get All in One SEO data
     */
    private function get_aioseo_data($post_id) {
        global $wpdb;
        
        $aioseo_posts_table = $wpdb->prefix . 'aioseo_posts';
        $post_data = $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM $aioseo_posts_table WHERE post_id = %d",
            $post_id
        ));
        
        if (!$post_data) {
            return [];
        }
        
        return [
            'title' => $post_data->title,
            'description' => $post_data->description,
            'keywords' => $post_data->keywords,
            'canonical_url' => $post_data->canonical_url,
            'og_title' => $post_data->og_title,
            'og_description' => $post_data->og_description
        ];
    }
    
    /**
     * Update All in One SEO data
     */
    private function update_aioseo_data($post_id, $data) {
        global $wpdb;
        
        $aioseo_posts_table = $wpdb->prefix . 'aioseo_posts';
        $update_data = [];
        
        if (isset($data['title'])) {
            $update_data['title'] = $data['title'];
        }
        
        if (isset($data['description'])) {
            $update_data['description'] = $data['description'];
        }
        
        if (!empty($update_data)) {
            $wpdb->update(
                $aioseo_posts_table,
                $update_data,
                ['post_id' => $post_id]
            );
        }
    }
    
    /**
     * Get Rank Math data
     */
    private function get_rankmath_data($post_id) {
        return [
            'title' => get_post_meta($post_id, 'rank_math_title', true),
            'description' => get_post_meta($post_id, 'rank_math_description', true),
            'focus_keyword' => get_post_meta($post_id, 'rank_math_focus_keyword', true),
            'canonical_url' => get_post_meta($post_id, 'rank_math_canonical_url', true),
            'facebook_title' => get_post_meta($post_id, 'rank_math_facebook_title', true),
            'facebook_description' => get_post_meta($post_id, 'rank_math_facebook_description', true)
        ];
    }
    
    /**
     * Update Rank Math data
     */
    private function update_rankmath_data($post_id, $data) {
        if (isset($data['title'])) {
            update_post_meta($post_id, 'rank_math_title', $data['title']);
        }
        
        if (isset($data['description'])) {
            update_post_meta($post_id, 'rank_math_description', $data['description']);
        }
        
        if (isset($data['focus_keyword'])) {
            update_post_meta($post_id, 'rank_math_focus_keyword', $data['focus_keyword']);
        }
    }
    
    /**
     * Get SEO Framework data
     */
    private function get_seoframework_data($post_id) {
        return [
            'title' => get_post_meta($post_id, '_genesis_title', true),
            'description' => get_post_meta($post_id, '_genesis_description', true),
            'canonical' => get_post_meta($post_id, '_genesis_canonical_uri', true),
            'noindex' => get_post_meta($post_id, '_genesis_noindex', true),
            'nofollow' => get_post_meta($post_id, '_genesis_nofollow', true)
        ];
    }
    
    /**
     * Update SEO Framework data
     */
    private function update_seoframework_data($post_id, $data) {
        if (isset($data['title'])) {
            update_post_meta($post_id, '_genesis_title', $data['title']);
        }
        
        if (isset($data['description'])) {
            update_post_meta($post_id, '_genesis_description', $data['description']);
        }
    }
    
    /**
     * Get basic meta data (fallback)
     */
    private function get_basic_meta($post_id) {
        return [
            'title' => get_post_meta($post_id, '_wpbm_seo_title', true),
            'description' => get_post_meta($post_id, '_wpbm_seo_description', true),
            'keywords' => get_post_meta($post_id, '_wpbm_seo_keywords', true)
        ];
    }
    
    /**
     * Update basic meta data
     */
    private function update_basic_meta($post_id, $data) {
        if (isset($data['title'])) {
            update_post_meta($post_id, '_wpbm_seo_title', $data['title']);
        }
        
        if (isset($data['description'])) {
            update_post_meta($post_id, '_wpbm_seo_description', $data['description']);
        }
        
        if (isset($data['keywords'])) {
            update_post_meta($post_id, '_wpbm_seo_keywords', $data['keywords']);
        }
    }
    
    /**
     * Bulk update SEO data
     */
    public function bulk_update_seo($updates) {
        $results = [
            'success' => 0,
            'failed' => 0,
            'errors' => []
        ];
        
        foreach ($updates as $update) {
            if (!isset($update['post_id'])) {
                continue;
            }
            
            try {
                $this->update_seo_data($update['post_id'], $update);
                $results['success']++;
            } catch (Exception $e) {
                $results['failed']++;
                $results['errors'][] = [
                    'post_id' => $update['post_id'],
                    'error' => $e->getMessage()
                ];
            }
        }
        
        return $results;
    }
}