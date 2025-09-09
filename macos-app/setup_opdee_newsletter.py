#!/usr/bin/env python3
"""
Setup Opdee site and create newsletter page
"""

from wpbm_manager_v2 import WPBulkManagerV2

def setup_and_create_newsletter():
    """Add Opdee site and create newsletter page"""
    
    # Initialize manager
    manager = WPBulkManagerV2()
    
    # Add Opdee site to database
    print("📝 Adding Opdee site to database...")
    success = manager.add_site(
        name='opdee',
        url='https://opdee.com',
        api_key='27013065aa24d225b5ea9db967d191f3'
    )
    
    if success:
        print("✅ Successfully added Opdee site!")
        
        # Now create the newsletter page
        print("\n🚀 Creating newsletter page...")
        
        # Get client
        client = manager.get_client('opdee')
        if not client:
            print("❌ Error: Failed to get client")
            return
            
        # Newsletter page content with proper Gutenberg blocks
        content = """<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Stay Connected with Opdee Newsletter</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Join our exclusive newsletter community and be the first to know about:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<li>Industry insights and trends</li>
<li>Exclusive offers and promotions</li>
<li>Expert tips and best practices</li>
<li>Company updates and announcements</li>
<li>Special events and webinars</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Why Subscribe to Opdee Newsletter?</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">📊 Data-Driven Insights</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Get access to carefully curated industry data and analysis that helps you make informed decisions for your business.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">🎯 Targeted Content</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Receive content tailored to your interests and industry, ensuring every newsletter delivers value to your inbox.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">🔒 Privacy First</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Your privacy is our priority. We never share your information with third parties and you can unsubscribe anytime.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Subscribe to Our Newsletter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Enter your email below to join thousands of professionals who rely on Opdee for industry insights:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="newsletter-signup-form" style="background-color: #f5f5f5; padding: 30px; border-radius: 8px; margin: 20px 0;">
    <form id="newsletter-form" style="max-width: 500px; margin: 0 auto;">
        <div style="margin-bottom: 20px;">
            <label for="email" style="display: block; margin-bottom: 8px; font-weight: bold;">Email Address *</label>
            <input type="email" id="email" name="email" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;">
        </div>
        <div style="margin-bottom: 20px;">
            <label for="name" style="display: block; margin-bottom: 8px; font-weight: bold;">Full Name</label>
            <input type="text" id="name" name="name" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;">
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: flex; align-items: flex-start;">
                <input type="checkbox" name="consent" required style="margin-right: 10px; margin-top: 4px;">
                <span style="font-size: 14px;">I agree to receive newsletters and promotional emails from Opdee. I can unsubscribe at any time.</span>
            </label>
        </div>
        <button type="submit" style="background-color: #0073aa; color: white; padding: 12px 30px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; width: 100%;">Subscribe Now</button>
    </form>
    <p style="text-align: center; margin-top: 15px; font-size: 14px; color: #666;">We respect your privacy. Unsubscribe at any time.</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">What Our Subscribers Say</h2>
<!-- /wp:heading -->

<!-- wp:quote -->
<blockquote class="wp-block-quote">
<p>"The Opdee newsletter has become an essential part of my weekly reading. The insights are always relevant and actionable."</p>
<cite>Sarah Johnson, Marketing Director</cite>
</blockquote>
<!-- /wp:quote -->

<!-- wp:quote -->
<blockquote class="wp-block-quote">
<p>"I appreciate the quality over quantity approach. Every newsletter delivers real value without overwhelming my inbox."</p>
<cite>Michael Chen, Business Owner</cite>
</blockquote>
<!-- /wp:quote -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Newsletter Archive</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Missed a newsletter? Browse our archive to catch up on past editions:</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/newsletter-archive">View Newsletter Archive</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center"><em>Questions about our newsletter? Contact us at newsletter@opdee.com</em></p>
<!-- /wp:paragraph -->"""

        # SEO metadata
        seo_data = {
            "title": "Newsletter Subscription | Stay Updated with Opdee",
            "description": "Subscribe to the Opdee newsletter for exclusive industry insights, expert tips, and special offers. Join our community of professionals today.",
            "focus_keyword": "opdee newsletter subscription"
        }
        
        # Create the page data
        page_data = {
            "type": "page",
            "title": "Newsletter",
            "content": content,
            "status": "draft",
            "seo": seo_data,
            "slug": "newsletter",
            "template": "default"
        }
        
        try:
            # Create the page
            result = client.create_content(page_data)
            
            if result:
                page_id = result.get('id')
                print(f"✅ Successfully created newsletter page!")
                print(f"📄 Page ID: {page_id}")
                print(f"🔗 Edit URL: https://opdee.com/wp-admin/post.php?post={page_id}&action=edit")
                print(f"👁️ Preview URL: https://opdee.com/?page_id={page_id}&preview=true")
                print("\n📋 Page Details:")
                print(f"- Title: {result.get('title', {}).get('rendered', 'Newsletter')}")
                print(f"- Status: {result.get('status', 'draft')}")
                print(f"- Slug: {result.get('slug', 'newsletter')}")
                
                return result
            else:
                print(f"❌ Error creating page")
                return None
                
        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
            
    else:
        print("❌ Failed to add Opdee site to database")
        return None

if __name__ == "__main__":
    setup_and_create_newsletter()