#!/usr/bin/env python3
"""Update Services page to match home page style with linked headers"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from wpbm_manager import WPBulkManager

def create_services_page_content():
    """Create Services page matching home page style with Stackable blocks"""
    
    # Service pages with their IDs and URLs
    services = [
        {
            'title': 'Laser Cutting',
            'id': 952,
            'url': '/laser-cutting/',
            'description': 'Precision cutting for metal, wood, acrylic, rubber, and more materials.',
            'icon': 'fas-cut'
        },
        {
            'title': 'Commercial Laser Cutting',
            'id': 1246,
            'url': '/commercial-laser-cutting/',
            'description': 'High-volume production runs with fast turnaround times.',
            'icon': 'fas-industry'
        },
        {
            'title': 'Large Format Laser Cutting',
            'id': 1987,
            'url': '/large-format-laser-cutting/',
            'description': 'Oversized material cutting up to 60"x120".',
            'icon': 'fas-expand-arrows-alt'
        },
        {
            'title': 'Large Format Laser Engraving',
            'id': 1972,
            'url': '/large-format-laser-engraving/',
            'description': 'Engraving on oversized materials for signage and art.',
            'icon': 'fas-edit'
        },
        {
            'title': 'Laser Marking & Etching',
            'id': 788,
            'url': '/laser-marking-etching/',
            'description': 'Permanent marking on metal, plastic, and other materials.',
            'icon': 'fas-pen-fancy'
        },
        {
            'title': 'Metal Cutting',
            'id': 795,
            'url': '/metal-cutting/',
            'description': 'Industrial metal cutting for steel, aluminum, and more.',
            'icon': 'fas-hammer'
        },
        {
            'title': 'Acrylic Cutting',
            'id': 808,
            'url': '/acrylic-cutting/',
            'description': 'Custom acrylic displays and precision parts.',
            'icon': 'fas-cube'
        },
        {
            'title': 'Rubber Cutting',
            'id': 797,
            'url': '/rubber-cutting/',
            'description': 'Precision rubber cutting for gaskets and seals.',
            'icon': 'fas-ring'
        },
        {
            'title': 'Wood Burning',
            'id': 780,
            'url': '/wood-burning/',
            'description': 'Artistic wood burning and engraving for decorative pieces.',
            'icon': 'fas-fire'
        },
        {
            'title': 'Gasket Cutting',
            'id': 786,
            'url': '/gasket-cutting/',
            'description': 'Custom gaskets for industrial applications.',
            'icon': 'fas-cog'
        },
        {
            'title': 'Media Blasting',
            'id': 792,
            'url': '/media-blasting-garnet-sand/',
            'description': 'Sand and garnet blasting for surface preparation.',
            'icon': 'fas-spray-can'
        },
        {
            'title': 'Custom Awards',
            'id': 1773,
            'url': '/custom-awards/',
            'description': 'Trophies, plaques, and recognition awards.',
            'icon': 'fas-trophy'
        },
        {
            'title': 'Signs & Signage',
            'id': 1751,
            'url': '/signs-signage/',
            'description': 'Custom business signs for indoor and outdoor use.',
            'icon': 'fas-sign'
        },
        {
            'title': 'Multi-Media Murals',
            'id': 3006,
            'url': '/multi-media-murals/',
            'description': 'Custom artistic displays combining multiple materials.',
            'icon': 'fas-palette'
        }
    ]
    
    # Build the content with Stackable blocks matching home page style
    content = '''<!-- wp:stackable/heading {"uniqueId":"services-hero","contentAlign":"center","textColor":"#ffffff","backgroundColor":"#1e1e1e"} -->
<div class="wp-block-stackable-heading stk-block-heading stk-block-heading--v2 stk-block" id="services-hero">
<style>.stk-services-hero{background-color:#1e1e1e !important}.stk-services-hero .stk-block-heading__text{color:#ffffff !important;text-align:center !important}</style>
<h1 class="stk-block-heading__text">Our Services</h1>
</div>
<!-- /wp:stackable/heading -->

<!-- wp:stackable/text {"uniqueId":"services-intro","contentAlign":"center"} -->
<div class="wp-block-stackable-text stk-block-text stk-block" id="services-intro">
<style>.stk-services-intro .stk-block-text__text{text-align:center !important}</style>
<p class="stk-block-text__text">Professional laser cutting and fabrication services in Longmont, Colorado. Browse our comprehensive range of precision cutting, engraving, and custom fabrication solutions.</p>
</div>
<!-- /wp:stackable/text -->

<!-- wp:stackable/separator {"uniqueId":"sep1"} -->
<div class="wp-block-stackable-separator stk-block-separator stk-block" id="sep1">
<hr class="stk-block-separator__hr"/>
</div>
<!-- /wp:stackable/separator -->

<!-- wp:stackable/columns {"uniqueId":"services-grid","columns":3,"design":"plain"} -->
<div class="wp-block-stackable-columns stk-block-columns stk-block stk-columns--design-plain" id="services-grid" data-block-id="services-grid">
<style>.stk-services-grid{--stk-columns:3 !important}.stk-services-grid>.stk-inner-blocks{gap:30px !important}</style>
<div class="stk-inner-blocks stk-block-content">'''

    # Add each service as a column with linked header
    for i, service in enumerate(services):
        # Start new columns block every 3 services
        if i > 0 and i % 3 == 0:
            content += '''</div>
</div>
<!-- /wp:stackable/columns -->

<!-- wp:stackable/columns {"uniqueId":"services-grid-''' + str(i//3) + '''","columns":3,"design":"plain"} -->
<div class="wp-block-stackable-columns stk-block-columns stk-block stk-columns--design-plain" id="services-grid-''' + str(i//3) + '''" data-block-id="services-grid-''' + str(i//3) + '''">
<style>.stk-services-grid-''' + str(i//3) + '''{--stk-columns:3 !important}.stk-services-grid-''' + str(i//3) + '''>.stk-inner-blocks{gap:30px !important}</style>
<div class="stk-inner-blocks stk-block-content">'''
        
        content += f'''
<!-- wp:stackable/column {{"uniqueId":"service-col-{i}"}} -->
<div class="wp-block-stackable-column stk-block-column stk-block stk-block-column--v2" id="service-col-{i}" data-block-id="service-col-{i}">
<div class="stk-column-wrapper stk-block-column__content stk-container stk-inner-blocks">

<!-- wp:stackable/icon-box {{"uniqueId":"service-{i}","iconColor1":"#0693E3","design":"plain"}} -->
<div class="wp-block-stackable-icon-box stk-block-icon-box stk-block stk-icon-box--design-plain" id="service-{i}" data-block-id="service-{i}">
<style>.stk-service-{i} .stk-icon-box__icon{{color:#0693E3 !important}}</style>
<div class="stk-block-content">
<span class="stk-icon-box__icon"><i class="{service['icon']}"></i></span>
<div class="stk-icon-box__content">
<h3 class="stk-icon-box__title"><a href="{service['url']}">{service['title']}</a></h3>
<p class="stk-icon-box__description">{service['description']}</p>
<a class="stk-icon-box__button" href="{service['url']}">Learn More →</a>
</div>
</div>
</div>
<!-- /wp:stackable/icon-box -->

</div>
</div>
<!-- /wp:stackable/column -->'''

    # Close the final columns block
    content += '''</div>
</div>
<!-- /wp:stackable/columns -->

<!-- wp:stackable/separator {"uniqueId":"sep2"} -->
<div class="wp-block-stackable-separator stk-block-separator stk-block" id="sep2">
<hr class="stk-block-separator__hr"/>
</div>
<!-- /wp:stackable/separator -->

<!-- wp:stackable/cta {"uniqueId":"services-cta","backgroundColor":"#f7f7f7","design":"centered"} -->
<div class="wp-block-stackable-cta stk-block-cta stk-block stk-cta--design-centered" id="services-cta" data-block-id="services-cta">
<style>.stk-services-cta{background-color:#f7f7f7 !important}.stk-services-cta .stk-container{padding-top:60px !important;padding-bottom:60px !important}</style>
<div class="stk-container">
<h2 class="stk-block-cta__title">Ready to Start Your Project?</h2>
<p class="stk-block-cta__description">Contact us today for a free quote on your laser cutting or fabrication project. Fast turnaround times and competitive pricing.</p>
<div class="stk-block-cta__buttons">
<a href="/contact-us/" class="stk-button stk-button--primary">Get a Free Quote</a>
<a href="tel:3036840696" class="stk-button stk-button--secondary">Call (303) 684-0696</a>
</div>
</div>
</div>
<!-- /wp:stackable/cta -->

<!-- wp:stackable/heading {"uniqueId":"why-choose","headingTag":"h2","contentAlign":"center"} -->
<div class="wp-block-stackable-heading stk-block-heading stk-block-heading--v2 stk-block" id="why-choose">
<style>.stk-why-choose .stk-block-heading__text{text-align:center !important}</style>
<h2 class="stk-block-heading__text">Why Choose BoulderWorks?</h2>
</div>
<!-- /wp:stackable/heading -->

<!-- wp:stackable/feature-grid {"uniqueId":"benefits","columns":3,"design":"plain"} -->
<div class="wp-block-stackable-feature-grid stk-block-feature-grid stk-block stk-feature-grid--design-plain" id="benefits" data-block-id="benefits">
<style>.stk-benefits{--stk-columns:3 !important}</style>
<div class="stk-inner-blocks">

<!-- wp:stackable/feature {"uniqueId":"benefit-1"} -->
<div class="wp-block-stackable-feature stk-block-feature stk-block" id="benefit-1">
<div class="stk-block-content">
<h3 class="stk-feature__title">Fast Turnaround</h3>
<p class="stk-feature__description">Quick quotes and rapid production times to meet your deadlines.</p>
</div>
</div>
<!-- /wp:stackable/feature -->

<!-- wp:stackable/feature {"uniqueId":"benefit-2"} -->
<div class="wp-block-stackable-feature stk-block-feature stk-block" id="benefit-2">
<div class="stk-block-content">
<h3 class="stk-feature__title">Precision Quality</h3>
<p class="stk-feature__description">State-of-the-art equipment ensures accurate, clean cuts every time.</p>
</div>
</div>
<!-- /wp:stackable/feature -->

<!-- wp:stackable/feature {"uniqueId":"benefit-3"} -->
<div class="wp-block-stackable-feature stk-block-feature stk-block" id="benefit-3">
<div class="stk-block-content">
<h3 class="stk-feature__title">Expert Support</h3>
<p class="stk-feature__description">Our experienced team helps optimize your designs for best results.</p>
</div>
</div>
<!-- /wp:stackable/feature -->

</div>
</div>
<!-- /wp:stackable/feature-grid -->'''
    
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
    
    print("🔧 Updating Services Page to Match Home Page Style", "🎨")
    print("=" * 60)
    
    # Create new content
    new_content = create_services_page_content()
    
    # Save backup
    with open('backups/services_page_stackable_backup.html', 'w') as f:
        f.write(new_content)
    print("📄 Backup saved to: backups/services_page_stackable_backup.html")
    
    # Update via API
    print("\nAttempting to update page content...")
    response = requests.put(
        f"{bw_site['url']}/wp-json/wpbm/v1/content/830",
        headers={'X-API-Key': api_key},
        json={'content': new_content},
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ API update successful")
        
        # Also save for manual update if needed
        with open('exports/services_stackable_content.html', 'w') as f:
            f.write(new_content)
        print("📄 Content saved to: exports/services_stackable_content.html")
        
        print("\n📋 What's New:")
        print("• Matches home page Stackable block design")
        print("• All 14 service headers link to their pages")
        print("• Professional grid layout with icons")
        print("• CTA section with phone number")
        print("• 'Why Choose BoulderWorks' section")
        
        print("\n🔗 Service Links Added:")
        print("• Laser Cutting → /laser-cutting/")
        print("• Commercial Laser Cutting → /commercial-laser-cutting/")
        print("• Large Format Laser Cutting → /large-format-laser-cutting/")
        print("• And 11 more services...")
    else:
        print(f"❌ Update failed: {response.status_code}")
    
    print("\n🚨 ALERT: Services page updated - matches home page style with linked headers")

if __name__ == "__main__":
    main()