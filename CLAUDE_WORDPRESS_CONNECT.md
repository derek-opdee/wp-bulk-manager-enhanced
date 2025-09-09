# Claude Mode: WordPress Connect (WP Bulk Manager)

## Command: `/wordpress_connect`

Connect to and manage WordPress sites using the WP Bulk Manager system with SEO Generator integration.

## Overview

The WP Bulk Manager is a comprehensive system for managing WordPress content at scale, with special integration for the SEO Generator plugin. It consists of:

1. **WordPress Plugin** (`wp-bulk-manager-client.php`) - Installed on WordPress sites
2. **Python CLI** (`wpbm_cli_enhanced.py`) - Command-line interface for bulk operations
3. **macOS App** - Native Swift application for visual management
4. **SEO Generator Integration** - Manage dynamic content pages with search terms and locations

## Quick Start

```bash
# Navigate to the project
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app

# Activate virtual environment
source venv/bin/activate

# Run the assistant
python3 wpbm_assistant.py
```

## Core Features

### 1. Site Management
- Connect multiple WordPress sites
- Secure API key authentication
- Site status monitoring
- Bulk operations across sites

### 2. Content Operations
- **Bulk Import/Export**: CSV-based content management
- **Content Updates**: Update posts, pages, and custom post types
- **Media Management**: Upload and manage images in bulk
- **Category/Tag Management**: Bulk assign taxonomies

### 3. SEO Generator Integration
- **Dynamic Pages**: Manage pages with [search_term] and [location] placeholders
- **Bulk Updates**: Update search terms and locations across multiple pages
- **Template Management**: Apply consistent templates with dynamic fields
- **Grammar Rules**: Handles "Services" in search terms intelligently

### 4. User Management
- Create users in bulk
- Update user roles and metadata
- Export user data

## Key Commands

### Basic Operations
```python
# Connect to site
wpbm_connect()

# List all pages
/wordpress_list

# Show page content
/wordpress_show 3616

# Update page content
/wordpress_update 3616 "New content here"
```

### SEO Generator Operations
```python
# List SEO Generator pages
/wordpress_seo_pages

# Update SEO Generator page
/wordpress_gen_page 4732
# Then provide:
# - Search terms (one per line)
# - Locations (one per line)
# - Dynamic content updates
```

### Bulk Operations
```python
# Import content from CSV
/wordpress_import posts.csv

# Export content to CSV
/wordpress_export pages

# Bulk update categories
/wordpress_categories assign "New Category" 1,2,3,4,5
```

## File Structure

```
/wp-bulk-manager/
├── wordpress-plugin/
│   └── wp-bulk-manager-client.php    # WordPress plugin
├── macos-app/
│   ├── wpbm_manager.py               # Core manager class
│   ├── wpbm_cli_enhanced.py          # Enhanced CLI
│   ├── wpbm_assistant.py             # Interactive assistant
│   └── config.json                   # Site configurations
└── docs/
    ├── README.md                     # Project documentation
    ├── DYNAMIC_FIELDS_GUIDE.md       # SEO Generator guide
    └── API_DOCUMENTATION.md          # API reference
```

## API Endpoints

### WordPress Plugin Endpoints
- `GET /wp-json/wpbm/v1/test` - Test connection
- `GET /wp-json/wpbm/v1/content/{id}` - Get content
- `PUT /wp-json/wpbm/v1/content/{id}` - Update content
- `POST /wp-json/wpbm/v1/posts` - Create posts
- `POST /wp-json/wpbm/v1/media` - Upload media
- `GET /wp-json/wpbm/v1/users` - List users
- `POST /wp-json/wpbm/v1/users` - Create users

### SEO Generator Endpoints
- `GET /wp-json/wpbm/v1/seo-generator/pages` - List SEO pages
- `GET /wp-json/wpbm/v1/seo-generator/pages/{id}` - Get SEO page details
- `PUT /wp-json/wpbm/v1/seo-generator/pages/{id}` - Update SEO page

## Configuration

### Site Configuration (config.json)
```json
{
  "sites": [
    {
      "id": "opdee",
      "name": "Opdee",
      "url": "https://opdee.com",
      "status": "active"
    }
  ],
  "api_keys": {
    "opdee": "your-api-key-here"
  }
}
```

### Dynamic Fields (SEO Generator)
- `[search_term]` - Single search term
- `[search_terms]` - Plural search term
- `[location]` - Location name

### Grammar Rules
- If search term contains "Services", use as-is
- Otherwise, append "Services" or "services" based on context
- Handle special cases like "AI Development Services"

## Common Tasks

### 1. Update Multiple Pages with Same Content
```python
pages = [3616, 3629, 3631]
content = "Updated content"
for page_id in pages:
    manager.update_content(site['id'], page_id, content)
```

### 2. Bulk Update SEO Generator Pages
```python
search_terms = ["AI Development", "Machine Learning", "Web Apps"]
locations = ["Melbourne", "Sydney", "Brisbane"]
manager.update_seo_generator_page(site['id'], page_id, {
    'search_terms': search_terms,
    'locations': locations,
    'content': updated_content
})
```

### 3. Export All Pages
```python
pages = manager.list_content(site['id'], 'page')
manager.export_to_csv(pages, 'all_pages.csv')
```

### 4. Find and Replace Across Site
```python
# Use the assistant's search and replace functionality
/wordpress_search "old text"
/wordpress_replace "old text" "new text" 1,2,3
```

## Opdee Philosophy Integration

When updating content, apply Opdee's philosophy:
- Focus on human-AI balance
- Use "systems" not "solutions"
- Remove em/en dashes
- Australian English spelling
- Conversational, direct tone
- Emphasize "what people actually want to use"

## Troubleshooting

### Connection Issues
1. Check API key in config.json
2. Verify WordPress plugin is activated
3. Ensure REST API is accessible
4. Check site URL (no trailing slash)

### SEO Generator Issues
1. Verify SEO Generator plugin is installed
2. Check if page is actually an SEO Generator page
3. Ensure dynamic fields are properly formatted
4. Review grammar rules for search terms

### Performance Tips
- Use bulk operations for multiple updates
- Cache frequently accessed data
- Paginate large result sets
- Use CSV import/export for large datasets

## Security

- API keys stored locally in config.json
- All requests use X-API-Key header
- HTTPS required for all connections
- No credentials stored in code

## Advanced Usage

### Custom Scripts
Create Python scripts using the manager:
```python
from wpbm_manager import WPBulkManager

manager = WPBulkManager()
sites = manager.get_sites('active')
# Your custom logic here
```

### Extending Functionality
- Add new endpoints to WordPress plugin
- Create new CLI commands
- Build automation scripts
- Integrate with other tools

## Quick Reference

**Connect**: `/wordpress_connect`
**List**: `/wordpress_list [posts|pages|users]`
**Show**: `/wordpress_show [id]`
**Update**: `/wordpress_update [id] [content]`
**SEO Pages**: `/wordpress_seo_pages`
**Generate**: `/wordpress_gen_page [id]`
**Search**: `/wordpress_search [term]`
**Replace**: `/wordpress_replace [old] [new] [ids]`
**Export**: `/wordpress_export [type]`
**Import**: `/wordpress_import [file]`

## Notes

- Always backup before bulk operations
- Test on single items before bulk updates
- Monitor API rate limits
- Keep plugin updated on all sites
- Document custom modifications