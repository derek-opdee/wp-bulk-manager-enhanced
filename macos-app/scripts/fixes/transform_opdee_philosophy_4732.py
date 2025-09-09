#!/usr/bin/env python3
"""Transform page 4732 content with Opdee's human-in-the-loop philosophy"""

from wpbm_assistant import wpbm_connect
from wpbm_manager import WPBulkManager
import requests
import re

def transform_with_opdee_philosophy():
    assistant = wpbm_connect()
    
    # Read the current Australian content
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_4732_final_au.html', 'r') as f:
        content = f.read()
    
    print("Transforming content with Opdee's philosophy...")
    
    # Remove all em and en dashes
    content = re.sub(r'—|–|−', ' ', content)  # Replace with space
    content = re.sub(r' - ', ' ', content)  # Remove hyphen used as dash
    
    # Replace "solutions" with "systems" or other appropriate words
    content = re.sub(r'solutions', 'systems', content, flags=re.IGNORECASE)
    content = re.sub(r'solution', 'system', content, flags=re.IGNORECASE)
    
    # Update specific phrases to reflect philosophy
    
    # Hero section - emphasize human element
    content = re.sub(
        r'Need \[search_term\] in \[location\]\? Let\'s Talk',
        'Need [search_term] in [location]? We build what people actually want to use',
        content
    )
    
    # Opening paragraph - incorporate philosophy
    content = re.sub(
        r'We deliver \[search_term\] in \[location\]\. Our systems boost productivity, improve customer experience, and give you clear business insights\.',
        'We deliver [search_term] in [location] that people actually want to use. We know where AI helps and where humans excel, creating the right balance for real productivity gains.',
        content
    )
    
    content = re.sub(
        r'Our \[search_term\] works with your existing systems and scales as you grow\.',
        'Our [search_term] augments your team without replacing the human touch. We understand the line between helpful automation and overreach.',
        content
    )
    
    # Update business benefits paragraph
    content = re.sub(
        r'Your \[location\] business gets systems that actually work\. Staff find them easy to use, customers get better service, and you get the data you need to make decisions\.',
        'Your [location] business gets [search_term] that employees embrace, customers appreciate, and managers trust. We build systems that augment human capability, not replace it.',
        content
    )
    
    # Ready line
    content = re.sub(
        r'Ready to see how \[search_term\] can help your business\? Let\'s chat\.',
        'Ready for [search_term] that respects the human element? Let\'s talk about the right balance for your business.',
        content
    )
    
    # SERVICE BOXES - Update to reflect philosophy
    
    # Box 1: Customer Onboarding
    content = re.sub(
        r'We build \[search_term\] onboarding that makes signup easy\. Customers breeze through registration while you collect the data you need\.',
        'We build [search_term] onboarding that customers actually complete. Smart automation where it helps, human touch where it matters.',
        content
    )
    
    # Box 2: Beyond Chatbots
    content = re.sub(
        r'We build \[search_term\] that feels natural\. Not just chatbots.*?tools your customers will actually use\.',
        'We build [search_term] that enhances human interaction, not replaces it. Real tools that employees and customers choose to use because they make life easier.',
        content
    )
    
    # Box 3: Internal Tools
    content = re.sub(
        r'We develop \[search_term\] for \[location\] businesses\. Automate documents, analyse data, streamline workflows.*?tools your team will use every day\.',
        'We develop [search_term] for [location] businesses that augment your team\'s capabilities. Automate the tedious bits, keep humans in control of what matters.',
        content
    )
    
    # Box 4: Customer Experience
    content = re.sub(
        r'We create \[search_term\] your customers want to use\. No clunky interfaces.*?just helpful tools that fit naturally into their experience\.',
        'We create [search_term] that enhances human connection. Technology that knows its place, supporting real relationships instead of replacing them.',
        content
    )
    
    # Box 5: Data Processing
    content = re.sub(
        r'Turn your data into insights with \[search_term\]\. See what\'s working, spot opportunities, make better decisions\.',
        'Transform data into insights with [search_term] while keeping human judgment at the centre. We show you what matters, you decide what it means.',
        content
    )
    
    # Box 6: Full-Stack Development
    content = re.sub(
        r'We build complete web apps with \[search_term\] at the core\. Smart automation, dynamic content, interfaces that adapt.*?everything working together\.',
        'We build complete web apps where [search_term] enhances human work. Smart enough to help, wise enough to know when not to.',
        content
    )
    
    # Box 7: API Integration
    content = re.sub(
        r'Connect \[search_term\] to your existing systems\. We handle the technical bits so everything just works\.',
        'Connect [search_term] thoughtfully to your existing systems. We understand which processes benefit from automation and which need human oversight.',
        content
    )
    
    # Box 8: Enterprise
    content = re.sub(
        r'Deploy \[search_term\] that scales\. Secure, fast, reliable.*?built for businesses that can\'t afford downtime\.',
        'Deploy [search_term] that scales without losing the human element. Built for businesses that value both efficiency and relationships.',
        content
    )
    
    # WHY CHOOSE SECTION - Add philosophy
    content = re.sub(
        r'We build \[search_term\] that \[location\] businesses trust\. Real systems for real problems\.',
        'We build [search_term] that [location] businesses and their people actually want to use. We understand the balance between automation and human judgment.',
        content
    )
    
    # Add new section about philosophy
    philosophy_section = '''
    <!-- wp:paragraph -->
    <p><strong>The Opdee Difference:</strong> We believe in augmenting human capability, not replacing it. Our [search_term] systems respect the line between helpful automation and overreach. We build what people actually want to use because we understand where technology belongs and where the human touch matters most.</p>
    <!-- /wp:paragraph -->
    '''
    
    # Insert philosophy after "Why Choose Opdee" section
    content = re.sub(
        r'(We build \[search_term\] that \[location\] businesses and their people actually want to use.*?</p>)',
        r'\1\n' + philosophy_section,
        content
    )
    
    # Fix expertise section
    content = re.sub(
        r'Our \[location\] team knows both traditional dev and modern \[search_term\]\. Everything works together properly\.',
        'Our [location] team builds [search_term] with a deep understanding of where automation helps and where humans excel.',
        content
    )
    
    # Business-Ready section
    content = re.sub(
        r'We build \[search_term\] that solves actual problems, not tech for tech\'s sake\.',
        'We build [search_term] that people embrace because it makes their work better, not harder.',
        content
    )
    
    content = re.sub(
        r'You\'ll see real improvements in user experience, efficiency, and your bottom line\.',
        'Your team stays empowered, your customers stay happy, and your business grows sustainably.',
        content
    )
    
    # Architecture section
    content = re.sub(
        r'We build \[search_term\] that grows with you\. Start small, scale big\.',
        'We build [search_term] that grows with you without losing the human touch that made you successful.',
        content
    )
    
    content = re.sub(
        r'Fast and affordable whether you have 10 users or 10,000\.',
        'Works beautifully whether you have 10 users or 10,000, keeping people at the centre.',
        content
    )
    
    # Update pricing note
    content = re.sub(
        r'\*Pricing depends on your project\. Let\'s discuss what you need\.',
        '*Every business has different needs. Let\'s find the right balance of automation and human touch for yours.',
        content
    )
    
    # Fix any remaining "solution" words
    content = re.sub(r'\bsolution\b', 'system', content, flags=re.IGNORECASE)
    content = re.sub(r'\bsolutions\b', 'systems', content, flags=re.IGNORECASE)
    
    # Remove any remaining dashes in common patterns
    content = re.sub(r'([A-Za-z]+)-powered', r'\1 powered', content)
    content = re.sub(r'([A-Za-z]+)-based', r'\1 based', content)
    content = re.sub(r'([A-Za-z]+)-facing', r'\1 facing', content)
    content = re.sub(r'one-size-fits-all', 'one size fits all', content)
    content = re.sub(r'out-of-the-box', 'out of the box', content)
    
    # Save the philosophy version
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_4732_opdee_philosophy.html', 'w') as f:
        f.write(content)
    
    print("✅ Content transformed with Opdee philosophy!")
    
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
                    print("✅ Page updated with Opdee philosophy!")
                else:
                    print(f"❌ Update failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Show key philosophy points
    print("\nKey philosophy elements added:")
    print("1. Emphasis on 'what people actually want to use'")
    print("2. Balance between automation and human judgment")
    print("3. Augmenting human capability, not replacing it")
    print("4. Understanding where the line should be drawn")
    print("5. No tech for tech's sake")
    print("\nAll em/en dashes removed")
    print("All 'solutions' replaced with 'systems'")

if __name__ == "__main__":
    transform_with_opdee_philosophy()