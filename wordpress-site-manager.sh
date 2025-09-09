#!/bin/bash

# WordPress Site Management Script for Opdee
# Manages plugins, updates, and configurations across multiple sites

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
# Removed unused variables - functionality integrated directly

# Essential plugins for all sites
ESSENTIAL_PLUGINS=(
    "kadence-blocks"
    "kadence-starter-templates"
    "admin-site-enhancements"
    "the-seo-framework"
    "litespeed-cache"
    "wordfence"
    "updraftplus"
)

# Performance plugins (kept for future use)
# PERFORMANCE_PLUGINS=(
#     "perfmatters"
#     "wp-optimize"
#     "autoptimize"
# )

# Function to check if WP-CLI is installed
check_wpcli() {
    if ! command -v wp &> /dev/null; then
        echo -e "${RED}WP-CLI is not installed${NC}"
        echo "Install with: brew install wp-cli"
        exit 1
    fi
}

# Function to install essential plugins
install_essential_plugins() {
    local site_path=$1
    echo -e "${BLUE}Installing essential plugins for $site_path...${NC}"
    
    for plugin in "${ESSENTIAL_PLUGINS[@]}"; do
        echo -e "${YELLOW}Installing $plugin...${NC}"
        wp plugin install "$plugin" --activate --path="$site_path" 2>/dev/null || echo "Already installed or error"
    done
}

# Function to update all plugins
update_all_plugins() {
    local site_path=$1
    echo -e "${BLUE}Updating all plugins...${NC}"
    wp plugin update --all --path="$site_path"
}

# Function to configure Perfmatters
configure_perfmatters() {
    local site_path=$1
    echo -e "${BLUE}Configuring Perfmatters...${NC}"
    
    wp option update perfmatters_options '{
        "lazy_loading": true,
        "lazy_loading_iframes": true,
        "lazy_loading_videos": true,
        "add_missing_dimensions": true,
        "delay_js": true,
        "delay_timeout": 3,
        "remove_jquery_migrate": true,
        "remove_wp_embed": true,
        "remove_block_library_css": false,
        "disable_emojis": true,
        "disable_embeds": true,
        "disable_xml_rpc": true,
        "remove_feed_links": false,
        "remove_rest_api_links": false,
        "remove_shortlink": true,
        "remove_wlw_manifest": true,
        "remove_rsd_link": true,
        "remove_wordpress_version": true,
        "remove_comment_feed_links": true,
        "remove_comment_count": false,
        "limit_post_revisions": 10,
        "autosave_interval": 60,
        "disable_heartbeat": "default",
        "heartbeat_frequency": 60,
        "limit_login_attempts": true,
        "disable_google_fonts": false,
        "local_analytics": true,
        "disable_google_maps": false,
        "disable_password_strength_meter": false,
        "disable_comments": false,
        "close_comments": false,
        "remove_comment_url_field": true
    }' --path="$site_path" --format=json
}

# Function to configure Kadence theme
configure_kadence() {
    local site_path=$1
    echo -e "${BLUE}Configuring Kadence theme...${NC}"
    
    # Set Kadence theme options
    wp option update kadence_settings '{
        "page_layout": "normal",
        "page_title": false,
        "page_breadcrumbs": true,
        "header_sticky": "main",
        "header_transparent": false,
        "footer_widgets": "3",
        "scroll_to_top": true,
        "performance_preload": true,
        "performance_critical_css": true
    }' --path="$site_path" --format=json
}

# Function to take visual snapshot
take_visual_snapshot() {
    local site_url=$1
    local snapshot_dir="/Users/derekzar/Projects/wp-bulk-manager/visual-snapshots"
    local date
    date=$(date +%Y%m%d)
    
    mkdir -p "$snapshot_dir/$date"
    
    echo -e "${BLUE}Taking visual snapshot of $site_url...${NC}"
    
    # Use Playwright to take screenshots
    npx playwright screenshot \
        "$site_url" \
        "$snapshot_dir/$date/$(echo $site_url | sed 's/[^a-zA-Z0-9]/_/g').png" \
        --full-page \
        --wait-for-load-state networkidle
}

# Function to run visual regression test
run_visual_regression() {
    local site_url=$1
    echo -e "${BLUE}Running visual regression test for $site_url...${NC}"
    
    # This would integrate with BackstopJS or similar
    backstop test --config="backstop-$site_url.json"
}

# Function to check site health
check_site_health() {
    local site_path=$1
    echo -e "${BLUE}Checking site health...${NC}"
    
    # Check PHP version
    wp cli info --path="$site_path"
    
    # Check for updates
    wp core check-update --path="$site_path"
    wp plugin list --update=available --path="$site_path"
    wp theme list --update=available --path="$site_path"
    
    # Check database
    wp db check --path="$site_path"
}

# Function to setup monitoring
setup_monitoring() {
    local site_path=$1
    echo -e "${BLUE}Setting up monitoring...${NC}"
    
    # Install and configure monitoring plugin
    wp plugin install query-monitor --activate --path="$site_path"
    wp plugin install wp-crontrol --activate --path="$site_path"
}

# Main menu
show_menu() {
    echo -e "${GREEN}WordPress Site Management Tool${NC}"
    echo "================================"
    echo "1. Install essential plugins"
    echo "2. Update all plugins"
    echo "3. Configure Perfmatters"
    echo "4. Configure Kadence theme"
    echo "5. Take visual snapshot"
    echo "6. Run visual regression test"
    echo "7. Check site health"
    echo "8. Setup monitoring"
    echo "9. Bulk operations (Python CLI)"
    echo "0. Exit"
    echo ""
    read -p "Select option: " option
    
    case $option in
        1) read -p "Site path: " path && install_essential_plugins "$path" ;;
        2) read -p "Site path: " path && update_all_plugins "$path" ;;
        3) read -p "Site path: " path && configure_perfmatters "$path" ;;
        4) read -p "Site path: " path && configure_kadence "$path" ;;
        5) read -p "Site URL: " url && take_visual_snapshot "$url" ;;
        6) read -p "Site URL: " url && run_visual_regression "$url" ;;
        7) read -p "Site path: " path && check_site_health "$path" ;;
        8) read -p "Site path: " path && setup_monitoring "$path" ;;
        9) cd /Users/derekzar/Projects/wp-bulk-manager/macos-app && ./run_enhanced.sh ;;
        0) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
}

# Check requirements
check_wpcli

# Show menu
while true; do
    show_menu
    echo ""
    read -p "Press Enter to continue..."
    clear
done