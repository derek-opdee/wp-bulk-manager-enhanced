# WP Bulk Manager - Architecture Update

## Overview
WP Bulk Manager is now split into two components:
1. **macOS Management Application** - Runs on your Mac to manage all customer sites
2. **WordPress Companion Plugin** - Installed on each customer's WordPress site

## Architecture

### macOS Application (Python/Node.js)
- Central dashboard for managing all customer sites
- Secure credential storage using macOS Keychain
- Bulk content creation and updates
- SEO management interface
- Template and variable management
- Queue processing for bulk operations

### WordPress Companion Plugin
- Lightweight REST API endpoint
- Secure authentication via API keys
- Integration with The SEO Framework
- Content creation/update handlers
- Plugin/theme management endpoints
- Minimal footprint on customer sites

## The SEO Framework Integration

### Meta Keys Used by TSF
- Post meta stored with `_tsf_` prefix (based on research)
- Moving towards array-based storage in future versions
- Custom field API: `get_custom_field()`

### SEO Data Structure
```php
// Current TSF meta storage (individual keys)
_tsf_title_no_blogname
_tsf_description
_tsf_canonical
_tsf_noindex
_tsf_nofollow
_tsf_noarchive

// Future TSF storage (array-based)
_tsf_post_meta = [
    'title' => '',
    'description' => '',
    'canonical' => '',
    'robots' => []
]
```

### Integration Points
1. Use TSF filters for custom descriptions
2. Access TSF's post-meta API
3. Bulk update SEO meta through custom endpoints

## Security Model

### macOS App
- API keys stored in macOS Keychain
- SSL/TLS for all communications
- Request signing with HMAC
- Rate limiting

### WordPress Plugin
- API key validation
- Capability checks
- Nonce verification for admin actions
- IP whitelisting (optional)

## Data Flow

1. **Content Creation**
   ```
   macOS App → API Request → WP Plugin → TSF Integration → Database
   ```

2. **SEO Updates**
   ```
   macOS App → Bulk SEO Data → WP Plugin → TSF Filters → Meta Update
   ```

3. **Site Monitoring**
   ```
   WP Plugin → Status Data → API Response → macOS App Dashboard
   ```

## Database Schema

### macOS App (SQLite)
```sql
-- Sites table
CREATE TABLE sites (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    api_key TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    last_sync DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Templates table
CREATE TABLE templates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    variables TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Operations table
CREATE TABLE operations (
    id INTEGER PRIMARY KEY,
    site_id INTEGER,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    data TEXT,
    error TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (site_id) REFERENCES sites(id)
);
```

### WordPress Plugin
- No custom tables needed
- Uses WordPress options table for settings
- Leverages existing post meta structure

## API Endpoints (WordPress Plugin)

### Authentication
All requests require `X-API-Key` header

### Endpoints
- `POST /wp-json/wpbm/v1/auth` - Verify API key
- `GET /wp-json/wpbm/v1/status` - Site status and info
- `POST /wp-json/wpbm/v1/content` - Create/update content
- `GET /wp-json/wpbm/v1/content/{id}` - Get content
- `PUT /wp-json/wpbm/v1/seo/{id}` - Update SEO meta
- `GET /wp-json/wpbm/v1/plugins` - List plugins
- `POST /wp-json/wpbm/v1/bulk` - Bulk operations

## Features Comparison

### Previous (All-in-One Plugin)
- Heavy plugin on each site
- Database tables on each site
- Complex permission management
- Single point of failure

### New Architecture
- Lightweight plugin on customer sites
- Central management from macOS
- Better security isolation
- Easier updates and maintenance
- Works with existing SEO Framework