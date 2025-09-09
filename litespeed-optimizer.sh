#!/bin/bash

# LiteSpeed Cache Optimizer for WordPress on Vultr Servers
# Optimized settings for OpenLiteSpeed/LiteSpeed Enterprise

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to install LiteSpeed Cache plugin
install_litespeed() {
    local site_path=$1
    echo -e "${BLUE}Installing LiteSpeed Cache plugin...${NC}"
    wp plugin install litespeed-cache --activate --path="$site_path"
}

# Function to configure LiteSpeed Cache for optimal performance
configure_litespeed_optimal() {
    local site_path=$1
    echo -e "${BLUE}Configuring LiteSpeed Cache with optimal settings...${NC}"
    
    # Cache settings
    wp litespeed-option set cache-browser true --path="$site_path"
    wp litespeed-option set cache-mobile true --path="$site_path"
    wp litespeed-option set cache-mobile_rules 'Mobile|Android|Silk/|Kindle|BlackBerry|Opera Mini|Opera Mobi' --path="$site_path"
    
    # Enable all cache types
    wp litespeed-option set cache true --path="$site_path"
    wp litespeed-option set cache-commenter true --path="$site_path"
    wp litespeed-option set cache-rest true --path="$site_path"
    wp litespeed-option set cache-page_login true --path="$site_path"
    wp litespeed-option set cache-favicon true --path="$site_path"
    wp litespeed-option set cache-resources true --path="$site_path"
    
    # TTL settings (in seconds)
    wp litespeed-option set cache-ttl_pub 604800 --path="$site_path"  # 7 days for public pages
    wp litespeed-option set cache-ttl_priv 1800 --path="$site_path"   # 30 min for private pages
    wp litespeed-option set cache-ttl_frontpage 604800 --path="$site_path"  # 7 days for homepage
    wp litespeed-option set cache-ttl_feed 604800 --path="$site_path"  # 7 days for feeds
    
    # Purge settings
    wp litespeed-option set purge-upgrade true --path="$site_path"
    wp litespeed-option set purge-post_all true --path="$site_path"
    wp litespeed-option set purge-post_f true --path="$site_path"
    wp litespeed-option set purge-post_h true --path="$site_path"
    wp litespeed-option set purge-post_p true --path="$site_path"
    wp litespeed-option set purge-post_a true --path="$site_path"
    wp litespeed-option set purge-post_y true --path="$site_path"
    wp litespeed-option set purge-post_m true --path="$site_path"
    wp litespeed-option set purge-post_d true --path="$site_path"
    wp litespeed-option set purge-post_t true --path="$site_path"
    wp litespeed-option set purge-post_cat true --path="$site_path"
    
    echo -e "${GREEN}✓ Cache settings configured${NC}"
}

# Function to configure image optimization
configure_litespeed_images() {
    local site_path=$1
    echo -e "${BLUE}Configuring image optimization...${NC}"
    
    # Image optimization settings
    wp litespeed-option set img_optm-auto true --path="$site_path"
    wp litespeed-option set img_optm-cron true --path="$site_path"
    wp litespeed-option set img_optm-ori false --path="$site_path"  # Don't keep originals to save space
    wp litespeed-option set img_optm-rm_bkup false --path="$site_path"
    wp litespeed-option set img_optm-webp true --path="$site_path"
    wp litespeed-option set img_optm-lossless false --path="$site_path"  # Lossy for better compression
    wp litespeed-option set img_optm-exif false --path="$site_path"  # Remove EXIF data
    wp litespeed-option set img_optm-webp_replace true --path="$site_path"
    
    # Lazy load settings
    wp litespeed-option set media-lazy true --path="$site_path"
    wp litespeed-option set media-lazy_inc_img true --path="$site_path"
    wp litespeed-option set media-lazy_inc_iframe true --path="$site_path"
    wp litespeed-option set media-lazyjs_inline true --path="$site_path"
    wp litespeed-option set media-placeholder_resp_svg true --path="$site_path"
    
    echo -e "${GREEN}✓ Image optimization configured${NC}"
}

