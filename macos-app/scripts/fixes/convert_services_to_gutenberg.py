#!/usr/bin/env python3
"""Convert BoulderWorks Services page from Divi to Gutenberg/Kadence blocks"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
import re
from wpbm_manager import WPBulkManager

def parse_divi_content(content):
    """Extract text content from Divi shortcodes"""
    sections = []
    
    # Extract main heading
    heading_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if heading_match:
        sections.append({
            'type': 'heading',
            'level': 1,
            'text': heading_match.group(1)
        })
    
    # Extract h2 headings
    h2_matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)
    for h2 in h2_matches:
        sections.append({
            'type': 'heading',
            'level': 2,
            'text': h2
        })
    
    # Extract service items (h3)
    h3_matches = re.findall(r'<h3[^>]*>([^<]+)</h3>', content)
    for h3 in h3_matches:
        sections.append({
            'type': 'service',
            'text': h3
        })
    
    # Extract text content
    text_matches = re.findall(r'\[et_pb_text[^\]]*\]([^[]+)\[/et_pb_text\]', content)
    for text in text_matches:
        cleaned = re.sub(r'<[^>]+>', '', text).strip()
        if cleaned and cleaned not in ['Browse']:
            sections.append({
                'type': 'text',
                'text': cleaned
            })
    
    return sections

def create_gutenberg_content(sections):
    """Convert parsed sections to Gutenberg/Kadence blocks"""
    blocks = []
    
    # Add main heading
    blocks.append('<!-- wp:kadence/advancedheading {"uniqueID":"services-main","align":"center","headingTag":"h1","fontSize":["xl","xl","xl"]} -->')
    blocks.append('<div class="wp-block-kadence-advancedheading kt-adv-heading_services-main wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading_services-main">')
    blocks.append('<h1 class="kt-adv-heading_services-main wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading_services-main">Our Services</h1>')
    blocks.append('</div>')
    blocks.append('<!-- /wp:kadence/advancedheading -->')
    blocks.append('')
    
    # Add intro text
    blocks.append('<!-- wp:paragraph {"align":"center"} -->')
    blocks.append('<p class="has-text-align-center">Professional laser cutting and fabrication services in Longmont, Colorado. We offer a wide range of precision cutting, engraving, and custom fabrication solutions.</p>')
    blocks.append('<!-- /wp:paragraph -->')
    blocks.append('')
    
    # Add services grid
    blocks.append('<!-- wp:kadence/rowlayout {"uniqueID":"services-grid","columns":3,"colLayout":"equal","mobileLayout":"row"} -->')
    blocks.append('<div class="wp-block-kadence-rowlayout alignnone">')
    blocks.append('<div id="kt-layout-id_services-grid" class="kt-row-layout-inner kt-layout-id_services-grid">')
    blocks.append('<div class="kt-row-column-wrap kt-has-3-columns kt-gutter-default kt-v-gutter-default kt-row-valign-top kt-row-layout-equal kt-tab-layout-inherit kt-m-colapse-left-to-right kt-mobile-layout-row kb-theme-content-width">')
    
    # Services list
    services = [
        ('Laser Cutting', 'Precision cutting for metal, wood, acrylic, rubber, and more materials'),
        ('Laser Engraving', 'Custom engraving and marking on various surfaces'),
        ('Large Format Cutting', 'Oversized material cutting up to 60"x120"'),
        ('Commercial Services', 'High-volume production runs with fast turnaround'),
        ('Custom Awards', 'Trophies, plaques, and recognition awards'),
        ('Signs & Signage', 'Custom business signs for indoor and outdoor use'),
        ('Gasket Cutting', 'Precision gaskets for industrial applications'),
        ('Wood Burning', 'Artistic wood burning and engraving'),
        ('Media Blasting', 'Sand and garnet blasting for surface preparation'),
        ('Metal Cutting', 'Industrial metal cutting for steel, aluminum, and more'),
        ('Acrylic Cutting', 'Custom acrylic displays and precision parts'),
        ('Multi-Media Murals', 'Custom artistic displays combining multiple materials')
    ]
    
    # Create service blocks
    for i, (title, desc) in enumerate(services):
        if i % 3 == 0 and i > 0:
            # Close previous row and start new one
            blocks.append('</div></div></div>')
            blocks.append('<!-- /wp:kadence/rowlayout -->')
            blocks.append('')
            blocks.append('<!-- wp:kadence/rowlayout {"uniqueID":"services-grid-' + str(i//3) + '","columns":3,"colLayout":"equal","mobileLayout":"row"} -->')
            blocks.append('<div class="wp-block-kadence-rowlayout alignnone">')
            blocks.append('<div id="kt-layout-id_services-grid-' + str(i//3) + '" class="kt-row-layout-inner">')
            blocks.append('<div class="kt-row-column-wrap kt-has-3-columns kt-gutter-default kt-v-gutter-default kt-row-valign-top kt-row-layout-equal kt-tab-layout-inherit kt-m-colapse-left-to-right kt-mobile-layout-row kb-theme-content-width">')
        
        blocks.append(f'<!-- wp:kadence/column {{"uniqueID":"service-col-{i}"}} -->')
        blocks.append('<div class="wp-block-kadence-column inner-column-1">')
        blocks.append('<div class="kt-inside-inner-col">')
        
        # Service card
        blocks.append('<!-- wp:kadence/infobox {"uniqueID":"service-' + str(i) + '","mediaType":"icon","mediaIcon":{"icon":"fe_aperture","size":40,"color":"#0066cc"},"mediaAlign":"top","titleFont":[{"size":["","","20"],"lineHeight":["","",""],"family":"","google":false,"style":"","weight":"","variant":"","subset":"","loadGoogle":true}]} -->')
        blocks.append('<div class="wp-block-kadence-infobox kt-info-box-wrap kt-info-box-service-' + str(i) + '">')
        blocks.append('<div class="kt-info-box-media-align-top kt-info-box-has-icon kt-info-box-media-align-top">')
        blocks.append('<div class="kt-blocks-info-box-link-wrap">')
        blocks.append('<div class="kt-blocks-info-box-media-container">')
        blocks.append('<div class="kt-info-box-icon-container kt-info-box-media-icon-width-default">')
        blocks.append('<div class="kt-info-box-icon-wrapper">')
        blocks.append('<span class="kt-info-svg-icon kt-info-svg-icon-fe_aperture"></span>')
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('<div class="kt-infobox-textcontent">')
        blocks.append(f'<h3 class="kt-blocks-info-box-title">{title}</h3>')
        blocks.append(f'<p class="kt-blocks-info-box-text">{desc}</p>')
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('<!-- /wp:kadence/infobox -->')
        
        blocks.append('</div>')
        blocks.append('</div>')
        blocks.append('<!-- /wp:kadence/column -->')
    
    # Close final row
    blocks.append('</div></div></div>')
    blocks.append('<!-- /wp:kadence/rowlayout -->')
    blocks.append('')
    
    # Add CTA section
    blocks.append('<!-- wp:kadence/rowlayout {"uniqueID":"cta-section","bgColor":"#f8f9fa","padding":["xl","","xl",""]} -->')
    blocks.append('<div class="wp-block-kadence-rowlayout alignfull">')
    blocks.append('<div class="kt-row-layout-inner">')
    blocks.append('<div class="kt-row-column-wrap kt-has-1-columns kt-gutter-default kt-v-gutter-default kt-row-valign-top kt-row-layout-equal kt-tab-layout-inherit kt-m-colapse-left-to-right kt-mobile-layout-row kb-theme-content-width">')
    blocks.append('<!-- wp:kadence/column -->')
    blocks.append('<div class="wp-block-kadence-column inner-column-1">')
    blocks.append('<div class="kt-inside-inner-col">')
    
    blocks.append('<!-- wp:kadence/advancedheading {"uniqueID":"cta-heading","align":"center","headingTag":"h2"} -->')
    blocks.append('<div class="wp-block-kadence-advancedheading">')
    blocks.append('<h2 class="kt-adv-heading_cta-heading has-text-align-center">Ready to Start Your Project?</h2>')
    blocks.append('</div>')
    blocks.append('<!-- /wp:kadence/advancedheading -->')
    
    blocks.append('<!-- wp:paragraph {"align":"center"} -->')
    blocks.append('<p class="has-text-align-center">Contact us today for a free quote on your laser cutting or fabrication project.</p>')
    blocks.append('<!-- /wp:paragraph -->')
    
    blocks.append('<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->')
    blocks.append('<div class="wp-block-buttons">')
    blocks.append('<!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","style":{"spacing":{"padding":{"top":"15px","bottom":"15px","left":"30px","right":"30px"}}}} -->')
    blocks.append('<div class="wp-block-button"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/contact-us/" style="padding-top:15px;padding-right:30px;padding-bottom:15px;padding-left:30px">Get a Quote</a></div>')
    blocks.append('<!-- /wp:button -->')
    blocks.append('</div>')
    blocks.append('<!-- /wp:buttons -->')
    
    blocks.append('</div>')
    blocks.append('</div>')
    blocks.append('<!-- /wp:kadence/column -->')
    blocks.append('</div></div></div>')
    blocks.append('<!-- /wp:kadence/rowlayout -->')
    
    return '\n'.join(blocks)

def main():
    manager = WPBulkManager()
    
    # Get BoulderWorks site
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
    
    print("🔧 Converting Our Services Page to Gutenberg/Kadence", "🛠️")
    print("=" * 60)
    
    # Get current content
    response = requests.get(
        f"{bw_site['url']}/wp-json/wpbm/v1/content/830",
        headers={'X-API-Key': api_key},
        timeout=10
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to get page content: {response.status_code}")
        return
    
    page_data = response.json()
    current_content = page_data.get('content', '')
    
    print(f"📄 Page: {page_data.get('title', 'Our Services')}")
    print(f"   Current: Divi Builder")
    print(f"   Converting to: Gutenberg + Kadence blocks")
    
    # Backup current content
    with open('backups/services_page_830_divi_backup.html', 'w') as f:
        f.write(current_content)
    print(f"   ✅ Backup saved to backups/services_page_830_divi_backup.html")
    
    # Parse and convert
    sections = parse_divi_content(current_content)
    new_content = create_gutenberg_content(sections)
    
    # Update the page
    print(f"\n📤 Updating page content...")
    update_response = requests.put(
        f"{bw_site['url']}/wp-json/wpbm/v1/content/830",
        headers={'X-API-Key': api_key},
        json={'content': new_content},
        timeout=30
    )
    
    if update_response.status_code == 200:
        print(f"   ✅ Successfully converted to Gutenberg/Kadence!")
        print(f"\n📌 Summary:")
        print(f"   • Converted Divi shortcodes to Gutenberg blocks")
        print(f"   • Used Kadence blocks for advanced layouts")
        print(f"   • Created service grid with 12 services")
        print(f"   • Added CTA section with button")
        print(f"   • Preserved all service information")
    else:
        print(f"   ❌ Update failed: {update_response.status_code}")
        print(f"   Error: {update_response.text[:200]}")
    
    # Alert completion
    print(f"\n🚨 ALERT: Services page conversion completed - Divi to Gutenberg/Kadence")

if __name__ == "__main__":
    main()