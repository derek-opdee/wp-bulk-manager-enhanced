# Claude WordPress Generate Page Mode

## Command: `/wordpress_gen_page`

This document provides Claude with instructions for creating SEO Generator pages using the WP Bulk Manager system.

## Overview

SEO Generator pages use dynamic fields to create multiple variations of a page for different search terms and locations. This process involves:
1. Finding a template page
2. Copying its Gutenberg/Kadence blocks
3. Replacing static content with dynamic fields
4. Configuring search terms and locations

## Dynamic Fields

- `[search_term]` - Singular form (e.g., "Web Design")
- `[search_terms]` - Plural form (e.g., "Web Design Services")
- `[location]` - Location name (e.g., "Melbourne")

## Grammar Best Practices

### 1. Avoid Common Mistakes

**❌ DON'T DO:**
- `[search_term] & [search_term]` - Repeats the same term
- `We build [search_term]s` - Creates awkward plurals like "AI Development Services-s"
- `[search_term] services services` - Double "services" when term already includes it

**✅ DO INSTEAD:**
- `[search_term] Solutions` - Use "solutions" to avoid double "services"
- `We build [search_term] solutions` - Cleaner grammar
- `Our [search_term] helps` - Singular usage

### 2. Handle Terms with "Services"

When search terms already include "Services":
```
Term: "AI Web Development Services"

❌ Wrong: "AI Web Development Services services"
✅ Right: "AI Web Development Services solutions"
✅ Right: "Our AI Web Development Services help..."
```

### 3. Natural Phrasing

**Test each phrase with different terms:**
```
Pattern: "We provide [search_term] in [location]"

✅ "We provide AI Integration in Melbourne"
✅ "We provide AI Development Services in Sydney"
✅ "We provide AI API Integration in Brisbane"
```

### 4. Location Usage

**Strategic placement:**
- H1: Include both [search_term] and [location]
- First paragraph: Mention [location] early
- Throughout: 3-5 natural [location] mentions
- CTAs: "Get started in [location]"

**Natural patterns:**
- "Our [location] team"
- "Serving [location] businesses"
- "[location]'s trusted [search_term] provider"
- "Help your [location] business grow"

## Step-by-Step Process

### 1. Connect to the Site
```python
from wpbm_assistant import wpbm_connect
assistant = wpbm_connect()
```

### 2. Find a Suitable Template Page
```python
# List pages to find a good template
pages = assistant.manager.list_all_content(assistant.current_site_id, 'page', 50)
for page in pages:
    print(f"ID: {page['id']} - {page['title']}")

# Get full content of chosen page
template_page = assistant.get_page_content(PAGE_ID)
content = template_page['content']
```

### 3. Transform Content with Dynamic Fields

```python
import re

# Replace service terms
content = re.sub(r'web design(?:er)?s?', '[search_term]', content, flags=re.I)
content = re.sub(r'website development', '[search_term]', content, flags=re.I)
content = re.sub(r'wordpress development', '[search_term]', content, flags=re.I)

# Replace plural forms
content = re.sub(r'web design services', '[search_terms]', content, flags=re.I)
content = re.sub(r'website developers', '[search_terms]', content, flags=re.I)

# Replace locations
content = re.sub(r'Melbourne|Sydney|Brisbane|Perth|Adelaide', '[location]', content)

# Update specific patterns
content = content.replace('in Melbourne', 'in [location]')
content = content.replace('Melbourne\'s', '[location]\'s')
content = content.replace('Melbourne-based', '[location]-based')
```

### 4. Common Content Patterns to Replace

#### Headings
```html
<!-- Original -->
<h2>Professional Web Design Services in Melbourne</h2>

<!-- Dynamic -->
<h2>Professional [search_term] Services in [location]</h2>
```

#### Body Text
```html
<!-- Original -->
<p>Looking for expert web designers in Melbourne? Our team specializes in creating stunning websites for Melbourne businesses.</p>

<!-- Dynamic -->
<p>Looking for expert [search_terms] in [location]? Our team specializes in creating stunning websites for [location] businesses.</p>
```

#### CTAs
```html
<!-- Original -->
<a href="/contact">Get Web Design Quote</a>

<!-- Dynamic -->
<a href="/contact">Get [search_term] Quote</a>
```

### 5. Create the SEO Generator Page

After preparing the content:

1. **In WordPress Admin**:
   - Go to SEO Generator > Add New
   - Paste the transformed content
   - Save as draft

