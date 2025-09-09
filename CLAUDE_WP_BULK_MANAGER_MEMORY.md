# WordPress Bulk Manager - Claude Code Memory

## Overview
WordPress Bulk Manager is a comprehensive system for managing multiple WordPress sites remotely through a REST API. It consists of a WordPress plugin installed on target sites and a Python CLI tool for bulk operations, with advanced plugin management capabilities.

## Active Sites

### 1. Opdee (opdee.com)
- **URL**: https://opdee.com
- **Status**: Active  
- **API Key**: 27013065aa24d225b5ea9db967d191f3
- **IP Restrictions**: 202.62.150.192 (whitelisted)
- **Features**: Full plugin management system
- **Special**: Has dynamic content pages with [search_term] and [location] fields

### 2. BoulderWorks (boulderworks.net)
- **URL**: https://www.boulderworks.net
- **Status**: Active
- **API Key**: HKq068Yl4ybRqhGjBfhF9siINYIl31G6
- **Business**: Laser cutting & engraving services
- **Location**: Longmont, CO
- **Notes**: Uses Divi Builder and Stackable blocks

## What This Plugin Does

### Core Features:
1. **Remote Content Management** - Create, read, update, delete posts/pages via REST API
2. **Plugin Management** - Upload, install, activate, update, and delete plugins remotely
3. **SEO Management** - Update SEO titles, descriptions, and meta data
4. **Bulk Operations** - Update multiple pages at once, import/export CSV
5. **Media Management** - Upload and manage images remotely
6. **User Management** - Create and manage WordPress users
7. **Plugin/Theme Info** - Check installed plugins and themes
8. **Security Features** - API key authentication and IP whitelisting

### Plugin Management Features (NEW):
- **Upload plugins** from local computer (ZIP files)
- **Install plugins** from WordPress.org or direct URLs
- **Bulk plugin operations** - Install multiple plugins from configuration files
- **Plugin updates** - Update all plugins with available updates
- **Plugin activation/deactivation** - Manage plugin status remotely
- **Export plugin lists** - Backup current plugin configurations

### Security Features:
- **API Key Authentication** - Cryptographically secure API keys
- **IP Whitelisting** - Restrict access to specific IP addresses/ranges
- **Timing-safe comparisons** - Prevent timing attacks
- **Input validation** - All requests properly sanitized

## Current Plugin Architecture

### WordPress Plugin (wp-bulk-manager-client-robust.php):
```php
wordpress-plugin/
├── wp-bulk-manager-client-robust.php    # Main plugin file (ACTIVE)
├── includes/                            # Plugin components
│   ├── class-wpbm-plugin-manager.php   # Plugin management functionality
│   ├── class-wpbm-api-handler.php      # API request handling
│   ├── class-wpbm-security.php         # Security features
│   └── class-wpbm-seo-manager.php      # SEO management
├── assets/                              # Admin UI assets
│   ├── css/admin.css                    # Admin styling
│   └── js/admin.js                      # Admin JavaScript
├── old-versions/                        # Previous plugin versions
└── README.md                            # Documentation
```

### Python Package (wpbm/):
```python
macos-app/
├── wpbm/                               # Main package
│   ├── __init__.py                     # Package exports
│   ├── api/                            # API client
│   │   ├── client.py                   # Base API client with caching
│   │   └── auth.py                     # Authentication handling
│   ├── operations/                     # Operation classes
│   │   ├── content.py                  # Content operations
│   │   ├── media.py                    # Media operations
│   │   └── plugins.py                  # Plugin operations (NEW)
│   └── utils/                          # Utilities
│       ├── cache.py                    # Caching system
│       └── logger.py                   # Logging setup
├── manage_plugins.py                   # Plugin management CLI
├── example-plugins-config.json         # Example bulk install config
└── wpbm_assistant.py                   # Interactive assistant
```

## How It Works