# Function to configure CSS/JS optimization
configure_litespeed_assets() {
    local site_path=$1
    echo -e "${BLUE}Configuring CSS/JS optimization...${NC}"
    
    # CSS optimization
    wp litespeed-option set optm-css_min true --path="$site_path"
    wp litespeed-option set optm-css_comb true --path="$site_path"
    wp litespeed-option set optm-css_comb_ext_inl true --path="$site_path"
    wp litespeed-option set optm-css_async true --path="$site_path"
    wp litespeed-option set optm-ccss_gen true --path="$site_path"  # Generate critical CSS
    wp litespeed-option set optm-ccss_async true --path="$site_path"
    wp litespeed-option set optm-css_async_inline true --path="$site_path"
    wp litespeed-option set optm-css_font_display 'swap' --path="$site_path"
    
    # JavaScript optimization
    wp litespeed-option set optm-js_min true --path="$site_path"
    wp litespeed-option set optm-js_comb true --path="$site_path"
    wp litespeed-option set optm-js_comb_ext_inl true --path="$site_path"
    wp litespeed-option set optm-js_defer 2 --path="$site_path"  # Defer all JS
    
    # HTML optimization
    wp litespeed-option set optm-html_min true --path="$site_path"
    wp litespeed-option set optm-html_lazy true --path="$site_path"
    wp litespeed-option set optm-qs_rm true --path="$site_path"  # Remove query strings
    wp litespeed-option set optm-ggfonts_rm false --path="$site_path"  # Keep Google fonts
    wp litespeed-option set optm-ggfonts_async true --path="$site_path"
    
    # DNS prefetch
    wp litespeed-option set optm-dns_prefetch 'fonts.googleapis.com
fonts.gstatic.com
ajax.googleapis.com
cdnjs.cloudflare.com' --path="$site_path"
    
    echo -e "${GREEN}✓ CSS/JS optimization configured${NC}"
}

# Function to configure database optimization
configure_litespeed_database() {
    local site_path=$1
    echo -e "${BLUE}Configuring database optimization...${NC}"
    
    # Database cleanup settings
    wp litespeed-option set db_optm-revisions 10 --path="$site_path"
    wp litespeed-option set db_optm-auto_draft true --path="$site_path"
    wp litespeed-option set db_optm-trashed_posts true --path="$site_path"
    wp litespeed-option set db_optm-spam_comments true --path="$site_path"
    wp litespeed-option set db_optm-trashed_comments true --path="$site_path"
    wp litespeed-option set db_optm-expired_transients true --path="$site_path"
    wp litespeed-option set db_optm-all_transients false --path="$site_path"
    wp litespeed-option set db_optm-optimize_tables true --path="$site_path"
    
    echo -e "${GREEN}✓ Database optimization configured${NC}"
}

# Function to configure CDN (Cloudflare)
configure_litespeed_cdn() {
    local site_path=$1
    echo -e "${BLUE}Configuring CDN settings for Cloudflare...${NC}"
    
    # CDN settings
    wp litespeed-option set cdn true --path="$site_path"
    wp litespeed-option set cdn-ori '/wp-content
/wp-includes
/wp-admin' --path="$site_path"
    wp litespeed-option set cdn-inc_img true --path="$site_path"
    wp litespeed-option set cdn-inc_css true --path="$site_path"
    wp litespeed-option set cdn-inc_js true --path="$site_path"
    wp litespeed-option set cdn-attr 'src
data-src
href
poster
data-poster' --path="$site_path"
    
    echo -e "${GREEN}✓ CDN configured${NC}"
}

# Function to configure crawler for cache warmup
configure_litespeed_crawler() {
    local site_path=$1
    echo -e "${BLUE}Configuring crawler for cache warmup...${NC}"
    
    # Crawler settings
    wp litespeed-option set crawler true --path="$site_path"
    wp litespeed-option set crawler-run_interval 3600 --path="$site_path"  # Run every hour
    wp litespeed-option set crawler-run_duration 300 --path="$site_path"  # Run for 5 minutes
    wp litespeed-option set crawler-threads 3 --path="$site_path"
    wp litespeed-option set crawler-load_limit 1 --path="$site_path"
    wp litespeed-option set crawler-sitemap 'sitemap.xml' --path="$site_path"
    
    echo -e "${GREEN}✓ Crawler configured${NC}"
}

# Function to configure ESI (Edge Side Includes)
configure_litespeed_esi() {
    local site_path=$1
    echo -e "${BLUE}Configuring ESI for dynamic content...${NC}"
    
    # ESI settings (requires LiteSpeed Enterprise)
    wp litespeed-option set esi true --path="$site_path"
    wp litespeed-option set esi-cache_admbar true --path="$site_path"
    wp litespeed-option set esi-cache_commform true --path="$site_path"
    wp litespeed-option set esi-nonce 'wp_rest' --path="$site_path"
    
    echo -e "${GREEN}✓ ESI configured${NC}"
}

