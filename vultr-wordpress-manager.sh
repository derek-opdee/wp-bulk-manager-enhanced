#!/bin/bash

# Vultr + WordPress + OpenLiteSpeed Comprehensive Management System
# Manages Vultr servers, WordPress sites, and OpenLiteSpeed configuration
# Author: Derek - Opdee Digital

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
# MAGENTA='\033[0;35m'  # Reserved for future use
NC='\033[0m'

# Configuration
VULTR_API_KEY="${VULTR_API_KEY}"
WPBM_DIR="/Users/derekzar/Projects/wp-bulk-manager"
# SITES_DB will be used for future integration with the Python management app
# SITES_DB="$WPBM_DIR/macos-app/site_connections.db"
LOGS_DIR="$WPBM_DIR/logs"
BACKUP_DIR="$WPBM_DIR/backups"

# Create necessary directories
mkdir -p "$LOGS_DIR" "$BACKUP_DIR"

# ========================================
# Vultr Management Functions
# ========================================

# Check if Vultr CLI is installed
check_vultr_cli() {
    if ! command -v vultr &> /dev/null; then
        echo -e "${YELLOW}Vultr CLI not installed. Installing...${NC}"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install vultr/vultr-cli/vultr
        else
            curl -L https://github.com/vultr/vultr-cli/releases/latest/download/vultr_Linux_x86_64.tar.gz | tar xz
            sudo mv vultr /usr/local/bin/
        fi
    fi
    
    # Configure API key if not set
    if [ -z "$VULTR_API_KEY" ]; then
        read -p "Enter your Vultr API key: " VULTR_API_KEY
        export VULTR_API_KEY="$VULTR_API_KEY"
        echo "export VULTR_API_KEY='$VULTR_API_KEY'" >> ~/.bashrc
    fi
}

# List all Vultr servers
list_vultr_servers() {
    echo -e "${BLUE}Fetching Vultr servers...${NC}"
    vultr instance list --output json | jq -r '.instances[] | "\(.id) | \(.label) | \(.main_ip) | \(.region) | \(.status)"' | column -t -s '|'
}

# Get server details
get_server_details() {
    local server_id=$1
    echo -e "${BLUE}Server Details for $server_id:${NC}"
    vultr instance get "$server_id" --output json | jq '.'
}

# Monitor server resources
monitor_server_resources() {
    local server_id=$1
    echo -e "${BLUE}Monitoring resources for server $server_id...${NC}"
    
    # Get bandwidth usage
    echo -e "${CYAN}Bandwidth Usage:${NC}"
    vultr instance bandwidth "$server_id" --output json | jq '.'
    
    # Get server metrics (if available)
    echo -e "${CYAN}Server Status:${NC}"
    vultr instance get "$server_id" --output json | jq '{
        status: .status,
        cpu_count: .cpu_count,
        ram: .ram,
        disk: .disk,
        bandwidth_gb: .allowed_bandwidth_gb,
        current_bandwidth_gb: .current_bandwidth_gb
    }'
}

# Create WordPress optimized server
create_wordpress_server() {
    echo -e "${BLUE}Creating WordPress optimized Vultr server...${NC}"
    
    # Get available plans
    echo "Available plans:"
    vultr plans list --output json | jq -r '.plans[] | select(.type == "vc2") | "\(.id) | \(.vcpu_count) vCPU | \(.ram) MB | \(.disk) GB | $\(.monthly_cost)"' | column -t -s '|'
    
    read -p "Enter plan ID: " plan_id
    read -p "Enter server label: " label
    read -p "Enter region (e.g., ewr, lax): " region
    
    # Create server with WordPress app
    vultr instance create \
        --plan "$plan_id" \
        --region "$region" \
        --os 387 \
        --label "$label" \
        --hostname "$label" \
        --enable-ipv6=true \
        --backups=true \
        --ddos=true \
        --activation-email=false \
        --tags "wordpress,openlitespeed" \
        --output json | jq '.'
    
    echo -e "${GREEN}✓ Server created! Waiting for it to be ready...${NC}"
}

# ========================================
# OpenLiteSpeed Management Functions
# ========================================

