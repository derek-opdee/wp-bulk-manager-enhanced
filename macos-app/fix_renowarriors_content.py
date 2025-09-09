#!/usr/bin/env python3
"""
Fix US to AU spelling in Reno Warriors content using correct endpoints
"""
import re
from wpbm_manager_v2 import WPBulkManagerV2

# Common US to AU spelling fixes
US_TO_AU = {
    # Common words
    'color': 'colour',
    'Color': 'Colour',
    'colors': 'colours',
    'Colors': 'Colours',
    'colored': 'coloured',
    'Colored': 'Coloured',
    'coloring': 'colouring',
    'Coloring': 'Colouring',
    
    'center': 'centre',
    'Center': 'Centre',
    'centers': 'centres',
    'Centers': 'Centres',
    'centered': 'centred',
    'Centered': 'Centred',
    
    'organize': 'organise',
    'Organize': 'Organise',
    'organized': 'organised',
    'Organized': 'Organised',
    'organizing': 'organising',
    'Organizing': 'Organising',
    'organization': 'organisation',
    'Organization': 'Organisation',
    
    'realize': 'realise',
    'Realize': 'Realise',
    'realized': 'realised',
    'Realized': 'Realised',
    
    'recognize': 'recognise',
    'Recognize': 'Recognise',
    'recognized': 'recognised',
    'Recognized': 'Recognised',
    
    'minimize': 'minimise',
    'Minimize': 'Minimise',
    'minimized': 'minimised',
    'Minimized': 'Minimised',
    
    'maximize': 'maximise',
    'Maximize': 'Maximise',
    'maximized': 'maximised',
    'Maximized': 'Maximised',
    
    'customize': 'customise',
    'Customize': 'Customise',
    'customized': 'customised',
    'Customized': 'Customised',
    
    'modernize': 'modernise',
    'Modernize': 'Modernise',
    'modernized': 'modernised',
    'Modernized': 'Modernised',
    
    'optimize': 'optimise',
    'Optimize': 'Optimise',
    'optimized': 'optimised',
    'Optimized': 'Optimised',
    
    'specialize': 'specialise',
    'Specialize': 'Specialise',
    'specialized': 'specialised',
    'Specialized': 'Specialised',
    'specializing': 'specialising',
    'Specializing': 'Specialising',
    
    # Common nouns
    'neighbor': 'neighbour',
    'Neighbor': 'Neighbour',
    'neighbors': 'neighbours',
    'Neighbors': 'Neighbours',
    'neighborhood': 'neighbourhood',
    'Neighborhood': 'Neighbourhood',
    
    'favor': 'favour',
    'Favor': 'Favour',
    'favors': 'favours',
    'favorite': 'favourite',
    'Favorite': 'Favourite',
    'favorites': 'favourites',
    
    'honor': 'honour',
    'Honor': 'Honour',
    'honored': 'honoured',
    'Honored': 'Honoured',
    
    'labor': 'labour',
    'Labor': 'Labour',
    
    'behavior': 'behaviour',
    'Behavior': 'Behaviour',
    
    # Materials
    'aluminum': 'aluminium',
    'Aluminum': 'Aluminium',
    'fiber': 'fibre',
    'Fiber': 'Fibre',
    
    # Measurements
    'meter': 'metre',
    'Meter': 'Metre',
    'meters': 'metres',
    'Meters': 'Metres',
    'liter': 'litre',
    'Liter': 'Litre',
    'liters': 'litres',
    
    # Other common words
    'defense': 'defence',
    'Defense': 'Defence',
    'offense': 'offence',
    'Offense': 'Offence',
    'license': 'licence',
    'License': 'Licence',
    'practicing': 'practising',
    'Practicing': 'Practising',
    'aging': 'ageing',
    'Aging': 'Ageing',
    'gray': 'grey',
    'Gray': 'Grey',
    'mold': 'mould',
    'Mold': 'Mould',
    'molding': 'moulding',
    'Molding': 'Moulding'
}

def fix_spelling(text):
    """Fix US to AU spelling"""
    if not text:
        return text, 0
    
    changes = 0
    for us, au in US_TO_AU.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(us) + r'\b'
        if re.search(pattern, text):
            text, count = re.subn(pattern, au, text)
            changes += count
    
    return text, changes

def main():
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Get client
    client = manager.get_client('renowarriors', cache_enabled=False)
    if not client:
        print("Error: Could not connect to renowarriors site")
        return
    
    print("=== Fixing US to AU Spelling in Reno Warriors Content ===\n")
    
    # Use the content endpoint directly
    try:
        # Get all pages via the content endpoint
        response = client.get('content', params={'type': 'page', 'per_page': 100})
        
        if isinstance(response, list):
            pages = response
        elif isinstance(response, dict) and 'pages' in response:
            pages = response['pages']
        else:
            print("Unexpected response format. Trying alternative approach...")
            # Try getting pages directly
            pages = client.get_content(content_type='page', status='publish')
            
        print(f"Found {len(pages)} pages\n")
        
        total_fixes = 0
        pages_updated = 0
        
        for page in pages:
            page_id = page['id']
            
            # Get page details
            try:
                # Try to get full content
                page_data = client.get(f'content/{page_id}')
                
                # Extract title and content
                title = page_data.get('title', '')
                if isinstance(title, dict):
                    title = title.get('rendered', '')
                    
                content = page_data.get('content', '')
                if isinstance(content, dict):
                    content = content.get('rendered', '')
                
                print(f"\nChecking Page {page_id}: {title[:50]}...")
                
                # Fix spelling in title and content
                new_title, title_changes = fix_spelling(title)
                new_content, content_changes = fix_spelling(content)
                
                if title_changes or content_changes:
                    print(f"  Found {title_changes + content_changes} spelling issues")
                    
                    # Update the page
                    update_data = {}
                    if title_changes:
                        update_data['title'] = new_title
                        print(f"  - Fixed {title_changes} issues in title")
                    if content_changes:
                        update_data['content'] = new_content
                        print(f"  - Fixed {content_changes} issues in content")
                    
                    try:
                        client.put(f'content/{page_id}', update_data)
                        print(f"  ✓ Updated successfully")
                        pages_updated += 1
                        total_fixes += title_changes + content_changes
                    except Exception as e:
                        print(f"  ✗ Error updating: {e}")
                else:
                    print("  No US spellings found")
                    
            except Exception as e:
                print(f"  Error processing page {page_id}: {e}")
                
    except Exception as e:
        print(f"Error getting pages: {e}")
        return
    
    print(f"\n=== Summary ===")
    print(f"Total pages processed: {len(pages)}")
    print(f"Pages updated: {pages_updated}")
    print(f"Total spelling fixes: {total_fixes}")
    print("\n✓ Spelling update complete!")

if __name__ == "__main__":
    main()