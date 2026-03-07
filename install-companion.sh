#!/bin/bash
#
# Companion Server Installer
# Downloads and sets up the companion server from the MCP server
#

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
MCP_SERVER_URL="${MCP_SERVER_URL:-http://localhost:8080}"
INSTALL_DIR="${COMPANION_INSTALL_DIR:-$HOME/.companion}"
DOWNLOAD_URL="$MCP_SERVER_URL/companion/download"

echo -e "${BLUE}[INFO]${NC} Companion Server Installer"
echo ""

# Check Node.js
echo -e "${BLUE}[INFO]${NC} Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Node.js not found"
    echo ""
    echo "Please install Node.js v16+ first:"
    echo "  Ubuntu/Debian: sudo apt install nodejs npm"
    echo "  macOS: brew install node"
    echo "  Windows: Download from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}[OK]${NC} Node.js $NODE_VERSION installed"

# Create install directory
echo -e "${BLUE}[INFO]${NC} Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Download companion server
echo -e "${BLUE}[INFO]${NC} Downloading companion server from $DOWNLOAD_URL..."
if command -v curl &> /dev/null; then
    curl -fSL "$DOWNLOAD_URL" -o "$INSTALL_DIR/companion-server.tar.gz"
elif command -v wget &> /dev/null; then
    wget -q "$DOWNLOAD_URL" -O "$INSTALL_DIR/companion-server.tar.gz"
else
    echo -e "${RED}[ERROR]${NC} Neither curl nor wget found"
    exit 1
fi

# Extract
echo -e "${BLUE}[INFO]${NC} Extracting files..."
cd "$INSTALL_DIR"
tar -xzf companion-server.tar.gz
rm companion-server.tar.gz

# Make CLI executable
if [ -f "$INSTALL_DIR/companion-cli.sh" ]; then
    chmod +x "$INSTALL_DIR/companion-cli.sh"
fi

# Success
echo ""
echo -e "${GREEN}[OK]${NC} Companion server installed to $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "  1. Start companion: $INSTALL_DIR/companion-cli.sh start"
echo "  2. Verify: $INSTALL_DIR/companion-cli.sh test"
echo ""
echo "Or run directly:"
echo "  node $INSTALL_DIR/companion/server.js"
echo ""
