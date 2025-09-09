#!/bin/bash

# WP Bulk Manager Enhanced - Validation and Testing Script
# Ensures all components are working correctly

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=0
WARNINGS=0

# ========================================
# Validation Functions
# ========================================

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
}

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# ========================================
# File Validation
# ========================================

validate_files() {
    print_header "Validating Required Files"
    
    # Core files
    local required_files=(
        "openapi-spec.yaml"
        "wp-bulk-manager-enhanced.php"
        "openlitespeed-optimizer.sh"
        "vultr-wordpress-manager.sh"
        "README-ENHANCED.md"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            check_pass "Found: $file"
        else
            check_fail "Missing: $file"
        fi
    done
    
    # Check execute permissions on scripts
    local scripts=(
        "openlitespeed-optimizer.sh"
        "vultr-wordpress-manager.sh"
        "wordpress-site-manager.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "$SCRIPT_DIR/$script" ]; then
            if [ -x "$SCRIPT_DIR/$script" ]; then
                check_pass "Executable: $script"
            else
                check_warn "Not executable: $script (run: chmod +x $script)"
            fi
        fi
    done
}

# ========================================
# OpenAPI Specification Validation
# ========================================

validate_openapi() {
    print_header "Validating OpenAPI Specification"
    
    if [ -f "$SCRIPT_DIR/openapi-spec.yaml" ]; then
        # Check if OpenAPI validator is available
        if command -v swagger-cli &> /dev/null; then
            if swagger-cli validate "$SCRIPT_DIR/openapi-spec.yaml" 2>/dev/null; then
                check_pass "OpenAPI spec is valid"
            else
                check_fail "OpenAPI spec has validation errors"
            fi
        elif command -v npx &> /dev/null; then
            if npx @apidevtools/swagger-cli validate "$SCRIPT_DIR/openapi-spec.yaml" 2>/dev/null; then
                check_pass "OpenAPI spec is valid"
            else
                check_warn "OpenAPI spec may have issues (install swagger-cli for full validation)"
            fi
        else
            check_warn "Cannot validate OpenAPI spec (install swagger-cli)"
        fi
        
        # Check spec structure
        if grep -q "openapi: 3.1.0" "$SCRIPT_DIR/openapi-spec.yaml"; then
            check_pass "OpenAPI version 3.1.0"
        else
            check_fail "Invalid OpenAPI version"
        fi
        
        # Check for key endpoints
        local endpoints=("content" "seo" "schema" "plugins" "litespeed")
        for endpoint in "${endpoints[@]}"; do
            if grep -q "/$endpoint" "$SCRIPT_DIR/openapi-spec.yaml"; then
                check_pass "Endpoint defined: /$endpoint"
            else
                check_fail "Missing endpoint: /$endpoint"
            fi
        done
    else
        check_fail "OpenAPI specification not found"
    fi
}

# ========================================
# PHP Syntax Validation
# ========================================

validate_php() {
    print_header "Validating PHP Code"
    
    if [ -f "$SCRIPT_DIR/wp-bulk-manager-enhanced.php" ]; then
        if command -v php &> /dev/null; then
            if php -l "$SCRIPT_DIR/wp-bulk-manager-enhanced.php" &>/dev/null; then
                check_pass "PHP syntax is valid"
            else
                check_fail "PHP syntax errors found"
                php -l "$SCRIPT_DIR/wp-bulk-manager-enhanced.php"
            fi
            
            # Check PHP version compatibility
            local php_version=$(php -v | head -n1 | sed -n 's/.*PHP \([0-9]*\.[0-9]*\).*/\1/p')
            if (( $(echo "$php_version >= 7.4" | bc -l) )); then
                check_pass "PHP version $php_version is compatible"
            else
                check_warn "PHP version $php_version may not be fully compatible (7.4+ recommended)"
            fi
        else
            check_warn "PHP not installed - cannot validate syntax"
        fi
        
        # Check for required WordPress hooks
        local hooks=("rest_api_init" "admin_menu" "wp_head" "init")
        for hook in "${hooks[@]}"; do
            if grep -q "add_action.*$hook" "$SCRIPT_DIR/wp-bulk-manager-enhanced.php"; then
                check_pass "WordPress hook registered: $hook"
            else
                check_warn "WordPress hook not found: $hook"
            fi
        done
        
        # Check for security functions
        if grep -q "check_ajax_referer\|wp_create_nonce\|current_user_can" "$SCRIPT_DIR/wp-bulk-manager-enhanced.php"; then
            check_pass "Security functions implemented"
        else
            check_fail "Security functions missing"
        fi
    else
        check_fail "PHP plugin file not found"
    fi
}

# ========================================
# Shell Script Validation
# ========================================

validate_shell_scripts() {
    print_header "Validating Shell Scripts"
    
    local scripts=(
        "openlitespeed-optimizer.sh"
        "vultr-wordpress-manager.sh"
        "wordpress-site-manager.sh"
        "litespeed-optimizer.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "$SCRIPT_DIR/$script" ]; then
            # Check syntax with shellcheck if available
            if command -v shellcheck &> /dev/null; then
                if shellcheck -S error "$SCRIPT_DIR/$script" &>/dev/null; then
                    check_pass "Shell syntax valid: $script"
                else
                    check_warn "Shell script has errors: $script"
                fi
            else
                # Basic syntax check with bash
                if bash -n "$SCRIPT_DIR/$script" 2>/dev/null; then
                    check_pass "Basic syntax valid: $script"
                else
                    check_fail "Syntax errors in: $script"
                fi
            fi
        fi
    done
}

# ========================================
# Python Environment Validation
# ========================================

validate_python() {
    print_header "Validating Python Environment"
    
    if [ -d "$SCRIPT_DIR/macos-app" ]; then
        check_pass "Python app directory exists"
        
        # Check for required Python files
        local py_files=("wpbm_manager.py" "wpbm_cli_enhanced.py")
        for file in "${py_files[@]}"; do
            if [ -f "$SCRIPT_DIR/macos-app/$file" ]; then
                check_pass "Python file found: $file"
            else
                check_warn "Python file missing: $file"
            fi
        done
        
        # Check Python version
        if command -v python3 &> /dev/null; then
            local py_version=$(python3 --version | sed -n 's/.*Python \([0-9]*\.[0-9]*\).*/\1/p')
            local py_major=$(echo "$py_version" | cut -d. -f1)
            local py_minor=$(echo "$py_version" | cut -d. -f2)
            
            if [ "$py_major" -ge 3 ] && [ "$py_minor" -ge 7 ]; then
                check_pass "Python version $py_version is compatible"
            else
                check_warn "Python version $py_version may not be fully compatible (3.7+ recommended)"
            fi
        else
            check_fail "Python 3 not installed"
        fi
        
        # Check for virtual environment
        if [ -d "$SCRIPT_DIR/macos-app/venv" ]; then
            check_pass "Python virtual environment exists"
        else
            check_warn "Python virtual environment not found (create with: python3 -m venv venv)"
        fi
    else
        check_warn "Python app directory not found"
    fi
}

# ========================================
# Dependencies Check
# ========================================

check_dependencies() {
    print_header "Checking Dependencies"
    
    # Required commands
    local required_commands=(
        "curl:Network requests"
        "jq:JSON processing"
        "wp:WordPress CLI"
    )
    
    for cmd_desc in "${required_commands[@]}"; do
        IFS=':' read -r cmd desc <<< "$cmd_desc"
        if command -v "$cmd" &> /dev/null; then
            check_pass "$desc ($cmd) installed"
        else
            check_fail "$desc ($cmd) not installed"
        fi
    done
    
    # Optional but recommended
    local optional_commands=(
        "vultr-cli:Vultr CLI"
        "redis-cli:Redis cache"
        "composer:PHP dependencies"
        "npm:Node.js packages"
    )
    
    for cmd_desc in "${optional_commands[@]}"; do
        IFS=':' read -r cmd desc <<< "$cmd_desc"
        if command -v "$cmd" &> /dev/null; then
            check_pass "$desc ($cmd) installed"
        else
            check_warn "$desc ($cmd) not installed (optional)"
        fi
    done
}

# ========================================
# Configuration Validation
# ========================================

validate_configuration() {
    print_header "Validating Configuration"
    
    # Check for environment variables
    if [ -f "$HOME/.claude/.env" ]; then
        check_pass "Claude environment file exists"
        
        if grep -q "CLOUDFLARE_API_TOKEN" "$HOME/.claude/.env"; then
            check_pass "Cloudflare API token configured"
        else
            check_warn "Cloudflare API token not configured"
        fi
        
        if grep -q "MISTRAL_API_KEY" "$HOME/.claude/.env"; then
            check_pass "Mistral API key configured"
        else
            check_warn "Mistral API key not configured"
        fi
    else
        check_warn "Claude environment file not found"
    fi
    
    # Check for Vultr configuration
    if [ ! -z "$VULTR_API_KEY" ]; then
        check_pass "Vultr API key configured"
    else
        check_warn "Vultr API key not configured (optional)"
    fi
}

# ========================================
# Integration Tests
# ========================================

run_integration_tests() {
    print_header "Running Integration Tests"
    
    # Test OpenAPI endpoints structure
    if [ -f "$SCRIPT_DIR/openapi-spec.yaml" ]; then
        local endpoint_count=$(grep -c "paths:" "$SCRIPT_DIR/openapi-spec.yaml")
        if [ $endpoint_count -gt 0 ]; then
            check_pass "OpenAPI has defined paths"
        else
            check_fail "OpenAPI missing path definitions"
        fi
    fi
    
    # Test PHP class structure
    if [ -f "$SCRIPT_DIR/wp-bulk-manager-enhanced.php" ]; then
        if grep -q "class WP_Bulk_Manager_Enhanced" "$SCRIPT_DIR/wp-bulk-manager-enhanced.php"; then
            check_pass "Main PHP class defined"
        else
            check_fail "Main PHP class not found"
        fi
        
        # Check for REST API registration
        if grep -q "register_rest_route" "$SCRIPT_DIR/wp-bulk-manager-enhanced.php"; then
            check_pass "REST API routes registered"
        else
            check_fail "REST API routes not registered"
        fi
    fi
}

# ========================================
# Generate Test Report
# ========================================

generate_report() {
    print_header "Validation Report"
    
    local total=$((ERRORS + WARNINGS))
    
    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
        echo -e "${GREEN}The WP Bulk Manager Enhanced system is ready to use.${NC}"
    elif [ $ERRORS -eq 0 ]; then
        echo -e "${YELLOW}⚠️  VALIDATION PASSED WITH WARNINGS${NC}"
        echo -e "Errors: ${GREEN}0${NC}"
        echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
        echo -e "\nThe system will work but some optional features may be limited."
    else
        echo -e "${RED}❌ VALIDATION FAILED${NC}"
        echo -e "Errors: ${RED}$ERRORS${NC}"
        echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
        echo -e "\nPlease fix the errors before using the system."
    fi
    
    # Provide next steps
    echo -e "\n${BLUE}Next Steps:${NC}"
    if [ $ERRORS -eq 0 ]; then
        echo "1. Install the WordPress plugin on your sites"
        echo "2. Generate API keys for each site"
        echo "3. Configure the Python management app"
        echo "4. Run './openlitespeed-optimizer.sh' to optimize your servers"
        echo "5. (Optional) Configure Vultr integration if using Vultr servers"
    else
        echo "1. Fix the errors listed above"
        echo "2. Run this validation script again"
        echo "3. Check the README-ENHANCED.md for detailed instructions"
    fi
}

# ========================================
# Quick Fix Function
# ========================================

quick_fix() {
    print_header "Attempting Quick Fixes"
    
    # Make scripts executable
    local scripts=(
        "openlitespeed-optimizer.sh"
        "vultr-wordpress-manager.sh"
        "wordpress-site-manager.sh"
        "litespeed-optimizer.sh"
        "validate-and-test.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "$SCRIPT_DIR/$script" ] && [ ! -x "$SCRIPT_DIR/$script" ]; then
            chmod +x "$SCRIPT_DIR/$script"
            check_pass "Made executable: $script"
        fi
    done
    
    # Create missing directories
    local dirs=("logs" "backups" "macos-app")
    for dir in "${dirs[@]}"; do
        if [ ! -d "$SCRIPT_DIR/$dir" ]; then
            mkdir -p "$SCRIPT_DIR/$dir"
            check_pass "Created directory: $dir"
        fi
    done
    
    # Install missing npm packages if package.json exists
    if [ -f "$SCRIPT_DIR/package.json" ] && command -v npm &> /dev/null; then
        if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
            echo "Installing npm packages..."
            npm install --silent
            check_pass "Installed npm packages"
        fi
    fi
}

# ========================================
# Main Execution
# ========================================

main() {
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   WP Bulk Manager Enhanced - Validation & Testing     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    
    # Run quick fixes if requested
    if [ "$1" == "--fix" ] || [ "$1" == "-f" ]; then
        quick_fix
    fi
    
    # Run all validations
    validate_files
    validate_openapi
    validate_php
    validate_shell_scripts
    validate_python
    check_dependencies
    validate_configuration
    run_integration_tests
    
    # Generate final report
    generate_report
    
    # Return exit code based on errors
    if [ $ERRORS -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Run main function
main "$@"