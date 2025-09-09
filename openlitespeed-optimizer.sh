#!/bin/bash

# OpenLiteSpeed + LiteSpeed Cache Optimizer for WordPress on Vultr
# Optimized specifically for OpenLiteSpeed (not Enterprise)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# OpenLiteSpeed specific paths
OLS_CONF="/usr/local/lsws/conf/httpd_config.conf"
# OLS_VHOST_CONF="/usr/local/lsws/conf/vhosts"  # Reserved for future vhost management
# OLS_ADMIN="/usr/local/lsws/admin"  # Reserved for admin panel integration

# Function to configure LiteSpeed Cache for OpenLiteSpeed
configure_litespeed_for_ols() {
    local site_path=$1
    echo -e "${BLUE}Configuring LiteSpeed Cache for OpenLiteSpeed...${NC}"
    
    # Install if not present
    wp plugin is-installed litespeed-cache --path="$site_path" || \
        wp plugin install litespeed-cache --activate --path="$site_path"
    
    # === CACHE SETTINGS (OpenLiteSpeed optimized) ===
    wp litespeed-option set cache true --path="$site_path"
    wp litespeed-option set cache-browser true --path="$site_path"
    wp litespeed-option set cache-mobile true --path="$site_path"
    wp litespeed-option set cache-commenter true --path="$site_path"
    wp litespeed-option set cache-rest true --path="$site_path"
    wp litespeed-option set cache-page_login true --path="$site_path"
    
    # TTL Settings optimized for OpenLiteSpeed
    wp litespeed-option set cache-ttl_pub 604800 --path="$site_path"      # 7 days
    wp litespeed-option set cache-ttl_priv 1800 --path="$site_path"       # 30 min
    wp litespeed-option set cache-ttl_frontpage 604800 --path="$site_path" # 7 days
    wp litespeed-option set cache-ttl_feed 0 --path="$site_path"          # No cache for feeds
    
    # Purge settings
    wp litespeed-option set purge-upgrade true --path="$site_path"
    wp litespeed-option set purge-post_all false --path="$site_path"  # Don't purge all on post update
    wp litespeed-option set purge-post_f true --path="$site_path"     # Purge front page
    wp litespeed-option set purge-post_h true --path="$site_path"     # Purge home
    wp litespeed-option set purge-post_p true --path="$site_path"     # Purge post page
    wp litespeed-option set purge-post_a true --path="$site_path"     # Purge archive
    
    # Exclude pages that should never be cached
    wp litespeed-option set cache-exc '/cart
/checkout
/my-account
/wp-admin
/wp-login.php' --path="$site_path"
    
    # Exclude cookies
    wp litespeed-option set cache-exc_cookies 'wordpress_logged_in_
wp-postpass_
woocommerce_items_in_cart
woocommerce_cart_hash
wptouch_switch_toggle' --path="$site_path"
    
    echo -e "${GREEN}✓ Cache configured for OpenLiteSpeed${NC}"
}

# Function to optimize images (works great with OLS)
configure_image_optimization() {
    local site_path=$1
    echo -e "${BLUE}Configuring image optimization...${NC}"
    
    # Image optimization - OpenLiteSpeed handles WebP well
    wp litespeed-option set img_optm-auto true --path="$site_path"
    wp litespeed-option set img_optm-cron true --path="$site_path"
    wp litespeed-option set img_optm-ori true --path="$site_path"        # Keep originals
    wp litespeed-option set img_optm-rm_bkup true --path="$site_path"    # Remove backups after success
    wp litespeed-option set img_optm-webp true --path="$site_path"       # Create WebP
    wp litespeed-option set img_optm-lossless false --path="$site_path"  # Lossy for better compression
    wp litespeed-option set img_optm-exif true --path="$site_path"       # Remove EXIF
    wp litespeed-option set img_optm-webp_replace true --path="$site_path" # Serve WebP when possible
    
    # Lazy load - critical for performance
    wp litespeed-option set media-lazy true --path="$site_path"
    wp litespeed-option set media-lazy_inc_img true --path="$site_path"
    wp litespeed-option set media-lazy_inc_iframe true --path="$site_path"
    wp litespeed-option set media-lazy_inc_vid true --path="$site_path"
    wp litespeed-option set media-lazyjs_inline true --path="$site_path"
    wp litespeed-option set media-placeholder_resp_svg true --path="$site_path"
    
    # VPI (Viewport Images) - preload above-fold images
    wp litespeed-option set media-vpi true --path="$site_path"
    wp litespeed-option set media-vpi_cron true --path="$site_path"
    
    echo -e "${GREEN}✓ Image optimization configured${NC}"
}

