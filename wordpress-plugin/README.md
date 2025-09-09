# WP Bulk Manager WordPress Plugin

A comprehensive WordPress plugin for bulk content management with REST API integration and plugin management capabilities.

## 🚀 Features

### Core Content Management
- **Bulk content operations** - Create, read, update, delete posts, pages, and custom post types
- **Advanced filtering** - Filter by post type, status, date ranges
- **Search & replace** - Find and replace text across all content
- **Revision tracking** - Track changes with rollback capability
- **Backup before operations** - Automatic backups before bulk changes

### Plugin Management
- **Upload plugins** from your computer
- **Install plugins** from WordPress.org or direct URLs
- **Bulk plugin operations** - Install multiple plugins from configuration files
- **Plugin updates** - Update all plugins with available updates
- **Plugin activation/deactivation** - Manage plugin status remotely

### Security & Performance
- **API key authentication** - Secure access with custom API keys
- **IP whitelisting** - Restrict access to specific IP addresses or ranges
- **Caching system** - Intelligent caching for improved performance
- **Rate limiting** - Built-in protection against abuse

## 📦 Installation

1. Upload the plugin files to `/wp-content/plugins/wp-bulk-manager/`
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to **Settings → Bulk Manager**
4. Generate an API key
5. Configure allowed IPs if needed (optional but recommended)

## 🔧 Configuration

### API Key Setup
1. Navigate to **Settings → Bulk Manager** in your WordPress admin
2. Click **"Generate API Key"** to create a secure API key
3. Copy the generated key for use with the Python client
4. **Important**: Keep this key secure - never share it publicly

### API Key Management
The Python client stores API keys securely in the macOS Keychain:
```bash
# Add a new site
python wpbm_manager.py add-site "Site Name" "https://yoursite.com" "your-api-key"

# Show current API key for a site
python update_api_key.py yoursite --show

# Update API key if regenerated
python update_api_key.py yoursite --key "new-api-key-here"

# List all connected sites
python wpbm_manager.py list-sites
```

### IP Whitelisting (Recommended)
1. In the **IP Address Whitelist** section, enter your IP addresses
2. One IP per line, supports CIDR notation (e.g., `192.168.1.0/24`)
3. Leave empty to allow all IP addresses (not recommended for production)
4. Click **"Save IP Addresses"**

## 🐍 Python Client Usage

### Basic Setup
```bash
cd /path/to/wp-bulk-manager/macos-app
source venv/bin/activate
```

### Content Management
```python
from wpbm import WPBMClient

# Initialize client
client = WPBMClient('https://yoursite.com', 'your-api-key-here')

# Get all posts
posts = client.get('/content', {'type': 'post', 'limit': 50})

# Create new post
new_post = client.post('/content', {
    'title': 'New Post Title',
    'content': 'Post content here',
    'type': 'post',
    'status': 'draft'
})

# Update existing post
client.put('/content/123', {
    'title': 'Updated Title',
    'content': 'Updated content'
})
```

### Plugin Management
```bash
# List all plugins
python manage_plugins.py yoursite list

# Upload and install a plugin
python manage_plugins.py yoursite upload /path/to/plugin.zip --activate

# Install plugin from WordPress.org
python manage_plugins.py yoursite install-url https://downloads.wordpress.org/plugin/akismet.latest.zip --activate

# Update all plugins
python manage_plugins.py yoursite update-all

# Bulk install from configuration file
python manage_plugins.py yoursite bulk-install plugins-config.json

# Export plugin list for backup
python manage_plugins.py yoursite export --output site-plugins.json
```

### Bulk Plugin Installation Config
Create a JSON file with plugins to install:
```json
{
  "description": "Plugin installation config",
  "plugins": [
    {
      "url": "https://downloads.wordpress.org/plugin/wordpress-seo.latest.zip",
      "activate": true,
      "description": "Yoast SEO"
    },
    {
      "path": "/Users/yourname/Downloads/premium-plugin.zip",
      "activate": false,
      "description": "Local premium plugin"
    }
  ]
}
```

## 🏗️ File Structure

```
wordpress-plugin/
├── wp-bulk-manager-client-robust.php    # Main plugin file (use this!)
├── includes/                            # Plugin components
│   ├── class-wpbm-plugin-manager.php   # Plugin management functionality
│   ├── class-wpbm-api-handler.php      # API request handling
│   ├── class-wpbm-security.php         # Security features
│   └── class-wpbm-seo-manager.php      # SEO management
├── assets/                              # Admin UI assets
│   ├── css/admin.css                    # Admin styling
│   └── js/admin.js                      # Admin JavaScript
├── old-versions/                        # Previous plugin versions
└── README.md                            # This file
```

## 🔌 REST API Endpoints

The plugin provides a comprehensive REST API at `/wp-json/wpbm/v1/`:

### Content Endpoints
- `GET /content` - List content with filtering
- `POST /content` - Create new content
- `GET /content/{id}` - Get single content item
- `PUT /content/{id}` - Update content
- `DELETE /content/{id}` - Delete content

