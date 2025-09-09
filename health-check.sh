#!/bin/bash

# WP Bulk Manager Enhanced - System Health Check
# Comprehensive health monitoring for all components

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEALTH_SCORE=100
ISSUES=()

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
}

check_service() {
    local service=$1
    local check_command=$2
    local importance=$3  # critical=10, high=5, medium=3, low=1
    
    if eval "$check_command" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $service is healthy"
        return 0
    else
        echo -e "${RED}✗${NC} $service has issues"
        HEALTH_SCORE=$((HEALTH_SCORE - importance))
        ISSUES+=("$service is not functioning properly")
        return 1
    fi
}

# ========================================
# Core Services Check
# ========================================

check_core_services() {
    print_header "Core Services Health"
    
    # Check PHP
    check_service "PHP Runtime" "php -v" 10
    
    # Check WordPress CLI
    check_service "WordPress CLI" "wp --version" 10
    
    # Check Redis
    check_service "Redis Cache" "redis-cli ping" 5
    
    # Check Vultr CLI
    check_service "Vultr CLI" "vultr version" 3
    
    # Check Python
    check_service "Python Environment" "python3 --version" 5
    
    # Check Node.js
    check_service "Node.js" "node --version" 3
}

# ========================================
# API Endpoints Check
# ========================================

check_api_endpoints() {
    print_header "API Endpoints Health"
    
    if [ -f "$SCRIPT_DIR/config.json" ]; then
        local sites=$(jq -r '.sites[] | @json' "$SCRIPT_DIR/config.json" 2>/dev/null)
        
        if [ ! -z "$sites" ]; then
            echo "$sites" | while read -r site_json; do
                local site=$(echo "$site_json" | jq -r '.')
                local name=$(echo "$site" | jq -r '.name')
                local url=$(echo "$site" | jq -r '.url')
                local api_key=$(echo "$site" | jq -r '.api_key')
                
                echo -e "\n${CYAN}Checking: $name${NC}"
                
                # Test API endpoint
                local response=$(curl -s -o /dev/null -w "%{http_code}" \
                    -H "X-API-Key: $api_key" \
                    "$url/wp-json/wpbm/v1/auth" 2>/dev/null)
                
                if [ "$response" = "200" ]; then
                    echo -e "${GREEN}✓${NC} API endpoint responding"
                else
                    echo -e "${RED}✗${NC} API endpoint not responding (HTTP $response)"
                    HEALTH_SCORE=$((HEALTH_SCORE - 5))
                    ISSUES+=("$name API endpoint not responding")
                fi
                
                # Check SSL certificate
                if echo | openssl s_client -connect "${url#https://}:443" 2>/dev/null | openssl x509 -noout -checkend 86400; then
                    echo -e "${GREEN}✓${NC} SSL certificate valid"
                else
                    echo -e "${YELLOW}⚠${NC} SSL certificate expiring soon"
                    HEALTH_SCORE=$((HEALTH_SCORE - 2))
                    ISSUES+=("$name SSL certificate needs renewal")
                fi
            done
        else
            echo -e "${YELLOW}No sites configured${NC}"
        fi
    fi
}

# ========================================
# File System Check
# ========================================

check_filesystem() {
    print_header "File System Health"
    
    # Check required directories
    local dirs=("logs" "backups" "macos-app" "monitoring" "performance-reports")
    
    for dir in "${dirs[@]}"; do
        if [ -d "$SCRIPT_DIR/$dir" ]; then
            echo -e "${GREEN}✓${NC} Directory exists: $dir"
        else
            echo -e "${YELLOW}⚠${NC} Directory missing: $dir (creating...)"
            mkdir -p "$SCRIPT_DIR/$dir"
        fi
    done
    
    # Check disk space
    local disk_usage=$(df -h "$SCRIPT_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$disk_usage" -lt 80 ]; then
        echo -e "${GREEN}✓${NC} Disk space adequate ($disk_usage% used)"
    elif [ "$disk_usage" -lt 90 ]; then
        echo -e "${YELLOW}⚠${NC} Disk space warning ($disk_usage% used)"
        HEALTH_SCORE=$((HEALTH_SCORE - 3))
        ISSUES+=("Disk space is running low")
    else
        echo -e "${RED}✗${NC} Disk space critical ($disk_usage% used)"
        HEALTH_SCORE=$((HEALTH_SCORE - 10))
        ISSUES+=("Disk space is critically low")
    fi
    
    # Check log file sizes
    if [ -d "$SCRIPT_DIR/logs" ]; then
        local log_size=$(du -sh "$SCRIPT_DIR/logs" 2>/dev/null | cut -f1)
        echo -e "${GREEN}✓${NC} Log directory size: $log_size"
    fi
}

