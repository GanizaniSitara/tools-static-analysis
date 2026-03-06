#!/bin/bash
# companion-cli.sh - Install, manage, and control the companion server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPANION_DIR="$SCRIPT_DIR/companion"
PID_FILE="$SCRIPT_DIR/.companion.pid"
LOG_FILE="$SCRIPT_DIR/companion.log"
DEFAULT_PORT=3000

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        return 1
    fi
    return 0
}

# Get Node.js version
get_node_version() {
    node --version 2>/dev/null || echo "not installed"
}

# Check if companion is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

# Get companion PID
get_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    fi
}

# Check companion health
check_health() {
    local port=${1:-$DEFAULT_PORT}
    curl -s "http://localhost:$port/_ping" > /dev/null 2>&1
    return $?
}

# Install dependencies (Node.js check)
cmd_install() {
    print_header "Installing Companion Server"

    # Check Node.js
    print_info "Checking Node.js installation..."
    if check_node; then
        local version=$(get_node_version)
        print_success "Node.js $version installed"
    else
        print_error "Node.js not found"
        echo ""
        echo "Please install Node.js v16+ from:"
        echo "  • Ubuntu/Debian: sudo apt install nodejs npm"
        echo "  • macOS: brew install node"
        echo "  • Or download: https://nodejs.org"
        exit 1
    fi

    # Check companion files
    print_info "Checking companion files..."
    if [ ! -f "$COMPANION_DIR/server.js" ]; then
        print_error "companion/server.js not found"
        exit 1
    fi
    print_success "Companion files found"

    # Check config (optional)
    if [ -f "$SCRIPT_DIR/config.yaml" ]; then
        print_success "config.yaml found"
    else
        print_info "No config.yaml (will use defaults)"
    fi

    print_success "Installation check complete!"
    echo ""
    print_info "Start with: $0 start"
}

# Start companion server
cmd_start() {
    local port=${1:-$DEFAULT_PORT}
    local background=${2:-true}

    print_header "Starting Companion Server"

    # Check if already running
    if is_running; then
        print_warning "Companion already running (PID: $(get_pid))"
        cmd_status
        return 0
    fi

    # Check Node.js
    if ! check_node; then
        print_error "Node.js not installed"
        print_info "Run: $0 install"
        exit 1
    fi

    # Start server
    print_info "Starting on port $port..."

    if [ "$background" = "true" ]; then
        nohup node "$COMPANION_DIR/server.js" --port "$port" > "$LOG_FILE" 2>&1 &
        local pid=$!
        echo "$pid" > "$PID_FILE"
        sleep 2

        # Verify started
        if check_health "$port"; then
            print_success "Companion started (PID: $pid)"
            print_info "Logs: $LOG_FILE"
            print_info "Check health: curl http://localhost:$port/_ping"
        else
            print_error "Failed to start companion"
            print_info "Check logs: tail -f $LOG_FILE"
            exit 1
        fi
    else
        print_info "Running in foreground (Ctrl+C to stop)..."
        node "$COMPANION_DIR/server.js" --port "$port"
    fi
}

# Stop companion server
cmd_stop() {
    print_header "Stopping Companion Server"

    if ! is_running; then
        print_warning "Companion not running"
        return 0
    fi

    local pid=$(get_pid)
    print_info "Stopping companion (PID: $pid)..."

    kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"

    sleep 1

    if is_running; then
        print_warning "Process still running, force killing..."
        kill -9 "$pid" 2>/dev/null || true
        rm -f "$PID_FILE"
    fi

    print_success "Companion stopped"
}

# Restart companion server
cmd_restart() {
    print_header "Restarting Companion Server"
    cmd_stop
    sleep 1
    cmd_start "$@"
}

# Show companion status
cmd_status() {
    print_header "Companion Server Status"

    if is_running; then
        local pid=$(get_pid)
        print_success "Running (PID: $pid)"

        # Try to get health
        if check_health; then
            local response=$(curl -s "http://localhost:$DEFAULT_PORT/_ping" 2>/dev/null)
            echo "  Health: OK"
            echo "  Endpoint: http://localhost:$DEFAULT_PORT"
            echo "  Response: $response"
        else
            print_warning "Running but not responding to health checks"
        fi
    else
        print_error "Not running"
    fi

    # Show logs if available
    if [ -f "$LOG_FILE" ]; then
        echo ""
        print_info "Recent logs (last 5 lines):"
        tail -5 "$LOG_FILE"
    fi
}

