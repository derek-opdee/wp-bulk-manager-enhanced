#!/usr/bin/env python3
"""Clean up excessive adjectives using WP Bulk Manager"""

import re
from wpbm_manager import WPBulkManager

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
    
    for page_id, page_name in pages:
        print(f'\nProcessing {page_name} (ID: {page_id})...')
        
        # Get current content
        content_data = manager.get_content(bw_site['id'], 'page', page_id)
        if not content_data:
            print(f'❌ Could not fetch page {page_id}')
            continue
        
        original_content = content_data.get('content', '')
        
        # Clean the content
        cleaned_content = clean_content(original_content)
        
        # Update if changed
        if original_content != cleaned_content:
            print(f'📝 Content cleaned for {page_name}')
            
            # Save cleaned content for review
            with open(f'{page_id}_cleaned.html', 'w') as f:
                f.write(cleaned_content)
            
            # Update the page
            success = manager.update_content(bw_site['id'], 'page', page_id, {
                'content': cleaned_content
            })
            
            if success:
                print(f'✅ Successfully updated {page_name}')
            else:
                print(f'❌ Failed to update {page_name}')
        else:
            print(f'No changes needed for {page_name}')
    
    print('\n✨ Cleanup complete!')

if __name__ == "__main__":
    main()