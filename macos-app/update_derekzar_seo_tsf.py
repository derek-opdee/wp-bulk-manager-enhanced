#!/usr/bin/env python3
"""
Update SEO titles and descriptions for derekzar.com using The SEO Framework meta fields
Research shows TSF uses specific meta field names
"""
import requests
import json
from typing import Dict, List

class DerekZarSEOUpdater:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://derekzar.com'
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
        
        # SEO data for each page - Australian English, lean communicator voice, Melbourne-focused
        self.seo_data = {
            'home': {
                'title': 'AI Innovation Strategist & Consultant Melbourne | Derek Zar',
                'description': 'Transform your business with AI. Melbourne-based strategist Derek Zar delivers practical AI solutions, executive training, and innovation consulting.'
            },
            'about': {
                'title': 'About Derek Zar | AI Innovation Strategist Melbourne',
                'description': 'Meet Derek Zar, Melbourne\'s trusted AI strategist. Specialising in practical AI transformation, cloud architecture, and executive enablement.'
            },
            'contact': {
                'title': 'Contact Derek Zar | AI Consultant Melbourne',
                'description': 'Ready to transform with AI? Contact Melbourne-based AI strategist Derek Zar for consulting, training, and innovation solutions.'
            },
            'projects': {
                'title': 'AI Projects & Case Studies | Derek Zar Melbourne',
                'description': 'Explore Derek Zar\'s AI transformation projects. Real-world case studies from Melbourne businesses implementing practical AI solutions.'
            },
            'all-services': {
                'title': 'AI Services & Solutions | Derek Zar Melbourne',
                'description': 'Complete AI services from Melbourne\'s leading strategist. Strategy, architecture, training, and agentic AI development solutions.'
            },
            'ai-strategy-transformation': {
                'title': 'AI Strategy & Transformation | Derek Zar Melbourne',
                'description': 'Strategic AI transformation for Melbourne businesses. Practical roadmaps, implementation planning, and organisational change management.'
            },
            'fractional-ai-executive': {
                'title': 'Fractional AI Executive | Derek Zar Melbourne',
                'description': 'Part-time AI leadership for Melbourne companies. Executive guidance, strategic planning, and AI governance without full-time commitment.'
            },
            'agentic-ai-development': {
                'title': 'Agentic AI Development | Derek Zar Melbourne',
                'description': 'Build autonomous AI agents for your Melbourne business. Custom development, integration, and deployment of intelligent automation systems.'
            },
            'ai-cloud-architecture': {
                'title': 'AI Cloud Architecture | Derek Zar Melbourne',
                'description': 'Scalable AI infrastructure for Melbourne enterprises. Cloud-native architectures, deployment strategies, and platform optimisation.'
            },
            'ai-training-enablement': {
                'title': 'AI Training & Enablement | Derek Zar Melbourne',
                'description': 'Empower your Melbourne team with AI skills. Executive workshops, technical training, and organisational enablement programmes.'
            },
            'speaking-workshops': {
                'title': 'AI Speaking & Workshops | Derek Zar Melbourne',
                'description': 'Engage your Melbourne audience with AI insights. Expert keynote speaking, executive workshops, and comprehensive team training sessions.'
            },
            'investment-opportunities': {
                'title': 'AI Investment Opportunities | Derek Zar Melbourne',
                'description': 'Strategic AI investment advice for Melbourne investors. Comprehensive market analysis, technology evaluation, and portfolio guidance strategies.'
            },
            'privacy-policy': {
                'title': 'Privacy Policy | Derek Zar AI Consultant Melbourne',
                'description': 'Privacy policy for Derek Zar AI consulting services. How we protect your data and respect your privacy in Melbourne and beyond.'
            }
        }
    
    def test_tsf_meta_keys(self, page_id: int = 2265) -> Dict:
        """Test different TSF meta key combinations"""
        print(f"Testing TSF meta key combinations on page {page_id}...")
        
        # The SEO Framework uses these meta keys (from plugin source)
        test_combinations = [
            {
                'name': 'TSF Standard Keys',
                'meta': {
                    '_tsf_title_no_blogname': 'Test Title TSF Standard',
                    '_tsf_description_no_additions': 'Test Description TSF Standard'
                }
            },
            {
                'name': 'TSF Alternative Keys', 
                'meta': {
                    '_open_graph_title': 'Test Title OG',
                    '_open_graph_description': 'Test Description OG',
                    '_twitter_title': 'Test Title Twitter',
                    '_twitter_description': 'Test Description Twitter'
                }
            },
            {
                'name': 'TSF Simple Keys',
                'meta': {
                    '_tsf_title': 'Test Title Simple',
                    '_tsf_description': 'Test Description Simple'
                }
            },
            {
                'name': 'WordPress Standard',
                'meta': {
                    '_wp_page_template': 'default'  # Just test if we can update any meta
                }
            }
        ]
        
        results = {}
        
        for combo in test_combinations:
            try:
                print(f"\\nTesting {combo['name']}...")
                
                response = requests.put(
                    f'{self.base_url}/wp-json/wpbm/v1/content/{page_id}',
                    headers=self.headers,
                    json={'meta': combo['meta']}
                )
                
                if response.status_code == 200:
                    print(f"✅ {combo['name']} update successful")
                    results[combo['name']] = 'success'
                else:
                    print(f"❌ {combo['name']} update failed: {response.text}")
                    results[combo['name']] = 'failed'
                    
            except Exception as e:
                print(f"❌ {combo['name']} error: {e}")
                results[combo['name']] = 'error'
        
        return results
    
    def test_direct_wp_api_update(self, page_id: int = 2265) -> bool:
        """Test updating via WordPress REST API directly"""
        print(f"\\nTesting direct WordPress API update on page {page_id}...")
        
        # Try multiple authentication methods
        auth_methods = [
            {
                'name': 'Bearer Token',
                'headers': {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'API Key Header',
                'headers': {
                    'X-API-Key': self.api_key,
                    'Content-Type': 'application/json'
                }
            }
        ]
        
        # Try different meta field combinations
        meta_combinations = [
            {
                '_tsf_title_no_blogname': 'Direct API Test Title',
                '_tsf_description_no_additions': 'Direct API Test Description'
            },
            {
                '_open_graph_title': 'Direct API OG Title',
                '_open_graph_description': 'Direct API OG Description'
            }
        ]
        
        for auth in auth_methods:
            for i, meta in enumerate(meta_combinations):
                try:
                    print(f"Trying {auth['name']} with meta combo {i+1}...")
                    
                    data = {'meta': meta}
                    
                    response = requests.post(
                        f'{self.base_url}/wp-json/wp/v2/pages/{page_id}',
                        headers=auth['headers'],
                        json=data
                    )
                    
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ Success with {auth['name']} and meta combo {i+1}")
                        return True
                    else:
                        print(f"Failed: {response.text[:200]}")
                        
                except Exception as e:
                    print(f"Error: {e}")
        
        return False
    
    def check_tsf_api_endpoint(self) -> bool:
        """Check if TSF has its own API endpoint"""
        print("\\nChecking for TSF-specific API endpoints...")
        
        try:
            # Check WordPress API namespace discovery
            response = requests.get(f'{self.base_url}/wp-json/')
            if response.status_code == 200:
                data = response.json()
                namespaces = data.get('namespaces', [])
                
                tsf_namespaces = [ns for ns in namespaces if 'tsf' in ns.lower() or 'seo' in ns.lower()]
                
                if tsf_namespaces:
                    print(f"Found SEO-related namespaces: {tsf_namespaces}")
                    return True
                else:
                    print("No TSF-specific API namespaces found")
                    return False
            else:
                print(f"API discovery failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error checking TSF API: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive test to find working SEO update method"""
        print("Derek Zar SEO Update - TSF Comprehensive Test")
        print("=" * 60)
        
        # 1. Check for TSF API endpoints
        self.check_tsf_api_endpoint()
        
        # 2. Test TSF meta key combinations via WPBM
        test_results = self.test_tsf_meta_keys()
        
        # 3. Test direct WordPress API
        direct_success = self.test_direct_wp_api_update()
        
        # 4. Summary
        print("\\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        print("\\nWPBM API Tests:")
        for test_name, result in test_results.items():
            status = "✅" if result == 'success' else "❌"
            print(f"  {status} {test_name}: {result}")
        
        print(f"\\nDirect WordPress API: {'✅ Success' if direct_success else '❌ Failed'}")
        
        # 5. Check actual HTML output
        print("\\nChecking current HTML output...")
        self.check_live_seo_output()
    
    def check_live_seo_output(self):
        """Check the current SEO output in HTML"""
        import re
        import time
        
        time.sleep(2)  # Wait for any updates to process
        
        try:
            response = requests.get('https://derekzar.com/investment-opportunities/')
            html = response.text
            
            # Look for title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                print(f"Current title: {title}")
                
                # Check if any of our test titles appear
                test_keywords = ['Test Title', 'Direct API', 'TSF Standard', 'TSF Simple']
                for keyword in test_keywords:
                    if keyword in title:
                        print(f"✅ Found test keyword in title: {keyword}")
                        return True
            
            # Look for description
            desc_patterns = [
                r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
                r'<meta\s+content=["\']([^"\']*)["\'][^>]*name=["\']description["\']'
            ]
            
            for pattern in desc_patterns:
                desc_match = re.search(pattern, html, re.IGNORECASE)
                if desc_match:
                    desc = desc_match.group(1)
                    print(f"Current description: {desc}")
                    
                    # Check if any test descriptions appear
                    test_keywords = ['Test Description', 'Direct API', 'TSF Standard', 'TSF Simple']
                    for keyword in test_keywords:
                        if keyword in desc:
                            print(f"✅ Found test keyword in description: {keyword}")
                            return True
                    break
            
            print("❌ No test keywords found in HTML output")
            return False
            
        except Exception as e:
            print(f"Error checking HTML: {e}")
            return False


def main():
    """Main execution function"""
    updater = DerekZarSEOUpdater('0b2d82ec91d2d876558ce460e57a7a1e')
    updater.run_comprehensive_test()


if __name__ == "__main__":
    main()