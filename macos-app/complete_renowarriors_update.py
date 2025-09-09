#!/usr/bin/env python3
"""
Complete update for Reno Warriors - SEO and spelling fixes
"""
import re
import json
from wpbm_manager_v2 import WPBulkManagerV2
from wpbm.operations.content import ContentOperations

# US to AU spelling mappings
SPELLING_FIXES = {
    'color': 'colour',
    'Color': 'Colour', 
    'colors': 'colours',
    'Colors': 'Colours',
    'colored': 'coloured',
    'center': 'centre',
    'Center': 'Centre',
    'organize': 'organise',
    'organized': 'organised',
    'organization': 'organisation',
    'realize': 'realise',
    'realized': 'realised', 
    'recognize': 'recognise',
    'recognized': 'recognised',
    'minimize': 'minimise',
    'minimized': 'minimised',
    'maximize': 'maximise',
    'maximized': 'maximised',
    'customize': 'customise',
    'customized': 'customised',
    'optimize': 'optimise',
    'optimized': 'optimised',
    'specialize': 'specialise',
    'specialized': 'specialised',
    'neighbor': 'neighbour',
    'neighbors': 'neighbours',
    'neighborhood': 'neighbourhood',
    'favor': 'favour',
    'favorite': 'favourite',
    'honor': 'honour',
    'honored': 'honoured',
    'behavior': 'behaviour',
    'aluminum': 'aluminium',
    'fiber': 'fibre',
    'meter': 'metre',
    'meters': 'metres',
    'liter': 'litre',
    'defense': 'defence',
    'offense': 'offence',
    'license': 'licence',
    'practicing': 'practising',
    'aging': 'ageing',
    'gray': 'grey',
    'mold': 'mould',
    'molding': 'moulding'
}

def main():
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Get client
    client = manager.get_client('renowarriors', cache_enabled=False)
    if not client:
        print("Error: Could not connect to renowarriors site")
        return
        
    content_ops = ContentOperations(client)
    
    print("=== Reno Warriors Content Update ===\n")
    print("This will fix US to AU spelling in all page content.")
    print("SEO metadata has already been updated.\n")
    
    # Process each spelling fix
    total_replacements = 0
    total_pages_updated = set()
    
    for us_word, au_word in SPELLING_FIXES.items():
        print(f"\nChecking for '{us_word}'...")
        
        # Search for the US spelling
        results = content_ops.search_replace_content(
            search=us_word,
            replace=au_word,
            post_types=['page'],
            dry_run=True
        )
        
        if results['changes']:
            print(f"  Found {results['total_replacements']} instances in {len(results['changes'])} pages")
            
            # Apply the fix
            actual_results = content_ops.search_replace_content(
                search=us_word,
                replace=au_word,
                post_types=['page'],
                dry_run=False
            )
            
            if actual_results['posts_modified'] > 0:
                print(f"  ✓ Fixed {actual_results['total_replacements']} instances")
                total_replacements += actual_results['total_replacements']
                
                # Track which pages were updated
                for change in actual_results['changes']:
                    total_pages_updated.add(change['id'])
            else:
                print("  ✗ Error applying fixes")
                
    print("\n" + "="*50)
    print("=== Update Summary ===")
    print(f"Total spelling corrections: {total_replacements}")
    print(f"Pages updated: {len(total_pages_updated)}")
    
    if total_pages_updated:
        print("\nUpdated pages:")
        pages = client.get_content(content_type='page')
        for page_id in total_pages_updated:
            page_info = next((p for p in pages if p['id'] == page_id), None)
            if page_info:
                title = page_info.get('title', '')
                if isinstance(title, dict):
                    title = title.get('rendered', '')
                print(f"  - Page {page_id}: {title}")
    
    print("\n✓ Reno Warriors content update complete!")
    print("\nNotes:")
    print("- SEO metadata (titles & descriptions) have been updated for all pages")
    print("- US spellings have been converted to Australian English")
    print("- The SEO Framework fields should now be properly populated")

if __name__ == "__main__":
    main()