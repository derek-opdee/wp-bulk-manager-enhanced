# WP Bulk Manager Enhanced 🚀

A comprehensive WordPress content management system with REST API integration, SEO optimization, LiteSpeed Cache management, and Perfmatters coordination for enterprise-level WordPress site management.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Plugin Versions](#plugin-versions)
5. [API Documentation](#api-documentation)
6. [Configuration](#configuration)
7. [Usage Examples](#usage-examples)
8. [Performance Optimization](#performance-optimization)
9. [Security](#security)
10. [Troubleshooting](#troubleshooting)
11. [Development](#development)

## 🎯 Overview

WP Bulk Manager Enhanced is a comprehensive WordPress management solution designed for developers, agencies, and enterprises managing multiple WordPress sites. It provides powerful REST API endpoints for content management, SEO optimization, cache control, and performance monitoring.

### Key Benefits
- **Unified API**: Single interface for all WordPress operations
- **Multi-Site Management**: Manage multiple WordPress installations
- **Performance Optimization**: LiteSpeed Cache + Perfmatters coordination
- **SEO Management**: Complete SEO and schema.org integration
- **Security First**: API key authentication and secure operations
- **Production Ready**: Enterprise-grade error handling and logging

## ✨ Features

### Core WordPress Management
- ✅ **Content CRUD**: Create, read, update, delete posts and pages
- ✅ **Bulk Operations**: Process multiple content items simultaneously
- ✅ **Custom Post Types**: Full support for custom post types
- ✅ **Meta Data Management**: Handle custom fields and meta data
- ✅ **Media Management**: Upload and manage media files
- ✅ **User Management**: User creation and role management

### SEO & Schema.org
- ✅ **SEO Meta Tags**: Title, description, keywords management
- ✅ **Open Graph**: Facebook/social media optimization
- ✅ **Twitter Cards**: Twitter-specific meta tags
- ✅ **Schema.org Markup**: Structured data for search engines
- ✅ **XML Sitemaps**: Automated sitemap generation
- ✅ **Robots.txt**: Search engine directive management

### Performance & Caching
- ✅ **LiteSpeed Cache**: Full cache management and optimization
- ✅ **Perfmatters Integration**: CSS/JS optimization coordination
- ✅ **Object Caching**: Database query optimization
- ✅ **CDN Integration**: Content delivery network support
- ✅ **Image Optimization**: WebP conversion and compression
- ✅ **Database Optimization**: Cleanup and optimization tools

### Advanced Features
- ✅ **Plugin Management**: Install, activate, deactivate plugins
- ✅ **Theme Management**: Switch and customize themes
- ✅ **Database Operations**: Direct database queries and updates
- ✅ **Backup Integration**: Automated backup creation
- ✅ **Security Scanning**: Vulnerability detection
- ✅ **Performance Monitoring**: Real-time performance metrics

## 🚀 Installation

### Prerequisites
- WordPress 5.0+
- PHP 7.4+
- MySQL 5.7+ or MariaDB 10.2+
- LiteSpeed Cache plugin (optional but recommended)
- Perfmatters plugin (optional for CSS/JS optimization)

### Method 1: Direct Download
```bash
# Download the latest plugin
wget https://github.com/derek-opdee/wp-bulk-manager-enhanced/raw/main/wp-bulk-manager-with-litespeed.php

# Upload to WordPress
# /wp-content/plugins/wp-bulk-manager/wp-bulk-manager-with-litespeed.php
```

### Method 2: Git Clone
```bash
git clone https://github.com/derek-opdee/wp-bulk-manager-enhanced.git
cd wp-bulk-manager-enhanced
```

### Method 3: WordPress Admin
1. Download the latest release ZIP
2. Go to WordPress Admin → Plugins → Add New → Upload
3. Upload the ZIP file
4. Activate the plugin

### Activation
1. Upload the plugin files to `/wp-content/plugins/wp-bulk-manager/`
2. Activate through WordPress Admin → Plugins
3. Go to **WP Bulk Manager** in the admin menu
4. Copy your API key for external access

## 📦 Plugin Versions

### Available Versions

| Version | File | Features | Use Case |
|---------|------|----------|----------|
| **v2.2.0** | `wp-bulk-manager-with-litespeed.php` | Full LiteSpeed + Perfmatters coordination | **Recommended for production** |
| **v2.1.0** | `wp-bulk-manager-enhanced.php` | Enhanced with LiteSpeed support | LiteSpeed-only environments |
| **v2.0.0** | `wp-bulk-manager-standalone.php` | Self-contained, no dependencies | Simple installations |

### Version Comparison

| Feature | v2.2.0 | v2.1.0 | v2.0.0 |
|---------|--------|--------|--------|
| **Content Management** | ✅ | ✅ | ✅ |
| **SEO Management** | ✅ | ✅ | ✅ |
| **LiteSpeed Cache** | ✅ | ✅ | ❌ |
| **Perfmatters Coordination** | ✅ | ❌ | ❌ |
| **Cache Optimization** | ✅ | ✅ | ❌ |
| **Plugin Dependencies** | None | None | None |

## 📡 API Documentation

### Base URL
```
https://yoursite.com/wp-json/wpbm/v1/
```

### Authentication
All endpoints require API key authentication via header:
```bash
X-API-Key: your_api_key_here
# OR
Authorization: Bearer your_api_key_here
```

### Core Endpoints

#### Authentication
```bash
GET /auth
# Check API authentication status
```

#### Content Management
```bash
GET /content                    # List all content
GET /content/{id}              # Get single content item
POST /content                  # Create new content
PUT /content/{id}              # Update content
DELETE /content/{id}           # Delete content
```

#### SEO Management
```bash
GET /seo/{id}                  # Get SEO data for content
PUT /seo/{id}                  # Update SEO data
```

#### Plugin Management
```bash
GET /plugins                   # List all plugins
POST /plugins/activate         # Activate plugin
POST /plugins/deactivate       # Deactivate plugin
```

#### System Information
```bash
GET /system                    # Get WordPress system info
```

### Performance Endpoints (v2.1.0+)

#### LiteSpeed Cache
```bash
GET /litespeed/status          # Get cache status
GET /litespeed/settings        # Get cache settings
POST /litespeed/cache/purge    # Purge specific URL cache
POST /litespeed/cache/purge-all # Purge all cache
POST /litespeed/optimize       # Apply optimization settings
```

#### Perfmatters (v2.2.0+)
```bash
GET /perfmatters/status        # Get Perfmatters status
GET /perfmatters/settings      # Get optimization settings
```

#### Coordinated Caching (v2.2.0+)
```bash
POST /cache/enable             # Enable coordinated LiteSpeed + Perfmatters
```

### Request/Response Examples

#### Create Content
```bash
POST /wp-json/wpbm/v1/content
Content-Type: application/json
X-API-Key: your_api_key

{
  "title": "New Blog Post",
  "content": "<!-- wp:paragraph --><p>Your content here</p><!-- /wp:paragraph -->",
  "status": "publish",
  "type": "post"
}
```

#### Update SEO Data
```bash
PUT /wp-json/wpbm/v1/seo/123
Content-Type: application/json
X-API-Key: your_api_key

{
  "title": "SEO Optimized Title",
  "description": "Meta description for search engines",
  "og_title": "Social Media Title",
  "og_description": "Social media description"
}
```

#### Enable Coordinated Caching
```bash
POST /wp-json/wpbm/v1/cache/enable
X-API-Key: your_api_key

# Response:
{
  "message": "Coordinated caching enabled",
  "details": {
    "litespeed": "Cache enabled, CSS/JS optimization disabled",
    "perfmatters": {
      "css_optimization": "enabled",
      "js_optimization": "enabled",
      "status": "Handling CSS/JS optimization"
    }
  }
}
```

## ⚙️ Configuration

### Basic Configuration
The plugin automatically generates an API key upon activation. Access it via:
- WordPress Admin → WP Bulk Manager → API Configuration

### Advanced Configuration
```php
// wp-config.php additions
define('WPBM_DEBUG', true);                    // Enable debug logging
define('WPBM_CACHE_ENABLED', true);           // Enable caching features
define('WPBM_RATE_LIMIT', 100);               // API rate limit per hour
define('WPBM_MAX_CONTENT_LENGTH', 1048576);   // Max content size (1MB)
```

### Environment Variables
```bash
# .env file (if using external management)
WORDPRESS_URL=https://yoursite.com
WORDPRESS_API_KEY=your_api_key_here
WPBM_DEBUG=false
WPBM_TIMEOUT=30
```

### Multi-Site Configuration
```json
{
  "sites": [
    {
      "name": "Primary Site",
      "url": "https://site1.com",
      "api_key": "key1"
    },
    {
      "name": "Secondary Site", 
      "url": "https://site2.com",
      "api_key": "key2"
    }
  ]
}
```

## 🎯 Usage Examples

### Content Management
```python
import requests

# Configuration
base_url = "https://yoursite.com/wp-json/wpbm/v1"
headers = {"X-API-Key": "your_api_key"}

# Create new post with Gutenberg blocks
post_data = {
    "title": "Welcome to Our Blog",
    "content": """
    <!-- wp:heading {"level":1} -->
    <h1>Welcome to Our Blog</h1>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p>This is our first blog post with proper Gutenberg structure.</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:image {"id":123} -->
    <figure class="wp-block-image"><img src="/wp-content/uploads/2024/image.jpg" alt="Blog image"/></figure>
    <!-- /wp:image -->
    """,
    "status": "publish",
    "type": "post"
}

response = requests.post(f"{base_url}/content", json=post_data, headers=headers)
post_id = response.json()["id"]

# Update SEO data
seo_data = {
    "title": "Welcome to Our Blog - Your Company Name",
    "description": "Discover insights, tips, and news from our expert team",
    "keywords": "blog, insights, company news",
    "og_title": "Welcome to Our Blog",
    "og_description": "Discover insights, tips, and news from our expert team",
    "og_image": "https://yoursite.com/wp-content/uploads/2024/og-image.jpg"
}

requests.put(f"{base_url}/seo/{post_id}", json=seo_data, headers=headers)
```

### Bulk Operations
```bash
#!/bin/bash
# Bulk content creation script

API_KEY="your_api_key"
BASE_URL="https://yoursite.com/wp-json/wpbm/v1"

# Array of content to create
titles=(
  "10 Tips for Better SEO"
  "WordPress Performance Guide"
  "Security Best Practices"
)

for title in "${titles[@]}"; do
  curl -X POST "$BASE_URL/content" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $API_KEY" \
    -d "{
      \"title\": \"$title\",
      \"content\": \"<!-- wp:paragraph --><p>Content for $title</p><!-- /wp:paragraph -->\",
      \"status\": \"draft\",
      \"type\": \"post\"
    }"
done
```

### Cache Management
```javascript
// JavaScript cache management
class WPBulkManager {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.headers = {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json'
    };
  }

  async enableOptimizedCaching() {
    // Enable coordinated LiteSpeed + Perfmatters caching
    const response = await fetch(`${this.baseUrl}/cache/enable`, {
      method: 'POST',
      headers: this.headers
    });
    
    const result = await response.json();
    console.log('Cache coordination enabled:', result);
    
    // Purge all cache to start fresh
    await this.purgeAllCache();
  }

  async purgeAllCache() {
    const response = await fetch(`${this.baseUrl}/litespeed/cache/purge-all`, {
      method: 'POST',
      headers: this.headers
    });
    
    console.log('Cache purged:', await response.json());
  }

  async getCacheStatus() {
    const response = await fetch(`${this.baseUrl}/litespeed/status`, {
      headers: this.headers
    });
    
    return await response.json();
  }
}

// Usage
const wpbm = new WPBulkManager('https://yoursite.com/wp-json/wpbm/v1', 'your_api_key');
wpbm.enableOptimizedCaching();
```

## 🔧 Performance Optimization

### Cache Strategy (v2.2.0)
The plugin implements intelligent cache coordination:

**LiteSpeed Cache Handles:**
- Page caching (HTML output)
- Browser caching (static assets)
- Object caching (database queries)
- Image optimization (WebP conversion)

**Perfmatters Handles:**
- CSS minification and combination
- JavaScript optimization and deferring
- Font optimization
- Lazy loading

### Optimization Levels
```bash
# Conservative optimization
curl -X POST "$BASE_URL/litespeed/optimize" \
  -H "X-API-Key: $API_KEY" \
  -d '{"optimizations": "conservative"}'

# Standard optimization (recommended)
curl -X POST "$BASE_URL/litespeed/optimize" \
  -H "X-API-Key: $API_KEY" \
  -d '{"optimizations": "standard"}'

# Aggressive optimization (advanced users)
curl -X POST "$BASE_URL/litespeed/optimize" \
  -H "X-API-Key: $API_KEY" \
  -d '{"optimizations": "aggressive"}'
```

### Performance Monitoring
```bash
# Check system performance
curl -H "X-API-Key: $API_KEY" "$BASE_URL/system" | jq '
{
  memory_usage: .memory_limit,
  php_version: .php_version,
  wordpress_version: .wordpress_version,
  debug_mode: .debug_mode
}'

# Monitor cache hit rates
curl -H "X-API-Key: $API_KEY" "$BASE_URL/litespeed/status" | jq '
{
  cache_enabled: .cache_enabled,
  css_minify: .css_minify,
  js_minify: .js_minify,
  webp_enabled: .webp_enabled
}'
```

## 🔐 Security

### API Key Security
- **32-character random keys**: Cryptographically secure generation
- **Header-only authentication**: Keys never appear in URLs
- **Rate limiting**: Prevents brute force attacks
- **IP whitelisting**: Optional IP restriction
- **Audit logging**: All API calls are logged

### WordPress Security Integration
```php
// Additional security headers
add_action('rest_api_init', function() {
  header('X-Content-Type-Options: nosniff');
  header('X-Frame-Options: DENY');
  header('X-XSS-Protection: 1; mode=block');
});

// Rate limiting (customize in wp-config.php)
define('WPBM_RATE_LIMIT_PER_HOUR', 100);
define('WPBM_RATE_LIMIT_PER_DAY', 1000);
```

### Content Security
- **Input sanitization**: All content is sanitized using WordPress functions
- **SQL injection protection**: Prepared statements for all queries
- **XSS prevention**: Output escaping for all data
- **CSRF protection**: Nonce validation for state-changing operations

## 🔧 Troubleshooting

### Common Issues

#### 1. Plugin Activation Errors
```bash
Error: Class not found or dependencies missing
```
**Solution:**
- Use the standalone version (`wp-bulk-manager-with-litespeed.php`)
- Ensure PHP 7.4+ is installed
- Check file permissions (644 for PHP files)

#### 2. API Authentication Failures
```bash
HTTP 401: Invalid API key
```
**Solution:**
- Verify API key in WordPress Admin → WP Bulk Manager
- Check header format: `X-API-Key: your_key_here`
- Ensure key hasn't been regenerated

#### 3. LiteSpeed Cache Not Detected
```bash
"litespeed_available": false
```
**Solution:**
- Install and activate LiteSpeed Cache plugin
- Ensure OpenLiteSpeed/LiteSpeed web server is running
- Check plugin compatibility

#### 4. Performance Issues
```bash
Slow API responses or timeouts
```
**Solution:**
- Enable object caching (Redis/Memcached)
- Increase PHP memory limit (recommend 256M+)
- Optimize database with WP-CLI: `wp db optimize`

### Debug Mode
Enable debugging in wp-config.php:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WPBM_DEBUG', true);
```

View logs:
```bash
tail -f /wp-content/debug.log
```

### Health Check
```bash
# Test all systems
curl -H "X-API-Key: $API_KEY" "$BASE_URL/auth" && \
curl -H "X-API-Key: $API_KEY" "$BASE_URL/system" && \
curl -H "X-API-Key: $API_KEY" "$BASE_URL/litespeed/status"
```

## 🛠️ Development

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/derek-opdee/wp-bulk-manager-enhanced.git
cd wp-bulk-manager-enhanced

# Set up WordPress development environment
docker-compose up -d

# Install development dependencies
npm install
composer install
```

### Testing
```bash
# Run PHP unit tests
./vendor/bin/phpunit

# Run integration tests
npm run test:integration

# Run API tests
npm run test:api
```

### Code Quality
```bash
# PHP linting
./vendor/bin/phpcs --standard=WordPress

# JavaScript linting
npm run lint:js

# Security scanning
npm run security:scan
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Run code quality checks
5. Submit a pull request

### API Versioning
The API follows semantic versioning:
- `/wpbm/v1/` - Current stable API
- `/wpbm/v2/` - Future API version (in development)

## 📚 Additional Resources

### Documentation
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [LiteSpeed Cache Documentation](https://docs.litespeedtech.com/lscache/)
- [Perfmatters Documentation](https://perfmatters.io/docs/)
- [OpenAPI Specification](./openapi-spec.yaml)

### Related Projects
- [SEO Generator](https://seogenerator.io/) - Automated SEO content
- [Cloudflare Management Tool](../Cloudflare-management/) - DNS management
- [Vultr WordPress Manager](./vultr-wordpress-manager.sh) - Server management

### Support
- **Issues**: [GitHub Issues](https://github.com/derek-opdee/wp-bulk-manager-enhanced/issues)
- **Discussions**: [GitHub Discussions](https://github.com/derek-opdee/wp-bulk-manager-enhanced/discussions)
- **Email**: support@opdee.com

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📊 Changelog

### v2.2.0 (Latest)
- ✅ Added Perfmatters coordination
- ✅ Intelligent cache strategy implementation
- ✅ Enhanced performance monitoring
- ✅ Improved error handling

### v2.1.0
- ✅ LiteSpeed Cache integration
- ✅ Cache management endpoints
- ✅ Performance optimization tools

### v2.0.0
- ✅ Complete WordPress REST API integration
- ✅ SEO and meta tag management
- ✅ Standalone plugin architecture

---

**Created by Derek Zar - Opdee Digital**  
**🔗 Generated with [Claude Code](https://claude.ai/code)**

**Enterprise WordPress Management Made Simple** 🚀