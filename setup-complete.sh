#!/bin/bash

# WP Bulk Manager Enhanced - Complete Setup Script
# One-command setup for the entire system

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║    WP Bulk Manager Enhanced - Complete Setup          ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"

# ========================================
# Step 1: Make all scripts executable
# ========================================
echo -e "\n${BLUE}Step 1: Setting up executables...${NC}"
chmod +x "$SCRIPT_DIR"/*.sh
echo -e "${GREEN}✓ All scripts are now executable${NC}"

# ========================================
# Step 2: Create required directories
# ========================================
echo -e "\n${BLUE}Step 2: Creating directories...${NC}"
mkdir -p "$SCRIPT_DIR"/{logs,backups,temp,cache}
mkdir -p "$SCRIPT_DIR/macos-app/data"
echo -e "${GREEN}✓ Directories created${NC}"

# ========================================
# Step 3: Setup Python environment
# ========================================
echo -e "\n${BLUE}Step 3: Setting up Python environment...${NC}"
if [ ! -d "$SCRIPT_DIR/macos-app/venv" ]; then
    cd "$SCRIPT_DIR/macos-app"
    python3 -m venv venv
    source venv/bin/activate
    pip install --quiet requests sqlite3 python-dotenv beautifulsoup4 jinja2
    echo -e "${GREEN}✓ Python virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Python virtual environment already exists${NC}"
fi

# ========================================
# Step 4: Create configuration file
# ========================================
echo -e "\n${BLUE}Step 4: Creating configuration...${NC}"
if [ ! -f "$SCRIPT_DIR/config.json" ]; then
    cat > "$SCRIPT_DIR/config.json" << 'EOF'
{
  "sites": [],
  "features": {
    "seo": true,
    "schema": true,
    "litespeed": true,
    "vultr": false,
    "performance": true
  },
  "settings": {
    "backup_enabled": true,
    "backup_interval": "daily",
    "monitoring_enabled": true,
    "auto_update": false
  }
}
EOF
    echo -e "${GREEN}✓ Configuration file created${NC}"
else
    echo -e "${GREEN}✓ Configuration file already exists${NC}"
fi

# ========================================
# Step 5: Check dependencies
# ========================================
echo -e "\n${BLUE}Step 5: Checking dependencies...${NC}"
missing_deps=()

# Required dependencies
for cmd in curl jq wp php; do
    if ! command -v $cmd &> /dev/null; then
        missing_deps+=($cmd)
    fi
done

if [ ${#missing_deps[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Missing dependencies: ${missing_deps[*]}${NC}"
    echo "Install them with:"
    for dep in "${missing_deps[@]}"; do
        case $dep in
            wp)
                echo "  curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp"
                ;;
            jq)
                echo "  brew install jq  # macOS"
                echo "  apt-get install jq  # Ubuntu/Debian"
                ;;
            *)
                echo "  Install $dep using your package manager"
                ;;
        esac
    done
fi

# ========================================
# Step 6: Setup WordPress plugin
# ========================================
echo -e "\n${BLUE}Step 6: WordPress plugin setup...${NC}"
echo -e "${YELLOW}To install on your WordPress site:${NC}"
echo "1. Copy wp-bulk-manager-enhanced.php to wp-content/plugins/wp-bulk-manager/"
echo "2. Activate the plugin: wp plugin activate wp-bulk-manager"
echo "3. Get your API key: wp option get wpbm_api_key"
echo ""

# ========================================
# Step 7: Quick start guide
# ========================================
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Quick Start Commands:${NC}"
echo ""
echo "1. ${BLUE}Validate everything:${NC}"
echo "   ./validate-and-test.sh"
echo ""
echo "2. ${BLUE}Manage WordPress sites:${NC}"
echo "   ./wordpress-site-manager.sh"
echo ""
echo "3. ${BLUE}Optimize OpenLiteSpeed:${NC}"
echo "   ./openlitespeed-optimizer.sh"
echo ""
echo "4. ${BLUE}Vultr server management (optional):${NC}"
echo "   ./vultr-wordpress-manager.sh"
echo ""
echo "5. ${BLUE}Python CLI management:${NC}"
echo "   cd macos-app && source venv/bin/activate"
echo "   python3 wpbm_cli_enhanced.py"
echo ""
echo -e "${GREEN}Documentation:${NC} README-ENHANCED.md"
echo -e "${GREEN}API Spec:${NC} openapi-spec.yaml"
echo ""

# ========================================
# Step 8: Add site wizard
# ========================================
echo -e "${YELLOW}Would you like to add a WordPress site now? (y/n)${NC}"
read -r add_site

if [[ "$add_site" =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Site URL (e.g., https://opdee.com): " site_url
    read -p "Site name: " site_name
    read -p "API key: " api_key
    
    # Add to config
    cat > "$SCRIPT_DIR/temp_site.json" << EOF
{
  "name": "$site_name",
  "url": "$site_url",
  "api_key": "$api_key",
  "added": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    
    # Update config.json using jq
    if command -v jq &> /dev/null; then
        jq '.sites += [input]' "$SCRIPT_DIR/config.json" "$SCRIPT_DIR/temp_site.json" > "$SCRIPT_DIR/config_new.json"
        mv "$SCRIPT_DIR/config_new.json" "$SCRIPT_DIR/config.json"
        rm "$SCRIPT_DIR/temp_site.json"
        echo -e "${GREEN}✓ Site added to configuration${NC}"
    else
        echo -e "${YELLOW}Note: Install jq to automatically update config.json${NC}"
        echo "Site details saved to temp_site.json - add manually to config.json"
    fi
fi

echo -e "\n${GREEN}🚀 WP Bulk Manager Enhanced is ready to use!${NC}"