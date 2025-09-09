#!/usr/bin/env python3
"""
Demo content analysis - analyze sample content to show what issues would be found
"""

import re
from analyze_derekzar_quality import detect_placeholder_text, analyze_h1_structure, analyze_seo_meta

# Sample content with various issues
sample_contents = [
    {
        'title': 'Example Page with Lorem Ipsum',
        'content': '''
        <h1>Welcome to Our Services</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. We provide excellent services.</p>
        <h2>Our Approach</h2>
        <p>Your content here - we'll add more details soon!</p>
        <h1>Another H1 Tag</h1>
        <p>This page has multiple H1s which is not ideal for SEO.</p>
        ''',
        'seo_title': 'Services',  # Too short
        'seo_description': 'Our services page'  # Too short
    },
    {
        'title': 'Page Under Construction',
        'content': '''
        <p>This page is under construction. Coming soon!</p>
        <h2>Placeholder Section</h2>
        <p>Insert text here about our upcoming features.</p>
        ''',
        'seo_title': '',  # Missing
        'seo_description': ''  # Missing
    },
    {
        'title': 'Good Example Page',
        'content': '''
        <h1>Professional Web Development Services in Denver</h1>
        <p>We specialize in creating custom WordPress websites that drive results for your business.</p>
        <h2>Our Services</h2>
        <p>From design to development, we handle every aspect of your web presence.</p>
        ''',
        'seo_title': 'Web Development Services Denver | DerekZar',
        'seo_description': 'Professional web development services in Denver. Custom WordPress sites, responsive design, and ongoing maintenance. Contact us for a free consultation.'
    }
]

def demo_analysis():
    print("🔍 Content Quality Analysis Demo")
    print("=" * 60)
    print("This demonstrates what the analysis would find on your pages:\n")
    
    for i, sample in enumerate(sample_contents, 1):
        print(f"\n{'='*60}")
        print(f"📄 Sample Page {i}: {sample['title']}")
        print(f"{'='*60}")
        
        # Analyze placeholder text
        placeholder_findings = detect_placeholder_text(sample['content'])
        print("\n🔤 Placeholder Text Analysis:")
        if placeholder_findings:
            print(f"   ⚠️  Found {len(placeholder_findings)} placeholder text instance(s):")
            for finding in placeholder_findings:
                print(f"      - \"{finding['text']}\" in: ...{finding['context']}...")
        else:
            print("   ✅ No placeholder text found")
        
        # Analyze H1 structure
        h1_analysis = analyze_h1_structure(sample['content'])
        print("\n📊 H1 Structure Analysis:")
        print(f"   H1 Count: {h1_analysis['count']}")
        if h1_analysis['h1_tags']:
            print(f"   H1 Tags Found: {h1_analysis['h1_tags']}")
        if h1_analysis['issues']:
            print(f"   ⚠️  Issues: {', '.join(h1_analysis['issues'])}")
        else:
            print("   ✅ H1 structure is good")
        
        # Analyze SEO meta (simulated)
        page_data = {
            'yoast_head_json': {
                'title': sample.get('seo_title', ''),
                'description': sample.get('seo_description', '')
            }
        }
        seo_analysis = analyze_seo_meta(page_data)
        print("\n🔍 SEO Meta Analysis:")
        if seo_analysis['title']:
            print(f"   Title ({seo_analysis['title_length']} chars): {seo_analysis['title']}")
        if seo_analysis['description']:
            print(f"   Description ({seo_analysis['description_length']} chars): {seo_analysis['description']}")
        if seo_analysis['issues']:
            print(f"   ⚠️  Issues: {', '.join(seo_analysis['issues'])}")
        else:
            print("   ✅ SEO meta data is good")
    
    print(f"\n{'='*60}")
    print("📋 Summary of What This Analysis Checks:")
    print("- Lorem ipsum and placeholder text in 12+ patterns")
    print("- H1 tag presence, count, and quality")
    print("- SEO title and description presence and length")
    print("- Content structure and semantic HTML")
    print("\nRun the full analysis on derekzar.com to check all your pages!")

if __name__ == "__main__":
    demo_analysis()