# Show logs
cmd_logs() {
    local lines=${1:-50}

    if [ ! -f "$LOG_FILE" ]; then
        print_warning "No log file found"
        return 0
    fi

    print_header "Companion Logs (last $lines lines)"
    tail -n "$lines" "$LOG_FILE"
}

# Follow logs
cmd_follow() {
    if [ ! -f "$LOG_FILE" ]; then
        print_warning "No log file found. Start companion first."
        return 0
    fi

    print_info "Following logs (Ctrl+C to stop)..."
    tail -f "$LOG_FILE"
}

# Test companion connection
cmd_test() {
    local port=${1:-$DEFAULT_PORT}

    print_header "Testing Companion Connection"

    print_info "Checking if companion is running..."
    if ! is_running; then
        print_error "Companion not running"
        print_info "Start with: $0 start"
        exit 1
    fi

    print_success "Companion is running"

    print_info "Testing health endpoint..."
    if curl -s "http://localhost:$port/_ping" > /dev/null 2>&1; then
        print_success "Health check passed"
        echo ""
        echo "Response:"
        curl -s "http://localhost:$port/_ping" | python3 -m json.tool 2>/dev/null || \
        curl -s "http://localhost:$port/_ping"
    else
        print_error "Health check failed"
        print_info "Check logs: $0 logs"
        exit 1
    fi
}

# Uninstall/clean up
cmd_uninstall() {
    print_header "Uninstalling Companion Server"

    print_warning "This will:"
    echo "  • Stop the companion server"
    echo "  • Remove PID and log files"
    echo "  • Keep companion code (in case you need it later)"
    echo ""
    read -p "Continue? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cancelled"
        return 0
    fi

    # Stop if running
    if is_running; then
        cmd_stop
    fi

    # Remove files
    rm -f "$PID_FILE"
    rm -f "$LOG_FILE"

    print_success "Companion uninstalled (code preserved)"
    print_info "To reinstall: $0 install"
}

# Show help
cmd_help() {
    cat << EOF
Companion Server CLI - Manage the static analysis companion agent

USAGE:
    $0 <command> [options]

COMMANDS:
    install             Check dependencies and setup
    start [port]        Start companion server (default port: 3000)
    stop                Stop companion server
    restart [port]      Restart companion server
    status              Show companion status
    logs [lines]        Show recent logs (default: 50 lines)
    follow              Follow logs in real-time
    test [port]         Test companion connection
    uninstall           Stop and clean up companion
    help                Show this help message

EXAMPLES:
    # Install and setup
    $0 install

    # Start on default port (3000)
    $0 start

    # Start on custom port
    $0 start 19280

    # Check status
    $0 status

    # View logs
    $0 logs 100

    # Test connection
    $0 test

    # Stop
    $0 stop

FILES:
    Companion:  $COMPANION_DIR/server.js
    PID file:   $PID_FILE
    Logs:       $LOG_FILE
    Config:     $SCRIPT_DIR/config.yaml (optional)

ENDPOINTS (when running):
    Health:     http://localhost:3000/_ping
    Open file:  http://localhost:3000/_open?editor=claude&path=...
    Start fix:  http://localhost:3000/_fix/start?smell_type=...

DOCUMENTATION:
    Full setup guide: $SCRIPT_DIR/COMPANION_SETUP.md

For more help, see: https://github.com/GanizaniSitara/tools-static-analysis
EOF
}

# Main command dispatcher
main() {
    local command=${1:-help}
    shift || true

    case "$command" in
        install)
            cmd_install "$@"
            ;;
        start)
            cmd_start "$@"
            ;;
        stop)
            cmd_stop "$@"
            ;;
        restart)
            cmd_restart "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        logs)
            cmd_logs "$@"
            ;;
        follow)
            cmd_follow "$@"
            ;;
        test)
            cmd_test "$@"
            ;;
        uninstall)
            cmd_uninstall "$@"
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
}

# Run main
main "$@"
