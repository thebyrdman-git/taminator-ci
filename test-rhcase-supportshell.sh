#!/bin/bash
# Test rhcase SupportShell Integration
# Validates that rhcase can connect to Red Hat SupportShell and pull case data

set -e

BASE_URL="http://127.0.0.1:8765"
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BOLD}🔗 Testing rhcase → SupportShell Integration${NC}\n"

# Check if case ID provided
CASE_ID="$1"

# Test 1: Check rhcase configuration
echo -e "${BOLD}Test 1: rhcase Configuration Check${NC}"
echo "Running: rhcase doctor"
RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/doctor")

SUCCESS=$(echo "$RESULT" | jq -r '.success')
OUTPUT=$(echo "$RESULT" | jq -r '.output')

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ rhcase doctor succeeded${NC}"
    echo "$OUTPUT" | grep -i "credential\|config\|token" || true
else
    echo -e "${YELLOW}⚠️  rhcase doctor reported issues:${NC}"
    echo "$OUTPUT"
    echo ""
    echo -e "${BLUE}💡 Tip: Run 'rhcase config setup' to configure credentials${NC}"
fi

# Test 2: Check if rhcase can access SupportShell
echo -e "\n${BOLD}Test 2: SupportShell Connectivity${NC}"

if [ -z "$CASE_ID" ]; then
    echo -e "${YELLOW}⚠️  No case ID provided - skipping live case test${NC}"
    echo ""
    echo "Usage: $0 <case_id>"
    echo "Example: $0 04056105"
    echo ""
    echo -e "${BLUE}💡 Testing with 'rhcase list' instead...${NC}"
    
    # Try to list cases (this will test SupportShell auth)
    RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/list" \
        -H "Content-Type: application/json" \
        -d '{}')
    
    SUCCESS=$(echo "$RESULT" | jq -r '.success')
    
    if [ "$SUCCESS" = "true" ]; then
        echo -e "${GREEN}✅ SupportShell connection works${NC}"
        echo "   (rhcase list command succeeded)"
    else
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo -e "${RED}❌ SupportShell connection failed${NC}"
        echo "   Error: $ERROR"
        echo ""
        echo -e "${BLUE}Possible causes:${NC}"
        echo "   - rhcase not configured (run: rhcase config setup)"
        echo "   - Not connected to Red Hat VPN"
        echo "   - Invalid/expired credentials"
    fi
else
    # Test with specific case
    echo "Testing case analysis: $CASE_ID"
    
    RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/analyze" \
        -H "Content-Type: application/json" \
        -d "{\"case_id\": \"$CASE_ID\"}")
    
    SUCCESS=$(echo "$RESULT" | jq -r '.success')
    OUTPUT=$(echo "$RESULT" | jq -r '.output')
    
    if [ "$SUCCESS" = "true" ]; then
        echo -e "${GREEN}✅ Case analysis succeeded${NC}"
        echo ""
        echo -e "${BOLD}Case Data Retrieved:${NC}"
        echo "$OUTPUT" | head -20
        echo ""
        echo -e "${GREEN}✅ rhcase successfully pulled case data from SupportShell${NC}"
    else
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo -e "${RED}❌ Case analysis failed${NC}"
        echo "   Error: $ERROR"
        echo ""
        echo -e "${BLUE}Possible causes:${NC}"
        echo "   - Case ID doesn't exist: $CASE_ID"
        echo "   - Not connected to Red Hat VPN"
        echo "   - rhcase not configured"
        echo "   - No access to this case"
    fi
fi

# Test 3: Test KCS search (another SupportShell integration point)
echo -e "\n${BOLD}Test 3: KCS Article Search (SupportShell Integration)${NC}"
echo "Searching KCS for: OpenShift"

RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/kcs/search" \
    -H "Content-Type: application/json" \
    -d '{"query": "OpenShift", "limit": 3}')

SUCCESS=$(echo "$RESULT" | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ KCS search succeeded${NC}"
    echo "   (rhcase can query Red Hat knowledge base)"
else
    ERROR=$(echo "$RESULT" | jq -r '.error')
    echo -e "${YELLOW}⚠️  KCS search failed${NC}"
    echo "   Error: $ERROR"
fi

# Summary
echo -e "\n${BOLD}════════════════════════════════════════${NC}"
echo -e "${BOLD}📊 SupportShell Integration Summary${NC}"
echo -e "${BOLD}════════════════════════════════════════${NC}"

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ rhcase is properly integrated with SupportShell${NC}"
    echo -e "${GREEN}✅ Can pull case data from Red Hat infrastructure${NC}"
    echo ""
    echo "Next steps:"
    echo "  - Test with more cases"
    echo "  - Test JIRA integration"
    echo "  - Test from GUI"
else
    echo -e "${YELLOW}⚠️  rhcase integration needs configuration${NC}"
    echo ""
    echo "Setup steps:"
    echo "  1. Connect to Red Hat VPN"
    echo "  2. Run: rhcase config setup"
    echo "  3. Enter your Red Hat credentials"
    echo "  4. Re-run this test"
fi

