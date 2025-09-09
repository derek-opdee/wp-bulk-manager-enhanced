#!/usr/bin/env python3
"""
Update Reno Warriors SEO metadata and fix US to AU spelling
"""
import re
import sys
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
    'centering': 'centring',
    'organize': 'organise',
    'organizes': 'organises',
    'organized': 'organised',
    'organizing': 'organising',
    'organization': 'organisation',
    'organizations': 'organisations',
    'specialize': 'specialise',
    'specializes': 'specialises',
    'specialized': 'specialised',
    'specializing': 'specialising',
    'realize': 'realise',
    'realizes': 'realises',
    'realized': 'realised',
    'realizing': 'realising',
    'recognize': 'recognise',
    'recognizes': 'recognises',
    'recognized': 'recognised',
    'recognizing': 'recognising',
    'analyze': 'analyse',
    'analyzes': 'analyses',
    'analyzed': 'analysed',
    'analyzing': 'analysing',
    'minimize': 'minimise',
    'minimizes': 'minimises',
    'minimized': 'minimised',
    'minimizing': 'minimising',
    'maximize': 'maximise',
    'maximizes': 'maximises',
    'maximized': 'maximised',
    'maximizing': 'maximising',
    'optimize': 'optimise',
    'optimizes': 'optimises',
    'optimized': 'optimised',
    'optimizing': 'optimising',
    'prioritize': 'prioritise',
    'prioritizes': 'prioritises',
    'prioritized': 'prioritised',
    'prioritizing': 'prioritising',
    'customize': 'customise',
    'customizes': 'customises',
    'customized': 'customised',
    'customizing': 'customising',
    'modernize': 'modernise',
    'modernizes': 'modernises',
    'modernized': 'modernised',
    'modernizing': 'modernising',
    'fiber': 'fibre',
    'fibers': 'fibres',
    'theater': 'theatre',
    'theaters': 'theatres',
    'meter': 'metre',
    'meters': 'metres',
    'liter': 'litre',
    'liters': 'litres',
    'harbor': 'harbour',
    'harbors': 'harbours',
    'labor': 'labour',
    'labors': 'labours',
    'labored': 'laboured',
    'laboring': 'labouring',
    'neighbor': 'neighbour',
    'neighbors': 'neighbours',
    'neighborhood': 'neighbourhood',
    'neighborhoods': 'neighbourhoods',
    'favor': 'favour',
    'favors': 'favours',
    'favored': 'favoured',
    'favoring': 'favouring',
    'favorable': 'favourable',
    'favorite': 'favourite',
    'favorites': 'favourites',
    'honor': 'honour',
    'honors': 'honours',
    'honored': 'honoured',
    'honoring': 'honouring',
    'honorable': 'honourable',
    'behavior': 'behaviour',
    'behaviors': 'behaviours',
    'behavioral': 'behavioural',
    'endeavor': 'endeavour',
    'endeavors': 'endeavours',
    'aluminum': 'aluminium',
    'defense': 'defence',
    'defenses': 'defences',
    'offense': 'offence',
    'offenses': 'offences',
    'license': 'licence',
    'licenses': 'licences',
    'licensed': 'licensed',  # verb form stays the same
    'licensing': 'licensing',  # verb form stays the same
    'practice': 'practice',  # noun stays the same
    'practiced': 'practised',  # verb changes
    'practicing': 'practising',  # verb changes
    'practices': 'practices',  # can be noun or verb
    'aging': 'ageing',
    'acknowledgment': 'acknowledgement',
    'acknowledgments': 'acknowledgements',
    'judgment': 'judgement',
    'judgments': 'judgements',
    'fulfill': 'fulfil',
    'fulfills': 'fulfils',
    'fulfilled': 'fulfilled',
    'fulfilling': 'fulfilling',
    'fulfillment': 'fulfilment',
    'installment': 'instalment',
    'installments': 'instalments',
    'skillful': 'skilful',
    'skillfully': 'skilfully',
    'willful': 'wilful',
    'willfully': 'wilfully',
    'maneuver': 'manoeuvre',
    'maneuvers': 'manoeuvres',
    'maneuvered': 'manoeuvred',
    'maneuvering': 'manoeuvring',
    'catalog': 'catalogue',
    'catalogs': 'catalogues',
    'dialog': 'dialogue',
    'dialogs': 'dialogues',
    'analog': 'analogue',
    'analogs': 'analogues',
    'program': 'programme',  # except computer programs
    'programs': 'programmes',
    'programmed': 'programmed',
    'programming': 'programming',  # computer context stays
    'gray': 'grey',
    'grays': 'greys',
    'grayed': 'greyed',
    'graying': 'greying',
    'plow': 'plough',
    'plows': 'ploughs',
    'plowed': 'ploughed',
    'plowing': 'ploughing',
    'mold': 'mould',
    'molds': 'moulds',
    'molded': 'moulded',
    'molding': 'moulding',
    'smolder': 'smoulder',
    'smolders': 'smoulders',
    'smoldered': 'smouldered',
    'smoldering': 'smouldering',
    'estrogen': 'oestrogen',
    'pediatric': 'paediatric',
    'orthopedic': 'orthopaedic',
    'anesthesia': 'anaesthesia',
    'anesthetic': 'anaesthetic',
    'archaeology': 'archaeology',  # both acceptable
    'archeology': 'archaeology',
    'medieval': 'mediaeval',  # though medieval is common in AU too
    'encyclopedia': 'encyclopaedia',
    'encyclopedias': 'encyclopaedias'
}