# Connect to server and configure OpenLiteSpeed
configure_openlitespeed_remote() {
    local server_ip=$1
    local ssh_key=${2:-~/.ssh/id_rsa}
    
    echo -e "${BLUE}Configuring OpenLiteSpeed on $server_ip...${NC}"
    
    # Create configuration script
    cat << 'EOF' > /tmp/ols_config.sh
#!/bin/bash

# Update system
apt-get update && apt-get upgrade -y

# Install OpenLiteSpeed if not installed
if ! command -v /usr/local/lsws/bin/lshttpd &> /dev/null; then
    wget -O - https://repo.litespeed.sh | bash
    apt-get install -y openlitespeed lsphp81 lsphp81-* 
fi

# Configure OpenLiteSpeed for WordPress
cat << 'OLSCONF' > /usr/local/lsws/conf/vhosts/wordpress/vhconf.conf
docRoot                   /var/www/html
index  {
  useServer               0
  indexFiles              index.php index.html
}

rewrite  {
  enable                  1
  autoLoadHtaccess        1
  rules                   <<<END_rules
RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
END_rules
}

context /wp-admin/ {
  location                /wp-admin/
  allowBrowse             1
  extraHeaders            X-Frame-Options SAMEORIGIN
  accessControl  {
    allow                 *
  }
}

scripthandler  {
  add                     lsapi:lsphp81 php
}

module cache {
  checkPrivateCache       1
  checkPublicCache        1
  maxCacheObjSize         10000000
  maxStaleAge             200
  qsCache                 1
  reqCookieCache          1
  respCookieCache         1
  ignoreReqCacheCtrl      1
  ignoreRespCacheCtrl     0
  enableCache             1
  expireInSeconds         3600
  enablePrivateCache      1
  privateExpireInSeconds  3600
  storagePath             /usr/local/lsws/cachedata/
}
OLSCONF

# Optimize PHP settings
cat << 'PHPCONF' > /usr/local/lsws/lsphp81/etc/php/8.1/litespeed/php.ini
memory_limit = 256M
max_execution_time = 300
max_input_time = 300
post_max_size = 64M
upload_max_filesize = 64M
max_file_uploads = 20

opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 10000
opcache.revalidate_freq = 2
opcache.save_comments = 1
PHPCONF

# Install Redis for object caching
apt-get install -y redis-server
systemctl enable redis-server
systemctl start redis-server

# Configure Redis
cat << 'REDISCONF' >> /etc/redis/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
REDISCONF

systemctl restart redis-server

# Install WP-CLI
if ! command -v wp &> /dev/null; then
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    chmod +x wp-cli.phar
    mv wp-cli.phar /usr/local/bin/wp
fi

# Restart OpenLiteSpeed
/usr/local/lsws/bin/lswsctrl restart

echo "OpenLiteSpeed configured for WordPress!"
EOF
    
    # Execute configuration on remote server
    scp -i "$ssh_key" /tmp/ols_config.sh root@"$server_ip":/tmp/
    ssh -i "$ssh_key" root@"$server_ip" "bash /tmp/ols_config.sh"
    
    echo -e "${GREEN}✓ OpenLiteSpeed configured!${NC}"
}

# ========================================
# WordPress Management Functions
# ========================================

# Deploy WordPress to Vultr server
deploy_wordpress() {
    local server_ip=$1
    local domain=$2
    local ssh_key=${3:-~/.ssh/id_rsa}
    
    echo -e "${BLUE}Deploying WordPress to $server_ip for $domain...${NC}"
    
    ssh -i "$ssh_key" root@"$server_ip" << 'EOF'
# Create directory
mkdir -p /var/www/html
cd /var/www/html

# Download WordPress
wp core download --allow-root

# Create wp-config
wp config create \
    --dbname=wordpress \
    --dbuser=wpuser \
    --dbpass="$(openssl rand -base64 32)" \
    --dbhost=localhost \
    --allow-root

# Create database
mysql -e "CREATE DATABASE IF NOT EXISTS wordpress;"
mysql -e "CREATE USER IF NOT EXISTS 'wpuser'@'localhost' IDENTIFIED BY '$(openssl rand -base64 32)';"
mysql -e "GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# Install WordPress
wp core install \
    --url="$domain" \
    --title="WordPress Site" \
    --admin_user=admin \
    --admin_password="$(openssl rand -base64 32)" \
    --admin_email=admin@$domain \
    --allow-root

# Install essential plugins
wp plugin install litespeed-cache --activate --allow-root
wp plugin install wordfence --activate --allow-root
wp plugin install updraftplus --activate --allow-root
wp plugin install the-seo-framework --activate --allow-root

# Install WP Bulk Manager Enhanced
wget https://github.com/opdee/wp-bulk-manager/releases/latest/wp-bulk-manager-enhanced.zip
wp plugin install wp-bulk-manager-enhanced.zip --activate --allow-root

# Set permissions
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html

echo "WordPress deployed successfully!"
EOF
    
    echo -e "${GREEN}✓ WordPress deployed!${NC}"
}

# ========================================
# Bulk Management Functions
# ========================================

