#!/usr/bin/env python3
"""
Fix Opdee brand kit and ensure all sites have proper language settings
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.utils.site_manager import SiteManager
from pathlib import Path
import json

def fix_all_language_settings():
    """Fix language settings for all sites"""
    manager = WPBulkManagerMySQL()
    site_manager = SiteManager()
    
    print("🌍 Fixing Language Settings for All Sites")
    print("=" * 50)
    
    # Define language settings for each site
    language_configs = {
        'opdee': {
            'language': 'en-AU',
            'country': 'Australia',
            'spelling': 'Australian English',
            'reason': 'Opdee.com uses Australian English'
        },
        'boulderworks': {
            'language': 'en-US', 
            'country': 'United States',
            'spelling': 'American English',
            'reason': 'BoulderWorks is in Colorado, USA'
        },
        'dmbelectrical': {
            'language': 'en-AU',
            'country': 'Australia', 
            'spelling': 'Australian English',
            'reason': '.au domain - Australian business'
        },
        'renowarriors': {
            'language': 'en-AU',
            'country': 'Australia',
            'spelling': 'Australian English', 
            'reason': '.au domain - Australian business'
        },
        'lawnenforcement': {
            'language': 'en-AU',
            'country': 'Australia',
            'spelling': 'Australian English',
            'reason': '.au domain - Australian business'
        },
        'mavent': {
            'language': 'en-AU',
            'country': 'Australia',
            'spelling': 'Australian English',
            'reason': '.au domain - Australian business'
        }
    }
    
    for site_name, config in language_configs.items():
        print(f"\n📝 Processing {site_name}...")
        print(f"   Language: {config['language']}")
        print(f"   Country: {config['country']}")
        print(f"   Reason: {config['reason']}")
        
        # Ensure site has folder structure
        folder = site_manager.get_site_folder(site_name)
        if not folder:
            print(f"   📁 Creating missing folder structure...")
            site = manager.db.get_site(site_name)
            if site:
                # Create basic folder structure
                base_path = Path.home() / "Documents/WPBulkManager/sites" / site_name
                base_path.mkdir(parents=True, exist_ok=True)
                
                # Create subdirectories
                for subdir in ['templates', 'branding', 'content', 'backups', 'exports', 'logs']:
                    (base_path / subdir).mkdir(exist_ok=True)
                
                # Update database with folder path
                manager.db.update_site(site['id'], folder_path=str(base_path))
                print(f"   ✅ Created folder: {base_path}")
        
        # Create/update brand kit file
        brand_kit_path = site_manager.get_site_folder(site_name) / 'branding' / 'brand_kit.json'
        
        if config['language'] == 'en-AU':
            # Australian English settings
            brand_data = {
                'language': 'en-AU',
                'spelling_standard': 'Australian English (colour, centre, organisation, realise)',
                'vocabulary_preferences': 'Australian spelling and terminology',
                'vocabulary_avoid': 'American spelling (color, center, organization, realize)',
                'spelling_examples': {
                    'correct_au': ['colour', 'centre', 'organisation', 'realise', 'honour', 'favour', 'behaviour', 'defence', 'licence', 'analyse'],
                    'avoid_us': ['color', 'center', 'organization', 'realize', 'honor', 'favor', 'behavior', 'defense', 'license', 'analyze']
                },
                'currency_format': 'AUD ($XX.XX)',
                'measurement_system': 'Metric (metres, litres, kilograms)',
                'date_format': 'DD/MM/YYYY',
                'terminology': {
                    'preferred': ['mobile phone', 'lift', 'car park', 'footpath', 'petrol', 'rubbish bin', 'jumper', 'biscuit', 'holiday'],
                    'avoid': ['cell phone', 'elevator', 'parking lot', 'sidewalk', 'gas', 'trash can', 'sweater', 'cookie', 'vacation']
                },
                'compliance': 'Australian Consumer Law, Fair Trading Acts',
                'updated_at': '2025-06-09T18:38:00Z'
            }
        else:
            # US English settings  
            brand_data = {
                'language': 'en-US',
                'spelling_standard': 'American English (color, center, organization, realize)',
                'vocabulary_preferences': 'American spelling and terminology',
                'currency_format': 'USD ($XX.XX)',
                'measurement_system': 'Imperial (feet, gallons, pounds) with metric alternatives',
                'date_format': 'MM/DD/YYYY',
                'compliance': 'US Federal Trade Commission, State regulations',
                'updated_at': '2025-06-09T18:38:00Z'
            }
        
        # Load existing brand kit and merge
        existing_brand = {}
        if brand_kit_path.exists():
            with open(brand_kit_path, 'r') as f:
                existing_brand = json.load(f)
        
        # Merge with new language settings
        existing_brand.update(brand_data)
        
        # Save updated brand kit
        brand_kit_path.parent.mkdir(exist_ok=True)
        with open(brand_kit_path, 'w') as f:
            json.dump(existing_brand, f, indent=2)
        
        print(f"   ✅ Updated brand kit with {config['language']} settings")
    
    print(f"\n🎯 Language Settings Summary:")
    print("   🇦🇺 Australian English (en-AU):")
    au_sites = [name for name, config in language_configs.items() if config['language'] == 'en-AU']
    for site in au_sites:
        print(f"      • {site}")
    
    print("   🇺🇸 American English (en-US):")
    us_sites = [name for name, config in language_configs.items() if config['language'] == 'en-US']
    for site in us_sites:
        print(f"      • {site}")

def verify_language_settings():
    """Verify all language settings are applied correctly"""
    site_manager = SiteManager()
    
    print(f"\n" + "=" * 60)
    print("🔍 VERIFICATION: Language Settings")
    print("=" * 60)
    
    sites = ['opdee', 'boulderworks', 'dmbelectrical', 'renowarriors', 'lawnenforcement', 'mavent']
    
    for site_name in sites:
        print(f"\n🏢 {site_name.upper()}")
        
        brand_kit = site_manager.get_brand_kit(site_name)
        if brand_kit:
            lang = brand_kit.get('language', 'Not set')
            spelling = brand_kit.get('spelling_standard', 'Not specified')
            
            if lang == 'en-AU':
                flag = "🇦🇺"
                expected = "Australian English"
            elif lang == 'en-US':
                flag = "🇺🇸"
                expected = "American English"
            else:
                flag = "❓"
                expected = "Unknown"
            
            print(f"   {flag} Language: {lang}")
            print(f"   📝 Spelling: {spelling}")
            print(f"   ✅ Status: {expected}")
        else:
            print("   ❌ Brand kit not found")

if __name__ == "__main__":
    fix_all_language_settings()
    verify_language_settings()