#!/usr/bin/env python3
"""Transform page 4732 content with proper dynamic fields"""

from wpbm_assistant import wpbm_connect
import re

def transform_content():
    assistant = wpbm_connect()
    
    # Get the current page content
    page = assistant.get_page_content(4732)
    
    if not page:
        print("Could not fetch page 4732")
        return
    
    original_content = page['content']
    print("Transforming content with proper dynamic fields...")
    
    # Start with the original content
    content = original_content
    
    # MAIN HEADING - Fix the H1
    content = re.sub(
        r'AI Development &amp; Web App Integration for Websites',
        '[search_term] in [location] | Professional AI Solutions',
        content
    )
    
    # HERO SECTION
    content = re.sub(
        r'Build an AI-Powered Web Application that suits your business',
        'Get Expert [search_term] Solutions for Your [location] Business',
        content
    )
    
    # Opening paragraph
    content = re.sub(
        r'We create AI-powered web applications and integrate intelligent features',
        'We deliver professional [search_term] in [location], creating intelligent solutions',
        content
    )
    
    content = re.sub(
        r'Our AI integrations work across all facets of your business',
        'Our [search_term] solutions work across all facets of your [location] business',
        content
    )
    
    # Fix "Your business will gain"
    content = re.sub(
        r'Your business will gain practical AI solutions',
        'Your [location] business will gain practical solutions',
        content
    )
    
    # Ready to build line
    content = re.sub(
        r'Ready to build AI integrations that actually work for your business\?',
        'Ready to transform your business with professional [search_term]?',
        content
    )
    
    # SERVICES SECTION HEADING
    content = re.sub(
        r'Our AI Development &amp; Integration Services',
        'Our [search_term] Services in [location]',
        content
    )
    
    # SERVICE BOXES
    # Box 1: Customer Onboarding
    content = re.sub(
        r'using visual interfaces and AI-powered assistance',
        'using visual interfaces powered by [search_term]',
        content
    )
    
    # Box 2: Seamless AI Integration
    content = re.sub(
        r'Seamless AI Integration Beyond Chatbots',
        'Advanced [search_term] Solutions',
        content
    )
    
    content = re.sub(
        r'We build AI integrations so natural and helpful',
        'We build [search_term] solutions so natural and helpful',
        content
    )
    
    # Box 3: Custom Internal AI Tools
    content = re.sub(
        r'Custom Internal AI Tools for Business Operations',
        'Custom [search_term] for Operations',
        content
    )
    
    content = re.sub(
        r'We develop dependable internal AI systems',
        'We develop dependable [search_term] systems',
        content
    )
    
    # Box 4: AI-Powered Customer Experience
    content = re.sub(
        r'AI-Powered Customer Experience Systems',
        '[search_term]-Powered Experience Systems',
        content
    )
    
    content = re.sub(
        r'We create customer-facing AI systems',
        'We create customer-facing [search_term] solutions',
        content
    )
    
    # Box 5: Intelligent Data Processing
    content = re.sub(
        r'We build AI systems that transform raw business data',
        'We build [search_term] systems that transform raw data',
        content
    )
    
    # Box 6: Full-Stack AI Web Application
    content = re.sub(
        r'Full-Stack AI Web Application Development',
        'Full-Stack [search_term] Development',
        content
    )
    
    content = re.sub(
        r'with AI capabilities built into the core',
        'with [search_term] capabilities built into the core',
        content
    )
    
    # Box 7: Custom AI API Integration
    content = re.sub(
        r'Custom AI API Integration &amp; Development',
        'Custom API & [search_term] Development',
        content
    )
    
    content = re.sub(
        r'We integrate leading AI platforms',
        'We integrate leading platforms for [search_term]',
        content
    )
    
    # Box 8: Enterprise AI Infrastructure
    content = re.sub(
        r'Enterprise AI Infrastructure &amp; Deployment',
        'Enterprise [search_term] Deployment',
        content
    )
    
    content = re.sub(
        r'We deploy AI-integrated applications',
        'We deploy [search_term] applications',
        content
    )
    
    # WHY CHOOSE SECTION
    content = re.sub(
        r'Why Choose Opdee',
        'Why Choose Opdee for [search_term] in [location]',
        content
    )
    
    content = re.sub(
        r'We create AI tools that businesses rely on',
        'We create [search_term] solutions that [location] businesses rely on',
        content
    )
    
    # Fix expertise section
    content = re.sub(
        r'We handle every aspect of AI development',
        'We handle every aspect of [search_term]',
        content
    )
    
    content = re.sub(
        r'Our team understands both traditional web development and cutting-edge AI integration',
        'Our [location] team understands both traditional development and cutting-edge [search_term]',
        content
    )
    
    # Business-Ready section
    content = re.sub(
        r'Business-Ready AI Solutions',
        'Business-Ready [search_term] Solutions',
        content
    )
    
    content = re.sub(
        r'We create AI solutions that solve real business problems',
        'We create [search_term] solutions that solve real problems',
        content
    )
    
    # Architecture section
    content = re.sub(
        r'We build AI-integrated web applications with growth in mind',
        'We build [search_term] applications with growth in mind',
        content
    )
    
    # Security section
    content = re.sub(
        r'security measures specifically designed for AI-integrated applications',
        'security measures specifically designed for [search_term] applications',
        content
    )
    
    # FAQ SECTION - Fix all questions
    faqs = [
        (r'How do you test and ensure the quality of AI implementations\?',
         'How do you test and ensure the quality of [search_term] implementations?'),
        
        (r'What types of AI integration application can OpDee Digital develop',
         'What types of [search_term] solutions can Opdee develop'),
        
        (r'How do you ensure AI integration applications integrate seamlessly',
         'How do you ensure [search_term] solutions integrate seamlessly'),
        
        (r"What's involved in the AI integration and integration process\?",
         "What's involved in the [search_term] implementation process?"),
        
        (r'How do you measure the success and ROI of AI implementations\?',
         'How do you measure the success and ROI of [search_term] implementations?'),
        
        (r'How long does it typically take to develop and integrate an AI integration application\?',
         'How long does it typically take to implement [search_term] solutions?'),
        
        (r'Can you help train our team to manage the AI integration applications',
         'Can you help train our [location] team to manage [search_term] solutions'),
        
        (r'Do we need large amounts of data to implement effective AI integration applications\?',
         'Do we need large amounts of data to implement effective [search_term]?'),
        
        (r'What if our AI integration application needs to scale',
         'What if our [search_term] solution needs to scale'),
        
        (r'How do you ensure AI implementations don\'t become technical debt\?',
         'How do you ensure [search_term] implementations don\'t become technical debt?'),
        
        (r'What makes your AI integrations different from basic chatbot solutions\?',
         'What makes your [search_term] solutions different from basic chatbot solutions?'),
        
        (r'How do you handle data security and privacy in AI implementations\?',
         'How do you handle data security and privacy in [search_term] implementations?'),
        
        (r'What happens if the AI makes mistakes or provides incorrect information\?',
         'What happens if the system makes mistakes or provides incorrect information?'),
        
        (r'Do you provide AI integration services for specific industries',
         'Do you provide [search_term] solutions for specific industries'),
        
        (r'How do you stay current with rapidly evolving AI technologies\?',
         'How do you stay current with rapidly evolving technologies?'),
        
        (r"What's the difference between working with OpDee versus other AI integration companies\?",
         "What's the difference between working with Opdee versus other [search_term] providers in [location]?")
    ]
    
    for old, new in faqs:
        content = re.sub(old, new, content)
    
    # Add location to more places
    content = re.sub(
        r'that businesses rely on for critical operations',
        'that [location] businesses rely on for critical operations',
        content
    )
    
    content = re.sub(
        r'From automated document processing',
        'From automated processing',
        content
    )
    
    # Fix any double AI references
    content = re.sub(r'AI AI', 'AI', content)
    content = re.sub(r'AI-AI', 'AI', content)
    
    # Save the transformed content
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_4732_final.html', 'w') as f:
        f.write(content)
    
    # Count dynamic fields
    search_term_count = content.count('[search_term]')
    search_terms_count = content.count('[search_terms]')
    location_count = content.count('[location]')
    
    print(f"\nDynamic field usage:")
    print(f"[search_term]: {search_term_count} occurrences")
    print(f"[search_terms]: {search_terms_count} occurrences")
    print(f"[location]: {location_count} occurrences")
    
    print("\n✅ Content transformed and saved!")
    
    # Now update the page
    from wpbm_manager import WPBulkManager
    import requests
    
    manager = WPBulkManager()
    sites = manager.get_sites('active')
    
    if sites:
        site = sites[0]
        api_key = manager.get_site_api_key(site['id'])
        
        if api_key:
            print("\nUpdating page 4732...")
            try:
                response = requests.put(
                    f"{site['url']}/wp-json/wpbm/v1/content/4732",
                    headers={'X-API-Key': api_key},
                    json={'content': content},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ Page content updated successfully!")
                else:
                    print(f"❌ Update failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Test renders
    print("\nExample renders:")
    test_terms = [
        ('AI Integration', 'Melbourne'),
        ('AI Web Development Services', 'Sydney'),
        ('AI Stack Development Services', 'Brisbane')
    ]
    
    # Get a sample heading
    match = re.search(r'Get Expert \[search_term\] Solutions for Your \[location\] Business', content)
    if match:
        for term, loc in test_terms:
            sample = "Get Expert [search_term] Solutions for Your [location] Business"
            rendered = sample.replace('[search_term]', term).replace('[location]', loc)
            print(f"\n{term} + {loc}:")
            print(f"  → {rendered}")

if __name__ == "__main__":
    transform_content()