# Function to optimize CSS/JS (adjusted for OLS limitations)
configure_assets_optimization() {
    local site_path=$1
    echo -e "${BLUE}Configuring CSS/JS optimization for OpenLiteSpeed...${NC}"
    
    # CSS Optimization
    wp litespeed-option set optm-css_min true --path="$site_path"
    wp litespeed-option set optm-css_comb true --path="$site_path"
    wp litespeed-option set optm-css_comb_ext_inl true --path="$site_path"
    
    # Critical CSS (UCSS) - Great for OLS
    wp litespeed-option set optm-ccss_gen true --path="$site_path"
    wp litespeed-option set optm-ccss_async true --path="$site_path"
    wp litespeed-option set optm-ccss_per_url true --path="$site_path"
    
    # JS Optimization
    wp litespeed-option set optm-js_min true --path="$site_path"
    wp litespeed-option set optm-js_comb true --path="$site_path"
    wp litespeed-option set optm-js_comb_ext_inl true --path="$site_path"
    wp litespeed-option set optm-js_defer 2 --path="$site_path"  # Defer all
    
    # HTML Optimization
    wp litespeed-option set optm-html_min true --path="$site_path"
    wp litespeed-option set optm-qs_rm true --path="$site_path"
    wp litespeed-option set optm-ggfonts_async true --path="$site_path"
    
    # DNS Prefetch & Preconnect
    wp litespeed-option set optm-dns_prefetch 'fonts.googleapis.com
fonts.gstatic.com
www.googletagmanager.com
www.google-analytics.com' --path="$site_path"
    
    wp litespeed-option set optm-dns_preconnect 'https://fonts.googleapis.com
https://fonts.gstatic.com' --path="$site_path"
    
    echo -e "${GREEN}✓ CSS/JS optimization configured${NC}"
}

