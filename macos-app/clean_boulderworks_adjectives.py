#!/usr/bin/env python3
"""Clean up excessive adjectives from BoulderWorks pages"""

import re
import requests
import json
from html import unescape

# BoulderWorks API credentials
url = 'https://www.boulderworks.net'
api_key = 'gq1aoxaYyiYGn8o7nTMNOZwLwm0TNBau'

# Pages to clean
pages = [
    (1987, 'Large Format Laser Cutting'),
    (1972, 'Large Format Laser Engraving'),
    (795, 'Metal Cutting'),
    (788, 'Laser Marking & Etching')
]

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

def get_page_content(page_id):
    """Get page content from WordPress"""
    # First try the wpbm endpoint
    response = requests.get(
        f'{url}/wp-json/wpbm/v1/content/{page_id}',
        headers={'X-API-Key': api_key},
        timeout=10
    )
    if response.status_code == 200:
        return response.json()
    
    # Fallback to standard WordPress API
    response = requests.get(f'{url}/wp-json/wp/v2/pages/{page_id}', timeout=10)
    if response.status_code == 200:
        data = response.json()
        return {'content': data.get('content', {}).get('rendered', '')}
    return None

def update_page(page_id, new_content):
    """Update page content in WordPress"""
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    data = {
        'content': new_content
    }
    
    response = requests.put(
        f'{url}/wp-json/wpbm/v1/content/{page_id}',
        headers=headers,
        json=data,
        timeout=30
    )
    
    return response.status_code == 200

def update_page_with_details(page_id, new_content):
    """Update page content and return details"""
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    data = {
        'content': new_content
    }
    
    try:
        response = requests.put(
            f'{url}/wp-json/wpbm/v1/content/{page_id}',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return {'success': True}
        else:
            return {'success': False, 'error': f'Status {response.status_code}: {response.text[:200]}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Process each page
for page_id, page_name in pages:
    print(f'\nProcessing {page_name} (ID: {page_id})...')
    
    # Get current content
    page_data = get_page_content(page_id)
    if not page_data:
        print(f'Error: Could not fetch page {page_id}')
        continue
    
    # Get the content
    original_content = page_data.get('content', '')
    
    # Clean the content
    cleaned_content = clean_content(original_content)
    
    # Show changes
    if original_content != cleaned_content:
        print(f'Content cleaned for {page_name}')
        
        # Save cleaned content for review
        with open(f'{page_id}_cleaned.html', 'w') as f:
            f.write(cleaned_content)
        
        # Update the page
        result = update_page_with_details(page_id, cleaned_content)
        if result['success']:
            print(f'✅ Successfully updated {page_name}')
        else:
            print(f'❌ Failed to update {page_name}: {result["error"]}')
    else:
        print(f'No changes needed for {page_name}')

print('\nCleanup complete!')