# ========================================
# Performance Metrics
# ========================================

check_performance() {
    print_header "Performance Metrics"
    
    # Check CPU usage
    local cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
    
    if (( $(echo "$cpu_usage < 70" | bc -l) )); then
        echo -e "${GREEN}✓${NC} CPU usage normal ($cpu_usage%)"
    else
        echo -e "${YELLOW}⚠${NC} CPU usage high ($cpu_usage%)"
        HEALTH_SCORE=$((HEALTH_SCORE - 3))
        ISSUES+=("High CPU usage detected")
    fi
    
    # Check memory usage
    local mem_info=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local mem_free=$((mem_info * 4096 / 1048576))  # Convert to MB
    
    if [ "$mem_free" -gt 1000 ]; then
        echo -e "${GREEN}✓${NC} Memory available: ${mem_free}MB"
    else
        echo -e "${YELLOW}⚠${NC} Low memory: ${mem_free}MB"
        HEALTH_SCORE=$((HEALTH_SCORE - 5))
        ISSUES+=("Low memory available")
    fi
    
    # Check Redis performance
    if command -v redis-cli &> /dev/null; then
        local redis_ping=$(redis-cli ping 2>/dev/null)
        if [ "$redis_ping" = "PONG" ]; then
            local redis_memory=$(redis-cli info memory | grep used_memory_human | cut -d: -f2 | tr -d '\r')
            echo -e "${GREEN}✓${NC} Redis memory usage: $redis_memory"
        fi
    fi
}

# ========================================
# Security Check
# ========================================

check_security() {
    print_header "Security Status"
    
    # Check file permissions
    local bad_perms=$(find "$SCRIPT_DIR" -type f -perm 0777 2>/dev/null | wc -l)
    
    if [ "$bad_perms" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} File permissions secure"
    else
        echo -e "${RED}✗${NC} Found $bad_perms files with insecure permissions"
        HEALTH_SCORE=$((HEALTH_SCORE - 5))
        ISSUES+=("Files with insecure permissions found")
    fi
    
    # Check for sensitive data in logs
    if [ -d "$SCRIPT_DIR/logs" ]; then
        local sensitive=$(grep -r "password\|api_key\|secret" "$SCRIPT_DIR/logs" 2>/dev/null | wc -l)
        
        if [ "$sensitive" -eq 0 ]; then
            echo -e "${GREEN}✓${NC} No sensitive data in logs"
        else
            echo -e "${YELLOW}⚠${NC} Potential sensitive data found in logs"
            HEALTH_SCORE=$((HEALTH_SCORE - 3))
            ISSUES+=("Sensitive data may be exposed in logs")
        fi
    fi
    
    # Check API key configuration
    if [ ! -z "$VULTR_API_KEY" ] && [ "$VULTR_API_KEY" != "YOUR_VULTR_API_KEY_HERE" ]; then
        echo -e "${GREEN}✓${NC} Vultr API key configured"
    else
        echo -e "${YELLOW}⚠${NC} Vultr API key not configured"
    fi
    
    if [ ! -z "$CLOUDFLARE_API_TOKEN" ]; then
        echo -e "${GREEN}✓${NC} Cloudflare API token configured"
    else
        echo -e "${YELLOW}⚠${NC} Cloudflare API token not configured"
    fi
}

