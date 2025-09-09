# WP Bulk Manager - Comprehensive WordPress Management System

A two-part system for managing multiple WordPress sites from your Mac, with support for bulk content creation, SEO optimization, and integration with The SEO Framework.

## System Components

### 1. WordPress Client Plugin (`wordpress-plugin/`)
A lightweight plugin installed on each customer's WordPress site that provides:
- Secure REST API endpoints
- The SEO Framework integration
- Content management capabilities
- Minimal footprint

### 2. macOS Management Application (`macos-app/`)
A desktop application that runs on your Mac for central management:
- Secure credential storage using macOS Keychain
- Bulk content creation with dynamic variables
- SEO meta management
- Multi-site dashboard

## Installation

### Step 1: Install WordPress Plugin on Customer Sites

1. Upload `wordpress-plugin/wp-bulk-manager-client.php` to the customer's `/wp-content/plugins/` directory
2. Activate the plugin through WordPress admin
3. Go to **Settings → Bulk Manager**
4. Generate and copy the API key

### Step 2: Set Up macOS Application

1. Install Python 3.8+ on your Mac
2. Navigate to the `macos-app` directory:
   ```bash
   cd /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Make scripts executable:
   ```bash
   chmod +x wpbm_manager.py wpbm_gui.py
   ```

## Usage

### Command Line Interface

Add a new site:
```bash
./wpbm_manager.py add-site "Customer Site" "https://customer.com" "API_KEY_HERE"
```

List all sites:
```bash
./wpbm_manager.py list-sites
```

Create content:
```bash
./wpbm_manager.py create-content --sites 1 2 3 --title "Test Page" --content "<p>Content here</p>" --type page
```

### Graphical Interface

Launch the GUI application:
```bash
./wpbm_gui.py
```

## Features

### Dynamic Content Variables

SEO Generator Pages use square bracket syntax:
- `[search_term]` - Singular form of the search term
- `[search_terms]` - Plural form of the search term  
- `[location]` - The location name

Legacy bulk create uses curly brace syntax:
- `{location}` - Location name
- `{service}` - Service name (singular)
- `{service_plural}` - Service name (plural)
- Modifiers: `{location|upper}`, `{service|capitalize}`, etc.

### Dynamic Field Best Practices

#### 1. Grammar Considerations

**Use [search_term] for:**
- Singular references: "Our [search_term] helps..."
- Service names: "Professional [search_term] in [location]"
- Adjectives: "[search_term]-powered solutions"

**Use [search_terms] for:**
- Plural references: "We offer [search_terms]"
- Multiple services: "Our [search_terms] include..."

**Avoid:**
- Double dynamic fields: ❌ "[search_term] & [search_term]"
- Awkward plurals: ❌ "build [search_term]s that" 
- Instead use: ✅ "build [search_term] solutions that"

#### 2. Natural Language Flow

**Good Examples:**
```
✅ "Expert [search_term] services in [location]"
✅ "Transform your [location] business with [search_term]"
✅ "Our [location] team specializes in [search_term]"
```

**Poor Examples:**
```
❌ "[search_term]s so natural" (awkward with "Services")
❌ "We create [search_term]s" (double plural)
❌ "[search_term] [search_term] solutions" (repetitive)
```

#### 3. Handling Search Terms with "Services"

When your search terms include "Services" (e.g., "AI Web Development Services"):
- Don't add extra "services": ❌ "AI Web Development Services services"
- Use "solutions" instead: ✅ "AI Web Development Services solutions"
- Or rephrase: ✅ "Our AI Web Development Services help..."

#### 4. Location Integration

**Effective location usage:**
- Opening: "Leading [search_term] provider in [location]"
- Benefits: "Help [location] businesses grow"
- Team: "Our [location]-based experts"
- Service area: "Serving [location] and surrounding areas"

**Distribution:**
- Include location 3-5 times per page
- Use in H1, H2 headings
- Include in opening and closing paragraphs
- Add to CTAs: "Get a free [location] consultation"

#### 5. Testing Your Content

Before publishing, test with various search terms:
- Single word: "AI Integration"
- With "Services": "AI Development Services"
- Multiple words: "AI Stack Development"
- Technical terms: "AI API Integration"

#### 6. Common Patterns to Use

**Headlines:**
- "Expert [search_term] in [location] | Your Business"
- "[location]'s Leading [search_term] Provider"
- "Professional [search_term] for [location] Businesses"

**Body Content:**
- "We provide [search_term] solutions that..."
- "Our [search_term] services help [location] businesses..."
- "Transform your operations with our [search_term]"

**CTAs:**
- "Get [search_term] Quote in [location]"
- "Start Your [search_term] Project Today"
- "Contact Our [location] [search_term] Experts"

### Spintax Support

Create variations using spintax:
```
{Welcome to|Visit|Discover} our {amazing|fantastic} {service} in {location}!
```

### The SEO Framework Integration

The plugin automatically detects and integrates with The SEO Framework:
- Updates meta titles and descriptions
- Manages robots meta (noindex, nofollow, noarchive)
- Sets canonical URLs
- Uses TSF's filters for custom content

### Bulk Operations

- Create hundreds of location/service pages
- Update SEO meta across all sites
- Manage plugins and themes
- Monitor site status

## Security

### macOS App
- API keys stored in macOS Keychain (never in plain text)
- SSL/TLS for all communications
- Request validation

### WordPress Plugin
- API key authentication
- Capability checks
- Optional IP whitelisting
- No database tables (uses native WordPress structure)

## API Reference

### Authentication
All requests require `X-API-Key` header

### Endpoints

#### Create Content
```
POST /wp-json/wpbm/v1/content
{
    "title": "Page Title",
    "content": "Page content with {variables}",
    "type": "page",
    "status": "draft",
    "seo": {
        "title": "SEO Title",
        "description": "SEO Description"
    }
}
```

#### Update SEO
```
PUT /wp-json/wpbm/v1/seo/{post_id}
{
    "title": "New SEO Title",
    "description": "New SEO Description",
    "noindex": false,
    "nofollow": false
}
```

#### Get Site Status
```
GET /wp-json/wpbm/v1/status
```

## Troubleshooting

### Connection Issues
1. Verify the API key is correct
2. Check if the plugin is activated
3. Ensure REST API is accessible
4. Test with: `curl -H "X-API-Key: YOUR_KEY" https://site.com/wp-json/wpbm/v1/status`

### The SEO Framework Not Working
1. Ensure The SEO Framework plugin is installed and activated
2. Check WordPress admin for any conflicts
3. Verify meta fields are being saved

### macOS Keychain Access
If prompted for keychain access, always click "Allow" to let the app store API keys securely.

## Examples

### Creating Location-Based Service Pages

Template:
```html
<h1>{service|capitalize} in {location}</h1>
<p>Looking for {service} in {location}? We provide professional {service_plural} with experienced technicians.</p>
```

Variables:
- Locations: Brisbane, Sydney, Melbourne
- Services: painting service, plumbing service

Result: Creates unique pages for each location/service combination

## Support

For issues or feature requests, contact Derek at derekzar.com

## License

GPL v2 or later

## Credits

Developed by Derek for efficient WordPress site management at scale.