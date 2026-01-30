#!/bin/bash

# 🐵 DONNIE$ Installer - Easy Setup Script
# Installs DONNIE$ AI Terminal Agent on your system

set -e

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🐵 DONNIE$ Installer - Monkey Power Setup! 🍌          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Choose version
echo -e "${CYAN}Which version do you want to install?${NC}\n"
echo "1) Standard Edition - Classic AI terminal agent"
echo "2) Crypto Edition - With \$DONNIE token integration 💰"
echo ""
read -p "Enter your choice (1 or 2): " VERSION_CHOICE

if [ "$VERSION_CHOICE" = "2" ]; then
    EDITION="crypto"
    SCRIPT_NAME="donnie_crypto_agent.py"
    echo -e "\n${GREEN}Installing Crypto Edition! 🚀💰${NC}"
else
    EDITION="standard"
    SCRIPT_NAME="donnie_agent_en.py"
    echo -e "\n${GREEN}Installing Standard Edition! 🐵${NC}"
fi

echo -e "\n${YELLOW}Step 1/5: Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

echo -e "\n${YELLOW}Step 2/5: Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found!${NC}"
    echo "Please install pip3 first"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"

echo -e "\n${YELLOW}Step 3/5: Installing dependencies...${NC}"
echo "This may take a moment..."

# Install anthropic
if pip3 install anthropic --break-system-packages &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ anthropic installed with --break-system-packages${NC}"
elif pip3 install anthropic &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ anthropic installed${NC}"
else
    echo -e "${RED}❌ Could not install anthropic${NC}"
    echo "Try manually: pip3 install anthropic"
    exit 1
fi

# Install requests if crypto edition
if [ "$EDITION" = "crypto" ]; then
    if pip3 install requests --break-system-packages &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ requests installed with --break-system-packages${NC}"
    elif pip3 install requests &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ requests installed${NC}"
    else
        echo -e "${RED}❌ Could not install requests${NC}"
        echo "Try manually: pip3 install requests"
        exit 1
    fi
fi

echo -e "\n${YELLOW}Step 4/5: Installing DONNIE\$...${NC}"

# Create installation directory
INSTALL_DIR="$HOME/.donnie"
mkdir -p "$INSTALL_DIR"

# Download or copy the script
if [ -f "$SCRIPT_NAME" ]; then
    echo "Local file found, copying..."
    cp "$SCRIPT_NAME" "$INSTALL_DIR/donnie.py"
else
    echo "Downloading DONNIE\$..."
    # If you put this on GitHub, use this URL:
    # curl -sL https://raw.githubusercontent.com/your-username/donnie/main/$SCRIPT_NAME -o "$INSTALL_DIR/donnie.py"
    echo -e "${RED}❌ $SCRIPT_NAME not found in current directory${NC}"
    echo "Make sure you have this script in the same folder as $SCRIPT_NAME"
    exit 1
fi

chmod +x "$INSTALL_DIR/donnie.py"
echo -e "${GREEN}✅ DONNIE\$ installed in $INSTALL_DIR${NC}"

echo -e "\n${YELLOW}Step 5/5: Setting up alias...${NC}"

# Detect shell
SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "Could not detect shell type, try manual setup"
fi

if [ -n "$SHELL_RC" ]; then
    # Check if alias already exists
    if grep -q "alias donnie=" "$SHELL_RC" 2>/dev/null; then
        echo "Alias already exists in $SHELL_RC"
    else
        echo "" >> "$SHELL_RC"
        echo "# DONNIE\$ AI Terminal Agent 🐵" >> "$SHELL_RC"
        echo "alias donnie='python3 $INSTALL_DIR/donnie.py'" >> "$SHELL_RC"
        echo -e "${GREEN}✅ Alias added to $SHELL_RC${NC}"
    fi
fi

echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║   🎉 DONNIE\$ successfully installed! 🍌                   ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"

if [ "$EDITION" = "crypto" ]; then
    echo -e "\n${CYAN}💰 Crypto Edition Features:${NC}"
    echo "   - Live \$DONNIE token price tracking"
    echo "   - Earn \$DONNIE tokens for tasks!"
    echo "   - Web3 development support"
    echo "   - Base Network integration"
    echo ""
    echo -e "${BLUE}\$DONNIE Token: 0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07${NC}"
    echo -e "${BLUE}Network: Base (Chain ID: 8453)${NC}"
fi

echo -e "\n${BLUE}📋 Next Steps:${NC}\n"
echo "1. Restart your terminal or run:"
if [ -n "$SHELL_RC" ]; then
    echo -e "   ${YELLOW}source $SHELL_RC${NC}"
fi
echo ""
echo "2. Get your Anthropic API key:"
echo -e "   ${YELLOW}https://console.anthropic.com/${NC}"
echo ""
echo "3. Start DONNIE\$:"
echo -e "   ${YELLOW}donnie${NC}"
echo ""
echo "4. On first start, enter your API key"
echo "   (it will be securely saved in ~/.donnie/.env)"
echo ""

if [ "$EDITION" = "crypto" ]; then
    echo -e "${GREEN}🚀 LFG! WAGMI! To the moon! 🌙${NC}\n"
else
    echo -e "${GREEN}🐵 Happy coding with DONNIE\$! 🍌${NC}\n"
fi
