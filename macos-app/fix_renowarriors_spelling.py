#!/usr/bin/env python3
"""
Fix US to AU spelling in Reno Warriors content
"""
import re
from wpbm_manager_v2 import WPBulkManagerV2
from wpbm.api.client import WPBMClient
from wpbm.operations.content import ContentOperations

# US to AU spelling mappings
US_TO_AU_SPELLINGS = {
    'color': 'colour',
    'colors': 'colours', 
    'colored': 'coloured',
    'coloring': 'colouring',
    'colorful': 'colourful',
    'center': 'centre',
    'centers': 'centres',
    'centered': 'centred',
    'organize': 'organise',
    'organized': 'organised',
    'organizing': 'organising',
    'organization': 'organisation',
    'specialize': 'specialise',
    'specialized': 'specialised',
    'specializing': 'specialising',
    'realize': 'realise',
    'realized': 'realised',
    'recognize': 'recognise',
    'recognized': 'recognised',
    'minimize': 'minimise',
    'minimized': 'minimised',
    'maximize': 'maximise',
    'maximized': 'maximised',
    'optimize': 'optimise',
    'optimized': 'optimised',
    'customize': 'customise',
    'customized': 'customised',
    'modernize': 'modernise',
    'modernized': 'modernised',
    'fiber': 'fibre',
    'meter': 'metre',
    'meters': 'metres',
    'liter': 'litre',
    'harbor': 'harbour',
    'labor': 'labour',
    'neighbor': 'neighbour',
    'neighborhood': 'neighbourhood',
    'favor': 'favour',
    'favorable': 'favourable',
    'favorite': 'favourite',
    'honor': 'honour',
    'honored': 'honoured',
    'behavior': 'behaviour',
    'aluminum': 'aluminium',
    'defense': 'defence',
    'offense': 'offence',
    'license': 'licence',
    'practicing': 'practising',
    'aging': 'ageing',
    'acknowledgment': 'acknowledgement',
    'judgment': 'judgement',
    'fulfill': 'fulfil',
    'fulfillment': 'fulfilment',
    'installment': 'instalment',
    'catalog': 'catalogue',
    'dialog': 'dialogue',
    'program': 'programme',
    'gray': 'grey',
    'plow': 'plough',
    'mold': 'mould',
    'molding': 'moulding',
    'smolder': 'smoulder'
}

def fix_spelling_in_text(text):
    """Fix US to AU spelling in text while preserving case"""
    if not text:
        return text, 0
        
    changes = 0
    for us_spelling, au_spelling in US_TO_AU_SPELLINGS.items():
        # Create case-insensitive pattern but preserve original case
        pattern = re.compile(r'\b' + re.escape(us_spelling) + r'\b', re.IGNORECASE)
        
        def replace_with_case(match):
            nonlocal changes
            original = match.group()
            changes += 1
            # Preserve the case pattern
            if original.isupper():
                return au_spelling.upper()
            elif original[0].isupper():
                return au_spelling.capitalize()
            else:
                return au_spelling
                
        text = pattern.sub(replace_with_case, text)
        
    return text, changes

def main():
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Get client
    client = manager.get_client('renowarriors', cache_enabled=False)
    if not client:
        print("Error: Could not connect to renowarriors site")
        return
        
    content_ops = ContentOperations(client)
    
    print("=== Fixing US to AU Spelling in Reno Warriors Content ===\n")
    
    # Use search replace with dry run first to preview changes
    print("Running spelling check (dry run)...\n")
    
    total_fixes = 0
    pages_fixed = 0
    
    # Check each spelling one by one
    for us_spelling, au_spelling in US_TO_AU_SPELLINGS.items():
        print(f"Checking for '{us_spelling}'...")
        
        result = content_ops.search_replace_content(
            search=us_spelling,
            replace=au_spelling,
            post_types=['page'],
            dry_run=True
        )
        
        if result['changes']:
            print(f"  Found {result['total_replacements']} instances in {len(result['changes'])} pages")
            
            # Show affected pages
            for change in result['changes']:
                print(f"    - Page {change['id']}: {change['title']} ({change['content_replacements']} in content, {change['title_replacements']} in title)")
            
            # Ask for confirmation
            confirm = input(f"\nReplace '{us_spelling}' with '{au_spelling}'? (y/n): ")
            
            if confirm.lower() == 'y':
                # Apply the changes
                actual_result = content_ops.search_replace_content(
                    search=us_spelling,
                    replace=au_spelling,
                    post_types=['page'],
                    dry_run=False
                )
                
                print(f"  ✓ Replaced {actual_result['total_replacements']} instances")
                total_fixes += actual_result['total_replacements']
                pages_fixed += actual_result['posts_modified']
            else:
                print("  Skipped")
        else:
            print(f"  No instances found")
    
    print(f"\n=== Summary ===")
    print(f"Total spelling fixes applied: {total_fixes}")
    print(f"Pages updated: {pages_fixed}")
    print("\n✓ Spelling update complete!")

if __name__ == "__main__":
    main()