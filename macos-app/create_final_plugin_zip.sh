#!/bin/bash

echo "Creating final WordPress plugin zip with correct structure..."

# Create a temporary directory
TEMP_DIR="/tmp/wp-bulk-manager-client"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy plugin files to temp directory
echo "Copying plugin files..."
cp /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/wp-bulk-manager-client.php "$TEMP_DIR/"
cp -r /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/includes "$TEMP_DIR/"
cp -r /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/assets "$TEMP_DIR/"
cp /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/readme.txt "$TEMP_DIR/"
cp /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/README.md "$TEMP_DIR/"

# Create the zip file with proper structure
echo "Creating zip file..."
cd /tmp
zip -r wp-bulk-manager-client-final.zip wp-bulk-manager-client/ -x "*.DS_Store" -x "__MACOSX"

# Move to macos-app directory
mv wp-bulk-manager-client-final.zip /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app/

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ Plugin zip created successfully!"
echo ""
echo "The plugin has been packaged as wp-bulk-manager-client-final.zip"
echo ""
echo "Key points:"
echo "- Plugin folder name: wp-bulk-manager-client"
echo "- Main plugin file: wp-bulk-manager-client.php (matches folder name)"
echo "- Has proper WordPress plugin header"
echo ""
echo "To install:"
echo "1. Go to WordPress Admin → Plugins → Add New"
echo "2. Click 'Upload Plugin'"
echo "3. Choose wp-bulk-manager-client-final.zip"
echo "4. Click 'Install Now' then 'Activate'"