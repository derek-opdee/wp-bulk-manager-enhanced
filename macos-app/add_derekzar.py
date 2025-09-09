#!/usr/bin/env python3
"""
Add derekzar.com to WP Bulk Manager with Australian English settings
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the wpbm package to path
sys.path.insert(0, str(Path(__file__).parent))

from wpbm_manager_mysql import WPBulkManagerMySQL
from wpbm.utils.logger import get_logger

logger = get_logger(__name__)


def add_derekzar_site():
    """Add derekzar.com with Australian English configuration"""
    
    manager = WPBulkManagerMySQL()
    
    # Site configuration
    site_config = {
        'name': 'derekzar',
        'url': 'https://derekzar.com',
        'api_key': '0b2d82ec91d2d876558ce460e57a7a1e',
        'brand_voice': 'Professional Australian tone with clear, direct communication'
    }
    
    # Add the site
    print(f"\n🌐 Adding site: {site_config['name']}")
    result = manager.add_site(**site_config)
    
    if not result['success']:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return False
    
    print(f"✅ Site added successfully with ID: {result['site_id']}")
    print(f"📁 Folder created at: {result['folder_path']}")
    
    # Australian English brand kit configuration
    australian_brand_kit = {
        'brand_voice': 'Professional Australian tone with clear, direct communication',
        'language': 'en-AU',
        'spelling': 'Australian',
        'tone_attributes': ['professional', 'approachable', 'knowledgeable', 'Australian'],
        'vocabulary_preferences': '''Australian spelling and terminology:
- colour (not color)
- centre (not center)
- organisation (not organization)
- realise (not realize)
- favourite (not favorite)
- honour (not honor)
- labour (not labor)
- programme (for computer programs)
- defence (not defense)
- licence (noun), license (verb)
- practise (verb), practice (noun)''',
        'vocabulary_avoid': '''Avoid American spellings:
- color, center, organization, realize
- favorite, honor, labor, defense
- Avoid overly formal or British expressions
- Avoid slang unless contextually appropriate''',
        'writing_style': '''Australian professional style:
- Clear, direct communication
- Professional but approachable tone
- Use active voice where possible
- Short, punchy sentences for web content
- Include relevant local context where appropriate''',
        'content_guidelines': {
            'do': [
                'Use Australian English spelling consistently',
                'Write in a clear, professional tone',
                'Be direct and to the point',
                'Use active voice for engagement',
                'Include Australian context where relevant',
                'Use metric measurements (kilometres, metres)',
                'Format dates as DD/MM/YYYY',
                'Use Australian currency format ($100, not 100$)'
            ],
            'dont': [
                'Mix spelling conventions (US/UK/AU)',
                'Use overly formal or stuffy language',
                'Use American idioms or expressions',
                'Use imperial measurements without metric',
                'Format dates as MM/DD/YYYY'
            ]
        },
        'regional_considerations': {
            'timezone': 'Australia/Sydney (AEDT/AEST)',
            'currency': 'AUD ($)',
            'date_format': 'DD/MM/YYYY',
            'measurement_system': 'Metric',
            'phone_format': '+61 X XXXX XXXX'
        },
        'seo_guidelines': {
            'local_targeting': 'Australian audience',
            'spelling_consistency': 'Always use Australian spelling for SEO',
            'local_keywords': 'Include .au domain references where relevant'
        }
    }
    
    # Update brand kit
    print("\n🎨 Configuring Australian English brand settings...")
    if manager.update_brand_voice(site_config['name'], australian_brand_kit):
        print("✅ Australian English brand kit configured successfully")
    else:
        print("⚠️  Warning: Could not update brand kit")
    
    # Create Australian-specific templates
    print("\n📝 Creating Australian English templates...")
    
    # Contact page template with Australian formatting
    contact_template = '''<!-- Australian Contact Page Template -->
<!-- Variables: {business_name}, {phone}, {email}, {address}, {abn} -->

<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Contact {business_name}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We'd love to hear from you. Get in touch with our team for enquiries about our services.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Contact Details</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<li><strong>Phone:</strong> {phone}</li>
<li><strong>Email:</strong> <a href="mailto:{email}">{email}</a></li>
<li><strong>Address:</strong> {address}</li>
<li><strong>ABN:</strong> {abn}</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Business Hours</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Monday - Friday: 9:00am - 5:00pm AEST<br>
Saturday - Sunday: Closed<br>
Public Holidays: Closed</p>
<!-- /wp:paragraph -->'''
    
    # About page template with Australian spelling
    about_template = '''<!-- Australian About Page Template -->
<!-- Variables: {company_name}, {year_established}, {mission} -->

<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">About {company_name}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Established in {year_established}, we're proud to be an Australian-owned and operated organisation dedicated to delivering exceptional service to our clients across Australia.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Our Mission</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{mission}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Why Choose Us</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<li>100% Australian owned and operated</li>
<li>Personalised service tailored to your needs</li>
<li>Industry-recognised expertise</li>
<li>Commitment to quality and excellence</li>
</ul>
<!-- /wp:list -->'''
    
    # Save templates
    folder = manager.site_manager.get_site_folder(site_config['name'])
    if folder:
        templates_dir = folder / 'templates'
        
        with open(templates_dir / 'contact-au.html', 'w') as f:
            f.write(contact_template)
        print("✅ Created contact-au.html template")
        
        with open(templates_dir / 'about-au.html', 'w') as f:
            f.write(about_template)
        print("✅ Created about-au.html template")
    
    # Test the connection
    print("\n🔌 Testing connection to WordPress site...")
    client = manager.get_client(site_config['name'])
    
    if client:
        try:
            # Test with a simple API call
            test_response = client.get_content('posts', params={'per_page': 1})
            print("✅ Connection successful!")
            print(f"   API is responding correctly")
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            print("   Please check:")
            print("   - The API key is correct")
            print("   - The WP Bulk Manager Client plugin is installed and activated")
            print("   - The site URL is accessible")
    
    # Display summary
    print("\n" + "="*60)
    print("📊 SITE CONFIGURATION SUMMARY")
    print("="*60)
    print(f"Site Name:     {site_config['name']}")
    print(f"URL:           {site_config['url']}")
    print(f"Language:      Australian English (en-AU)")
    print(f"Spelling:      Australian")
    print(f"Date Format:   DD/MM/YYYY")
    print(f"Currency:      AUD ($)")
    print(f"Measurements:  Metric")
    print(f"Folder:        {result['folder_path']}")
    print("="*60)
    
    # Show site info
    site_info = manager.get_site_info(site_config['name'])
    if site_info and not site_info.get('error'):
        print(f"\n✅ Site successfully configured with Australian English settings!")
        print(f"   Brand Kit: {site_info['folder_path']}/branding/brand_kit.json")
        print(f"   Templates: {site_info['folder_path']}/templates/")
    
    return True


if __name__ == "__main__":
    add_derekzar_site()