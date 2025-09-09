# Gutenberg Content Editing Rules for WP Bulk Manager

## 🚨 CRITICAL: Never Break Gutenberg Block Structure

When updating WordPress content through the API, **ALWAYS** preserve Gutenberg block comments and structure.

### ✅ DO:
1. **Preserve all Gutenberg comments**: `<!-- wp:blockname -->` and `<!-- /wp:blockname -->`
2. **Update content within blocks**: Only modify the content between block markers
3. **Use Gutenberg blocks for new content**: When adding elements, create proper block syntax
4. **Respect block attributes**: Keep JSON attributes in block comments intact

### ❌ DON'T:
1. **Never inject raw HTML**: Don't add `<h1>`, `<p>`, etc. outside of Gutenberg blocks
2. **Never remove block comments**: These are essential for the WordPress editor
3. **Never mix HTML with blocks**: Keep everything in Gutenberg format

## Examples:

### Adding an H1 (Correct Way):
```html
<!-- wp:heading {"level":1} -->
<h1>Your Heading Text</h1>
<!-- /wp:heading -->
```

### Changing H1 to H2 (Correct Way):
```html
<!-- Before -->
<!-- wp:heading {"level":1} -->
<h1>Browse</h1>
<!-- /wp:heading -->

<!-- After -->
<!-- wp:heading {"level":2} -->
<h2>Browse</h2>
<!-- /wp:heading -->
```

### Adding a Paragraph (Correct Way):
```html
<!-- wp:paragraph -->
<p>Your paragraph text here.</p>
<!-- /wp:paragraph -->
```

### Common Gutenberg Blocks:
- `<!-- wp:heading {"level":1} -->` - H1-H6 headings
- `<!-- wp:paragraph -->` - Paragraphs
- `<!-- wp:image -->` - Images
- `<!-- wp:list -->` - Lists
- `<!-- wp:kadence/advancedheading -->` - Kadence theme headings

## SEO Updates:
When updating SEO meta data (title, description), use the `seo` field in the API request - never modify content structure for SEO purposes.

## Testing:
Always verify after updates that:
1. The page displays correctly in the browser
2. The WordPress block editor can still open the page
3. No "block recovery" errors appear in the editor