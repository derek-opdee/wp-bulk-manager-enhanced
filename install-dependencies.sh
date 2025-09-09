#!/bin/bash

# WP Bulk Manager Enhanced - Dependency Installer
# Helps install optional dependencies for enhanced functionality

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /etc/debian_version ]; then
        OS="debian"
    elif [ -f /etc/redhat-release ]; then
        OS="redhat"
    else
        OS="linux"
    fi
fi

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is already installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        return 1
    fi
}

install_homebrew() {
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
}

install_wpcli() {
    print_header "Installing WP-CLI"
    
    if check_command wp; then
        return
    fi
    
    echo -e "${YELLOW}Installing WP-CLI...${NC}"
    
    if [ "$OS" = "macos" ]; then
        brew install wp-cli
    else
        curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
        chmod +x wp-cli.phar
        sudo mv wp-cli.phar /usr/local/bin/wp
    fi
    
    check_command wp
}

install_jq() {
    print_header "Installing jq (JSON processor)"
    
    if check_command jq; then
        return
    fi
    
    echo -e "${YELLOW}Installing jq...${NC}"
    
    case "$OS" in
        macos)
            brew install jq
            ;;
        debian)
            sudo apt-get update && sudo apt-get install -y jq
            ;;
        redhat)
            sudo yum install -y jq
            ;;
        *)
            echo -e "${RED}Please install jq manually for your system${NC}"
            ;;
    esac
    
    check_command jq
}

install_vultr_cli() {
    print_header "Installing Vultr CLI (Optional)"
    
    if check_command vultr; then
        return
    fi
    
    echo -e "${YELLOW}Would you like to install Vultr CLI? (y/n)${NC}"
    read -r response
    
    if [[ "$response" != "y" ]]; then
        echo "Skipping Vultr CLI installation"
        return
    fi
    
    echo -e "${YELLOW}Installing Vultr CLI...${NC}"
    
    if [ "$OS" = "macos" ]; then
        brew tap vultr/vultr-cli
        brew install vultr-cli
    else
        # Download latest release for Linux
        VULTR_VERSION=$(curl -s https://api.github.com/repos/vultr/vultr-cli/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
        curl -L "https://github.com/vultr/vultr-cli/releases/download/${VULTR_VERSION}/vultr_${VULTR_VERSION#v}_linux_amd64.tar.gz" | tar xz
        sudo mv vultr /usr/local/bin/
    fi
    
    check_command vultr
}

install_redis() {
    print_header "Installing Redis (Optional - for object caching)"
    
    if check_command redis-cli; then
        return
    fi
    
    echo -e "${YELLOW}Would you like to install Redis for object caching? (y/n)${NC}"
    read -r response
    
    if [[ "$response" != "y" ]]; then
        echo "Skipping Redis installation"
        return
    fi
    
    echo -e "${YELLOW}Installing Redis...${NC}"
    
    case "$OS" in
        macos)
            brew install redis
            brew services start redis
            ;;
        debian)
            sudo apt-get update && sudo apt-get install -y redis-server
            sudo systemctl start redis-server
            sudo systemctl enable redis-server
            ;;
        redhat)
            sudo yum install -y redis
            sudo systemctl start redis
            sudo systemctl enable redis
            ;;
        *)
            echo -e "${RED}Please install Redis manually for your system${NC}"
            ;;
    esac
    
    check_command redis-cli
}

install_composer() {
    print_header "Installing Composer (Optional - for PHP dependencies)"
    
    if check_command composer; then
        return
    fi
    
    echo -e "${YELLOW}Would you like to install Composer? (y/n)${NC}"
    read -r response
    
    if [[ "$response" != "y" ]]; then
        echo "Skipping Composer installation"
        return
    fi
    
    echo -e "${YELLOW}Installing Composer...${NC}"
    
    if [ "$OS" = "macos" ]; then
        brew install composer
    else
        curl -sS https://getcomposer.org/installer | php
        sudo mv composer.phar /usr/local/bin/composer
    fi
    
    check_command composer
}

install_npm() {
    print_header "Installing Node.js and npm (Optional)"
    
    if check_command npm; then
        return
    fi
    
    echo -e "${YELLOW}Would you like to install Node.js and npm? (y/n)${NC}"
    read -r response
    
    if [[ "$response" != "y" ]]; then
        echo "Skipping Node.js installation"
        return
    fi
    
    echo -e "${YELLOW}Installing Node.js and npm...${NC}"
    
    if [ "$OS" = "macos" ]; then
        brew install node
    else
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
    
    check_command npm
}

install_shellcheck() {
    print_header "Installing ShellCheck (Optional - for script validation)"
    
    if check_command shellcheck; then
        return
    fi
    
    echo -e "${YELLOW}Would you like to install ShellCheck for script validation? (y/n)${NC}"
    read -r response
    
    if [[ "$response" != "y" ]]; then
        echo "Skipping ShellCheck installation"
        return
    fi
    
    echo -e "${YELLOW}Installing ShellCheck...${NC}"
    
    case "$OS" in
        macos)
            brew install shellcheck
            ;;
        debian)
            sudo apt-get update && sudo apt-get install -y shellcheck
            ;;
        redhat)
            sudo yum install -y ShellCheck
            ;;
        *)
            echo -e "${RED}Please install ShellCheck manually for your system${NC}"
            ;;
    esac
    
    check_command shellcheck
}

install_python_deps() {
    print_header "Installing Python Dependencies"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is required but not installed${NC}"
        
        if [ "$OS" = "macos" ]; then
            echo "Install with: brew install python3"
        else
            echo "Install with: sudo apt-get install python3 python3-pip"
        fi
        return 1
    fi
    
    echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    if [ ! -d "$SCRIPT_DIR/macos-app/venv" ]; then
        cd "$SCRIPT_DIR/macos-app" || exit
        python3 -m venv venv
        source venv/bin/activate
        pip install --quiet requests beautifulsoup4 jinja2 python-dotenv
        echo -e "${GREEN}✓ Python virtual environment created${NC}"
    else
        echo -e "${GREEN}✓ Python virtual environment already exists${NC}"
    fi
}

show_summary() {
    print_header "Installation Summary"
    
    echo -e "\n${CYAN}Required Dependencies:${NC}"
    check_command curl
    check_command jq
    check_command wp
    check_command php
    check_command python3
    
    echo -e "\n${CYAN}Optional Dependencies:${NC}"
    check_command vultr
    check_command redis-cli
    check_command composer
    check_command npm
    check_command shellcheck
    
    echo -e "\n${GREEN}Setup complete!${NC}"
    echo "You can now use the WP Bulk Manager Enhanced system."
}

main() {
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   WP Bulk Manager Enhanced - Dependency Installer     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    
    echo -e "\nDetected OS: ${CYAN}$OS${NC}"
    
    # Install required dependencies
    if [ "$OS" = "macos" ]; then
        install_homebrew
    fi
    
    install_wpcli
    install_jq
    install_python_deps
    
    # Ask about optional dependencies
    echo -e "\n${YELLOW}Would you like to install optional dependencies? (y/n)${NC}"
    read -r response
    
    if [[ "$response" == "y" ]]; then
        install_vultr_cli
        install_redis
        install_composer
        install_npm
        install_shellcheck
    fi
    
    # Show summary
    show_summary
}

# Run main function
main "$@"