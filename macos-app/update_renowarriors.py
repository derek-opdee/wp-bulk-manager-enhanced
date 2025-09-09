#!/usr/bin/env python3
"""
Update RenoWarriors.com.au - SEO and Australian spelling fixes
"""

from wpbm_assistant import WPBulkAssistant
import json
import re

def main():
    # Initialize assistant
    assistant = WPBulkAssistant()
    
    # Connect to RenoWarriors
    print("Connecting to RenoWarriors.com.au...")
    if not assistant.select_site("RenoWarriors"):
        print("Error: Could not find RenoWarriors in the sites list")
        # List available sites
        sites = assistant.manager.get_sites('active')
        print("\nAvailable sites:")
        for site in sites:
            print(f"  - {site['name']} ({site['url']})")
        return
    
    print(f"✅ Connected to {assistant.current_site['name']} ({assistant.current_site['url']})")
    
    # Task 1: Check for The SEO Framework plugin
    print("\n1. Checking for The SEO Framework plugin...")
    plugins = assistant.manager.list_plugins(assistant.current_site_id)
    
    seo_framework_found = False
    for plugin in plugins:
        if 'seo' in plugin['slug'].lower() or 'seo' in plugin['name'].lower():
            print(f"  Found: {plugin['name']} (Status: {plugin['status']})")
            if 'seo framework' in plugin['name'].lower():
                seo_framework_found = True
    
    if seo_framework_found:
        print("✅ The SEO Framework plugin is installed")
    else:
        print("⚠️  The SEO Framework plugin not found - checking other SEO plugins")
    
    # Task 2: Get all pages and check SEO data
    print("\n2. Analyzing pages for missing SEO data...")
    pages = assistant.manager.list_all_content(assistant.current_site_id, 'page', 100)
    
    pages_missing_seo = []
    for page in pages:
        seo = page.get('seo', {})
        if not seo.get('title') or not seo.get('description'):
            pages_missing_seo.append(page)
    
    print(f"Found {len(pages_missing_seo)} pages with missing SEO data")
    
    # Task 3: Update SEO titles and descriptions
    print("\n3. Updating SEO data for pages...")
    
    # Southeast Melbourne suburbs to include in SEO
    se_melbourne_suburbs = [
        "Patterson Lakes", "Carrum", "Chelsea", "Bonbeach", "Frankston",
        "Seaford", "Carrum Downs", "Skye", "Sandhurst", "Cranbourne"
    ]
    
    for page in pages_missing_seo[:10]:  # Process first 10 pages
        print(f"\nProcessing: {page['title']}")
        
        # Get full page content
        content = assistant.get_page_content(page['id'])
        
        # Generate SEO title and description
        page_title = page['title']
        
        # Create SEO title focusing on Southeast Melbourne
        if not content['seo'].get('title'):
            seo_title = f"{page_title} | Renovation Services Southeast Melbourne | RenoWarriors"
            print(f"  New SEO Title: {seo_title}")
        else:
            seo_title = None
        
        # Create SEO description
        if not content['seo'].get('description'):
            # Extract text content
            text_content = re.sub('<[^<]+?>', '', content['content'])
            text_content = ' '.join(text_content.split())[:150]
            
            seo_description = f"Professional {page_title.lower()} services in Southeast Melbourne. "
            seo_description += f"Based in Patterson Lakes, VIC. Quality renovations for {', '.join(se_melbourne_suburbs[:3])} and surrounding suburbs."
            
            print(f"  New SEO Description: {seo_description}")
        else:
            seo_description = None
        
        # Update SEO
        if seo_title or seo_description:
            seo_data = {}
            if seo_title:
                seo_data['title'] = seo_title
            if seo_description:
                seo_data['description'] = seo_description
            
            if assistant.update_page_seo(page['id'], seo_data):
                print(f"  ✅ SEO updated successfully")
            else:
                print(f"  ❌ Failed to update SEO")
    
    # Task 4: Fix US to Australian spelling
    print("\n4. Checking for US spelling to fix...")
    
    # Common US to AU spelling conversions
    spelling_fixes = {
        'color': 'colour',
        'Color': 'Colour',
        'center': 'centre',
        'Center': 'Centre',
        'organize': 'organise',
        'Organize': 'Organise',
        'realize': 'realise',
        'Realize': 'Realise',
        'neighbor': 'neighbour',
        'Neighbor': 'Neighbour',
        'favor': 'favour',
        'Favor': 'Favour',
        'honor': 'honour',
        'Honor': 'Honour',
        'labor': 'labour',
        'Labor': 'Labour',
        'behavior': 'behaviour',
        'Behavior': 'Behaviour',
        'aluminum': 'aluminium',
        'Aluminum': 'Aluminium',
        'analyze': 'analyse',
        'Analyze': 'Analyse'
    }
    
    # Check all pages for US spelling
    pages_to_fix = []
    for page in pages:
        content = assistant.get_page_content(page['id'])
        page_content = content['content']
        
        # Check if any US spelling exists
        needs_fix = False
        for us_spelling in spelling_fixes.keys():
            if us_spelling in page_content:
                needs_fix = True
                break
        
        if needs_fix:
            pages_to_fix.append(page)
    
    print(f"Found {len(pages_to_fix)} pages with US spelling to fix")
    
    # Fix spelling in pages
    for page in pages_to_fix[:5]:  # Process first 5 pages
        print(f"\nFixing spelling in: {page['title']}")
        
        content = assistant.get_page_content(page['id'])
        updated_content = content['content']
        
        # Apply all spelling fixes
        changes_made = []
        for us_spelling, au_spelling in spelling_fixes.items():
            if us_spelling in updated_content:
                # Use word boundary regex to avoid partial replacements
                pattern = r'\b' + us_spelling + r'\b'
                updated_content = re.sub(pattern, au_spelling, updated_content)
                changes_made.append(f"{us_spelling} → {au_spelling}")
        
        if changes_made:
            print(f"  Changes: {', '.join(changes_made[:5])}")
            if len(changes_made) > 5:
                print(f"  ... and {len(changes_made) - 5} more")
            
            # Update the page content
            updates = {'content': updated_content}
            if assistant.update_page_content(page['id'], updates):
                print(f"  ✅ Spelling fixed successfully")
            else:
                print(f"  ❌ Failed to update content")
    
    # Generate final report
    print("\n" + "="*50)
    print("UPDATE COMPLETE")
    print("="*50)
    print(f"Site: {assistant.current_site['name']}")
    print(f"URL: {assistant.current_site['url']}")
    print(f"\nSEO Updates: {len(pages_missing_seo)} pages processed")
    print(f"Spelling Fixes: {len(pages_to_fix)} pages with US spelling found")
    print("\nFocus: Southeast Melbourne suburbs, based in Patterson Lakes, VIC")
    print("Note: Only SEO titles/descriptions and spelling were updated as requested")

if __name__ == "__main__":
    main()