#!/usr/bin/env python3
"""
Create 5 accessibility renovation service pages for Reno Warriors
"""

from wpbm_manager_mysql import WPBulkManagerMySQL
import time

def create_accessibility_pages():
    """Create accessibility renovation service pages for Reno Warriors"""
    
    manager = WPBulkManagerMySQL()
    
    # Service pages to create
    services = [
        {
            'title': 'Bathroom Accessibility Renovation Services',
            'slug': 'bathroom-accessibility-renovation',
            'service_name': 'Bathroom Accessibility Renovations',
            'description': 'Transform your bathroom into a beautiful, accessible space with European-inspired design',
            'focus': 'Bathroom accessibility modifications for improved mobility and independence',
            'features': [
                'Walk-in showers with grab rails and non-slip surfaces',
                'Height-adjustable vanities and storage solutions',
                'Accessible toilet installations with support features',
                'European-style accessible bathtubs and shower seats',
                'Improved lighting and easy-reach fixtures'
            ]
        },
        {
            'title': 'Kitchen Accessibility Renovation Services', 
            'slug': 'kitchen-accessibility-renovation',
            'service_name': 'Kitchen Accessibility Renovations',
            'description': 'Create a functional, beautiful kitchen that works for everyone with mobility considerations',
            'focus': 'Kitchen modifications for enhanced accessibility and ease of use',
            'features': [
                'Height-adjustable benchtops and work surfaces',
                'Pull-out drawers and accessible storage solutions',
                'European-style accessible appliances and fixtures',
                'Easy-grip handles and lever-style taps',
                'Improved lighting and accessible electrical outlets'
            ]
        },
        {
            'title': 'Laundry Accessibility Renovation Services',
            'slug': 'laundry-accessibility-renovation', 
            'service_name': 'Laundry Accessibility Renovations',
            'description': 'Design an accessible laundry space that combines European style with practical functionality',
            'focus': 'Laundry room modifications for improved accessibility and convenience',
            'features': [
                'Front-loading washer and dryer installations',
                'Height-adjustable work surfaces and folding areas',
                'Accessible storage and hanging solutions',
                'European-inspired accessible cabinetry',
                'Easy-access utility connections and controls'
            ]
        },
        {
            'title': 'Home Accessibility Design & Planning Services',
            'slug': 'home-accessibility-design-planning',
            'service_name': 'Home Accessibility Design & Planning',
            'description': 'Comprehensive accessibility planning with beautiful European design principles',
            'focus': 'Complete home accessibility assessment and design planning',
            'features': [
                'Professional accessibility assessments',
                'European-inspired accessible design concepts',
                'Mobility and layout optimisation plans',
                'Hardware and fixture recommendations',
                'Complete renovation project management'
            ]
        },
        {
            'title': 'European Accessible Hardware & Fixtures Installation',
            'slug': 'european-accessible-hardware-fixtures',
            'service_name': 'European Accessible Hardware & Fixtures',
            'description': 'Premium European accessibility hardware that combines style with functionality',
            'focus': 'High-quality European accessibility hardware and fixture installation',
            'features': [
                'European-style grab rails and support systems',
                'Accessible door handles and lever systems',
                'Height-adjustable European fixtures',
                'Premium accessible bathroom and kitchen hardware',
                'Stylish safety and mobility enhancement features'
            ]
        }
    ]
    
    print("🏠 Creating Accessibility Renovation Pages for Reno Warriors")
    print("=" * 60)
    
    created_pages = []
    
    for i, service in enumerate(services, 1):
        print(f"\n📄 Creating Page {i}/5: {service['title']}")
        
        # Create comprehensive content with Australian English and European design focus
        content = f"""<!-- wp:heading {{"level":1}} -->
<h1 class="wp-block-heading">{service['service_name']} in Australia</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Transform your home with beautiful, accessible renovations that combine European design excellence with practical mobility solutions.</strong> Reno Warriors specialises in creating stunning accessible spaces that enhance independence while maintaining sophisticated style.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">Why Choose Reno Warriors for Accessibility Renovations?</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">🇪🇺 European Design Excellence</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our accessibility renovations feature beautiful European design principles that prove accessible doesn't mean compromising on style. We source premium European fixtures and hardware for superior quality and aesthetics.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">♿ Mobility-Focused Solutions</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We understand the unique needs of people with mobility impairments. Our renovations enhance independence and safety while creating spaces that are easy to use and navigate for everyone.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">🔧 Expert Installation</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our experienced team ensures every accessibility feature is properly installed to Australian standards while maintaining the beautiful European aesthetic that sets your home apart.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">Our {service['service_name']} Include:</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">"""

        # Add service-specific features
        for feature in service['features']:
            content += f"""
<li>{feature}</li>"""

        content += """
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">Beautiful, Accessible, European-Inspired Design</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>At Reno Warriors, we believe accessibility should never mean sacrificing style. Our European-inspired approach to accessible renovations ensures your home maintains its beauty while becoming more functional for people with mobility considerations.</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Premium Materials</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We use only the finest European materials and fixtures, selected for both their accessibility features and aesthetic appeal. Quality craftsmanship ensures lasting beauty and functionality.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Thoughtful Planning</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Every renovation is carefully planned to optimise layout, improve accessibility, and enhance the overall flow of your space. We consider both current needs and future requirements.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">The Reno Warriors Process</h2>
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<li><strong>Initial Consultation:</strong> We assess your space and discuss your accessibility needs and design preferences</li>
<li><strong>Custom Design:</strong> Our team creates a tailored plan combining European design with accessibility features</li>
<li><strong>Material Selection:</strong> Choose from our curated range of European accessibility hardware and fixtures</li>
<li><strong>Professional Installation:</strong> Expert installation ensuring both safety and style</li>
<li><strong>Final Inspection:</strong> Thorough testing to ensure all accessibility features function perfectly</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">Why Accessible Renovations Matter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Creating accessible spaces isn't just about meeting immediate needs—it's about future-proofing your home and ensuring it remains comfortable and functional for years to come. Our renovations help:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<li>Increase independence and confidence in daily activities</li>
<li>Reduce the risk of accidents and injuries</li>
<li>Improve overall quality of life</li>
<li>Add value to your property</li>
<li>Create beautiful, welcoming spaces for all family members and guests</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">Get Your Free Accessibility Consultation</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Ready to transform your home with beautiful, accessible renovations? Contact Reno Warriors today for your free consultation. We'll assess your space and show you how European design excellence can enhance accessibility without compromising on style.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"center"}}}} -->
<div class="wp-block-buttons"><!-- wp:button {{"className":"is-style-fill"}} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link wp-element-button" href="/contact">Get Free Consultation</a></div>
<!-- /wp:button -->

<!-- wp:button {{"className":"is-style-outline"}} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="tel:1300RENO99">Call 1300 RENO 99</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:paragraph {{"align":"center"}} -->
<p class="has-text-align-center"><em>Reno Warriors - Creating beautiful, accessible Australian homes with European design excellence</em></p>
<!-- /wp:paragraph -->"""

        # SEO metadata with Australian English
        seo_data = {
            "title": f"{service['title']} | European Design | Reno Warriors",
            "description": f"{service['description']}. Expert accessibility renovations across Australia using premium European fixtures and design principles.",
            "focus_keyword": service['service_name'].lower()
        }
        
        # Create page data
        page_data = {
            "type": "page",
            "title": service['title'],
            "content": content,
            "status": "draft",
            "seo": seo_data,
            "slug": service['slug']
        }
        
        try:
            # Get client for Reno Warriors
            client = manager.get_client('renowarriors')
            if not client:
                print(f"   ❌ Error: Could not connect to Reno Warriors")
                continue
            
            # Create the page
            result = client.create_content(page_data)
            
            if result and result.get('id'):
                page_id = result['id']
                print(f"   ✅ Created successfully!")
                print(f"   📄 Page ID: {page_id}")
                print(f"   🔗 Edit: https://renowarriors.com.au/wp-admin/post.php?post={page_id}&action=edit")
                print(f"   👁️  Preview: https://renowarriors.com.au/?page_id={page_id}&preview=true")
                
                created_pages.append({
                    'title': service['title'],
                    'id': page_id,
                    'slug': service['slug']
                })
                
                # Log the creation
                site = manager.db.get_site('renowarriors')
                manager.db.log_change(
                    site_id=site['id'],
                    content_type='page',
                    content_id=page_id,
                    action='create',
                    summary=f"Created accessibility service page: {service['title']}"
                )
                
            else:
                print(f"   ❌ Failed to create page")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ACCESSIBILITY PAGES CREATION SUMMARY")
    print("=" * 60)
    
    print(f"\n✅ Successfully Created: {len(created_pages)}/5 pages")
    
    for page in created_pages:
        print(f"\n📄 {page['title']}")
        print(f"   ID: {page['id']}")
        print(f"   Slug: /{page['slug']}")
        print(f"   Status: Draft (ready for review)")
    
    print(f"\n🎯 Key Features of Created Pages:")
    print("   🇦🇺 Australian English spelling and terminology")
    print("   🇪🇺 European design focus and premium fixtures")
    print("   ♿ Comprehensive accessibility information")
    print("   📱 Mobile-friendly responsive design")
    print("   🔍 SEO optimised for accessibility renovation keywords")
    
    print(f"\n📋 Next Steps:")
    print("   1. Review and edit pages in WordPress admin")
    print("   2. Add relevant images and galleries")
    print("   3. Set featured images for each service")
    print("   4. Publish when ready")
    print("   5. Add to main navigation menu")
    
    print(f"\n🔗 Quick Access:")
    print("   WordPress Admin: https://renowarriors.com.au/wp-admin/edit.php?post_type=page")
    print("   View all drafts: Filter by 'Draft' status")

if __name__ == "__main__":
    create_accessibility_pages()