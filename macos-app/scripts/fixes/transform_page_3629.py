#!/usr/bin/env python3
"""Transform page 3629 (Branded Agent Kit) with Opdee's philosophy and writing style"""

from wpbm_manager import WPBulkManager
import requests
import re

def transform_page_3629():
    # Read the current content
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app/page_3629_content.html', 'r') as f:
        content = f.read()
    
    print("Transforming page 3629 (Branded Agent Kit) with Opdee philosophy...")
    
    # Remove all em and en dashes
    content = re.sub(r'—|–|−', ' ', content)
    content = re.sub(r' - ', ' ', content)
    
    # Replace "solutions" with "systems" where appropriate
    content = re.sub(r'\bsolutions\b', 'systems', content, flags=re.IGNORECASE)
    content = re.sub(r'\bsolution\b', 'system', content, flags=re.IGNORECASE)
    
    # Update main content sections
    
    # Main heading stays the same
    # "Full Branding Agent Kit (BAK)" - keep as is
    
    # Subheading - make more direct and philosophy-aligned
    content = re.sub(
        r'The Complete Business Brand\'s DNA, All in One Package!',
        'Keep Your Brand\'s Voice Intact in the AI Age',
        content
    )
    
    # Main description - incorporate the AI age philosophy
    content = re.sub(
        r'Revamp your business with our comprehensive Branded Agent Kit.*?We create a cohesive business identity by integrating both visual branding and brand voice across all digital touchpoints\.',
        'In the AI age, it\'s easier than ever to lose your brand\'s voice. With AI content creation everywhere and messages coming from customer service, sales teams, agencies, and social media, consistency matters more than ever. Our Branded Agent Kit keeps your voice intact across every channel.',
        content
    )
    
    # Add new paragraph about the purpose
    new_paragraph = '''
    <!-- wp:paragraph -->
    <p>We build training guides for AI agents that understand your brand's tonality. No more relying on AI to guess what your business does or how it speaks. Your team, your agencies, anyone creating content gets clear guidelines that ensure your brand sounds like you, everywhere, every time.</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:paragraph -->
    <p><strong>The Opdee Difference:</strong> We understand that AI tools are powerful but need human guidance. Our BAK creates the balance between AI efficiency and authentic brand voice. Because in this day and age, keeping your voice consistent is more crucial than it's ever been.</p>
    <!-- /wp:paragraph -->
    '''
    
    # Insert after the main description
    content = re.sub(
        r'(Our Branded Agent Kit keeps your voice intact across every channel\.</p>\s*<!-- /wp:kadence/advancedheading -->)',
        r'\1\n' + new_paragraph,
        content
    )
    
    # Update service boxes
    
    # Visual Branding
    content = re.sub(
        r'This service includes a full visual brand kit that reflects your brand values and resonates with your audience\. It will include distinctive logos, colour palettes, typography, and imagery guidelines\.',
        'Your visual identity that AI can\'t dilute. Clear logos, colours, typography, and imagery guidelines that stay consistent whether it\'s your team, an agency, or an AI tool creating content.',
        content
    )
    
    # Brand Voice
    content = re.sub(
        r'We establish a consistent tone and messaging strategy that aligns with your brand\'s personality, ensuring all communications reflect your company\'s unique character and values\.',
        'Your brand\'s voice, documented and trainable. We create guidelines that AI agents and human teams can follow, ensuring your personality comes through in every message, post, and interaction.',
        content
    )
    
    # Overall Brand Consistency
    content = re.sub(
        r'We ensure all branding elements work together harmoniously across all platforms, creating a seamless brand experience whether customers encounter you online, in print, or in person\.',
        'Complete alignment across every channel. From customer service chats to social posts, sales pitches to support emails, your brand stays consistent. Because with AI everywhere, consistency is your competitive edge.',
        content
    )
    
    # Comprehensive Understanding
    content = re.sub(
        r'We help clients gain valuable insights into their business and industry, so they are fully informed for branding decisions, creating a foundation for strategic brand development\.',
        'Deep understanding that AI can\'t infer. We document what your business actually does, who you serve, and why you matter. No more hoping AI "gets it" - your brand story is clear and consistent.',
        content
    )
    
    # Structured Template Sequence
    content = re.sub(
        r'We guide clients through a clear process that simplifies branding and ensures no crucial element is overlooked, providing a systematic approach to building brand identity\.',
        'A proven process that captures everything. Step by step, we build your complete brand guide so nothing gets lost when AI or new team members create content. Your brand stays intact as you grow.',
        content
    )
    
    # Update FAQ section to be more conversational and address AI concerns
    
    # Q1: What exactly is included
    content = re.sub(
        r'Our BAK includes comprehensive visual identity elements.*?This cohesive package ensures your brand is consistently represented across all touchpoints\.',
        'Everything you need to keep your brand consistent in the AI age. Visual identity (logos, colours, fonts), voice guidelines (how you speak, key phrases, tone), templates for everything from business cards to social posts, and a complete guide that AI agents and humans can follow. One package that protects your brand voice.',
        content
    )
    
    # Q2: Existing brand elements
    content = re.sub(
        r'We can work either way\. Our structured process accommodates both brand evolution and complete rebranding\. We\'ll assess your current branding assets and recommend the most strategic approach based on your business goals and market position\.',
        'We work with what you have or start fresh. If your brand is getting lost in AI-generated content, we\'ll strengthen what works and fix what doesn\'t. The goal: a brand voice so clear that even AI can\'t mess it up.',
        content
    )
    
    # Q3: Timeline
    content = re.sub(
        r'Most BAK projects take 8-12 weeks from concept to completion, depending on complexity and scope\. The process follows our structured template sequence, guiding you through each phase of brand development systematically\. We\'ll provide a detailed timeline during our initial consultation\.',
        'Usually 8 to 12 weeks to build your complete brand kit. We follow a proven process that captures everything about your brand. You\'ll know exactly where we are every step of the way.',
        content
    )
    
    # Q4: Platform consistency
    content = re.sub(
        r'Our BAK includes platform-specific guidelines and templates that address the unique requirements of various media\. We provide clear standards for adapting your brand across digital, print, environmental, and other applications while maintaining consistent brand recognition\.',
        'We create specific guidelines for every platform. Social media, websites, print, email, even AI chatbots. Each has its quirks, but your brand stays consistent. That\'s how you stand out when everyone else sounds like generic AI.',
        content
    )
    
    # Q6: Implementation support
    content = re.sub(
        r'Yes, we offer implementation services to help you roll out your brand identity effectively\. This can include website updates, social media profile redesigns, marketing material production, and training sessions for your team to ensure proper brand application\.',
        'Yes, we help you roll it out everywhere. Website updates, social profiles, marketing materials, and crucially, training your team and AI tools to use it properly. Because a brand guide gathering dust helps nobody.',
        content
    )
    
    # Q7: Understanding business
    content = re.sub(
        r'Our process includes in-depth discovery sessions to uncover your business values, audience needs, market positioning, and competitive landscape\. This comprehensive understanding informs all branding decisions and provides valuable insights that often extend beyond branding into broader business strategy\.',
        'We dig deep to understand your business. Values, audience, market position, what makes you different. This becomes the foundation AI agents need to represent you accurately. Often, clients discover insights that reshape their whole strategy.',
        content
    )
    
    # Q8: Connect with audience
    content = re.sub(
        r'Through our comprehensive understanding phase, we identify your audience\'s preferences, pain points, and motivations\. This insight informs both visual and verbal brand elements, creating a brand identity specifically designed to resonate with the people who matter most to your business\.',
        'We uncover what your audience actually wants to hear. Their preferences, problems, what motivates them. Then we build your brand voice to connect authentically. No generic AI speak - real connection with real people.',
        content
    )
    
    # Q9: Template sequence
    content = re.sub(
        r'Our template sequence guides you through a logical progression of brand development: discovery and strategy, visual identity creation, voice development, application design, and implementation planning\. This structured approach ensures all crucial elements are addressed in the proper order\.',
        'Simple: Discovery first (who you are), then visual identity (how you look), then voice (how you speak), then applications (where it all goes), and finally implementation (making it real). Each step builds on the last. Nothing gets missed.',
        content
    )
    
    # Q10: Future updates
    content = re.sub(
        r'Absolutely\. We design your BAK with scalability in mind, providing guidelines for how your brand can evolve while maintaining consistency\. We also offer brand refresh services when more significant updates are needed as your business grows and markets change\.',
        'Of course. Your brand will evolve, but the core stays consistent. We build flexibility into your guidelines so you can grow without losing your voice. When big changes come, we\'re here to help your brand evolve while staying true to who you are.',
        content
    )
    
    # Fix hyphenated terms
    content = re.sub(r'platform-specific', 'platform specific', content)
    content = re.sub(r'in-depth', 'in depth', content)
    content = re.sub(r'AI-generated', 'AI generated', content)
    content = re.sub(r'one-size-fits-all', 'one size fits all', content)
    content = re.sub(r'brand-building', 'brand building', content)
    content = re.sub(r'customer-facing', 'customer facing', content)
    content = re.sub(r'decision-making', 'decision making', content)
    content = re.sub(r'long-term', 'long term', content)
    content = re.sub(r'short-term', 'short term', content)
    content = re.sub(r'user-friendly', 'easy to use', content)
    content = re.sub(r'cost-effective', 'affordable', content)
    content = re.sub(r'time-consuming', 'time consuming', content)
    content = re.sub(r'well-defined', 'well defined', content)
    content = re.sub(r'clearly-defined', 'clearly defined', content)
    content = re.sub(r'professionally-designed', 'professionally designed', content)
    content = re.sub(r'carefully-crafted', 'carefully crafted', content)
    content = re.sub(r'fully-integrated', 'fully integrated', content)
    content = re.sub(r'results-driven', 'results focused', content)
    content = re.sub(r'detail-oriented', 'detailed', content)
    content = re.sub(r'client-focused', 'client focused', content)
    content = re.sub(r'solution-oriented', 'practical', content)
    content = re.sub(r'forward-thinking', 'forward thinking', content)
    content = re.sub(r'cutting-edge', 'modern', content)
    content = re.sub(r'state-of-the-art', 'modern', content)
    content = re.sub(r'industry-leading', 'proven', content)
    content = re.sub(r'award-winning', 'recognised', content)
    content = re.sub(r'world-class', 'excellent', content)
    content = re.sub(r'best-in-class', 'excellent', content)
    content = re.sub(r'purpose-built', 'built specifically', content)
    content = re.sub(r'custom-made', 'custom made', content)
    content = re.sub(r'tailor-made', 'tailored', content)
    content = re.sub(r'hand-picked', 'selected', content)
    content = re.sub(r'cherry-picked', 'carefully selected', content)
    content = re.sub(r'battle-tested', 'proven', content)
    content = re.sub(r'time-tested', 'proven', content)
    content = re.sub(r'field-tested', 'tested', content)
    content = re.sub(r'tried-and-true', 'proven', content)
    content = re.sub(r'tried-and-tested', 'proven', content)
    
    # Save the transformed version
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_3629_opdee_philosophy.html', 'w') as f:
        f.write(content)
    
    print("✅ Content transformed with Opdee philosophy!")
    
    # Update the page
    manager = WPBulkManager()
    sites = manager.get_sites('active')
    
    if sites:
        site = sites[0]
        api_key = manager.get_site_api_key(site['id'])
        
        if api_key:
            print("\nUpdating page 3629...")
            try:
                response = requests.put(
                    f"{site['url']}/wp-json/wpbm/v1/content/3629",
                    headers={'X-API-Key': api_key},
                    json={'content': content},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ Page 3629 updated with Opdee philosophy!")
                    print("\nKey changes:")
                    print("1. Emphasized keeping brand voice intact in the AI age")
                    print("2. Focused on AI training guides for brand consistency")
                    print("3. Highlighted the challenge of multiple content creators")
                    print("4. Stressed importance of consistency with AI proliferation")
                    print("5. Made content more conversational and direct")
                else:
                    print(f"❌ Update failed: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    transform_page_3629()