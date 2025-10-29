#!/bin/bash
# Taminator Intelligence - Quick Install Script
#
# Usage: ./deployment/install.sh

set -e

echo "🚀 Taminator Intelligence - Quick Install"
echo "=========================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v podman &> /dev/null; then
    echo "❌ Error: Podman not found. Please install podman first."
    echo "   RHEL/Fedora: sudo dnf install podman"
    exit 1
fi

if ! command -v systemctl &> /dev/null; then
    echo "❌ Error: systemctl not found. This script requires systemd."
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Build container image
echo "🔨 Building container image..."
podman build -t taminator-intelligence:2.1.0 -f Containerfile .
echo "✅ Image built"
echo ""

# Create data directory
echo "📁 Creating data directory..."
mkdir -p ~/.local/share/taminator
echo "✅ Data directory created: ~/.local/share/taminator"
echo ""

# Install systemd service
echo "⚙️  Installing systemd user service..."
mkdir -p ~/.config/systemd/user/
cp deployment/taminator-intelligence.service ~/.config/systemd/user/
systemctl --user daemon-reload
echo "✅ Service installed"
echo ""

# Enable and start service
echo "🎬 Starting service..."
systemctl --user enable --now taminator-intelligence
echo "✅ Service started"
echo ""

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 5

# Check status
echo "📊 Service status:"
systemctl --user status taminator-intelligence --no-pager || true
echo ""

# Verify database
if [ -f ~/.local/share/taminator/intelligence.db ]; then
    DB_SIZE=$(ls -lh ~/.local/share/taminator/intelligence.db | awk '{print $5}')
    echo "✅ Database created: $DB_SIZE"
else
    echo "⚠️  Database not yet created (will be created on first use)"
fi
echo ""

# Success message
echo "✅ Installation complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Access web interface: http://localhost:8080"
echo "   2. View logs: journalctl --user -u taminator-intelligence -f"
echo "   3. Check status: systemctl --user status taminator-intelligence"
echo ""
echo "📚 Documentation: docs/DEPLOYMENT-STRATEGY.md"
echo "💬 Support: #taminator-intelligence on Slack"
echo ""
echo "Happy analyzing! 🧠"

