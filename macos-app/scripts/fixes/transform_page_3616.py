#!/usr/bin/env python3
"""Transform page 3616 with Opdee's philosophy and writing style"""

from wpbm_assistant import wpbm_connect
from wpbm_manager import WPBulkManager
import requests
import re

def transform_page_3616():
    assistant = wpbm_connect()
    
    # Read the current content
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app/page_3616_content.html', 'r') as f:
        content = f.read()
    
    print("Transforming page 3616 with Opdee philosophy...")
    
    # Remove all em and en dashes
    content = re.sub(r'—|–|−', ' ', content)
    content = re.sub(r' - ', ' ', content)
    
    # Replace "solutions" with "systems"
    content = re.sub(r'\bsolutions\b', 'systems', content, flags=re.IGNORECASE)
    content = re.sub(r'\bsolution\b', 'system', content, flags=re.IGNORECASE)
    
    # Fix "AI Solutions" that became "AI systems"
    content = re.sub(r'AI Systems', 'AI systems', content)
    content = re.sub(r'AI System', 'AI system', content)
    
    # Update main content sections
    
    # Main description - make it more direct and philosophy-aligned
    content = re.sub(
        r'We create AI-powered web applications that deliver employee productivity gains, customer experiences people actually want to use and enjoy, and comprehensive business analytics for complete operational visibility\.',
        'We build AI systems that people actually want to use. Your team gets tools that make work easier, your customers get experiences they appreciate, and you get insights that matter.',
        content
    )
    
    content = re.sub(
        r'Our AI development integrates seamlessly with your existing systems, scales with your growth, and provides the intelligent automation your business needs to compete in today\'s digital landscape\.',
        'Our AI systems work with what you already have and grow as you grow. We understand the balance between automation and human judgment.',
        content
    )
    
    # Update service boxes
    
    # Customer Onboarding
    content = re.sub(
        r'We create intelligent onboarding systems that guide customers through complex processes using visual interfaces powered by AI\. Our systems simplify customer registration, account setup, and service configuration while collecting valuable data for business intelligence\.',
        'We build AI onboarding that customers actually complete. Smart guidance where it helps, human touch where it matters. Your customers get through signup easily while you gather the data you need.',
        content
    )
    
    # Beyond Chatbots
    content = re.sub(
        r'We develop AI integrations that go beyond simple chatbots to create systems so natural and helpful that customers won\'t believe the interaction is AI-generated\. Our systems solve real problems, provide genuine value, and enhance rather than complicate the user experience\.',
        'We build AI that enhances human interaction, not replaces it. Real tools that employees and customers choose to use because they make life easier. No gimmicks, just systems that work.',
        content
    )
    
    # Internal Tools
    content = re.sub(
        r'We develop dependable AI systems that businesses rely on for critical operations\. From automated document processing and data analysis to workflow optimisation and decision support, our internal tools become essential parts of your daily business operations\.',
        'We create AI tools your team will actually use. Automate the tedious bits, keep humans in control of what matters. From document processing to workflow optimisation, we build systems that become essential, not annoying.',
        content
    )
    
    # Customer Experience
    content = re.sub(
        r'We create intuitive AI-powered customer experience systems that delight users and drive engagement\. Our systems provide personalised interactions, intelligent recommendations, and seamless support that keeps customers coming back\.',
        'We create AI that enhances human connection. Technology that knows its place, supporting real relationships instead of replacing them. Your customers feel understood, not processed.',
        content
    )
    
    # Data Processing
    content = re.sub(
        r'Our AI systems transform raw data into actionable insights, providing comprehensive views of your operations, customer behaviour, and market opportunities\. We make complex data simple and accessible for better decision-making\.',
        'Transform data into insights while keeping human judgment at the centre. We show you what matters, you decide what it means. Complex data made simple, not simplistic.',
        content
    )
    
    # Full-Stack Development
    content = re.sub(
        r'We build complete web applications with AI capabilities at their core\. From intelligent automation and dynamic content generation to adaptive user interfaces and predictive analytics, every component works together seamlessly\.',
        'We build complete web apps where AI enhances human work. Smart enough to help, wise enough to know when not to. Every piece working together for real results.',
        content
    )
    
    # API Integration
    content = re.sub(
        r'We integrate leading AI platforms and develop custom APIs that connect AI capabilities with your existing business systems\. Our implementations ensure reliable performance and seamless operation within your established workflows\.',
        'Connect AI thoughtfully to your existing systems. We understand which processes benefit from automation and which need human oversight. Reliable integration that respects your workflows.',
        content
    )
    
    # Enterprise Deployment
    content = re.sub(
        r'We provide enterprise-grade AI infrastructure and deployment systems designed for reliability, security, and scalability\. Our cloud-based systems ensure your AI applications perform consistently across all platforms and environments\.',
        'Deploy AI that scales without losing the human element. Built for businesses that value both efficiency and relationships. Secure, reliable, and ready for growth.',
        content
    )
    
    # Why Choose section
    content = re.sub(
        r'We combine deep technical expertise with practical business understanding to deliver AI systems that work in the real world\.',
        'We build AI that businesses and their people actually want to use. We understand the balance between automation and human judgment.',
        content
    )
    
    # Add philosophy paragraph after Why Choose intro
    philosophy = '''
    <!-- wp:paragraph -->
    <p><strong>The Opdee Difference:</strong> We believe in augmenting human capability, not replacing it. Our AI systems respect the line between helpful automation and overreach. We build what people actually want to use because we understand where technology belongs and where the human touch matters most.</p>
    <!-- /wp:paragraph -->
    '''
    
    # Insert after the Why Choose intro paragraph
    content = re.sub(
        r'(We build AI that businesses and their people actually want to use\. We understand the balance between automation and human judgment\.</p>\s*<!-- /wp:kadence/advancedheading -->)',
        r'\1\n' + philosophy,
        content
    )
    
    # Update expertise boxes
    
    # Full-Stack Expertise
    content = re.sub(
        r'We handle every aspect of AI web development from initial concept through deployment and maintenance\. Our team understands both traditional development and cutting-edge AI technologies, ensuring seamless functionality across all components\.',
        'We handle everything from concept to deployment. Our team knows both traditional dev and modern AI, but more importantly, we know where each belongs. Seamless functionality with human sense.',
        content
    )
    
    # Business-Ready
    content = re.sub(
        r'We create AI integrations that solve real business problems rather than implementing technology for technology\'s sake\. You\'ll see real improvements in user experience, efficiency, and your bottom line\.',
        'We build AI that solves real problems, not tech for tech\'s sake. Your team stays empowered, your customers stay happy, and your business grows sustainably.',
        content
    )
    
    # Scalable Architecture
    content = re.sub(
        r'Our AI systems are built to grow with your business\. Whether you\'re serving hundreds or millions of users, our architecture ensures consistent performance and reliability without exponential cost increases\.',
        'We build AI that grows with you without losing the human touch that made you successful. Works beautifully whether you have 10 users or 10,000, keeping people at the centre.',
        content
    )
    
    # Security-First
    content = re.sub(
        r'We implement enterprise-grade security measures specifically designed for AI applications\. Your data remains protected through encryption, secure APIs, and comprehensive privacy protocols throughout all AI processing\.',
        'Your AI is secure. Encrypted data, protected APIs, privacy built in. Because trust matters as much as technology.',
        content
    )
    
    # Update FAQ answers to be more conversational and philosophy-aligned
    
    # Testing question
    content = re.sub(
        r'We employ rigorous testing protocols including unit testing, integration testing, user acceptance testing, and performance testing\. Our quality assurance process ensures that AI applications function reliably across all use cases and platforms\.',
        'We test everything, every day. Unit tests, integration tests, user tests, performance tests. But most importantly, we test with real people doing real work. Because AI that works in theory but fails in practice is worthless.',
        content
    )
    
    # What can you build question
    content = re.sub(
        r'We develop AI integrations across all business facets including customer onboarding systems with visual intelligence, internal productivity tools, data analysis platforms, process automation, document processing, and seamless customer experience systems\. Our systems are customised to address your specific business challenges rather than generic implementations\.',
        'We build AI across your whole business. Customer onboarding that people complete, internal tools teams actually use, data analysis that makes sense, automation that knows its limits. Everything tailored to your specific challenges, not generic tech.',
        content
    )
    
    # Integration question
    content = re.sub(
        r'Our development process begins with comprehensive assessment of your current technology infrastructure\. We use established APIs, middleware systems, and custom connectors to ensure smooth integration with existing systems while minimising disruption to operations\.',
        'We start by understanding what you already have. Then we connect AI using proven methods that won\'t break your existing systems. Smooth integration that respects your current workflows and the people who use them.',
        content
    )
    
    # Maintenance question
    content = re.sub(
        r'We offer comprehensive maintenance packages including system monitoring, performance optimisation, feature updates, and user support\. Our responsive support ensures your AI applications continue performing optimally across all platforms and environments\.',
        'We stick around. System monitoring, performance tweaks, new features, user support. Your AI keeps working because we build systems businesses depend on, not abandon.',
        content
    )
    
    # Process question
    content = re.sub(
        r'solution design',
        'system design',
        content
    )
    
    # ROI question
    content = re.sub(
        r'Before development begins, we establish clear key performance indicators aligned with your business objectives\. These include efficiency metrics, cost savings, productivity gains, customer satisfaction improvements, and other business-specific measurements that demonstrate tangible value and impact\.',
        'We set clear goals before we start. Efficiency gains, cost savings, happier customers, time saved. Real metrics that matter to your business, not vanity stats.',
        content
    )
    
    # Data requirements
    content = re.sub(
        r'While AI typically performs better with more data, we can develop effective applications even with limited datasets\. Our team can implement data collection strategies, utilise transfer learning techniques, or leverage pre-trained models to overcome data limitations where necessary\.',
        'More data helps, but we work with what you have. We can build data collection into the system, use transfer learning, or tap into pre-trained models. The key is knowing when you have enough data for AI to actually help.',
        content
    )
    
    # Technical debt question
    content = re.sub(
        r'We create practical, business-ready AI integrations that become assets, not liabilities\. Our systems are built with proper architecture, governance, and maintenance protocols\. We implement technology where it belongs and maintain human oversight where it matters, ensuring sustainable long-term value\.',
        'We build AI that stays maintainable. Proper architecture, clear governance, human oversight where needed. Systems that become assets, not nightmares. Because we understand the difference between clever and wise.',
        content
    )
    
    # Chatbot question
    content = re.sub(
        r'We go beyond chatbots to create comprehensive systems that customers and employees genuinely depend upon\. Our integrations are so natural and helpful that users focus on getting results rather than figuring out they\'re using AI\. We build tools for solving real problems, not technology showcases\.',
        'Chatbots are just the start. We build comprehensive systems that people genuinely depend on. So natural and helpful that users focus on results, not the tech. Real tools for real problems.',
        content
    )
    
    # Current tools question
    content = re.sub(
        r'Yes, we specialise in integrating AI capabilities with existing business systems including CRM platforms, customer service tools, sales systems, and internal databases\. Our integrations enhance current workflows rather than replacing them entirely\.',
        'Yes. We work with your CRM, customer service tools, sales systems, databases. Our AI enhances what you have rather than replacing it. Because good tools should play nicely together.',
        content
    )
    
    # Error handling
    content = re.sub(
        r'We implement multiple validation layers, human oversight protocols, and continuous monitoring systems to minimise errors\. Our systems include feedback mechanisms and correction processes that improve accuracy over time while maintaining reliability for business-critical operations\.',
        'We build in safety nets. Multiple validation layers, human oversight where it matters, continuous monitoring. When something does go wrong, the system learns and improves. Because perfection is a myth, but reliability isn\'t.',
        content
    )
    
    # Industries question
    content = re.sub(
        r'We\'ve successfully implemented AI systems across diverse industries including logistics, energy, healthcare, legal, manufacturing, and B2B services\. Our approach focuses on understanding unique business challenges rather than applying one-size-fits-all systems\.',
        'We\'ve built AI for logistics, energy, healthcare, legal, manufacturing, B2B services, and more. Each industry has its quirks, each business its needs. We listen first, build second.',
        content
    )
    
    # Tech changes
    content = re.sub(
        r'We maintain active engagement with leading AI platforms, participate in development communities, and continuously evaluate emerging technologies\. Our team\'s expertise spans multiple AI platforms including Anthropic, OpenAI, Mistral, Deepseek, Qwen, Perplexity, Meta Llama, and more, ensuring we can leverage the best tools for your needs\.',
        'We stay current without chasing shiny objects. Active with all major AI platforms, but selective about what we implement. We know the difference between trendy and transformative.',
        content
    )
    
    # Difference question
    content = re.sub(
        r'We\'re 100 steps ahead in the AI world, not just 10\. We identify what brings real value and productivity improvements with direct business impact\. We don\'t have pre-designed systems looking for problems; we solve your specific challenges with practical, dependable AI integrations\.',
        'We\'re 100 steps ahead, not just 10. We see past the hype to what actually works. No cookie-cutter systems looking for problems to solve. We listen, understand, then build AI that makes a real difference.',
        content
    )
    
    # Fix any remaining hyphenated terms
    content = re.sub(r'one-size-fits-all', 'one size fits all', content)
    content = re.sub(r'pre-designed', 'pre designed', content)
    content = re.sub(r'cookie-cutter', 'cookie cutter', content)
    content = re.sub(r'AI-powered', 'AI powered', content)
    content = re.sub(r'AI-Powered', 'AI Powered', content)
    content = re.sub(r'Full-Stack', 'Full Stack', content)
    content = re.sub(r'full-stack', 'full stack', content)
    content = re.sub(r'Security-First', 'Security First', content)
    content = re.sub(r'Business-Ready', 'Business Ready', content)
    content = re.sub(r'cutting-edge', 'modern', content)
    content = re.sub(r'enterprise-grade', 'enterprise', content)
    content = re.sub(r'cloud-based', 'cloud', content)
    content = re.sub(r'data-driven', 'data informed', content)
    content = re.sub(r'state-of-the-art', 'modern', content)
    content = re.sub(r'best-in-class', 'excellent', content)
    content = re.sub(r'world-class', 'excellent', content)
    content = re.sub(r'industry-leading', 'proven', content)
    content = re.sub(r'game-changing', 'innovative', content)
    content = re.sub(r'next-generation', 'modern', content)
    content = re.sub(r'mission-critical', 'critical', content)
    content = re.sub(r'business-critical', 'critical', content)
    content = re.sub(r'turn-key', 'ready to use', content)
    content = re.sub(r'plug-and-play', 'ready to use', content)
    content = re.sub(r'end-to-end', 'complete', content)
    content = re.sub(r'out-of-the-box', 'ready made', content)
    content = re.sub(r'tailor-made', 'custom', content)
    content = re.sub(r'purpose-built', 'built specifically', content)
    content = re.sub(r'future-proof', 'built to last', content)
    content = re.sub(r'battle-tested', 'proven', content)
    content = re.sub(r'time-tested', 'proven', content)
    content = re.sub(r'user-friendly', 'easy to use', content)
    content = re.sub(r'cost-effective', 'affordable', content)
    content = re.sub(r'high-performance', 'fast', content)
    content = re.sub(r'feature-rich', 'comprehensive', content)
    content = re.sub(r'data-encrypted', 'encrypted', content)
    content = re.sub(r'cloud-native', 'built for the cloud', content)
    content = re.sub(r'API-first', 'API focused', content)
    content = re.sub(r'mobile-first', 'mobile focused', content)
    content = re.sub(r'privacy-first', 'privacy focused', content)
    content = re.sub(r'customer-centric', 'customer focused', content)
    content = re.sub(r'results-driven', 'results focused', content)
    content = re.sub(r'value-added', 'valuable', content)
    content = re.sub(r'cross-platform', 'multi platform', content)
    content = re.sub(r'cross-functional', 'multi functional', content)
    content = re.sub(r'domain-specific', 'specialised', content)
    content = re.sub(r'context-aware', 'contextual', content)
    content = re.sub(r'self-learning', 'adaptive', content)
    content = re.sub(r'self-service', 'self serve', content)
    content = re.sub(r'plug-in', 'plugin', content)
    content = re.sub(r'add-on', 'addon', content)
    content = re.sub(r'built-in', 'included', content)
    content = re.sub(r'always-on', 'continuous', content)
    content = re.sub(r'set-and-forget', 'automated', content)
    content = re.sub(r'drag-and-drop', 'drag and drop', content)
    content = re.sub(r'point-and-click', 'point and click', content)
    content = re.sub(r'real-time', 'real time', content)
    content = re.sub(r'Real-time', 'Real time', content)
    content = re.sub(r'up-to-date', 'current', content)
    content = re.sub(r'ready-to-use', 'ready to use', content)
    content = re.sub(r'easy-to-use', 'easy to use', content)
    content = re.sub(r'hard-to-find', 'rare', content)
    content = re.sub(r'must-have', 'essential', content)
    content = re.sub(r'nice-to-have', 'helpful', content)
    content = re.sub(r'hands-on', 'practical', content)
    content = re.sub(r'hands-off', 'automated', content)
    content = re.sub(r'face-to-face', 'in person', content)
    content = re.sub(r'peer-to-peer', 'peer to peer', content)
    content = re.sub(r'B2B', 'business to business', content)
    content = re.sub(r'B2C', 'business to consumer', content)
    content = re.sub(r'win-win', 'mutually beneficial', content)
    content = re.sub(r'day-to-day', 'daily', content)
    content = re.sub(r'step-by-step', 'step by step', content)
    content = re.sub(r'one-on-one', 'one on one', content)
    content = re.sub(r'all-in-one', 'all in one', content)
    content = re.sub(r'one-stop-shop', 'complete service', content)
    content = re.sub(r'state-of-the-art', 'modern', content)
    content = re.sub(r'off-the-shelf', 'ready made', content)
    content = re.sub(r'made-to-measure', 'custom', content)
    content = re.sub(r'tried-and-true', 'proven', content)
    content = re.sub(r'back-end', 'backend', content)
    content = re.sub(r'front-end', 'frontend', content)
    content = re.sub(r'client-side', 'client side', content)
    content = re.sub(r'server-side', 'server side', content)
    content = re.sub(r'open-source', 'open source', content)
    content = re.sub(r'closed-source', 'closed source', content)
    content = re.sub(r'white-label', 'white label', content)
    content = re.sub(r'co-branded', 'co branded', content)
    content = re.sub(r'multi-tenant', 'multi tenant', content)
    content = re.sub(r'single-tenant', 'single tenant', content)
    content = re.sub(r'on-premise', 'on premise', content)
    content = re.sub(r'on-premises', 'on premises', content)
    content = re.sub(r'Software-as-a-Service', 'Software as a Service', content)
    content = re.sub(r'Platform-as-a-Service', 'Platform as a Service', content)
    content = re.sub(r'Infrastructure-as-a-Service', 'Infrastructure as a Service', content)
    
    # Save the transformed version
    with open('/Users/derekzar/Documents/Projects/wp-bulk-manager/page_3616_opdee_philosophy.html', 'w') as f:
        f.write(content)
    
    print("✅ Content transformed with Opdee philosophy!")
    
    # Update the page
    manager = WPBulkManager()
    sites = manager.get_sites('active')
    
    if sites:
        site = sites[0]
        api_key = manager.get_site_api_key(site['id'])
        
        if api_key:
            print("\nUpdating page 3616...")
            try:
                response = requests.put(
                    f"{site['url']}/wp-json/wpbm/v1/content/3616",
                    headers={'X-API-Key': api_key},
                    json={'content': content},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ Page 3616 updated with Opdee philosophy!")
                    print("\nKey changes:")
                    print("1. Removed all dashes")
                    print("2. Replaced 'solutions' with 'systems'")
                    print("3. Added human-in-the-loop philosophy throughout")
                    print("4. Made content more conversational and direct")
                    print("5. Emphasized balance between automation and human judgment")
                else:
                    print(f"❌ Update failed: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    transform_page_3616()