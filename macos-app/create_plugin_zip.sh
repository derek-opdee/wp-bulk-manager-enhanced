#!/bin/bash

echo "Creating WordPress Bulk Manager plugin zip files..."

# Navigate to the parent directory
cd /Users/derekzar/Documents/Projects/wp-bulk-manager/

# Create the main hub plugin zip
echo "Creating wp-bulk-manager-hub.zip..."
zip -r wp-bulk-manager-hub.zip wp-bulk-manager.php includes/ assets/ -x "*.DS_Store" -x "__MACOSX"

# Create the client plugin zip
echo "Creating wp-bulk-manager-client.zip..."
cd wordpress-plugin/
zip -r ../wp-bulk-manager-client.zip * -x "*.DS_Store" -x "__MACOSX"

cd ..

# Move zips to macos-app directory
mv wp-bulk-manager-hub.zip macos-app/
mv wp-bulk-manager-client.zip macos-app/

echo "✅ Plugin zip files created successfully!"
echo ""
echo "Two plugin files have been created:"
echo "1. wp-bulk-manager-hub.zip - Main hub plugin for managing multiple sites"
echo "2. wp-bulk-manager-client.zip - Client plugin to install on each WordPress site"
echo ""
echo "To install:"
echo "- For the main management site: Upload wp-bulk-manager-hub.zip"
echo "- For each site you want to manage: Upload wp-bulk-manager-client.zip"