# Manage multiple servers at once
bulk_server_management() {
    echo -e "${BLUE}Bulk Server Management${NC}"
    echo "1. Update all servers"
    echo "2. Check all server status"
    echo "3. Backup all WordPress sites"
    echo "4. Update WordPress on all servers"
    echo "5. Configure LiteSpeed on all servers"
    echo "6. Run security scan on all servers"
    read -p "Select option: " option
    
    # Get all server IPs
    servers=$(vultr instance list --output json | jq -r '.instances[].main_ip')
    
    case $option in
        1)
            for server in $servers; do
                echo -e "${YELLOW}Updating $server...${NC}"
                ssh root@"$server" "apt-get update && apt-get upgrade -y"
            done
            ;;
        2)
            for server in $servers; do
                echo -e "${YELLOW}Checking $server...${NC}"
                ssh root@"$server" "uptime && df -h && free -m"
            done
            ;;
        3)
            for server in $servers; do
                echo -e "${YELLOW}Backing up WordPress on $server...${NC}"
                backup_wordpress_site "$server"
            done
            ;;
        4)
            for server in $servers; do
                echo -e "${YELLOW}Updating WordPress on $server...${NC}"
                ssh root@"$server" "cd /var/www/html && wp core update --allow-root && wp plugin update --all --allow-root && wp theme update --all --allow-root"
            done
            ;;
        5)
            for server in $servers; do
                echo -e "${YELLOW}Configuring LiteSpeed on $server...${NC}"
                configure_openlitespeed_remote "$server"
            done
            ;;
        6)
            for server in $servers; do
                echo -e "${YELLOW}Running security scan on $server...${NC}"
                run_security_scan "$server"
            done
            ;;
    esac
}

# Backup WordPress site
backup_wordpress_site() {
    local server_ip=$1
    local backup_name
    backup_name="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    echo -e "${BLUE}Creating backup from $server_ip...${NC}"
    
    ssh -n root@"$server_ip" "cd /var/www/html && wp db export backup.sql --allow-root && tar -czf /tmp/$backup_name ."
    
    # Download backup
    scp root@"$server_ip":/tmp/"$backup_name" "$BACKUP_DIR/"
    
    # Upload to Vultr Object Storage (if configured)
    if command -v s3cmd &> /dev/null; then
        s3cmd put "$BACKUP_DIR/$backup_name" s3://wordpress-backups/
    fi
    
    echo -e "${GREEN}✓ Backup created: $backup_name${NC}"
}

# Run security scan
run_security_scan() {
    local server_ip=$1
    
    echo -e "${BLUE}Running security scan on $server_ip...${NC}"
    
    ssh root@"$server_ip" << 'EOF'
# Check for malware
if command -v clamscan &> /dev/null; then
    clamscan -r /var/www/html --infected --remove
else
    apt-get install -y clamav
    freshclam
    clamscan -r /var/www/html --infected
fi

# Check WordPress integrity
cd /var/www/html
wp core verify-checksums --allow-root
wp plugin verify-checksums --all --allow-root

# Check file permissions
find . -type f -perm 0777 -exec ls -la {} \;
find . -type d -perm 0777 -exec ls -la {} \;

# Check for suspicious files
find . -name "*.php" -exec grep -l "eval\|base64_decode\|system\|exec" {} \;

echo "Security scan complete!"
EOF
    
    echo -e "${GREEN}✓ Security scan completed${NC}"
}

# ========================================
# Performance Optimization Functions
# ========================================

# Optimize server performance
optimize_server_performance() {
    local server_ip=$1
    
    echo -e "${BLUE}Optimizing performance on $server_ip...${NC}"
    
    ssh root@"$server_ip" << 'EOF'
# Optimize MySQL/MariaDB
mysql -e "
SET GLOBAL query_cache_size = 67108864;
SET GLOBAL query_cache_type = 1;
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 268435456;
SET GLOBAL innodb_log_file_size = 67108864;
"

# Optimize system settings
cat << 'SYSCTL' >> /etc/sysctl.conf
# Network optimizations
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr

# File system
fs.file-max = 2097152
fs.inotify.max_user_watches = 524288

# Virtual memory
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
SYSCTL

sysctl -p

# Install and configure Memcached
apt-get install -y memcached
systemctl enable memcached
systemctl start memcached

# Configure swap if not exists
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo "Performance optimizations applied!"
EOF
    
    echo -e "${GREEN}✓ Performance optimized${NC}"
}

# ========================================
# Monitoring Functions
# ========================================

