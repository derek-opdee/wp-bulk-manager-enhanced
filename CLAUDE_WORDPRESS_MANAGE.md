# Claude WordPress Management Mode

## Command: `/wordpress_manage`

This document provides Claude with comprehensive information about the WP Bulk Manager system for managing WordPress sites.

## System Overview

WP Bulk Manager is a two-part system:
1. **Client Plugin** (`wp-bulk-manager-client.php`) - Installed on WordPress sites
2. **macOS Manager** - Python CLI application for remote management

## Key Files and Locations

```
/Users/derekzar/Documents/Projects/wp-bulk-manager/
├── wordpress-plugin/
│   └── wp-bulk-manager-client.php    # WordPress plugin (install on sites)
├── macos-app/
│   ├── wpbm_manager.py               # Core manager class
│   ├── wpbm_cli_enhanced.py         # Enhanced CLI with full features
│   ├── wpbm_assistant.py            # Assistant mode for Claude
│   ├── run_enhanced.sh              # Launch enhanced CLI
│   └── site_connections.db          # SQLite database for sites
```

## Quick Start Commands

```bash
# Navigate to project
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app

# Activate environment and run
source venv/bin/activate
./run_enhanced.sh

# Or use assistant mode
python3 wpbm_assistant.py
```

## Current Connected Sites

- **Opdee** (https://opdee.com)
  - API Key: 8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U

## Core Capabilities

### 1. Content Management
- List all pages/posts with filtering
- View/edit content including Gutenberg blocks
- Duplicate pages/posts
- Delete content (trash or permanent)
- Search across all content
- Bulk create with variable substitution

### 2. SEO Management (The SEO Framework)
- View/update SEO titles and descriptions
- Bulk SEO updates
- SEO analysis and recommendations
- Uses `_genesis_title` and `_genesis_description` meta keys

### 3. SEO Generator Integration
- List all SEO Generator pages
- Manage search terms (max 20 per page)
- Manage locations (max 300 per page)
- Update URL structures
- View dynamic field usage in content
- Dynamic fields: `[search_term]`, `[search_terms]`, `[location]`

### 4. Plugin/Theme Management
- List all plugins with version info
- List all themes
- Check active status

## API Endpoints

### Authentication
- `POST /wp-json/wpbm/v1/auth` - Verify connection

### Content
- `GET /wp-json/wpbm/v1/content` - List content
- `GET /wp-json/wpbm/v1/content/{id}` - Get single item
- `POST /wp-json/wpbm/v1/content` - Create content
- `PUT /wp-json/wpbm/v1/content/{id}` - Update content
- `DELETE /wp-json/wpbm/v1/content/{id}` - Delete content
- `POST /wp-json/wpbm/v1/content/{id}/duplicate` - Duplicate

### SEO
- `GET /wp-json/wpbm/v1/seo` - List all SEO data
- `PUT /wp-json/wpbm/v1/seo/{id}` - Update SEO

### SEO Generator
- `GET /wp-json/wpbm/v1/seo-generator/pages` - List SEO Gen pages
- `GET /wp-json/wpbm/v1/seo-generator/page/{id}` - Get page details
- `PUT /wp-json/wpbm/v1/seo-generator/page/{id}` - Update settings

## Common Tasks

### Connect to Opdee and Check Status
```python
from wpbm_assistant import wpbm_connect
assistant = wpbm_connect()
wpbm_status(assistant)
```

### List All Pages
```python
content = assistant.manager.list_all_content(assistant.current_site_id, 'page')
for page in content:
    print(f"ID: {page['id']} - {page['title']}")
```

### Get SEO Generator Page Details
```python
details = assistant.manager.get_seo_generator_page(assistant.current_site_id, 3202)
print(f"Search Terms: {details['search_terms']}")
print(f"Locations: {details['locations'][:10]}...")
```

### Update SEO Generator Page
```python
data = {
    'search_terms': ['Web Design', 'Website Development', 'WordPress Sites'],
    'locations': ['Melbourne', 'Sydney', 'Brisbane']
}
assistant.manager.update_seo_generator_page(assistant.current_site_id, 3202, data)
```

### Duplicate and Modify Content
```python
# Get original content
original = assistant.get_page_content(3616)

# Create new content with dynamic fields
new_content = original['content'].replace('Web Design', '[search_term]')
new_content = new_content.replace('Melbourne', '[location]')

# Create new page (would need to do in WordPress admin)
# Then configure via bulk manager
```

## SEO Generator Page Creation Process

1. **Find Template Page**: Identify a well-designed page to use as template
2. **Copy Content**: Get the full Gutenberg/Kadence block code
3. **Add Dynamic Fields**: Replace static terms with `[search_term]`, `[search_terms]`, `[location]`
4. **Create in WordPress**: SEO Generator > Add New, paste content
5. **Configure via CLI**: Add search terms, locations, URL structure

### Example Transformation
```html
<!-- Original -->
<h2>Professional Web Design Services in Melbourne</h2>
<p>Our web designers create stunning websites for Melbourne businesses.</p>

<!-- With Dynamic Fields -->
<h2>Professional [search_term] Services in [location]</h2>
<p>Our [search_terms] create stunning websites for [location] businesses.</p>
```

## Database Schema

### Sites Table
- id, name, url, domain, api_key_id, status, created_at, updated_at

### API Keys Table  
- id, site_id, key_reference, created_at

## Error Handling

Common issues:
- **Connection Failed**: Check API key and site URL
- **404 on Endpoints**: Update plugin on WordPress site
- **No SEO Data**: Ensure The SEO Framework is active

## Best Practices

1. Always backup before bulk operations
2. Test on single page before bulk updates
3. Keep search terms relevant and concise
4. Use proper location formatting (Title Case)
5. Monitor total variations (terms × locations)

## Command Examples for Claude

When asked to manage WordPress:
```python
# Standard connection
from wpbm_assistant import wpbm_connect
assistant = wpbm_connect()

# Check what needs attention
issues = assistant.analyze_seo_issues()
print(f"Found {len(issues)} pages with SEO issues")

# Get page for SEO Generator setup
page = assistant.get_page_content(3616)
# ... analyze and prepare content with dynamic fields
```

## Notes

- All API keys stored in macOS Keychain
- Database at `site_connections.db`
- Logs errors but continues operation
- Supports both legacy {var} and new [var] syntax
- Maximum limits: 20 search terms, 300 locations per page