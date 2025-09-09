# WP Bulk Manager - MySQL Database Setup & Usage

## Overview
WP Bulk Manager now uses MySQL to store site configurations, API keys, access logs, content changes, templates, and branded agent kits. This provides better security, tracking, and multi-site management capabilities.

## Database Configuration

### Environment Variables
```bash
DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=opdee-bulk-manager
DB_USERNAME=root
DB_PASSWORD=VXG4qwm2zqz0ydr-jxz
```

### Initial Setup

1. **Install MySQL Connector**
```bash
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app
source venv/bin/activate
pip install mysql-connector-python
```

2. **Create Database**
```bash
python database/setup_database.py
```

This creates all necessary tables and views.

3. **Apply Updates** (if needed)
```bash
python database/apply_updates.py
```

## Database Schema

### Core Tables

#### 1. **sites** - WordPress site information
- `id` - Primary key
- `name` - Unique site identifier
- `url` - Site URL
- `description` - Site description
- `status` - active/inactive/maintenance
- `brand_voice` - Brand voice guidelines
- `brand_guidelines` - JSON brand guidelines
- `folder_path` - Local folder for site files

#### 2. **api_keys** - API key storage
- `site_id` - Reference to sites table
- `api_key` - Encrypted API key
- `key_name` - Descriptive name
- `ip_whitelist` - Allowed IP addresses
- `is_active` - Key status
- `last_used_at` - Last usage timestamp

#### 3. **access_logs** - API access tracking
- `site_id` - Reference to sites table
- `endpoint` - API endpoint accessed
- `method` - HTTP method
- `ip_address` - Client IP
- `response_code` - HTTP response code
- `response_time_ms` - Response time

#### 4. **changes** - Content modification history
- `site_id` - Reference to sites table
- `content_type` - post/page/media/plugin
- `action` - create/update/delete
- `old_value` - Previous content
- `new_value` - New content
- `change_summary` - Description

#### 5. **templates** - Reusable content templates
- `site_id` - Reference to sites table
- `template_name` - Unique template name
- `template_type` - page/post/email
- `template_content` - Template HTML/Markdown
- `template_metadata` - Variables and instructions

#### 6. **branded_agent_kit** - Brand voice & guidelines
- `site_id` - Reference to sites table
- `brand_personality` - Overall brand voice
- `tone_attributes` - JSON array of attributes
- `writing_style` - Style guidelines
- `target_audience` - Audience profiles
- `primary_keywords` - SEO keywords
- `brand_colors` - Color palette
- `tagline` - Brand tagline

## Site Management

### Adding a New Site

```python
from wpbm_manager_mysql import WPBulkManagerMySQL

manager = WPBulkManagerMySQL()

# Add site with branding
result = manager.add_site(
    name="mysite",
    url="https://mysite.com",
    api_key="your-api-key-here",
    brand_voice="Professional yet approachable, focusing on clarity and trust",
    ip_whitelist="192.168.1.0/24"
)
```

This automatically:
1. Creates database entry
2. Stores API key securely
3. Creates folder structure:
   ```
   ~/Documents/WPBulkManager/sites/mysite/
   ├── README.md
   ├── site_info.json
   ├── templates/
   │   └── basic-page.html
   ├── content/
   ├── backups/
   ├── exports/
   ├── branding/
   │   └── brand_kit.json
   └── logs/
   ```

### Folder Structure Rules

When adding a new site:
1. **Site folder** is created at `~/Documents/WPBulkManager/sites/{site_name}/`
2. **Templates** go in `{site_folder}/templates/`
3. **Brand kit** is stored in `{site_folder}/branding/brand_kit.json`
4. **Backups** are saved to `{site_folder}/backups/`
5. **Content exports** go to `{site_folder}/exports/`

### Managing Templates

1. **Add a template** to site folder:
```bash
# Create template file
echo '<!-- wp:heading -->
<h1>{title}</h1>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>{content}</p>
<!-- /wp:paragraph -->' > ~/Documents/WPBulkManager/sites/mysite/templates/simple-page.html
```

2. **Use template** to create content:
```python
manager.create_content_from_template(
    site_name="mysite",
    template_name="simple-page",
    variables={
        "title": "Welcome to Our Site",
        "content": "This is the homepage content."
    }
)
```

### Brand Voice Management

Update brand guidelines:
```python
manager.update_brand_voice("mysite", {
    "brand_voice": "Friendly and professional",
    "tone_attributes": ["helpful", "clear", "trustworthy"],
    "keywords": {
        "primary": ["web development", "wordpress"],
        "secondary": ["cms", "website management"],
        "local": ["denver", "colorado"]
    },
    "vocabulary_preferences": "Use 'you' instead of 'one', active voice",
    "vocabulary_avoid": "jargon, technical terms without explanation"
})
```

## Usage Examples

### List Sites with Details
```python
sites = manager.list_sites()
for site in sites:
    print(f"{site['name']}:")
    print(f"  URL: {site['url']}")
    print(f"  Folder: {site.get('folder_path', 'Not set')}")
    print(f"  Templates: {site.get('has_templates', False)}")
    print(f"  Brand Kit: {site.get('has_brand_kit', False)}")
```

### Get Site Information
```python
info = manager.get_site_info("mysite")
print(f"Site: {info['site']['name']}")
print(f"Total API Calls: {info['statistics']['total_api_calls']}")
print(f"Templates: {len(info['templates'])}")
print(f"Brand Voice: {info['brand_kit']['brand_voice']}")
```

### Track Changes
```python
# Get recent activity
activity = manager.get_recent_activity("mysite")
for change in activity:
    print(f"{change['created_at']}: {change['action']} {change['content_type']}")
```

### Create Backup
```python
backup = manager.backup_site_content("mysite")
print(f"Backup saved to: {backup['backup_file']}")
```

## Security Features

1. **API keys** are stored separately from site configuration
2. **IP whitelisting** restricts access to specific addresses
3. **Access logs** track all API usage
4. **Change history** provides audit trail
5. **Secure storage** in MySQL with proper indexing

## Maintenance

### View Database Status
```bash
mysql -u root -p opdee-bulk-manager -e "
SELECT 
    s.name as Site,
    COUNT(DISTINCT al.id) as 'API Calls',
    COUNT(DISTINCT c.id) as 'Changes',
    MAX(al.created_at) as 'Last Access'
FROM sites s
LEFT JOIN access_logs al ON s.id = al.site_id
LEFT JOIN changes c ON s.id = c.site_id
GROUP BY s.id;"
```

### Clean Old Logs
```sql
-- Remove access logs older than 30 days
DELETE FROM access_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Archive old changes
INSERT INTO changes_archive SELECT * FROM changes WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM changes WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

## Troubleshooting

### Connection Issues
1. Check MySQL is running: `mysql.server status`
2. Verify credentials in `config/database.json`
3. Test connection: `mysql -h localhost -u root -p`

### Permission Errors
```bash
# Grant permissions
mysql -u root -p -e "
GRANT ALL PRIVILEGES ON \`opdee-bulk-manager\`.* TO 'root'@'localhost';
FLUSH PRIVILEGES;"
```

### Reset Database
```bash
python database/setup_database.py --drop-existing
```

## Integration with WP Bulk Manager

The MySQL database integrates seamlessly with the existing WP Bulk Manager:

1. **Site credentials** are fetched from MySQL instead of SQLite
2. **Templates** are loaded from the site's folder structure
3. **Brand voice** is applied to content generation
4. **All operations** are logged for tracking
5. **Backups** are stored in organized folders

This provides a complete content management system with proper organization, security, and tracking.