<?php
/**
 * API Handler for WP Bulk Manager
 * 
 * @package WPBulkManager
 */

if (!defined('ABSPATH')) {
    exit;
}

class WPBM_API_Handler {
    
    private $namespace = 'wpbm/v1';
    private $security;
    
    public function __construct($security) {
        $this->security = $security;
    }
    
    /**
     * Register all API routes
     */
    public function register_routes() {
        // Content endpoints
        register_rest_route($this->namespace, '/content', [
            'methods' => 'GET',
            'callback' => [$this, 'get_content'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/content', [
            'methods' => 'POST',
            'callback' => [$this, 'create_content'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/content/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_single_content'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/content/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_content'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/content/(?P<id>\d+)', [
            'methods' => 'DELETE',
            'callback' => [$this, 'delete_content'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        // Search & Replace endpoint
        register_rest_route($this->namespace, '/search-replace', [
            'methods' => 'POST',
            'callback' => [$this, 'search_replace'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        // Media endpoints
        register_rest_route($this->namespace, '/media', [
            'methods' => 'GET',
            'callback' => [$this, 'get_media'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/media/(?P<id>\d+)', [
            'methods' => 'GET',
            'callback' => [$this, 'get_single_media'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/media/(?P<id>\d+)', [
            'methods' => 'PUT',
            'callback' => [$this, 'update_media'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        // Backup endpoint
        register_rest_route($this->namespace, '/backup', [
            'methods' => 'POST',
            'callback' => [$this, 'create_backup'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        // Revision endpoints
        register_rest_route($this->namespace, '/content/(?P<id>\d+)/revisions', [
            'methods' => 'GET',
            'callback' => [$this, 'get_revisions'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
        
        register_rest_route($this->namespace, '/content/(?P<id>\d+)/revisions/(?P<revision_id>\d+)/restore', [
            'methods' => 'POST',
            'callback' => [$this, 'restore_revision'],
            'permission_callback' => [$this->security, 'verify_request']
        ]);
    }
    
    /**
     * Get content
     */
    public function get_content($request) {
        $params = $request->get_params();
        
        $args = [
            'post_type' => $params['type'] ?? 'post',
            'posts_per_page' => $params['limit'] ?? 100,
            'paged' => $params['page'] ?? 1,
            'post_status' => $params['status'] ?? 'any',
            'orderby' => $params['orderby'] ?? 'date',
            'order' => $params['order'] ?? 'DESC'
        ];
        
        if (isset($params['search'])) {
            $args['s'] = $params['search'];
        }
        
        $query = new WP_Query($args);
        $posts = [];
        
        foreach ($query->posts as $post) {
            $posts[] = $this->format_post($post);
        }
        
        return [
            'posts' => $posts,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages
        ];
    }
    
    /**
     * Search and replace across content
     */
    public function search_replace($request) {
        $params = $request->get_json_params();
        
        $search = $params['search'] ?? '';
        $replace = $params['replace'] ?? '';
        $post_types = $params['post_types'] ?? ['post', 'page'];
        $dry_run = $params['dry_run'] ?? true;
        
        if (empty($search)) {
            return new WP_Error('missing_search', 'Search parameter is required', ['status' => 400]);
        }
        
        $results = [
            'total_posts' => 0,
            'posts_modified' => 0,
            'total_replacements' => 0,
            'changes' => []
        ];
        
        // Get all posts
        $args = [
            'post_type' => $post_types,
            'posts_per_page' => -1,
            'post_status' => 'any'
        ];
        
        $query = new WP_Query($args);
        $results['total_posts'] = $query->found_posts;
        
        foreach ($query->posts as $post) {
            $content = $post->post_content;
            $title = $post->post_title;
            
            // Count replacements
            $content_count = substr_count($content, $search);
            $title_count = substr_count($title, $search);
            
            if ($content_count > 0 || $title_count > 0) {
                $new_content = str_replace($search, $replace, $content);
                $new_title = str_replace($search, $replace, $title);
                
                $change = [
                    'id' => $post->ID,
                    'title' => $post->post_title,
                    'url' => get_permalink($post->ID),
                    'content_replacements' => $content_count,
                    'title_replacements' => $title_count
                ];
                
                $results['changes'][] = $change;
                $results['total_replacements'] += $content_count + $title_count;
                
                // Apply changes if not dry run
                if (!$dry_run) {
                    $update_data = ['ID' => $post->ID];
                    
                    if ($content_count > 0) {
                        $update_data['post_content'] = $new_content;
                    }
                    
                    if ($title_count > 0) {
                        $update_data['post_title'] = $new_title;
                    }
                    
                    wp_update_post($update_data);
                    $results['posts_modified']++;
                }
            }
        }
        
        return $results;
    }
    
    /**
     * Get media items
     */
    public function get_media($request) {
        $params = $request->get_params();
        
        $args = [
            'post_type' => 'attachment',
            'post_status' => 'inherit',
            'posts_per_page' => $params['limit'] ?? 100,
            'paged' => $params['page'] ?? 1
        ];
        
        if (isset($params['mime_type'])) {
            $args['post_mime_type'] = $params['mime_type'];
        }
        
        $query = new WP_Query($args);
        $media = [];
        
        foreach ($query->posts as $attachment) {
            $media[] = $this->format_media($attachment);
        }
        
        return [
            'media' => $media,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages
        ];
    }
    
    /**
     * Create backup
     */
    public function create_backup($request) {
        $params = $request->get_json_params();
        $post_ids = $params['post_ids'] ?? [];
        
        $backup_data = [
            'timestamp' => current_time('mysql'),
            'posts' => []
        ];
        
        if (!empty($post_ids)) {
            // Backup specific posts
            foreach ($post_ids as $post_id) {
                $post = get_post($post_id);
                if ($post) {
                    $backup_data['posts'][] = $this->format_post_for_backup($post);
                }
            }
        } else {
            // Backup all posts and pages
            $posts = get_posts([
                'post_type' => ['post', 'page'],
                'posts_per_page' => -1,
                'post_status' => 'any'
            ]);
            
            foreach ($posts as $post) {
                $backup_data['posts'][] = $this->format_post_for_backup($post);
            }
        }
        
        // Store backup as transient (temporary storage)
        $backup_id = 'wpbm_backup_' . time();
        set_transient($backup_id, $backup_data, DAY_IN_SECONDS);
        
        return [
            'backup_id' => $backup_id,
            'post_count' => count($backup_data['posts']),
            'timestamp' => $backup_data['timestamp']
        ];
    }
    
    /**
     * Get post revisions
     */
    public function get_revisions($request) {
        $post_id = $request->get_param('id');
        
        $revisions = wp_get_post_revisions($post_id);
        $formatted_revisions = [];
        
        foreach ($revisions as $revision) {
            $formatted_revisions[] = [
                'id' => $revision->ID,
                'author' => get_the_author_meta('display_name', $revision->post_author),
                'date' => $revision->post_date,
                'date_gmt' => $revision->post_date_gmt,
                'modified' => $revision->post_modified,
                'title' => $revision->post_title
            ];
        }
        
        return $formatted_revisions;
    }
    
    /**
     * Restore revision
     */
    public function restore_revision($request) {
        $post_id = $request->get_param('id');
        $revision_id = $request->get_param('revision_id');
        
        $revision = wp_get_post_revision($revision_id);
        
        if (!$revision || $revision->post_parent != $post_id) {
            return new WP_Error('invalid_revision', 'Invalid revision ID', ['status' => 404]);
        }
        
        $restored = wp_restore_post_revision($revision_id);
        
        return [
            'success' => $restored !== false,
            'post_id' => $post_id,
            'revision_id' => $revision_id
        ];
    }
    
    // Helper methods remain the same...
    private function format_post($post) {
        return [
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'status' => $post->post_status,
            'type' => $post->post_type,
            'slug' => $post->post_name,
            'date' => $post->post_date,
            'modified' => $post->post_modified,
            'author' => get_the_author_meta('display_name', $post->post_author),
            'link' => get_permalink($post->ID),
            'featured_media' => get_post_thumbnail_id($post->ID)
        ];
    }
    
    private function format_media($attachment) {
        $metadata = wp_get_attachment_metadata($attachment->ID);
        
        return [
            'id' => $attachment->ID,
            'title' => $attachment->post_title,
            'filename' => basename(get_attached_file($attachment->ID)),
            'url' => wp_get_attachment_url($attachment->ID),
            'mime_type' => $attachment->post_mime_type,
            'file_size' => filesize(get_attached_file($attachment->ID)),
            'dimensions' => [
                'width' => $metadata['width'] ?? null,
                'height' => $metadata['height'] ?? null
            ],
            'uploaded' => $attachment->post_date
        ];
    }
    
    private function format_post_for_backup($post) {
        $formatted = $this->format_post($post);
        
        // Add meta data
        $formatted['meta'] = get_post_meta($post->ID);
        
        // Add custom fields
        $formatted['custom_fields'] = get_post_custom($post->ID);
        
        return $formatted;
    }
    
    // Other endpoint methods...
}