def fix_spelling_in_text(text):
    """Fix US to AU spelling in text while preserving case"""
    if not text:
        return text
        
    for us_spelling, au_spelling in US_TO_AU_SPELLINGS.items():
        # Create case-insensitive pattern but preserve original case
        pattern = re.compile(r'\b' + re.escape(us_spelling) + r'\b', re.IGNORECASE)
        
        def replace_with_case(match):
            original = match.group()
            # Preserve the case pattern
            if original.isupper():
                return au_spelling.upper()
            elif original[0].isupper():
                return au_spelling.capitalize()
            else:
                return au_spelling
                
        text = pattern.sub(replace_with_case, text)
        
    return text

def generate_seo_title(page_title, location="Patterson Lakes, VIC"):
    """Generate SEO-friendly title for renovation services"""
    # Clean the title
    clean_title = page_title.strip()
    
    # Common service mappings
    service_keywords = {
        'bathroom': 'Bathroom Renovation',
        'kitchen': 'Kitchen Renovation',
        'deck': 'Deck Building',
        'decking': 'Decking Installation',
        'pergola': 'Pergola Construction',
        'renovation': 'Home Renovation',
        'extension': 'Home Extension',
        'addition': 'Home Addition',
        'remodel': 'Home Remodelling',
        'flooring': 'Flooring Installation',
        'painting': 'House Painting',
        'tiling': 'Tiling Services',
        'plastering': 'Plastering Services',
        'carpentry': 'Carpentry Services',
        'electrical': 'Electrical Services',
        'plumbing': 'Plumbing Services',
        'landscaping': 'Landscaping Services',
        'fencing': 'Fencing Installation',
        'concreting': 'Concreting Services',
        'roofing': 'Roofing Services',
        'guttering': 'Guttering Installation',
        'window': 'Window Installation',
        'door': 'Door Installation'
    }
    
    # Find matching service
    service_found = None
    for key, service in service_keywords.items():
        if key.lower() in clean_title.lower():
            service_found = service
            break
            
    if service_found:
        # Format: "Service | Southeast Melbourne | Reno Warriors"
        return f"{service_found} | Southeast Melbourne | Reno Warriors"
    else:
        # Default format for other pages
        return f"{clean_title} | Reno Warriors | {location}"

def generate_meta_description(page_title, content=""):
    """Generate meta description for renovation services"""
    # Extract key info
    location_keywords = [
        "Patterson Lakes",
        "Southeast Melbourne", 
        "Carrum",
        "Chelsea",
        "Frankston",
        "Dandenong",
        "Cranbourne",
        "Berwick",
        "Narre Warren",
        "Pakenham",
        "Mornington Peninsula"
    ]
    
    # Service-specific descriptions
    if 'bathroom' in page_title.lower():
        return "Expert bathroom renovation services in Southeast Melbourne. Based in Patterson Lakes, we transform bathrooms across Carrum, Chelsea, Frankston & surrounding suburbs. Quality workmanship guaranteed."
    elif 'kitchen' in page_title.lower():
        return "Professional kitchen renovation in Southeast Melbourne. Local Patterson Lakes builders specialising in modern kitchen makeovers. Servicing Carrum to Cranbourne. Free quotes available."
    elif 'deck' in page_title.lower() or 'decking' in page_title.lower():
        return "Quality deck building & installation in Southeast Melbourne. Patterson Lakes based carpenters creating stunning outdoor decks. Servicing Frankston to Dandenong. Call for free quote."
    elif 'pergola' in page_title.lower():
        return "Custom pergola construction in Southeast Melbourne. Local Patterson Lakes builders creating beautiful outdoor pergolas. From Chelsea to Berwick. Professional installation guaranteed."
    elif 'extension' in page_title.lower() or 'addition' in page_title.lower():
        return "Home extensions & additions in Southeast Melbourne. Patterson Lakes builders specialising in quality home expansions. Servicing Carrum to Pakenham. Fully licensed & insured."
    elif 'flooring' in page_title.lower():
        return "Professional flooring installation in Southeast Melbourne. Patterson Lakes specialists in timber, laminate, vinyl & carpet. Servicing Chelsea to Narre Warren. Quality guaranteed."
    elif 'painting' in page_title.lower():
        return "Professional house painting services in Southeast Melbourne. Patterson Lakes painters delivering quality interior & exterior painting. From Frankston to Cranbourne. Free quotes."
    elif 'contact' in page_title.lower():
        return "Contact Reno Warriors for quality renovations in Southeast Melbourne. Based in Patterson Lakes, servicing Carrum, Chelsea, Frankston & surrounds. Call 0412 345 678 for free quote."
    elif 'about' in page_title.lower():
        return "Reno Warriors - trusted renovation specialists in Southeast Melbourne. Based in Patterson Lakes, delivering quality home improvements to Carrum, Chelsea, Frankston & beyond since 2015."
    else:
        # Generic description
        return f"Quality home renovation services in Southeast Melbourne. Based in Patterson Lakes, servicing Carrum, Chelsea, Frankston & surrounding suburbs. Professional builders you can trust."

