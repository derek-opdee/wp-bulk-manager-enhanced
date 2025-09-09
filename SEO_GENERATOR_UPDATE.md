# SEO Generator Integration Update

I've successfully extended the WP Bulk Manager to support SEO Generator page management! 🎉

## What's New

### WordPress Plugin Updates
The client plugin (`wp-bulk-manager-client.php`) now includes:
- New REST API endpoints for SEO Generator management
- Functions to read/update search terms and locations
- Support for managing URL structures
- Dynamic field counting in content

### New API Endpoints
- `GET /wp-json/wpbm/v1/seo-generator/pages` - List all SEO Generator pages
- `GET /wp-json/wpbm/v1/seo-generator/page/{id}` - Get page details including search terms and locations
- `PUT /wp-json/wpbm/v1/seo-generator/page/{id}` - Update search terms, locations, and URL structure

### Python Manager Updates
Added methods to `EnhancedWPBulkManager`:
- `get_seo_generator_pages()` - List all SEO Generator pages
- `get_seo_generator_page()` - Get detailed page info
- `update_seo_generator_page()` - Update page settings

### CLI Menu Updates
New menu options:
- **Option 9**: List SEO Generator Pages - Shows all pages with term/location counts
- **Option 10**: Manage SEO Generator Page - Full management interface for:
  - Viewing/editing search terms (max 20)
  - Viewing/editing locations (max 300)
  - Updating URL structure
  - Viewing content with dynamic field usage
  - Adding dynamic fields to content

## How to Use

### 1. Update the WordPress Plugin
First, upload the updated `wp-bulk-manager-client.php` to your WordPress site:
```bash
# The file is located at:
/Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/wp-bulk-manager-client.php
```

### 2. Run the Enhanced CLI
```bash
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app
./run_enhanced.sh
```

### 3. Manage SEO Generator Pages
From the menu:
1. Select option 9 to list all SEO Generator pages
2. Select option 10 to manage a specific page
3. You can now:
   - Edit search terms (up to 20)
   - Edit locations (up to 300)
   - Update the URL structure
   - View how many times each dynamic field is used

## Dynamic Fields
The system recognizes these dynamic fields in content:
- `[search_term]` - Singular form of the search term
- `[search_terms]` - Plural form of the search term  
- `[location]` - The location name

## Example Usage
To update page 3202's search terms:
1. Run the enhanced CLI
2. Select option 10 (Manage SEO Generator Page)
3. Enter page ID: 3202
4. Select option 1 (View/Edit Search Terms)
5. Choose to replace, add, or remove terms

## Note
The plugin needs to be updated on the WordPress site before the new features will work. The current error occurs because the WordPress site is still running the old version without SEO Generator support.