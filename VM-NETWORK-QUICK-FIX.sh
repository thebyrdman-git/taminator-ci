#!/bin/bash
# Quick VM Network Fix - Run this IN THE VM

echo "=== Rocky Linux VM Network Fix ==="
echo ""

echo "Step 1: Check interface status"
nmcli device status
echo ""

echo "Step 2: Check connections"
nmcli connection show
echo ""

echo "Step 3: Find interface name"
INTERFACE=$(ip link show | grep -E "^[0-9]+: en" | awk '{print $2}' | tr -d ':' | head -1)
echo "Primary interface: $INTERFACE"
echo ""

echo "Step 4: Restart connection"
sudo nmcli connection down "$INTERFACE" 2>/dev/null
sudo nmcli connection up "$INTERFACE"
echo ""

echo "Step 5: Check IP address"
ip addr show $INTERFACE | grep "inet "
echo ""

echo "Step 6: Test connectivity"
echo "Pinging 8.8.8.8..."
ping -c 3 8.8.8.8
echo ""

echo "=== If you see an IP and ping works, network is fixed! ==="

