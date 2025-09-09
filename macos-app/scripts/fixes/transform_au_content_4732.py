#!/usr/bin/env python3
"""Transform page 4732 content to Australian English with direct, conversational tone"""

from wpbm_assistant import wpbm_connect
from wpbm_manager import WPBulkManager
import requests
import re

def transform_to_australian_content():
    assistant = wpbm_connect()
    
    # Get the current page content
    page = assistant.get_page_content(4732)
    
    if not page:
        print("Could not fetch page 4732")
        return
    
    # Read the current transformed content
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_4732_final.html', 'r') as f:
        content = f.read()
    
    print("Transforming content to Australian English with direct, conversational tone...")
    
    # MAIN HEADING - More direct
    content = re.sub(
        r'\[search_term\] in \[location\] \| Professional AI Solutions',
        '[search_term] in [location] | Opdee Digital',
        content
    )
    
    # HERO SECTION - More conversational
    content = re.sub(
        r'Get Expert \[search_term\] Solutions for Your \[location\] Business',
        'Need [search_term] in [location]? Let\'s Talk',
        content
    )
    
    # Opening paragraph - Remove adjectives, be direct
    content = re.sub(
        r'We deliver professional \[search_term\] in \[location\], creating intelligent solutions that deliver employee productivity gains, customer experiences people actually want to use and enjoy, and comprehensive business analytics for complete operational visibility\.',
        'We deliver [search_term] in [location]. Our solutions boost productivity, improve customer experience, and give you clear business insights.',
        content
    )
    
    content = re.sub(
        r'Our \[search_term\] solutions work across all facets of your \[location\] business using modern frameworks and cloud platforms\.',
        'Our [search_term] works with your existing systems and scales as you grow.',
        content
    )
    
    # Fix "Your business will gain" - More direct
    content = re.sub(
        r'Your \[location\] business will gain practical solutions that solve real problems, with systems employees love using, customers enjoy interacting with, and management tools that provide clear insights for better decision making\.',
        'Your [location] business gets solutions that actually work. Staff find them easy to use, customers get better service, and you get the data you need to make decisions.',
        content
    )
    
    # Ready to build line - Conversational
    content = re.sub(
        r'Ready to transform your business with professional \[search_term\]\? Let us show you what\'s possible\.',
        'Ready to see how [search_term] can help your business? Let\'s chat.',
        content
    )
    
    # SERVICE BOXES - More direct language
    
    # Box 1: Customer Onboarding - Simplify
    content = re.sub(
        r'We create \[search_term\]-powered onboarding systems that guide customers through complex processes using visual interfaces powered by \[search_term\]\. Our solutions simplify customer registration, account setup, and service configuration while collecting valuable data for business intelligence\.',
        'We build [search_term] onboarding that makes signup easy. Customers breeze through registration while you collect the data you need.',
        content
    )
    
    # Box 2: Seamless Integration - Remove marketing speak
    old_text = r'We build \[search_term\] solutions so natural and helpful that customers won\'t believe the interaction is AI-generated\. Our solutions go beyond simple chatbots to create comprehensive tools that customers genuinely depend upon for solving real problems and completing important tasks\.'
    new_text = 'We build [search_term] that feels natural. Not just chatbots - real tools your customers will actually use.'
    content = re.sub(old_text, new_text, content)
    
    # Box 3: Internal Tools - Be specific
    content = re.sub(
        r'We develop dependable \[search_term\] systems that \[location\] businesses rely on for critical operations\. From automated document processing and data analysis to workflow optimisation and decision support, our tools become essential parts of daily business operations\.',
        'We develop [search_term] for [location] businesses. Automate documents, analyse data, streamline workflows - tools your team will use every day.',
        content
    )
    
    # Box 4: Customer Experience - Conversational
    content = re.sub(
        r'We create customer-facing \[search_term\] solutions that feel intuitive and genuinely helpful rather than obviously artificial\. Our solutions integrate seamlessly into existing customer workflows and provide value that keeps users engaged and satisfied\.',
        'We create [search_term] your customers want to use. No clunky interfaces - just helpful tools that fit naturally into their experience.',
        content
    )
    
    # Box 5: Data Processing - Clear benefits
    content = re.sub(
        r'We build \[search_term\] systems that transform raw data into actionable insights, providing comprehensive views across all business channels and operations\. Our solutions help businesses understand performance, identify opportunities, and make informed decisions\.',
        'Turn your data into insights with [search_term]. See what\'s working, spot opportunities, make better decisions.',
        content
    )
    
    # Box 6: Full-Stack Development - Direct
    content = re.sub(
        r'We develop complete web applications with \[search_term\] capabilities built into the core functionality\. Our applications feature intelligent automation, dynamic content generation, and adaptive interfaces that improve business operations and customer satisfaction\.',
        'We build complete web apps with [search_term] at the core. Smart automation, dynamic content, interfaces that adapt - everything working together.',
        content
    )
    
    # Box 7: API Integration - Technical but clear
    content = re.sub(
        r'We integrate leading platforms for \[search_term\] and develop custom APIs that connect your \[search_term\] capabilities with existing business systems\. Our implementations ensure reliable performance and seamless operation within established workflows\.',
        'Connect [search_term] to your existing systems. We handle the technical bits so everything just works.',
        content
    )
    
    # Box 8: Enterprise - Straightforward
    content = re.sub(
        r'We deploy \[search_term\] applications on enterprise-grade cloud platforms with security, scalability, and performance optimisation designed for business-critical operations that teams and customers depend upon daily\.',
        'Deploy [search_term] that scales. Secure, fast, reliable - built for businesses that can\'t afford downtime.',
        content
    )
    
    # WHY CHOOSE SECTION - More personal
    content = re.sub(
        r'We create \[search_term\] solutions that \[location\] businesses rely on for critical operations and customers depend on for important tasks\.',
        'We build [search_term] that [location] businesses trust. Real solutions for real problems.',
        content
    )
    
    # Fix expertise section - Conversational
    content = re.sub(
        r'We handle every aspect of \[search_term\] from initial concept through deployment and maintenance\.',
        'We handle your [search_term] project from start to finish.',
        content
    )
    
    content = re.sub(
        r'Our \[location\] team understands both traditional development and cutting-edge \[search_term\] implementation, ensuring seamless functionality across all components\.',
        'Our [location] team knows both traditional dev and modern [search_term]. Everything works together properly.',
        content
    )
    
    # Business-Ready section - Direct benefits
    content = re.sub(
        r'We create \[search_term\] solutions that solve real problems rather than implementing technology for technology\'s sake\.',
        'We build [search_term] that solves actual problems, not tech for tech\'s sake.',
        content
    )
    
    content = re.sub(
        r'Our solutions focus on measurable improvements to user experience, operational efficiency, and business outcomes\.',
        'You\'ll see real improvements in user experience, efficiency, and your bottom line.',
        content
    )
    
    # Architecture section - Plain English
    content = re.sub(
        r'We build \[search_term\] applications with growth in mind, using architecture patterns that scale efficiently as your user base and AI processing requirements expand\.',
        'We build [search_term] that grows with you. Start small, scale big.',
        content
    )
    
    content = re.sub(
        r'Our solutions remain performant and cost-effective at any scale\.',
        'Fast and affordable whether you have 10 users or 10,000.',
        content
    )
    
    # Security section - Reassuring
    content = re.sub(
        r'We implement robust security measures specifically designed for \[search_term\] applications, including data encryption, secure API communication, and privacy protection for AI processing workflows\.',
        'Your [search_term] is secure. Encrypted data, protected APIs, privacy built in.',
        content
    )
    
    # Update service pricing note
    content = re.sub(
        r'\*Our AI App Development Service is available through price on application and dependent on project scope\.',
        '*Pricing depends on your project. Let\'s discuss what you need.',
        content
    )
    
    # Fix any American spelling
    american_to_australian = [
        ('optimize', 'optimise'),
        ('optimization', 'optimisation'),
        ('analyze', 'analyse'),
        ('organization', 'organisation'),
        ('customize', 'customise'),
        ('realize', 'realise'),
        ('specialized', 'specialised'),
        ('center', 'centre')
    ]
    
    for american, australian in american_to_australian:
        content = re.sub(american, australian, content, flags=re.IGNORECASE)
    
    # Save the Australian version
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_4732_australian.html', 'w') as f:
        f.write(content)
    
    print("✅ Content transformed to Australian English!")
    
    # Update the page
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
                    print("✅ Page updated with Australian content!")
                else:
                    print(f"❌ Update failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Show examples
    print("\nExample transformations:")
    print("\n1. Heading:")
    print("   Before: Professional AI Solutions")
    print("   After: Opdee Digital")
    
    print("\n2. Hero:")
    print("   Before: Get Expert [search_term] Solutions for Your [location] Business")
    print("   After: Need [search_term] in [location]? Let's Talk")
    
    print("\n3. Opening:")
    print("   Before: We deliver professional [search_term]...comprehensive business analytics...")
    print("   After: We deliver [search_term] in [location]. Our solutions boost productivity...")

if __name__ == "__main__":
    transform_to_australian_content()