def main():
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Add site if not exists
    try:
        manager.add_site('renowarriors', 'https://renowarriors.com.au', '0ab365b5b83f46b65bf12466c404bfd3')
        print("✓ Added renowarriors.com.au to manager")
    except:
        print("✓ Site already exists")
    
    # Get client
    client = manager.get_client('renowarriors', cache_enabled=False)
    if not client:
        print("Error: Could not connect to renowarriors site")
        return
        
    content_ops = ContentOperations(client)
    
    print("\n=== Starting Reno Warriors SEO & Spelling Updates ===\n")
    
    # Get all pages
    pages = client.get_content(content_type='page', status='publish')
    print(f"Found {len(pages)} published pages\n")
    
    # Track updates
    updates_made = 0
    spelling_fixes = 0
    
    for page in pages:
        page_id = page['id']
        # Handle title as either string or dict
        title_data = page.get('title', '')
        if isinstance(title_data, dict):
            title = title_data.get('rendered', '')
        else:
            title = str(title_data)
            
        # Handle content as either string or dict
        content_data = page.get('content', '')
        if isinstance(content_data, dict):
            content = content_data.get('rendered', '')
        else:
            content = str(content_data)
        
        print(f"\nProcessing Page {page_id}: {title}")
        print(f"  URL: {page.get('link', '')}")
        
        updates = {}
        
        # Check current SEO meta
        current_seo = client.get(f'content/{page_id}')
        seo_title = current_seo.get('yoast_head_json', {}).get('title', '')
        meta_desc = current_seo.get('yoast_head_json', {}).get('description', '')
        
        # For The SEO Framework
        tsf_title = current_seo.get('meta', {}).get('_genesis_title', '')
        tsf_desc = current_seo.get('meta', {}).get('_genesis_description', '')
        
        print(f"  Current SEO Title: {seo_title or tsf_title or 'None'}")
        print(f"  Current Meta Desc: {meta_desc or tsf_desc or 'None'}")
        
        # Generate new SEO if missing
        if not (seo_title or tsf_title) or not (meta_desc or tsf_desc):
            new_seo_title = generate_seo_title(title)
            new_meta_desc = generate_meta_description(title, content)
            
            # Update via meta fields for The SEO Framework
            updates['meta'] = {
                '_genesis_title': new_seo_title,
                '_genesis_description': new_meta_desc
            }
            
            print(f"  → New SEO Title: {new_seo_title}")
            print(f"  → New Meta Desc: {new_meta_desc}")
        
        # Fix spellings in content
        original_content = content
        fixed_content = fix_spelling_in_text(content)
        
        if fixed_content != original_content:
            updates['content'] = fixed_content
            spelling_fixes += 1
            
            # Count spelling changes
            changes = 0
            for us, au in US_TO_AU_SPELLINGS.items():
                us_count = len(re.findall(r'\b' + re.escape(us) + r'\b', original_content, re.IGNORECASE))
                if us_count > 0:
                    changes += us_count
                    print(f"  → Fixed spelling: {us} → {au} ({us_count} instances)")
        
        # Apply updates if any
        if updates:
            try:
                result = client.put(f'content/{page_id}', updates)
                print(f"  ✓ Successfully updated page {page_id}")
                updates_made += 1
            except Exception as e:
                print(f"  ✗ Error updating page {page_id}: {e}")
    
    print(f"\n=== Update Summary ===")
    print(f"Total pages processed: {len(pages)}")
    print(f"Pages updated: {updates_made}")
    print(f"Pages with spelling fixes: {spelling_fixes}")
    print(f"\n✓ Reno Warriors SEO and spelling updates complete!")

if __name__ == "__main__":
    main()