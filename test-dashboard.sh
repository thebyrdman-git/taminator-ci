#!/bin/bash
# Test Dashboard CLI Command

echo "=================================="
echo "🧪 TESTING DASHBOARD COMMAND"
echo "=================================="
echo ""

echo "📋 Test 1: Dashboard Help"
echo "-----------------------------------"
tam-rfe dashboard --help
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📋 Test 2: Dashboard (Pretty Table)"
echo "-----------------------------------"
tam-rfe dashboard
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📋 Test 3: Dashboard (JSON Output)"
echo "-----------------------------------"
tam-rfe dashboard --json | jq '.' 2>/dev/null || tam-rfe dashboard --json
echo ""
read -p "Press Enter to continue..."
echo ""

echo "=================================="
echo "✅ DASHBOARD TEST COMPLETE"
echo "=================================="
echo ""
echo "Verify:"
echo "  1. ✅ Shows all customers (jpmc, test-oobe-customer)"
echo "  2. ✅ Shows account numbers"
echo "  3. ✅ Shows products"
echo "  4. ✅ Counts RFEs/Bugs from reports"
echo "  5. ✅ JSON output works"
echo ""
read -p "Press Enter to exit..."

