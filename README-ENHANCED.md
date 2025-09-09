# WP Bulk Manager Enhanced - Complete Documentation

## 🚀 Overview

WP Bulk Manager Enhanced is a comprehensive WordPress management system that provides enterprise-level control over multiple WordPress sites. It includes SEO management, Schema.org implementation, LiteSpeed Cache optimization, and optional Vultr server integration.

## 📋 Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [API Documentation](#api-documentation)
7. [SEO Management](#seo-management)
8. [Schema.org Management](#schemaorg-management)
9. [LiteSpeed Cache Management](#litespeed-cache-management)
10. [Vultr Integration (Optional)](#vultr-integration-optional)
11. [Security](#security)
12. [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features
- **Bulk Content Management**: Create, update, delete multiple posts/pages
- **SEO Optimization**: Comprehensive SEO meta management
- **Schema.org**: Full structured data implementation
- **Plugin Management**: Install, update, activate/deactivate plugins remotely
- **Performance Monitoring**: Track and optimize site performance
- **LiteSpeed Cache**: Full control over OpenLiteSpeed/LiteSpeed Cache settings

### Optional Features
- **Vultr Server Management**: Manage WordPress on Vultr servers
- **Visual Regression Testing**: Track visual changes
- **Automated Backups**: Schedule and manage backups

## 🏗️ Architecture

```
WP Bulk Manager Enhanced/
├── WordPress Plugin (wp-bulk-manager-enhanced.php)
│   ├── REST API Endpoints
│   ├── SEO Manager
│   ├── Schema Manager
│   └── LiteSpeed Manager
├── macOS Management App (Python)
│   ├── wpbm_cli_enhanced.py
│   ├── wpbm_manager.py
│   └── site_connections.db
├── OpenAPI Specification (openapi-spec.yaml)
└── Optional Integrations
    ├── vultr-wordpress-manager.sh
    └── openlitespeed-optimizer.sh
```

### Contract-Driven Development (CDD)

This system follows CDD principles with a complete OpenAPI 3.1 specification. All endpoints are documented and validated against the contract.

## 📦 Installation

### 1. Install WordPress Plugin

```bash
# On each WordPress site
cd /path/to/wordpress/wp-content/plugins/
wget https://github.com/opdee/wp-bulk-manager/releases/latest/wp-bulk-manager-enhanced.zip
unzip wp-bulk-manager-enhanced.zip
wp plugin activate wp-bulk-manager-enhanced
```

### 2. Setup Management System

```bash
# Clone repository
git clone https://github.com/opdee/wp-bulk-manager.git
cd wp-bulk-manager

# Install Python dependencies
cd macos-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Generate API Keys

```bash
# On WordPress site
wp option get wpbm_api_key

# Or generate new one
wp eval 'echo wp_generate_password(32, false);' | wp option update wpbm_api_key --stdin
```

## ⚙️ Configuration

### WordPress Plugin Configuration

1. Navigate to **WP Bulk Manager** in WordPress admin
2. Generate or view API key
3. Configure allowed IP addresses (optional)
4. Enable/disable features:
   - SEO Management
   - Schema.org
   - LiteSpeed Cache
   - Performance Monitoring

### Management App Configuration

Edit `macos-app/config.json`:

```json
{
  "sites": [
    {
      "name": "Opdee",
      "url": "https://opdee.com",
      "api_key": "YOUR_API_KEY_HERE"
    }
  ],
  "features": {
    "seo": true,
    "schema": true,
    "litespeed": true,
    "vultr": false
  }
}
```

## 📖 Usage Guide

### Using the Python CLI

```bash
cd macos-app
source venv/bin/activate

# Interactive mode
python3 wpbm_cli_enhanced.py

# Direct commands
python3 wpbm_cli_enhanced.py --site opdee.com --action list-content
python3 wpbm_cli_enhanced.py --site opdee.com --action update-seo --post-id 123
```

### Using Shell Scripts

```bash
# WordPress site management
./wordpress-site-manager.sh

# OpenLiteSpeed optimization
./openlitespeed-optimizer.sh

# Vultr integration (optional)
./vultr-wordpress-manager.sh
```

## 📡 API Documentation

### Authentication

All API requests require authentication via API key:

```bash
# Header authentication
curl -H "X-API-Key: YOUR_API_KEY" https://site.com/wp-json/wpbm/v1/content

# Bearer token
curl -H "Authorization: Bearer YOUR_API_KEY" https://site.com/wp-json/wpbm/v1/content
```

### Key Endpoints

#### Content Management
- `GET /wpbm/v1/content` - List all content
- `POST /wpbm/v1/content` - Create content
- `GET /wpbm/v1/content/{id}` - Get specific content
- `PUT /wpbm/v1/content/{id}` - Update content
- `DELETE /wpbm/v1/content/{id}` - Delete content

#### SEO Management
- `GET /wpbm/v1/seo/{id}` - Get SEO data
- `PUT /wpbm/v1/seo/{id}` - Update SEO data
- `POST /wpbm/v1/seo/bulk` - Bulk SEO update

#### Schema.org
- `GET /wpbm/v1/schema/{id}` - Get schema data
- `PUT /wpbm/v1/schema/{id}` - Update schema data

#### Plugin Management
- `GET /wpbm/v1/plugins` - List plugins
- `POST /wpbm/v1/plugins` - Install plugin
- `PUT /wpbm/v1/plugins/{slug}` - Update plugin
- `DELETE /wpbm/v1/plugins/{slug}` - Delete plugin

### Example API Calls

```bash
# List all pages
curl -H "X-API-Key: YOUR_KEY" \
  "https://site.com/wp-json/wpbm/v1/content?post_type=page"

# Update SEO data
curl -X PUT \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New SEO Title",
    "description": "Meta description",
    "focus_keyword": "main keyword"
  }' \
  "https://site.com/wp-json/wpbm/v1/seo/123"

# Bulk create content
curl -X POST \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": {
      "title": "Service in {location}",
      "content": "We provide services in {location}...",
      "type": "page",
      "status": "draft"
    },
    "variables": [
      {"location": "Melbourne"},
      {"location": "Sydney"},
      {"location": "Brisbane"}
    ]
  }' \
  "https://site.com/wp-json/wpbm/v1/bulk/content"
```

## 🔍 SEO Management

### Features
- **Meta Tags**: Title, description, canonical URLs
- **Open Graph**: Facebook/social media optimization
- **Twitter Cards**: Twitter-specific meta data
- **Robots**: Control indexing and following
- **Breadcrumbs**: Structured navigation
- **Focus Keywords**: SEO keyword targeting

### Usage

```python
# Python example
from wpbm_manager import WPBMManager

manager = WPBMManager(site_url, api_key)

# Update SEO for a page
manager.update_seo(
    post_id=123,
    title="Professional Services in Melbourne",
    description="Leading digital agency...",
    focus_keyword="digital agency Melbourne",
    og_image="https://site.com/image.jpg"
)

# Bulk SEO update
updates = [
    {"id": 1, "title": "Page 1 Title"},
    {"id": 2, "title": "Page 2 Title"},
]
manager.bulk_update_seo(updates)
```

## 🏗️ Schema.org Management

### Supported Schema Types
- Article
- Product
- Service
- LocalBusiness
- Organization
- Person
- Event
- FAQ
- HowTo

### Implementation

```python
# Add LocalBusiness schema
schema_data = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Opdee Digital",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "123 Main St",
        "addressLocality": "Frankston",
        "addressRegion": "VIC",
        "postalCode": "3199",
        "addressCountry": "AU"
    },
    "telephone": "+61-XXX-XXX-XXX",
    "openingHours": "Mo-Fr 09:00-17:30"
}

manager.update_schema(post_id=123, schema_type="LocalBusiness", data=schema_data)
```

## ⚡ LiteSpeed Cache Management

### Configuration Options

```bash
# Using the shell script
./openlitespeed-optimizer.sh

# Options:
# 1. Complete optimization
# 2. Configure cache only
# 3. Configure image optimization
# 4. Configure CSS/JS optimization
# 5. Configure database optimization
# 6. Configure object cache (Redis)
# 7. Configure crawler
# 8. Configure Cloudflare integration
```

### Programmatic Control

```python
# Configure LiteSpeed via API
litespeed_settings = {
    "cache": {
        "enabled": True,
        "browser": True,
        "mobile": True,
        "ttl_public": 604800,  # 7 days
        "ttl_private": 1800     # 30 minutes
    },
    "optimization": {
        "css_minify": True,
        "css_combine": True,
        "js_minify": True,
        "js_combine": True,
        "lazy_load": True,
        "webp": True
    }
}

manager.update_litespeed_settings(litespeed_settings)
```

## 🌐 Vultr Integration (Optional)

### When to Use
- Sites hosted on Vultr servers
- Need server-level management
- Want automated deployments
- Require server monitoring

### Setup

```bash
# Install Vultr CLI
brew install vultr/vultr-cli/vultr

# Configure API key
export VULTR_API_KEY="your_vultr_api_key"

# Run manager
./vultr-wordpress-manager.sh
```

### Features
- Create WordPress-optimized servers
- Deploy WordPress automatically
- Configure OpenLiteSpeed
- Bulk server management
- Automated backups to Vultr Object Storage
- Security scanning
- Performance optimization

### Usage Examples

```bash
# List all Vultr servers
./vultr-wordpress-manager.sh
# Select option 1

# Deploy WordPress to server
./vultr-wordpress-manager.sh
# Select option 6
# Enter server IP and domain

# Bulk update all WordPress sites
./vultr-wordpress-manager.sh
# Select option 10
# Choose "Update WordPress on all servers"
```

## 🔒 Security

### API Security
- API keys are hashed and stored securely
- Optional IP whitelisting
- Rate limiting on endpoints
- HTTPS required for all API calls

### WordPress Security
- Automatic security scanning
- File integrity checks
- Malware detection (ClamAV)
- Suspicious file detection
- Permission auditing

### Server Security (Vultr Integration)
- Fail2ban configuration
- Firewall rules
- SSH key authentication only
- Regular security updates

## 🔧 Troubleshooting

### Common Issues

#### API Connection Failed
```bash
# Check API key
wp option get wpbm_api_key

# Test connection
curl -H "X-API-Key: YOUR_KEY" https://site.com/wp-json/wpbm/v1/auth
```

#### LiteSpeed Cache Not Working
```bash
# Check if plugin is active
wp plugin is-active litespeed-cache

# Verify cache headers
curl -I https://site.com | grep -i "x-litespeed-cache"
```

#### Vultr CLI Not Found
```bash
# Install on macOS
brew install vultr/vultr-cli/vultr

# Install on Linux
curl -L https://github.com/vultr/vultr-cli/releases/latest/download/vultr_Linux_x86_64.tar.gz | tar xz
sudo mv vultr /usr/local/bin/
```

### Debug Mode

Enable debug logging:

```php
// In wp-config.php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WPBM_DEBUG', true);
```

Check logs:
```bash
tail -f /path/to/wordpress/wp-content/debug.log
```

## 📚 Additional Resources

- **OpenAPI Specification**: `/openapi-spec.yaml`
- **Python SDK Documentation**: `/macos-app/README.md`
- **WordPress Plugin Docs**: `/wordpress-plugin/README.md`
- **Video Tutorials**: [Coming Soon]
- **Support**: info@opdee.com

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

GPL v2 or later - see LICENSE file for details

## 👨‍💻 Author

**Derek Zar - Opdee Digital**
- Website: https://opdee.com
- Email: derek@opdee.com
- Location: Frankston, Victoria, Australia

---

*Built with ❤️ for the WordPress community*