### Plugin Management Endpoints
- `GET /plugins` - List all installed plugins
- `POST /plugins/upload` - Upload and install plugin file
- `POST /plugins/install-url` - Install plugin from URL
- `POST /plugins/activate` - Activate a plugin
- `POST /plugins/deactivate` - Deactivate a plugin
- `POST /plugins/delete` - Delete a plugin
- `POST /plugins/update` - Update a plugin

### System Endpoints
- `GET /health` - Health check (no authentication required)

All endpoints require the `X-API-Key` header except for `/health`.

## 🔐 Security Features

### API Key Protection
- Cryptographically secure API key generation
- Timing-safe key comparison to prevent timing attacks
- Secure storage in WordPress options table

### IP Whitelisting
- Support for individual IP addresses
- CIDR notation support for IP ranges
- Automatic client IP detection (supports proxies/CDNs)

### Request Validation
- All inputs sanitized and validated
- WordPress nonce verification for admin actions
- Proper error handling with informative messages

## ✅ Test Results (v3.0.0)

**Successfully tested on opdee.com with WordPress 6.8.1, PHP 8.2.20:**

### Plugin Management Features ✅
- **Plugin Listing**: 25 plugins detected and displayed correctly
- **Update Detection**: Successfully identified 1 plugin update (Elastic Email Sender v1.2.19 → v1.2.20)
- **Plugin Installation**: Hello Dolly successfully installed from WordPress.org
- **Plugin Updates**: AltText.ai successfully updated from v1.9.95 → v1.10.0
- **API Security**: Proper 401 protection with valid API key authentication
- **Masked API Keys**: Security feature working - shows `27013065••••••••••••••••••••••••`

### Core Features ✅
- **Health Check**: API responding with version 3.0.0
- **Content Management**: All existing features operational
- **IP Whitelisting**: 202.62.150.192 successfully configured and working
- **Connection Testing**: Built-in test button functional

### Command Examples (Working)
```bash
# Plugin listing (✅ Working)
python manage_plugins.py opdee list

# Update detection (✅ Working - found 1 update)
python manage_plugins.py opdee update-all

# Plugin installation via curl (✅ Working)
curl -H "X-API-Key: YOUR_KEY" -X POST \
  "https://opdee.com/wp-json/wpbm/v1/plugins/install-url" \
  -d '{"url":"https://downloads.wordpress.org/plugin/hello-dolly.1.7.3.zip"}'
```

## 🚨 Troubleshooting

### Plugin Won't Activate
- Check PHP version (requires PHP 7.4+)
- Verify all plugin files are uploaded correctly
- Check WordPress error logs for specific errors

### API Key Issues
- Ensure API key is copied correctly (no extra spaces)
- Check IP whitelist if connection fails
- Verify the key hasn't been regenerated
- Test with the built-in "Test Connection" button
- **New**: Use the "👁️ Show" button to reveal the full key when needed

### Plugin Upload Failures
- Verify the uploaded file is a valid ZIP archive
- Check WordPress file upload permissions
- Ensure sufficient disk space
- Check plugin compatibility with your WordPress version

### Python CLI Issues
- If getting 401 errors, verify the API key in the WPBulkManager database matches the current key
- Use the `update_api_key.py` utility to update stored API keys:
  ```bash
  # Show current stored API key
  python update_api_key.py yoursite --show
  
  # Update API key
  python update_api_key.py yoursite --key "new-api-key-here"
  ```
- Use direct API calls with curl for complex operations if needed
- Check that the correct API key is being used (recent updates may require key synchronization)

### Common Error Messages
- `"Class not found"` - WordPress admin files not loaded (check plugin loading)
- `"Invalid API key"` - Key mismatch or regenerated key
- `"IP not allowed"` - IP address not in whitelist
- `"Plugin manager unavailable"` - Plugin management classes failed to load
- `"Expecting value: line 1 column 1"` - JSON parsing error, usually indicates HTML mixed in response

## 📝 Development

### Python Package Structure
```
macos-app/
├── wpbm/                               # Main package
│   ├── __init__.py                     # Package exports
│   ├── api/                            # API client
│   │   ├── client.py                   # Base API client
│   │   └── auth.py                     # Authentication handling
│   ├── operations/                     # Operation classes
│   │   ├── content.py                  # Content operations
│   │   ├── media.py                    # Media operations
│   │   └── plugins.py                  # Plugin operations
│   └── utils/                          # Utilities
│       ├── cache.py                    # Caching system
│       └── logger.py                   # Logging setup
├── manage_plugins.py                   # Plugin management CLI
├── update_api_key.py                   # API key update utility
├── example-plugins-config.json         # Example bulk install config
└── wpbm_assistant.py                   # Interactive assistant
```

### Requirements
- Python 3.8+
- WordPress 5.0+
- PHP 7.4+
- `requests` library for Python client

## 📄 License

GPL v2 or later

## 🤝 Support

For issues and feature requests, please use the GitHub repository issue tracker.