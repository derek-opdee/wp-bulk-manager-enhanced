#!/bin/bash
# Add opdee.com to WP Bulk Manager

echo "Enter the API key from opdee.com (Settings → Bulk Manager):"
read -s API_KEY

# Activate virtual environment
source venv/bin/activate

# Add the site
python3 wpbm_manager.py add-site "Opdee" "https://opdee.com" "$API_KEY"

echo ""
echo "Now you can run the GUI with: ./run_gui.sh"