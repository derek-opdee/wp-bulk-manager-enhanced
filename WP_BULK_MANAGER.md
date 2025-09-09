# WP Bulk Manager Project Documentation

## WordPress Gutenberg Content Rules

### 🚨 CRITICAL: Preserve Gutenberg Block Structure

When updating WordPress content through WP Bulk Manager, **ALWAYS** preserve Gutenberg block structure:

#### ✅ DO:
- Preserve all Gutenberg comments: `<!-- wp:blockname -->` and `<!-- /wp:blockname -->`
- Update content only within existing blocks
- Use proper Gutenberg block syntax for new content
- Respect block attributes and JSON configuration

#### ❌ DON'T:
- Never inject raw HTML outside of Gutenberg blocks
- Never remove or modify block comment markers
- Never mix plain HTML with Gutenberg blocks
- Never update content without checking for Gutenberg structure first

#### Examples:
```html
<!-- Correct H1 Addition -->
<!-- wp:heading {"level":1} -->
<h1>Page Title</h1>
<!-- /wp:heading -->

<!-- Correct H1 to H2 Change -->
<!-- wp:heading {"level":2} -->
<h2>Section Title</h2>
<!-- /wp:heading -->

<!-- Correct Paragraph -->
<!-- wp:paragraph -->
<p>Your content here.</p>
<!-- /wp:paragraph -->
```

## Project Overview

WP Bulk Manager is a comprehensive WordPress content management system with:
- Python CLI for bulk operations
- WordPress plugin for REST API endpoints
- SEO Generator integration for dynamic content
- Support for multiple WordPress sites

## Key Components

1. **WordPress Plugin**: `/wordpress-plugin/wp-bulk-manager-client.php`
   - Provides REST API endpoints
   - Handles authentication via API keys
   - Integrates with SEO Generator plugin

2. **Python CLI**: `/macos-app/wpbm_assistant.py`
   - Interactive command-line interface
   - Bulk content management
   - CSV import/export
   - SEO optimization tools

3. **Database**: SQLite for site management
   - Stores site configurations
   - API keys in macOS Keychain
   - Connection history

## Current Sites

1. **Opdee** (opdee.com)
   - Production site
   - Full SEO Generator integration

2. **BoulderWorks** (www.boulderworks.net)
   - Location: Longmont, CO
   - Laser cutting & engraving services
   - API Key: Z5hwPL5NJzFXPslOKQCl42d84aYzrwHZ

## Alert Requirements

🚨 **MANDATORY: Always alert on task completion**
- Use clear status messages
- Include completion metrics
- Alert format: "Task completed - X items processed"