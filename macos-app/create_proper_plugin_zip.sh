#!/bin/bash

echo "Creating properly structured WordPress plugin zip..."

# Create a temporary directory
TEMP_DIR="/tmp/wp-bulk-manager-client"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy plugin files to temp directory
echo "Copying plugin files..."
cp -r /Users/derekzar/Documents/Projects/wp-bulk-manager/wordpress-plugin/* "$TEMP_DIR/"

# Remove old versions directory as it's not needed
rm -rf "$TEMP_DIR/old-versions"

# Create the zip file with proper structure
echo "Creating zip file..."
cd /tmp
zip -r wp-bulk-manager-client.zip wp-bulk-manager-client/ -x "*.DS_Store" -x "__MACOSX"

# Move to macos-app directory
mv wp-bulk-manager-client.zip /Users/derekzar/Documents/Projects/wp-bulk-manager/macos-app/

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ Plugin zip created successfully!"
echo ""
echo "The plugin has been packaged correctly as wp-bulk-manager-client.zip"
echo ""
echo "To install:"
echo "1. Go to WordPress Admin → Plugins → Add New"
echo "2. Click 'Upload Plugin'"
echo "3. Choose wp-bulk-manager-client.zip"
echo "4. Click 'Install Now' then 'Activate'"
echo ""
echo "The plugin structure is now:"
echo "wp-bulk-manager-client/"
echo "├── wp-bulk-manager-client-robust.php (main plugin file)"
echo "├── includes/"
echo "├── assets/"
echo "├── readme.txt"
echo "└── README.md"