# ========================================
# Backup Status
# ========================================

check_backups() {
    print_header "Backup Status"
    
    local backup_dir="$SCRIPT_DIR/backups"
    
    if [ -d "$backup_dir" ]; then
        # Find latest backup
        local latest_backup=$(find "$backup_dir" -type f -name "*.tar.gz" -mtime -7 2>/dev/null | head -1)
        
        if [ ! -z "$latest_backup" ]; then
            local backup_age=$(find "$latest_backup" -mtime +0 -mtime -1 2>/dev/null | wc -l)
            if [ "$backup_age" -gt 0 ]; then
                echo -e "${GREEN}✓${NC} Recent backup found (< 24 hours old)"
            else
                echo -e "${YELLOW}⚠${NC} Last backup is older than 24 hours"
                HEALTH_SCORE=$((HEALTH_SCORE - 2))
            fi
        else
            echo -e "${RED}✗${NC} No recent backups found"
            HEALTH_SCORE=$((HEALTH_SCORE - 5))
            ISSUES+=("No recent backups found")
        fi
        
        # Check backup directory size
        local backup_size=$(du -sh "$backup_dir" 2>/dev/null | cut -f1)
        echo -e "${CYAN}Backup directory size: $backup_size${NC}"
    else
        echo -e "${RED}✗${NC} Backup directory not found"
        HEALTH_SCORE=$((HEALTH_SCORE - 5))
        ISSUES+=("Backup directory missing")
    fi
}

# ========================================
# Generate Health Report
# ========================================

generate_report() {
    print_header "Health Check Summary"
    
    # Determine health status
    local status_color
    local status_text
    
    if [ $HEALTH_SCORE -ge 90 ]; then
        status_color=$GREEN
        status_text="EXCELLENT"
    elif [ $HEALTH_SCORE -ge 75 ]; then
        status_color=$YELLOW
        status_text="GOOD"
    elif [ $HEALTH_SCORE -ge 60 ]; then
        status_color=$YELLOW
        status_text="FAIR"
    else
        status_color=$RED
        status_text="CRITICAL"
    fi
    
    echo -e "\n${status_color}System Health Score: $HEALTH_SCORE/100 - $status_text${NC}"
    
    if [ ${#ISSUES[@]} -gt 0 ]; then
        echo -e "\n${YELLOW}Issues Found:${NC}"
        for issue in "${ISSUES[@]}"; do
            echo -e "  ${RED}•${NC} $issue"
        done
        
        echo -e "\n${CYAN}Recommendations:${NC}"
        echo "  1. Address critical issues immediately"
        echo "  2. Schedule regular maintenance"
        echo "  3. Review security configurations"
        echo "  4. Ensure backups are running"
    else
        echo -e "\n${GREEN}✅ No issues detected - System is healthy!${NC}"
    fi
    
    # Save report
    local report_file="$SCRIPT_DIR/logs/health-check-$(date +%Y%m%d-%H%M%S).log"
    mkdir -p "$SCRIPT_DIR/logs"
    
    {
        echo "Health Check Report - $(date)"
        echo "Score: $HEALTH_SCORE/100"
        echo "Status: $status_text"
        echo ""
        if [ ${#ISSUES[@]} -gt 0 ]; then
            echo "Issues:"
            for issue in "${ISSUES[@]}"; do
                echo "  - $issue"
            done
        fi
    } > "$report_file"
    
    echo -e "\n${GREEN}Report saved to: $report_file${NC}"
}

# ========================================
# Main Execution
# ========================================

main() {
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     WP Bulk Manager Enhanced - System Health Check    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    
    # Source environment
    if [ -f ~/.claude/.env ]; then
        source ~/.claude/.env
    fi
    
    # Run all checks
    check_core_services
    check_api_endpoints
    check_filesystem
    check_performance
    check_security
    check_backups
    
    # Generate report
    generate_report
}

# Run main function
main "$@"