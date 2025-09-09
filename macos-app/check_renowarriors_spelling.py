#!/usr/bin/env python3
"""
Check and fix US to AU spelling in Reno Warriors content
"""
import re
from wpbm_manager_v2 import WPBulkManagerV2
from wpbm.api.client import WPBMClient

# US to AU spelling mappings (abbreviated for checking)
US_TO_AU_SPELLINGS = {
    'color': 'colour',
    'colors': 'colours',
    'colored': 'coloured',
    'center': 'centre',
    'organize': 'organise',
    'organized': 'organised',
    'specialize': 'specialise',
    'specialized': 'specialised',
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
    'practice': 'practice',
    'practiced': 'practised',
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
    'molding': 'moulding'
}

def check_spelling_in_text(text):
    """Check for US spellings in text"""
    issues = []
    
    for us_spelling, au_spelling in US_TO_AU_SPELLINGS.items():
        pattern = re.compile(r'\b' + re.escape(us_spelling) + r'\b', re.IGNORECASE)
        matches = pattern.finditer(text)
        
        for match in matches:
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end]
            issues.append({
                'us': us_spelling,
                'au': au_spelling,
                'context': context.replace('\n', ' ').strip(),
                'position': match.start()
            })
    
    return issues

def main():
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Get client
    client = manager.get_client('renowarriors', cache_enabled=False)
    if not client:
        print("Error: Could not connect to renowarriors site")
        return
    
    print("=== Checking Reno Warriors Content for US Spellings ===\n")
    
    # Get all pages
    pages = client.get_content(content_type='page', status='publish')
    print(f"Found {len(pages)} published pages\n")
    
    total_issues = 0
    pages_with_issues = 0
    
    for page in pages:
        page_id = page['id']
        
        # Get full page content directly via API
        try:
            full_page = client.get(f'pages/{page_id}')
            
            # Handle title
            title_data = full_page.get('title', '')
            if isinstance(title_data, dict):
                title = title_data.get('rendered', '')
            else:
                title = str(title_data)
            
            # Handle content
            content_data = full_page.get('content', '')
            if isinstance(content_data, dict):
                content = content_data.get('rendered', '')
            else:
                content = str(content_data)
            
            # Check for spelling issues
            title_issues = check_spelling_in_text(title)
            content_issues = check_spelling_in_text(content)
            
            if title_issues or content_issues:
                pages_with_issues += 1
                print(f"\nPage {page_id}: {title}")
                print(f"  URL: {full_page.get('link', '')}")
                
                if title_issues:
                    print("  Title issues:")
                    for issue in title_issues:
                        print(f"    - '{issue['us']}' → '{issue['au']}'")
                        total_issues += 1
                
                if content_issues:
                    print(f"  Content issues ({len(content_issues)} found):")
                    # Show first 5 issues
                    for issue in content_issues[:5]:
                        print(f"    - '{issue['us']}' → '{issue['au']}' in: ...{issue['context']}...")
                        total_issues += 1
                    
                    if len(content_issues) > 5:
                        print(f"    ... and {len(content_issues) - 5} more")
                        total_issues += len(content_issues) - 5
                        
        except Exception as e:
            print(f"Error checking page {page_id}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Total pages checked: {len(pages)}")
    print(f"Pages with US spellings: {pages_with_issues}")
    print(f"Total spelling issues found: {total_issues}")
    
    if pages_with_issues > 0:
        print("\nRun update_renowarriors_spelling.py to fix these issues.")

if __name__ == "__main__":
    main()