### Architecture:
```
WordPress Site                    Your Computer
┌─────────────────┐              ┌─────────────────┐
│ WP Bulk Manager │              │ Python CLI Tool │
│     Plugin      │<--- API ---->│ wpbm_assistant  │
│ (REST Endpoints)│              │   + Database    │
│ + Plugin Mgmt   │              │ + Plugin CLI    │
└─────────────────┘              └─────────────────┘
```

### Plugin Side (WordPress):
- Registers REST API endpoints under `/wp-json/wpbm/v1/`
- Handles authentication via API keys with IP whitelisting
- On-demand loading of WordPress admin classes for plugin management
- Integrates with WordPress upgrader API for safe plugin operations
- Clean admin interface with security warnings

### CLI Side (Python):
- Interactive command-line interface with modular operations
- Plugin management CLI (`manage_plugins.py`)
- Intelligent caching system for performance
- Concurrent operations for bulk tasks
- macOS Keychain integration for secure API key storage

## REST API Endpoints

### Content Management:
- `GET /content` - List content with filtering
- `POST /content` - Create new content
- `GET /content/{id}` - Get single content item
- `PUT /content/{id}` - Update content
- `DELETE /content/{id}` - Delete content

### Plugin Management (NEW):
- `GET /plugins` - List all installed plugins with status
- `POST /plugins/upload` - Upload and install plugin file
- `POST /plugins/install-url` - Install plugin from WordPress.org URL
- `POST /plugins/activate` - Activate a plugin
- `POST /plugins/deactivate` - Deactivate a plugin
- `POST /plugins/delete` - Delete a plugin
- `POST /plugins/update` - Update a plugin to latest version

### System:
- `GET /health` - Health check (no authentication required)

## Commands & Usage

### Plugin Management Commands:
```bash
# Start environment
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app
source venv/bin/activate

# List all plugins
python manage_plugins.py opdee list

# Upload and install a plugin
python manage_plugins.py opdee upload /path/to/plugin.zip --activate

# Install plugin from WordPress.org
python manage_plugins.py opdee install-url https://downloads.wordpress.org/plugin/akismet.latest.zip --activate

# Update all plugins with available updates
python manage_plugins.py opdee update-all

# Bulk install from configuration file
python manage_plugins.py opdee bulk-install plugins-config.json

# Export current plugin list for backup
python manage_plugins.py opdee export --output opdee-plugins.json

# Activate an existing plugin
python manage_plugins.py opdee activate plugin-folder/plugin-file.php
```

### Content Management Commands:
```bash
# Start the assistant
python3 wpbm_assistant.py

# Primary commands
/wordpress_list [type]     # List content (posts, pages, users, all)
/wordpress_show [id]       # Show single item details
/wordpress_update [id]     # Update content interactively
/wordpress_create          # Create new content
/wordpress_delete [id]     # Delete content (move to trash)
/wordpress_search [term]   # Search content
/wordpress_replace         # Find & replace across site
/wordpress_export [type]   # Export to CSV
/wordpress_import [file]   # Import from CSV
```

### SEO Generator Commands:
```bash
/wordpress_seo_pages       # List SEO Generator pages
/wordpress_gen_page [id]   # Update SEO Generator page with variables
/wordpress_seo_export      # Export SEO configurations
```

## Bulk Plugin Installation Config

Create JSON files for bulk plugin installation:
```json
{
  "description": "Essential plugins for new site",
  "plugins": [
    {
      "url": "https://downloads.wordpress.org/plugin/wordpress-seo.latest.zip",
      "activate": true,
      "description": "Yoast SEO"
    },
    {
      "url": "https://downloads.wordpress.org/plugin/wordfence.latest.zip", 
      "activate": true,
      "description": "Wordfence Security"
    },
    {
      "path": "/Users/yourname/Downloads/premium-plugin.zip",
      "activate": false,
      "description": "Local premium plugin file"
    }
  ]
}
```

## Security Implementation

