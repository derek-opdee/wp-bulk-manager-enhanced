#!/usr/bin/env python3
"""Clean up excessive adjectives from BoulderWorks pages - Final version"""

import re
import requests
import json
from wpbm_manager import WPBulkManager

# BoulderWorks API credentials
url = 'https://www.boulderworks.net'

# List of excessive adjectives to remove or replace
excessive_adjectives = {
    'unparalleled': 'excellent',
    'exceptional': 'quality',
    'cutting-edge': 'modern',
    'state-of-the-art': 'advanced',
    'superior': 'quality',
    'unrivaled': 'precise',
    'exquisite': 'detailed',
    'unforgettable': 'memorable',
    'outstanding': 'quality',
    'impeccable': 'precise',
    'meticulous': 'careful',
    'utmost': 'great',
    'unmatched': 'precise',
    'remarkable': 'fast',
    'unwavering': 'consistent',
    'elevate': 'improve'
}

def clean_content(content):
    """Clean excessive adjectives from content"""
    
    # First, handle phrases
    content = re.sub(r'Unleash Impeccable Precision and Unparalleled Quality', 
                     'Precision and Quality', content, flags=re.IGNORECASE)
    
    content = re.sub(r'Elevate Large Format Laser Engraving for Exquisite Precision and Unforgettable Detail', 
                     'Large Format Laser Engraving with Precision and Detail', content, flags=re.IGNORECASE)
    
    # Replace excessive adjectives with simpler alternatives
    for excessive, replacement in excessive_adjectives.items():
        # Replace whole words only
        pattern = r'\b' + re.escape(excessive) + r'\b'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Clean up specific phrases
    replacements = [
        # Large Format Laser Cutting specific
        ('exceed your expectations', 'meet your needs'),
        ('elevate your projects to new heights', 'complete your projects successfully'),
        ('bring your vision to life with precision and excellence', 'complete your project with precision'),
        ('experience the difference our precision[^.]*make', 'see how our precision helps'),
        
        # Large Format Laser Engraving specific
        ('delivering outstanding results', 'delivering quality results'),
        ('unmatched precision and attention to detail', 'precision and attention to detail'),
        ('flawless execution from start to finish', 'professional execution from start to finish'),
        ('Quality That Transcends Boundaries', 'Quality Work'),
        ('leave a lasting impression', 'make an impact'),
        ('executed with meticulous care and artistry', 'executed with care and skill'),
        ('Timeliness and Reliable Service', 'Fast and Reliable Service'),
        ('Affordable Excellence', 'Affordable Quality'),
        ('exceptional quality should be accessible', 'quality should be accessible'),
        ('superior value for your investment', 'good value for your investment'),
        ('bring your creative visions to life', 'complete your creative projects'),
        
        # Metal Cutting specific
        ('exceptional results with remarkable speed', 'quality results with fast turnaround'),
        ('unparalleled accuracy', 'high accuracy'),
        ('Trust us for your laser cutting needs', 'Contact us for your laser cutting needs'),
        ('experience the exceptional precision', 'benefit from the precision'),
        
        # Laser Marking specific
        ('exceptional laser etching and marking services', 'laser etching and marking services'),
        ('unparalleled accuracy', 'high accuracy'),
        ('outstanding results every time', 'quality results every time'),
        ('exceed expectations', 'meet your needs'),
        
        # General cleanup
        ('state-of-the-art', 'advanced'),
        ('cutting-edge', 'modern'),
        ('top-notch', 'quality')
    ]
    
    for old_phrase, new_phrase in replacements:
        content = re.sub(old_phrase, new_phrase, content, flags=re.IGNORECASE)
    
    # Clean up double spaces
    content = re.sub(r'\s+', ' ', content)
    
    return content

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
        print("Please add BoulderWorks site first using wpbm_cli.py")
        return
    
    # Get API key
    api_key = manager.get_site_api_key(bw_site['id'])
    if not api_key:
        print("❌ Could not retrieve API key for BoulderWorks")
        return
    
    print("🧹 Cleaning up excessive adjectives from BoulderWorks pages")
    print("=" * 60)
    print(f"Site: {bw_site['url']}")
    
    # Pages to clean
    pages = [
        (1987, 'Large Format Laser Cutting'),
        (1972, 'Large Format Laser Engraving'),
        (795, 'Metal Cutting'),
        (788, 'Laser Marking & Etching')
    ]
    
    updated_count = 0
    
    for page_id, page_name in pages:
        print(f'\nProcessing {page_name} (ID: {page_id})...')
        
        try:
            # Get current content using the wpbm API
            response = requests.get(
                f"{bw_site['url']}/wp-json/wpbm/v1/content/{page_id}",
                headers={'X-API-Key': api_key},
                timeout=10
            )
            
            if response.status_code != 200:
                print(f'❌ Could not fetch page: {response.status_code}')
                continue
            
            page_data = response.json()
            original_content = page_data.get('content', '')
            
            # Clean the content
            cleaned_content = clean_content(original_content)
            
            # Update if changed
            if original_content != cleaned_content:
                print(f'📝 Content cleaned, updating...')
                
                # Save cleaned content for review
                with open(f'{page_id}_cleaned.html', 'w') as f:
                    f.write(cleaned_content)
                
                # Update the page
                update_data = {
                    'content': cleaned_content
                }
                
                response = requests.put(
                    f"{bw_site['url']}/wp-json/wpbm/v1/content/{page_id}",
                    headers={'X-API-Key': api_key},
                    json=update_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f'✅ Successfully updated {page_name}')
                    updated_count += 1
                else:
                    print(f'❌ Failed to update: {response.status_code} - {response.text[:200]}')
            else:
                print(f'No changes needed for {page_name}')
                
        except Exception as e:
            print(f'❌ Error processing page: {e}')
    
    print(f'\n✨ Cleanup complete! Updated {updated_count} pages.')
    
    if updated_count > 0:
        print("\n📌 Next steps:")
        print("1. Review the updated pages on the live site")
        print("2. Check that the content still flows naturally")
        print("3. Verify all key information is preserved")

if __name__ == "__main__":
    main()