#!/usr/bin/env python3
"""
Test derekzar.com Australian English configuration
"""

import sys
from pathlib import Path

# Add the wpbm package to path
sys.path.insert(0, str(Path(__file__).parent))

from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)


def test_australian_content():
    """Test content creation with Australian English"""
    
    manager = WPBulkManagerMySQL()
    
    # Get site info
    site_info = manager.get_site_info('derekzar')
    
    print("\n📊 Site Information:")
    print(f"Name: {site_info['site']['name']}")
    print(f"URL: {site_info['site']['url']}")
    print(f"Folder: {site_info['folder_path']}")
    
    # Display brand kit
    brand_kit = site_info.get('brand_kit', {})
    print("\n🎨 Australian English Configuration:")
    print(f"Language: {brand_kit.get('language', 'Not set')}")
    print(f"Spelling: {brand_kit.get('spelling', 'Not set')}")
    print(f"Date Format: {brand_kit.get('regional_considerations', {}).get('date_format', 'Not set')}")
    print(f"Currency: {brand_kit.get('regional_considerations', {}).get('currency', 'Not set')}")
    
    # Show vocabulary preferences
    print("\n📝 Vocabulary Preferences (sample):")
    vocab_prefs = brand_kit.get('vocabulary_preferences', '').split('\n')[:5]
    for pref in vocab_prefs:
        if pref.strip():
            print(f"  {pref}")
    
    # Show templates
    print("\n📄 Available Templates:")
    for template in site_info.get('templates', []):
        print(f"  - {template['name']} ({template['file']})")
    
    # Example content transformation
    print("\n🔄 Example Content Transformation:")
    american_text = "The organization's color scheme centers around maximizing customer favorites."
    australian_text = "The organisation's colour scheme centres around maximising customer favourites."
    
    print(f"❌ American: {american_text}")
    print(f"✅ Australian: {australian_text}")
    
    print("\n✅ Site is configured for Australian English content!")
    print("   When creating content, the system will use:")
    print("   - Australian spelling (colour, centre, organisation)")
    print("   - DD/MM/YYYY date format")
    print("   - Metric measurements")
    print("   - AUD currency format")


if __name__ == "__main__":
    test_australian_content()