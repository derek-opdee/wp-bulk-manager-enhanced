=== WP Bulk Manager Client ===
Contributors: derekzar
Tags: bulk management, content management, seo, api, remote management
Requires at least: 5.0
Tested up to: 6.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html

Lightweight client plugin for WP Bulk Manager - enables secure remote management of your WordPress site.

== Description ==

WP Bulk Manager Client is a lightweight plugin that allows you to manage your WordPress site remotely using the WP Bulk Manager macOS application. It provides secure REST API endpoints for content management, SEO updates, and site monitoring.

= Features =

* Secure API authentication
* Content creation and updates via REST API
* The SEO Framework integration
* Bulk operations support
* Minimal performance impact
* No database tables required

= Security =

* API key authentication
* Optional IP whitelisting
* WordPress capability checks
* SSL/TLS required

== Installation ==

1. Upload `wp-bulk-manager-client.php` to the `/wp-content/plugins/` directory
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to Settings → Bulk Manager to generate your API key
4. Use the API key in your WP Bulk Manager desktop application

== Frequently Asked Questions ==

= Is this plugin secure? =

Yes. The plugin uses API key authentication and follows WordPress security best practices. API keys are never exposed publicly.

= Does it work with The SEO Framework? =

Yes! The plugin automatically detects and integrates with The SEO Framework for SEO meta management.

= Will it slow down my site? =

No. The plugin is lightweight and only runs when API requests are made. It has minimal impact on site performance.

= Can I limit access by IP? =

Yes. You can configure IP whitelisting in the plugin settings.

== Changelog ==

= 1.0.0 =
* Initial release
* REST API endpoints for content management
* The SEO Framework integration
* Secure API key authentication

== API Endpoints ==

* POST /wp-json/wpbm/v1/auth - Verify authentication
* GET /wp-json/wpbm/v1/status - Get site status
* POST /wp-json/wpbm/v1/content - Create content
* GET /wp-json/wpbm/v1/content/{id} - Get content
* PUT /wp-json/wpbm/v1/content/{id} - Update content
* PUT /wp-json/wpbm/v1/seo/{id} - Update SEO meta
* GET /wp-json/wpbm/v1/plugins - List plugins
* POST /wp-json/wpbm/v1/bulk - Bulk operations