# Setup monitoring
setup_monitoring() {
    local server_ip=$1
    
    echo -e "${BLUE}Setting up monitoring on $server_ip...${NC}"
    
    ssh root@"$server_ip" << 'EOF'
# Install monitoring tools
apt-get install -y htop iotop iftop ncdu

# Install Netdata for real-time monitoring
bash <(curl -Ss https://my-netdata.io/kickstart.sh) --dont-wait

# Setup log monitoring
apt-get install -y logwatch
cat << 'LOGWATCH' > /etc/cron.daily/00logwatch
#!/bin/bash
/usr/sbin/logwatch --mailto admin@example.com --format html --detail high
LOGWATCH
chmod +x /etc/cron.daily/00logwatch

# Setup fail2ban
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

echo "Monitoring setup complete!"
EOF
    
    echo -e "${GREEN}✓ Monitoring configured${NC}"
}

# ========================================
# Integration with WP Bulk Manager
# ========================================

# Sync sites with WP Bulk Manager
sync_with_wp_bulk_manager() {
    echo -e "${BLUE}Syncing Vultr sites with WP Bulk Manager...${NC}"
    
    # Get all servers
    servers=$(vultr instance list --output json | jq -r '.instances[]')
    
    # For each server, get WordPress sites
    echo "$servers" | while read -r server; do
        server_ip=$(echo "$server" | jq -r '.main_ip')
        server_label=$(echo "$server" | jq -r '.label')
        
        # Check if WordPress is installed
        if ssh root@"$server_ip" "test -f /var/www/html/wp-config.php" 2>/dev/null; then
            # Get site URL
            site_url=$(ssh root@"$server_ip" "cd /var/www/html && wp option get siteurl --allow-root" 2>/dev/null)
            
            if [ ! -z "$site_url" ]; then
                # Add to WP Bulk Manager database
                echo "Adding $site_url to WP Bulk Manager..."
                
                # Get API key from WordPress
                api_key=$(ssh root@"$server_ip" "cd /var/www/html && wp option get wpbm_api_key --allow-root" 2>/dev/null)
                
                # Add to Python manager
                cd "$WPBM_DIR/macos-app"
                python3 -c "
import sqlite3
conn = sqlite3.connect('site_connections.db')
cursor = conn.cursor()
cursor.execute('''
    INSERT OR REPLACE INTO sites (name, url, api_key, server_ip, server_label)
    VALUES (?, ?, ?, ?, ?)
''', ('$server_label', '$site_url', '$api_key', '$server_ip', '$server_label'))
conn.commit()
conn.close()
print('Site added: $site_url')
"
            fi
        fi
    done
    
    echo -e "${GREEN}✓ Sync complete${NC}"
}

# ========================================
# Main Menu
# ========================================

show_main_menu() {
    clear
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Vultr + WordPress + OpenLiteSpeed Manager         ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Server Management:${NC}"
    echo "  1. List Vultr servers"
    echo "  2. Get server details"
    echo "  3. Monitor server resources"
    echo "  4. Create WordPress server"
    echo "  5. Configure OpenLiteSpeed"
    echo ""
    echo -e "${CYAN}WordPress Management:${NC}"
    echo "  6. Deploy WordPress"
    echo "  7. Backup WordPress site"
    echo "  8. Update WordPress"
    echo "  9. Run security scan"
    echo ""
    echo -e "${CYAN}Bulk Operations:${NC}"
    echo "  10. Bulk server management"
    echo "  11. Sync with WP Bulk Manager"
    echo ""
    echo -e "${CYAN}Optimization:${NC}"
    echo "  12. Optimize server performance"
    echo "  13. Setup monitoring"
    echo "  14. Configure LiteSpeed Cache"
    echo ""
    echo "  0. Exit"
    echo ""
    read -p "Select option: " option
    
    case $option in
        1) list_vultr_servers ;;
        2) read -p "Server ID: " id && get_server_details "$id" ;;
        3) read -p "Server ID: " id && monitor_server_resources "$id" ;;
        4) create_wordpress_server ;;
        5) read -p "Server IP: " ip && configure_openlitespeed_remote "$ip" ;;
        6) 
            read -p "Server IP: " ip
            read -p "Domain: " domain
            deploy_wordpress "$ip" "$domain"
            ;;
        7) read -p "Server IP: " ip && backup_wordpress_site "$ip" ;;
        8) 
            read -p "Server IP: " ip
            ssh root@"$ip" "cd /var/www/html && wp core update --allow-root && wp plugin update --all --allow-root"
            ;;
        9) read -p "Server IP: " ip && run_security_scan "$ip" ;;
        10) bulk_server_management ;;
        11) sync_with_wp_bulk_manager ;;
        12) read -p "Server IP: " ip && optimize_server_performance "$ip" ;;
        13) read -p "Server IP: " ip && setup_monitoring "$ip" ;;
        14) 
            read -p "Server IP: " ip
            ssh root@"$ip" "cd /var/www/html && bash /Users/derekzar/Projects/wp-bulk-manager/openlitespeed-optimizer.sh"
            ;;
        0) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    show_main_menu
}

# ========================================
# Script Initialization
# ========================================

# Check dependencies
check_vultr_cli

# Show main menu
show_main_menu