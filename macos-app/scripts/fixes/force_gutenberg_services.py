#!/usr/bin/env python3
"""Force convert Services page to Gutenberg by clearing Divi data"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from wpbm_manager import WPBulkManager

def create_gutenberg_services_content():
    """Create a complete Gutenberg services page"""
    return '''<!-- wp:heading {"level":1,"textAlign":"center"} -->
<h1 class="has-text-align-center">Our Services</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Professional laser cutting and fabrication services in Longmont, Colorado. We offer a wide range of precision cutting, engraving, and custom fabrication solutions.</p>
<!-- /wp:paragraph -->

<!-- wp:spacer {"height":"40px"} -->
<div style="height:40px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:heading {"level":2,"textAlign":"center"} -->
<h2 class="has-text-align-center">Browse Our Services</h2>
<!-- /wp:heading -->

<!-- wp:columns {"verticalAlignment":"top"} -->
<div class="wp-block-columns are-vertically-aligned-top"><!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Laser Cutting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Precision cutting for metal, wood, acrylic, rubber, and more. Our state-of-the-art laser systems deliver clean, accurate cuts for any project size.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><!-- wp:list-item -->
<li>Metal cutting (steel, aluminum, brass)</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Wood and plywood cutting</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Acrylic and plastic cutting</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Rubber and foam cutting</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Laser Engraving</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Custom engraving and marking on various surfaces. Perfect for personalization, branding, and identification needs.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><!-- wp:list-item -->
<li>Logo engraving</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Serial number marking</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Decorative patterns</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Text and graphics</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Large Format Cutting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Oversized material cutting up to 60"x120". Ideal for architectural projects, large signs, and industrial applications.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><!-- wp:list-item -->
<li>Architectural panels</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Large signage</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Industrial sheets</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li>Custom fixtures</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:spacer {"height":"40px"} -->
<div style="height:40px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:columns {"verticalAlignment":"top"} -->
<div class="wp-block-columns are-vertically-aligned-top"><!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Commercial Services</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>High-volume production runs with fast turnaround times. We handle projects from prototypes to full production.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Custom Awards</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Trophies, plaques, and recognition awards. Create memorable awards for corporate events, sports, and special occasions.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Signs & Signage</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Custom business signs for indoor and outdoor use. From lobby signs to directional signage, we create professional displays.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:spacer {"height":"40px"} -->
<div style="height:40px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:columns {"verticalAlignment":"top"} -->
<div class="wp-block-columns are-vertically-aligned-top"><!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Gasket Cutting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Precision gaskets for industrial applications. Custom gaskets cut to your exact specifications from various materials.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Wood Burning</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Artistic wood burning and engraving for decorative pieces, signs, and custom gifts. Beautiful results on all wood types.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Media Blasting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Sand and garnet blasting for surface preparation, cleaning, and texturing. Professional results for any surface treatment needs.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:spacer {"height":"40px"} -->
<div style="height:40px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:columns {"verticalAlignment":"top"} -->
<div class="wp-block-columns are-vertically-aligned-top"><!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Metal Cutting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Industrial metal cutting for steel, aluminum, brass, and more. Clean cuts with minimal heat-affected zones.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Acrylic Cutting</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Custom acrylic displays and precision parts. Crystal-clear cuts for retail displays, machine guards, and decorative pieces.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"top"} -->
<div class="wp-block-column is-vertically-aligned-top"><!-- wp:heading {"level":3} -->
<h3>Multi-Media Murals</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Custom artistic displays combining multiple materials. Create unique wall art and installations for any space.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:spacer {"height":"60px"} -->
<div style="height:60px" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->

<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|70"}}},"backgroundColor":"pale-cyan-blue","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-pale-cyan-blue-background-color has-background" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70)"><!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="has-text-align-center">Ready to Start Your Project?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Contact us today for a free quote on your laser cutting or fabrication project. Fast turnaround times and competitive pricing.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","style":{"spacing":{"padding":{"top":"15px","bottom":"15px","left":"40px","right":"40px"}}}} -->
<div class="wp-block-button"><a class="wp-block-button__link has-vivid-cyan-blue-background-color has-background wp-element-button" href="/contact-us/" style="padding-top:15px;padding-right:40px;padding-bottom:15px;padding-left:40px">Get a Free Quote</a></div>
<!-- /wp:button -->

<!-- wp:button {"backgroundColor":"white","textColor":"vivid-cyan-blue","style":{"spacing":{"padding":{"top":"15px","bottom":"15px","left":"40px","right":"40px"}}}} -->
<div class="wp-block-button"><a class="wp-block-button__link has-vivid-cyan-blue-color has-white-background-color has-text-color has-background wp-element-button" href="tel:3036840696" style="padding-top:15px;padding-right:40px;padding-bottom:15px;padding-left:40px">Call (303) 684-0696</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->'''

def main():
    manager = WPBulkManager()
    sites = manager.get_sites('all')
    bw_site = None
    
    for site in sites:
        if 'boulderworks' in site['url'].lower():
            bw_site = site
            break
    
    api_key = manager.get_site_api_key(bw_site['id'])
    
    print("🔧 Converting Services Page to Gutenberg", "🛠️")
    print("=" * 60)
    print("Note: If this doesn't work, you may need to:")
    print("1. Log into WordPress admin")
    print("2. Edit the 'Our Services' page")
    print("3. Switch from 'Divi Builder' to 'Default Editor'")
    print("4. Then run this script again")
    print()
    
    # Create new content
    new_content = create_gutenberg_services_content()
    
    # Update via API
    print("Attempting to update page content...")
    response = requests.put(
        f"{bw_site['url']}/wp-json/wpbm/v1/content/830",
        headers={'X-API-Key': api_key},
        json={
            'content': new_content,
            'meta': {
                '_et_pb_use_builder': '',  # Try to clear Divi builder flag
                '_et_pb_old_content': ''   # Clear old Divi content
            }
        },
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ API update successful")
        
        # Save the Gutenberg content locally
        with open('exports/services_gutenberg_content.html', 'w') as f:
            f.write(new_content)
        print("📄 Gutenberg content saved to: exports/services_gutenberg_content.html")
        
        print("\n📋 Next Steps:")
        print("1. Check the page at: https://www.boulderworks.net/our-services/")
        print("2. If still showing Divi, manually switch to Block Editor in WordPress")
        print("3. The Gutenberg content is saved locally if you need to paste it manually")
    else:
        print(f"❌ Update failed: {response.status_code}")
    
    print("\n🚨 ALERT: Services page conversion attempted - may require manual editor switch")

if __name__ == "__main__":
    main()