### API Key Management:
- Cryptographically secure generation using `random_bytes()`
- Timing-safe comparison with `hash_equals()`
- Separate storage from other settings to prevent clearing
- Copy-to-clipboard functionality in admin
- Regeneration with immediate invalidation of old keys

### IP Whitelisting:
- Support for individual IP addresses
- CIDR notation support (e.g., `192.168.1.0/24`)
- Automatic client IP detection (handles proxies/CDNs)
- IP validation and sanitization

### Request Security:
- WordPress nonce verification for admin actions
- Input sanitization and validation
- Proper error handling without information leakage
- Rate limiting considerations

## Troubleshooting

### Plugin Activation Issues:
- Check PHP version (requires PHP 7.4+)
- Verify all plugin files are uploaded correctly
- Check WordPress error logs for specific errors
- Ensure WordPress admin classes load properly

### API Key Issues:
- Ensure API key is copied correctly (no extra spaces)
- Check IP whitelist if connection fails
- Verify the key hasn't been regenerated
- Test with the built-in "Test Connection" button

### Plugin Management Issues:
- Verify ZIP files are valid WordPress plugins
- Check file upload permissions and disk space
- Ensure plugin compatibility with WordPress version
- Check for plugin conflicts or dependencies

### Common Error Messages:
- `"Class not found"` - WordPress admin files not loaded
- `"Invalid API key"` - Key mismatch or regenerated key  
- `"IP not allowed"` - IP address not in whitelist
- `"Plugin manager unavailable"` - Plugin management classes failed to load

## Important Rules & Best Practices

### Plugin Management:
1. **Always backup** before bulk plugin operations
2. **Test uploads** on staging sites first for premium plugins
3. **Check compatibility** before mass updates
4. **Use bulk configs** for consistent site setups
5. **Export plugin lists** before major changes

### Content Editing:
1. **Preserve Page Builders** - Always maintain Gutenberg/Divi/Elementor structure
2. **Use Proper Blocks** - Never inject raw HTML outside of block structures
3. **Respect SEO Fields** - Update via 'seo' object, not in content

### Security Practices:
1. **Use IP whitelisting** in production environments
2. **Regenerate API keys** regularly
3. **Never expose API keys** in documentation or logs
4. **Monitor access patterns** for unusual activity

## Recent Major Updates (v3.0.0)

### Plugin Architecture Overhaul:
- ✅ Lazy loading of plugin manager to prevent activation errors
- ✅ On-demand WordPress admin class loading
- ✅ Proper error handling and graceful degradation
- ✅ Removed API endpoint exposure from admin interface
- ✅ Enhanced security with separate API key management

### New Plugin Management System:
- ✅ Complete plugin upload/install/update/delete functionality
- ✅ Bulk plugin operations with progress tracking
- ✅ Integration with WordPress upgrader API
- ✅ Plugin list export for backup and migration
- ✅ Command-line interface for all plugin operations

### Performance & Caching:
- ✅ Intelligent caching system with TTL support
- ✅ Concurrent operations for bulk tasks
- ✅ Reduced API calls through smart caching
- ✅ Performance monitoring and optimization

## File Locations
- **Active Plugin**: `/wordpress-plugin/wp-bulk-manager-client-robust.php`
- **Plugin Manager**: `/wordpress-plugin/includes/class-wpbm-plugin-manager.php`
- **Python CLI**: `/macos-app/wpbm_assistant.py`  
- **Plugin CLI**: `/macos-app/manage_plugins.py`
- **Database**: `/macos-app/wpbm_sites.db`
- **Configs**: `/macos-app/config.json`

## Integration Support
- WordPress 5.0+ (tested with 6.8.1)
- PHP 7.4+ (tested with 8.2.20)
- All major page builders (Gutenberg, Divi, Elementor)
- SEO plugins (The SEO Framework, Yoast SEO)
- Security plugins (Wordfence, etc.)
- Plugin compatibility checking and management

This system now provides comprehensive WordPress site management including advanced plugin management capabilities while maintaining security and performance standards.