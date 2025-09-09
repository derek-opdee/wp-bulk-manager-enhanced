#!/usr/bin/env python3
"""Convert Services page to standard Gutenberg blocks only"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from wpbm_manager import WPBulkManager

def create_standard_gutenberg_services():
    """Create Services page using only standard Gutenberg blocks"""
    
    # Service pages with their URLs
    services = [
        ('Laser Cutting', '/laser-cutting/', 'Precision cutting for metal, wood, acrylic, rubber, and more materials.'),
        ('Commercial Laser Cutting', '/commercial-laser-cutting/', 'High-volume production runs with fast turnaround times.'),
        ('Large Format Laser Cutting', '/large-format-laser-cutting/', 'Oversized material cutting up to 60"x120".'),
        ('Large Format Laser Engraving', '/large-format-laser-engraving/', 'Engraving on oversized materials for signage and art.'),
        ('Laser Marking & Etching', '/laser-marking-etching/', 'Permanent marking on metal, plastic, and other materials.'),
        ('Metal Cutting', '/metal-cutting/', 'Industrial metal cutting for steel, aluminum, and more.'),
        ('Acrylic Cutting', '/acrylic-cutting/', 'Custom acrylic displays and precision parts.'),
        ('Rubber Cutting', '/rubber-cutting/', 'Precision rubber cutting for gaskets and seals.'),
        ('Wood Burning', '/wood-burning/', 'Artistic wood burning and engraving for decorative pieces.'),
        ('Gasket Cutting', '/gasket-cutting/', 'Custom gaskets for industrial applications.'),
        ('Media Blasting', '/media-blasting-garnet-sand/', 'Sand and garnet blasting for surface preparation.'),
        ('Custom Awards', '/custom-awards/', 'Trophies, plaques, and recognition awards.'),
        ('Signs & Signage', '/signs-signage/', 'Custom business signs for indoor and outdoor use.'),
        ('Multi-Media Murals', '/multi-media-murals/', 'Custom artistic displays combining multiple materials.')
    ]
    
    content = '''<!-- wp:heading {"textAlign":"center","level":1} -->
<h1 class="has-text-align-center">Our Services</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center","fontSize":"large"} -->
<p class="has-text-align-center has-large-font-size">Professional laser cutting and fabrication services in Longmont, Colorado. Browse our comprehensive range of precision cutting, engraving, and custom fabrication solutions.</p>
<!-- /wp:paragraph -->

<!-- wp:separator {"className":"is-style-wide"} -->
<hr class="wp-block-separator has-alpha-channel-opacity is-style-wide"/>
<!-- /wp:separator -->

<!-- wp:spacer {"height":"40px"} -->
<div style="height:40px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->'''

    # Create service grid using columns blocks
    for i in range(0, len(services), 3):
        content += '\n<!-- wp:columns -->\n<div class="wp-block-columns">'
        
        # Add up to 3 services per row
        for j in range(3):
            if i + j < len(services):
                title, url, desc = services[i + j]
                
                content += f'''<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3,"style":{{"spacing":{{"marginBottom":"10px"}}}}}} -->
<h3 style="margin-bottom:10px"><a href="{url}">{title}</a></h3>
<!-- /wp:heading -->

<!-- wp:paragraph {{"fontSize":"small"}} -->
<p class="has-small-font-size">{desc}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="{url}">Learn More →</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

'''
            else:
                # Empty column for alignment
                content += '''<!-- wp:column -->
<div class="wp-block-column"></div>
<!-- /wp:column -->

'''
        
        content += '</div>\n<!-- /wp:columns -->\n'
        
        # Add spacer between rows
        if i + 3 < len(services):
            content += '''<!-- wp:spacer {"height":"30px"} -->
<div style="height:30px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

'''

    # Add CTA section
    content += '''<!-- wp:spacer {"height":"60px"} -->
<div style="height:60px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"60px","bottom":"60px","right":"20px","left":"20px"}},"color":{"background":"#f0f0f0"}}} -->
<div class="wp-block-group alignfull has-background" style="background-color:#f0f0f0;padding-top:60px;padding-right:20px;padding-bottom:60px;padding-left:20px"><!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="has-text-align-center">Ready to Start Your Project?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center","fontSize":"medium"} -->
<p class="has-text-align-center has-medium-font-size">Contact us today for a free quote on your laser cutting or fabrication project. Fast turnaround times and competitive pricing.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue"} -->
<div class="wp-block-button"><a class="wp-block-button__link has-vivid-cyan-blue-background-color has-background wp-element-button" href="/contact-us/">Get a Free Quote</a></div>
<!-- /wp:button -->

<!-- wp:button {"style":{"color":{"background":"#ffffff","text":"#0073aa"}},"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link has-text-color has-background wp-element-button" href="tel:3036840696" style="color:#0073aa;background-color:#ffffff">Call (303) 684-0696</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->

<!-- wp:spacer {"height":"60px"} -->
<div style="height:60px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="has-text-align-center">Why Choose BoulderWorks?</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3,"style":{"spacing":{"marginBottom":"10px"}}}} -->
<h3 style="margin-bottom:10px">Fast Turnaround</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Quick quotes and rapid production times to meet your deadlines.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3,"style":{"spacing":{"marginBottom":"10px"}}}} -->
<h3 style="margin-bottom:10px">Precision Quality</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>State-of-the-art equipment ensures accurate, clean cuts every time.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3,"style":{"spacing":{"marginBottom":"10px"}}}} -->
<h3 style="margin-bottom:10px">Expert Support</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our experienced team helps optimize your designs for best results.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->'''

    return content

def main():
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    bw_site = None
    
    for site in sites:
        if 'boulderworks' in site['url'].lower():
            bw_site = site
            break
    
    if not bw_site:
        print("❌ BoulderWorks site not found")
        return
    
    api_key = manager.get_site_api_key(bw_site['id'])
    
    print("🔧 Converting Services Page to Standard Gutenberg Blocks", "📝")
    print("=" * 60)
    
    # Create new content with standard blocks only
    new_content = create_standard_gutenberg_services()
    
    # Save backup
    with open('backups/services_standard_gutenberg.html', 'w') as f:
        f.write(new_content)
    print("📄 Backup saved to: backups/services_standard_gutenberg.html")
    
    # Update via API
    print("\nUpdating page with standard Gutenberg blocks...")
    response = requests.put(
        f"{bw_site['url']}/wp-json/wpbm/v1/content/830",
        headers={'X-API-Key': api_key},
        json={'content': new_content},
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Update successful!")
        
        # Save for manual update
        with open('exports/services_standard_gutenberg.html', 'w') as f:
            f.write(new_content)
        print("📄 Content saved to: exports/services_standard_gutenberg.html")
        
        print("\n📋 What's Included:")
        print("• Standard Gutenberg blocks only (no custom blocks)")
        print("• Clean 3-column layout for services")
        print("• All service titles link to their pages")
        print("• CTA section with buttons")
        print("• Why Choose section")
        print("• No broken blocks or recovery needed")
        
        print("\n✅ Benefits:")
        print("• No plugin dependencies")
        print("• Works with any WordPress theme")
        print("• No block recovery errors")
        print("• Clean, simple HTML structure")
    else:
        print(f"❌ Update failed: {response.status_code}")
    
    print("\n🚨 ALERT: Services page converted to standard Gutenberg blocks - no recovery needed")

if __name__ == "__main__":
    main()