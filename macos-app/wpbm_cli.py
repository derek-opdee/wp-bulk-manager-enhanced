#!/usr/bin/env python3
"""
WP Bulk Manager CLI - Command Line Interface
"""

from wpbm_manager import WPBulkManager, ContentProcessor
import json

def show_menu():
    print("\n" + "="*50)
    print("WP BULK MANAGER - COMMAND LINE")
    print("="*50)
    print("1. List Sites")
    print("2. Create Single Page/Post")
    print("3. Bulk Create with Variables")
    print("4. Test Site Connection")
    print("5. Show Templates")
    print("6. Exit")
    print("="*50)

def list_sites(manager):
    sites = manager.get_sites('all')
    if not sites:
        print("No sites configured.")
        return
    
    print("\nConnected Sites:")
    print("-" * 60)
    print(f"{'ID':<5} {'Name':<20} {'Domain':<30} {'Status':<10}")
    print("-" * 60)
    for site in sites:
        print(f"{site['id']:<5} {site['name']:<20} {site['domain']:<30} {site['status']:<10}")

def create_single_content(manager):
    sites = manager.get_sites('active')
    if not sites:
        print("No active sites available.")
        return
    
    print("\nAvailable Sites:")
    for i, site in enumerate(sites, 1):
        print(f"{i}. {site['name']} ({site['domain']})")
    
    try:
        choice = int(input("\nSelect site number: ")) - 1
        if choice < 0 or choice >= len(sites):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    selected_site = sites[choice]
    
    title = input("Enter title: ")
    print("Enter content (HTML). Type 'END' on a new line when done:")
    content_lines = []
    while True:
        line = input()
        if line == 'END':
            break
        content_lines.append(line)
    content = '\n'.join(content_lines)
    
    content_type = input("Type (post/page) [page]: ") or 'page'
    status = input("Status (draft/publish) [draft]: ") or 'draft'
    
    # SEO fields
    seo_title = input("SEO Title (optional): ")
    seo_desc = input("SEO Description (optional): ")
    
    content_data = {
        'title': title,
        'content': content,
        'type': content_type,
        'status': status
    }
    
    if seo_title or seo_desc:
        content_data['seo'] = {}
        if seo_title:
            content_data['seo']['title'] = seo_title
        if seo_desc:
            content_data['seo']['description'] = seo_desc
    
    print("\nCreating content...")
    results = manager.create_content([selected_site['id']], content_data)
    
    for result in results:
        if result['success']:
            print(f"✅ Created successfully!")
            print(f"   Post ID: {result['post_id']}")
            print(f"   URL: {result['permalink']}")
        else:
            print(f"❌ Failed: {result['error']}")

def bulk_create_with_variables(manager):
    sites = manager.get_sites('active')
    if not sites:
        print("No active sites available.")
        return
    
    print("\nBULK CREATE WITH VARIABLES")
    print("-" * 40)
    
    # Template
    print("\nDefault Template:")
    template = """<h1>{service|capitalize} in {location}</h1>
<p>Looking for reliable {service} in {location}? We offer professional {service_plural} with experienced technicians.</p>
<p>Call us today for {service} in {location}!</p>"""
    print(template)
    
    use_default = input("\nUse default template? (y/n) [y]: ") or 'y'
    if use_default.lower() != 'y':
        print("Enter your template (use {location}, {service}, {service_plural}). Type 'END' when done:")
        template_lines = []
        while True:
            line = input()
            if line == 'END':
                break
            template_lines.append(line)
        template = '\n'.join(template_lines)
    
    # Locations
    print("\nEnter locations (comma-separated):")
    print("Example: Brisbane, Sydney, Melbourne")
    locations_input = input("> ")
    locations = [loc.strip() for loc in locations_input.split(',')]
    
    # Services
    print("\nEnter services (comma-separated):")
    print("Example: painting, plumbing, electrical")
    services_input = input("> ")
    service_keys = [svc.strip() for svc in services_input.split(',')]
    
    # Build service data
    services = {}
    for service in service_keys:
        services[service] = {
            'singular': f"{service} service",
            'plural': f"{service} services"
        }
    
    # Show preview
    print("\nPREVIEW:")
    print("-" * 40)
    processor = ContentProcessor()
    
    # Show first combination
    if locations and services:
        first_location = locations[0]
        first_service = list(services.keys())[0]
        replacements = {
            'location': first_location,
            'service': services[first_service]['singular'],
            'service_plural': services[first_service]['plural']
        }
        preview = processor.process(template, replacements)
        print(preview)
        print("-" * 40)
        print(f"\nTotal pages to create: {len(locations) * len(services)}")
    
    # Select sites
    print("\nAvailable Sites:")
    for i, site in enumerate(sites, 1):
        print(f"{i}. {site['name']} ({site['domain']})")
    
    print("\nSelect sites (comma-separated numbers, or 'all'):")
    sites_input = input("> ")
    
    if sites_input.lower() == 'all':
        selected_site_ids = [site['id'] for site in sites]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in sites_input.split(',')]
            selected_site_ids = [sites[i]['id'] for i in indices if 0 <= i < len(sites)]
        except:
            print("Invalid selection.")
            return
    
    # Confirm
    total_operations = len(selected_site_ids) * len(locations) * len(services)
    print(f"\nThis will create {total_operations} pages total.")
    confirm = input("Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    # Execute
    print("\nCreating pages...")
    results = manager.bulk_create_with_variables(
        selected_site_ids,
        template,
        {'location': locations, 'service': services}
    )
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ Created {success_count}/{len(results)} pages successfully!")

def test_connection(manager):
    sites = manager.get_sites('all')
    if not sites:
        print("No sites configured.")
        return
    
    print("\nSelect site to test:")
    for i, site in enumerate(sites, 1):
        print(f"{i}. {site['name']} ({site['domain']})")
    
    try:
        choice = int(input("\nSelect site number: ")) - 1
        if choice < 0 or choice >= len(sites):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    selected_site = sites[choice]
    api_key = manager.get_site_api_key(selected_site['id'])
    
    print(f"\nTesting connection to {selected_site['name']}...")
    if manager.test_connection(selected_site['url'], api_key):
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")

def show_templates(manager):
    print("\nAVAILABLE TEMPLATES:")
    print("-" * 60)
    
    print("\n1. Service Location Page")
    print("""<h1>{service|capitalize} in {location}</h1>
<p>Looking for reliable {service} in {location}? We offer professional {service_plural}.</p>""")
    
    print("\n2. Emergency Service Page")
    print("""<h1>24/7 Emergency {service|capitalize} in {location}</h1>
<p>Need emergency {service} in {location}? Available 24/7 with fast response times.</p>""")
    
    print("\n3. Best Service Page")
    print("""<h1>Best {service|capitalize} in {location}</h1>
<p>Discover the best {service} in {location}. Top-rated professionals with excellent reviews.</p>""")
    
    print("\nVariables: {location}, {service}, {service_plural}")
    print("Modifiers: |upper, |lower, |capitalize")

def main():
    manager = WPBulkManager()
    
    while True:
        show_menu()
        choice = input("\nSelect option: ")
        
        if choice == '1':
            list_sites(manager)
        elif choice == '2':
            create_single_content(manager)
        elif choice == '3':
            bulk_create_with_variables(manager)
        elif choice == '4':
            test_connection(manager)
        elif choice == '5':
            show_templates(manager)
        elif choice == '6':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()