2. **Configure via Bulk Manager**:
```python
# Get the new page ID
seo_pages = assistant.manager.get_seo_generator_pages(assistant.current_site_id)
new_page_id = # Find your new page

# Configure search terms and locations
data = {
    'search_terms': [
        'Web Design',
        'Website Development',
        'WordPress Development',
        'Web Application Development',
        'Custom Website Design'
    ],
    'locations': [
        'Melbourne',
        'Sydney',
        'Brisbane',
        'Perth',
        'Adelaide',
        'Canberra',
        'Gold Coast',
        'Newcastle'
    ],
    'url_structure': '[search_term]-in-[location]'
}

assistant.manager.update_seo_generator_page(
    assistant.current_site_id, 
    new_page_id, 
    data
)
```

### 6. Set SEO Patterns

Update the page's SEO settings:
```python
seo_data = {
    'title': 'Best [search_term] in [location] | Your Company',
    'description': 'Looking for professional [search_terms] in [location]? We deliver custom solutions for [location] businesses. Get a free quote today!'
}

assistant.update_page_seo(new_page_id, seo_data)
```

## Example Full Workflow

```python
# 1. Connect
from wpbm_assistant import wpbm_connect
assistant = wpbm_connect()

# 2. Find template (e.g., existing service page)
template = assistant.get_page_content(3616)

# 3. Transform content
import re
content = template['content']

# Service term replacements
service_terms = [
    'AI development', 'artificial intelligence', 'machine learning',
    'web app integration', 'API development', 'custom integration'
]

for term in service_terms:
    # Replace with singular
    content = re.sub(rf'\b{term}\b', '[search_term]', content, flags=re.I)
    # Replace plural/service forms
    content = re.sub(rf'\b{term} services?\b', '[search_terms]', content, flags=re.I)

# Location replacements (if any)
locations = ['Melbourne', 'Sydney', 'Brisbane', 'Australia']
for loc in locations:
    content = re.sub(rf'\b{loc}\b', '[location]', content)

# 4. Manual step: Create in WordPress
print("Create new SEO Generator page in WordPress with this content:")
print(content[:500] + "...")

# 5. After creating, configure it
# page_id = NEW_PAGE_ID
# data = {
#     'search_terms': ['AI Development', 'Machine Learning', 'API Integration'],
#     'locations': ['Melbourne', 'Sydney', 'Brisbane'],
#     'url_structure': '[search_term]-[location]'
# }
# assistant.manager.update_seo_generator_page(assistant.current_site_id, page_id, data)
```

## Best Practices

1. **Choose Good Templates**: Select pages with strong design and clear service descriptions
2. **Preserve Structure**: Keep all Gutenberg/Kadence blocks intact
3. **Natural Language**: Ensure dynamic fields create grammatically correct sentences
4. **Test First**: Create one variation and test before adding all terms/locations
5. **SEO Optimization**: Use dynamic fields in meta titles and descriptions

## Common Replacements

### Service Industries
- Web Design → [search_term]
- Web Designers → [search_terms]
- Website Development → [search_term]
- Digital Marketing → [search_term]
- SEO Services → [search_terms]

### Location Patterns
- in Melbourne → in [location]
- Melbourne's best → [location]'s best
- serving Melbourne → serving [location]
- Melbourne businesses → [location] businesses
- throughout Melbourne → throughout [location]

### Action Words
- Get Web Design → Get [search_term]
- Hire Web Designers → Hire [search_terms]
- Web Design Quote → [search_term] Quote

## Verification

After creating the page:
```python
# Check the configuration
details = assistant.manager.get_seo_generator_page(assistant.current_site_id, page_id)
print(f"Search Terms: {len(details['search_terms'])}")
print(f"Locations: {len(details['locations'])}")
print(f"Total Variations: {len(details['search_terms']) * len(details['locations'])}")
print(f"Dynamic Field Usage:")
for field, count in details['dynamic_fields'].items():
    print(f"  {field}: {count} occurrences")
```

## Troubleshooting

1. **Dynamic fields not working**: Check exact syntax `[search_term]` with square brackets
2. **Grammar issues**: Use both singular and plural forms appropriately
3. **URL conflicts**: Ensure URL structure creates unique paths
4. **Too many variations**: Limit to quality terms/locations (max 20 terms × 300 locations)

## Quick Reference

```python
# Get template
template = assistant.get_page_content(SOURCE_PAGE_ID)

# Transform content (basic)
content = template['content']
content = content.replace('Web Design', '[search_term]')
content = content.replace('Web Design Services', '[search_terms]')
content = content.replace('Melbourne', '[location]')

# After manual creation in WordPress, configure:
data = {
    'search_terms': ['Term 1', 'Term 2', 'Term 3'],
    'locations': ['Location 1', 'Location 2', 'Location 3'],
    'url_structure': '[search_term]-in-[location]'
}
assistant.manager.update_seo_generator_page(assistant.current_site_id, NEW_PAGE_ID, data)
```