# Function to configure for WooCommerce
configure_litespeed_woocommerce() {
    local site_path=$1
    echo -e "${BLUE}Configuring for WooCommerce...${NC}"
    
    # WooCommerce specific settings
    wp litespeed-option set cache-wc_session true --path="$site_path"
    wp litespeed-option set cache-vary_cookies 'woocommerce_items_in_cart
woocommerce_cart_hash' --path="$site_path"
    wp litespeed-option set cache-exc '/cart
/checkout
/my-account' --path="$site_path"
    
    echo -e "${GREEN}✓ WooCommerce optimization configured${NC}"
}

# Function to configure for Vultr Object Storage
configure_litespeed_vultr_object_storage() {
    local site_path=$1
    # Vultr Object Storage parameters - reserved for future S3-compatible storage
    # When implemented, these will configure CDN and object storage:
    # $2 = endpoint URL
    # $3 = access key  
    # $4 = secret key
    # $5 = bucket name
    
    echo -e "${BLUE}Configuring Vultr Object Storage...${NC}"
    
    # For now, configure Redis object cache (Vultr S3 integration coming soon)
    wp litespeed-option set object true --path="$site_path"
    wp litespeed-option set object-kind 1 --path="$site_path"  # Redis
    wp litespeed-option set object-host '127.0.0.1' --path="$site_path"
    wp litespeed-option set object-port 6379 --path="$site_path"
    
    # Future implementation will use parameters $3-$5 for S3 configuration
    echo -e "${GREEN}✓ Object cache configured (Redis)${NC}"
}

# Function to test configuration
test_litespeed_config() {
    local site_url=$1
    echo -e "${BLUE}Testing LiteSpeed Cache configuration...${NC}"
    
    # Test cache headers
    echo -e "${YELLOW}Testing cache headers...${NC}"
    curl -I -s "$site_url" | grep -i "x-litespeed-cache"
    
    # Test page load time
    echo -e "${YELLOW}Testing page load time...${NC}"
    curl -w "Time: %{time_total}s\n" -o /dev/null -s "$site_url"
    
    # Check cache status
    echo -e "${YELLOW}Cache status:${NC}"
    wp litespeed-purge all --path="$site_path"
    wp litespeed-show status --path="$site_path"
}

# Function for complete optimization
complete_optimization() {
    local site_path=$1
    
    echo -e "${GREEN}Starting complete LiteSpeed optimization...${NC}"
    
    install_litespeed "$site_path"
    configure_litespeed_optimal "$site_path"
    configure_litespeed_images "$site_path"
    configure_litespeed_assets "$site_path"
    configure_litespeed_database "$site_path"
    configure_litespeed_cdn "$site_path"
    configure_litespeed_crawler "$site_path"
    configure_litespeed_esi "$site_path"
    
    # Purge all cache after configuration
    wp litespeed-purge all --path="$site_path"
    
    echo -e "${GREEN}✅ LiteSpeed Cache fully optimized!${NC}"
}

# Main menu
show_menu() {
    echo -e "${GREEN}LiteSpeed Cache Optimizer for Vultr${NC}"
    echo "====================================="
    echo "1. Complete optimization (recommended)"
    echo "2. Configure cache only"
    echo "3. Configure image optimization"
    echo "4. Configure CSS/JS optimization"
    echo "5. Configure database optimization"
    echo "6. Configure CDN (Cloudflare)"
    echo "7. Configure crawler"
    echo "8. Configure ESI"
    echo "9. Configure for WooCommerce"
    echo "10. Test configuration"
    echo "11. Purge all cache"
    echo "0. Exit"
    echo ""
    read -p "Select option: " option
    
    case $option in
        1) read -p "Site path: " path && complete_optimization "$path" ;;
        2) read -p "Site path: " path && configure_litespeed_optimal "$path" ;;
        3) read -p "Site path: " path && configure_litespeed_images "$path" ;;
        4) read -p "Site path: " path && configure_litespeed_assets "$path" ;;
        5) read -p "Site path: " path && configure_litespeed_database "$path" ;;
        6) read -p "Site path: " path && configure_litespeed_cdn "$path" ;;
        7) read -p "Site path: " path && configure_litespeed_crawler "$path" ;;
        8) read -p "Site path: " path && configure_litespeed_esi "$path" ;;
        9) read -p "Site path: " path && configure_litespeed_woocommerce "$path" ;;
        10) read -p "Site URL: " url && test_litespeed_config "$url" ;;
        11) read -p "Site path: " path && wp litespeed-purge all --path="$path" ;;
        0) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
}

# Show menu loop
while true; do
    show_menu
    echo ""
    read -p "Press Enter to continue..."
    clear
done