# Function to configure database optimization
configure_database_optimization() {
    local site_path=$1
    echo -e "${BLUE}Configuring database optimization...${NC}"
    
    # Database cleanup
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

# Function to configure Object Cache (Redis/Memcached)
configure_object_cache() {
    local site_path=$1
    echo -e "${BLUE}Configuring Object Cache...${NC}"
    
    # Check if Redis is available
    if command -v redis-cli &> /dev/null; then
        echo -e "${YELLOW}Redis detected, configuring...${NC}"
        
        wp litespeed-option set object true --path="$site_path"
        wp litespeed-option set object-kind 1 --path="$site_path"  # Redis
        wp litespeed-option set object-host '127.0.0.1' --path="$site_path"
        wp litespeed-option set object-port 6379 --path="$site_path"
        wp litespeed-option set object-life 360 --path="$site_path"
        wp litespeed-option set object-persistent true --path="$site_path"
        wp litespeed-option set object-cache_wp_admin true --path="$site_path"
        wp litespeed-option set object-cache_comment true --path="$site_path"
        wp litespeed-option set object-cache_pagenavi true --path="$site_path"
        
        echo -e "${GREEN}✓ Redis object cache configured${NC}"
    else
        echo -e "${YELLOW}Redis not found. Install with: sudo apt install redis-server${NC}"
    fi
}

# Function to configure crawler (cache warmup)
configure_crawler() {
    local site_path=$1
    echo -e "${BLUE}Configuring crawler for cache warmup...${NC}"
    
    wp litespeed-option set crawler true --path="$site_path"
    wp litespeed-option set crawler-usleep 500 --path="$site_path"         # Microseconds between requests
    wp litespeed-option set crawler-run_interval 3600 --path="$site_path"  # Every hour
    wp litespeed-option set crawler-run_duration 400 --path="$site_path"   # 400 seconds max
    wp litespeed-option set crawler-threads 3 --path="$site_path"          # 3 parallel threads
    wp litespeed-option set crawler-load_limit 1 --path="$site_path"       # Server load limit
    wp litespeed-option set crawler-sitemap 'sitemap.xml
sitemap_index.xml' --path="$site_path"
    
    echo -e "${GREEN}✓ Crawler configured${NC}"
}

# Function to configure for Cloudflare integration
configure_cloudflare_integration() {
    local site_path=$1
    echo -e "${BLUE}Configuring Cloudflare integration...${NC}"
    
    # CDN settings for Cloudflare
    wp litespeed-option set cdn true --path="$site_path"
    wp litespeed-option set cdn-cloudflare true --path="$site_path"
    wp litespeed-option set cdn-cloudflare_status true --path="$site_path"
    
    # Use Cloudflare for static files
    wp litespeed-option set cdn-inc_img true --path="$site_path"
    wp litespeed-option set cdn-inc_css true --path="$site_path"
    wp litespeed-option set cdn-inc_js true --path="$site_path"
    
    # Guest mode optimization (works great with Cloudflare)
    wp litespeed-option set guest true --path="$site_path"
    wp litespeed-option set guest-ips '108.162.0.0/16
172.64.0.0/16
173.245.48.0/20
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
141.101.64.0/18
188.114.96.0/20
190.93.240.0/20
197.234.240.0/22
198.41.128.0/17' --path="$site_path"  # Cloudflare IPs
    
    echo -e "${GREEN}✓ Cloudflare integration configured${NC}"
}

# Function to optimize OpenLiteSpeed server config
optimize_ols_server_config() {
    echo -e "${BLUE}Optimizing OpenLiteSpeed server configuration...${NC}"
    
    # Create backup
    sudo cp "$OLS_CONF" "$OLS_CONF.backup.$(date +%Y%m%d)"
    
    # Optimize cache module settings
    cat << 'EOF' | sudo tee /usr/local/lsws/conf/modules/cache/cache.conf
checkPrivateCache   1
checkPublicCache    1
maxCacheObjSize     10000000
maxStaleAge         200
qsCache             1
reqCookieCache      1
respCookieCache     1
ignoreReqCacheCtrl  1
ignoreRespCacheCtrl 0

enableCache         0
expireInSeconds     3600
enablePrivateCache  0
privateExpireInSeconds 3600

storagePath /usr/local/lsws/cachedata/
EOF
    
    # Restart OpenLiteSpeed
    sudo /usr/local/lsws/bin/lswsctrl restart
    
    echo -e "${GREEN}✓ OpenLiteSpeed server optimized${NC}"
}

# Function for complete OpenLiteSpeed optimization
complete_ols_optimization() {
    local site_path=$1
    
    echo -e "${GREEN}Starting complete OpenLiteSpeed + LiteSpeed Cache optimization...${NC}"
    
    # Core optimizations
    configure_litespeed_for_ols "$site_path"
    configure_image_optimization "$site_path"
    configure_assets_optimization "$site_path"
    configure_database_optimization "$site_path"
    configure_object_cache "$site_path"
    configure_crawler "$site_path"
    configure_cloudflare_integration "$site_path"
    
    # Purge all cache
    wp litespeed-purge all --path="$site_path"
    
    # Generate critical CSS
    wp litespeed-online ccss --path="$site_path"
    
    # Start crawler to warm cache
    wp litespeed-crawler run --path="$site_path"
    
    echo -e "${GREEN}✅ OpenLiteSpeed + LiteSpeed Cache fully optimized!${NC}"
    echo -e "${YELLOW}Note: Critical CSS generation and crawler are running in background${NC}"
}

# Function to monitor cache performance
monitor_cache_performance() {
    local site_url=$1
    echo -e "${BLUE}Monitoring cache performance...${NC}"
    
    # Test cache hit rate
    echo -e "${YELLOW}Testing cache headers...${NC}"
    for i in {1..3}; do
        echo "Request $i:"
        curl -I -s "$site_url" | grep -E "x-litespeed-cache|x-litespeed-tag|cf-cache-status"
        sleep 1
    done
    
    # Test page speed
    echo -e "${YELLOW}Page load times:${NC}"
    for i in {1..3}; do
        time=$(curl -w "%{time_total}" -o /dev/null -s "$site_url")
        echo "Load $i: ${time}s"
    done
}

# Main menu
show_menu() {
    echo -e "${GREEN}OpenLiteSpeed + LiteSpeed Cache Optimizer${NC}"
    echo "=========================================="
    echo "1. Complete optimization (recommended)"
    echo "2. Configure cache only"
    echo "3. Configure image optimization"
    echo "4. Configure CSS/JS optimization"
    echo "5. Configure database optimization"
    echo "6. Configure object cache (Redis)"
    echo "7. Configure crawler"
    echo "8. Configure Cloudflare integration"
    echo "9. Optimize OpenLiteSpeed server config"
    echo "10. Monitor cache performance"
    echo "11. Purge all cache"
    echo "12. Generate critical CSS"
    echo "0. Exit"
    echo ""
    read -p "Select option: " option
    
    case $option in
        1) read -p "Site path: " path && complete_ols_optimization "$path" ;;
        2) read -p "Site path: " path && configure_litespeed_for_ols "$path" ;;
        3) read -p "Site path: " path && configure_image_optimization "$path" ;;
        4) read -p "Site path: " path && configure_assets_optimization "$path" ;;
        5) read -p "Site path: " path && configure_database_optimization "$path" ;;
        6) read -p "Site path: " path && configure_object_cache "$path" ;;
        7) read -p "Site path: " path && configure_crawler "$path" ;;
        8) read -p "Site path: " path && configure_cloudflare_integration "$path" ;;
        9) optimize_ols_server_config ;;
        10) read -p "Site URL: " url && monitor_cache_performance "$url" ;;
        11) read -p "Site path: " path && wp litespeed-purge all --path="$path" ;;
        12) read -p "Site path: " path && wp litespeed-online ccss --path="$site_path" ;;
        0) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
}

# Check if running as appropriate user
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Don't run as root unless optimizing server config${NC}"
fi

# Show menu loop
while true; do
    show_menu
    echo ""
    read -p "Press Enter to continue..."
    clear
done