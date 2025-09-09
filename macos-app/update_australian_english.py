#!/usr/bin/env python3
"""
Update Australian English settings for .au sites and Opdee.com
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
import json

def update_australian_english():
    """Update language and spelling for Australian sites"""
    manager = WPBulkManagerMySQL()
    
    # Sites that should use Australian English
    australian_sites = {
        'opdee': {
            'reason': 'Opdee.com should use Australian English',
            'language': 'en-AU',
            'spelling': 'Australian English (colour, centre, organisation, realise)'
        },
        'dmbelectrical': {
            'reason': '.au domain - Australian electrical services',
            'language': 'en-AU', 
            'spelling': 'Australian English (colour, centre, organisation, realise)'
        },
        'renowarriors': {
            'reason': '.au domain - Australian renovation services',
            'language': 'en-AU',
            'spelling': 'Australian English (colour, centre, organisation, realise)'
        },
        'lawnenforcement': {
            'reason': '.au domain - Australian lawn care services', 
            'language': 'en-AU',
            'spelling': 'Australian English (colour, centre, organisation, realise)'
        },
        'mavent': {
            'reason': '.au domain - Australian business solutions',
            'language': 'en-AU',
            'spelling': 'Australian English (colour, centre, organisation, realise)'
        }
    }
    
    print("🇦🇺 Updating Australian English Settings")
    print("=" * 50)
    
    for site_name, config in australian_sites.items():
        print(f"\n📝 Updating {site_name}...")
        print(f"   Reason: {config['reason']}")
        
        # Get current site info
        site_info = manager.get_site_info(site_name)
        if 'error' in site_info:
            print(f"   ❌ Error: {site_info['error']}")
            continue
        
        # Prepare Australian English brand data
        au_brand_data = {
            'language': config['language'],
            'spelling_standard': config['spelling'],
            'vocabulary_preferences': 'Australian English spelling and terminology',
            'vocabulary_avoid': 'American spelling (color, center, organization, realize)',
            'content_guidelines': {
                'spelling': [
                    'colour (not color)',
                    'centre (not center)', 
                    'organisation (not organization)',
                    'realise (not realize)',
                    'honour (not honor)',
                    'favour (not favor)',
                    'behaviour (not behavior)',
                    'neighbour (not neighbor)',
                    'theatre (not theater)',
                    'metre (not meter)',
                    'litre (not liter)',
                    'defence (not defense)',
                    'licence (not license)',
                    'practise (verb, not practice)',
                    'analyse (not analyze)'
                ],
                'terminology': [
                    'mobile phone (not cell phone)',
                    'lift (not elevator)', 
                    'car park (not parking lot)',
                    'footpath (not sidewalk)',
                    'petrol (not gas)',
                    'rubbish bin (not trash can)',
                    'jumper (not sweater)',
                    'biscuit (not cookie)',
                    'holiday (not vacation)'
                ]
            },
            'local_compliance': 'Australian Consumer Law, Fair Trading Acts',
            'currency_format': 'AUD ($XX.XX)',
            'measurement_system': 'Metric (metres, litres, kilograms)',
            'date_format': 'DD/MM/YYYY (Australian standard)'
        }
        
        # Update brand voice
        success = manager.update_brand_voice(site_name, au_brand_data)
        
        if success:
            print(f"   ✅ Updated with Australian English settings")
            print(f"   📍 Language: {config['language']}")
            print(f"   📝 Spelling: Australian standard")
        else:
            print(f"   ❌ Failed to update brand voice")
    
    print(f"\n🎯 Summary:")
    print(f"Updated {len(australian_sites)} sites with Australian English:")
    for site_name in australian_sites.keys():
        print(f"   • {site_name} → en-AU")
    
    print(f"\n📖 Australian English Guidelines Applied:")
    print("   • Spelling: colour, centre, organisation, realise")
    print("   • Currency: AUD format")
    print("   • Measurements: Metric system")
    print("   • Date format: DD/MM/YYYY")
    print("   • Terminology: Australian terms preferred")
    print("   • Compliance: Australian Consumer Law")

def show_brand_voice_summary():
    """Show updated brand voice for all sites"""
    manager = WPBulkManagerMySQL()
    
    print(f"\n" + "=" * 60)
    print("📋 UPDATED BRAND VOICE SUMMARY")
    print("=" * 60)
    
    sites = manager.list_sites()
    
    for site in sites:
        print(f"\n🏢 {site['name'].upper()}")
        print(f"   URL: {site['url']}")
        
        # Get brand kit
        brand_kit = manager.site_manager.get_brand_kit(site['name'])
        if brand_kit:
            print(f"   Language: {brand_kit.get('language', 'Not set')}")
            print(f"   Spelling: {brand_kit.get('spelling_standard', 'Not specified')}")
            print(f"   Voice: {brand_kit.get('brand_voice', 'Not set')}")
        else:
            print("   Brand Kit: Not found")

if __name__ == "__main__":
    update_australian_english()
    show_brand_voice_summary()