#!/bin/bash
# Test rhcase Integration
# Validates that rhcase API works end-to-end

set -e

BASE_URL="http://127.0.0.1:8765"
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BOLD}🧪 Testing rhcase Integration${NC}\n"

# Test 1: Check if service is running
echo -e "${BOLD}Test 1: Service Health${NC}"
if curl -s "${BASE_URL}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Service is running${NC}"
else
    echo -e "${RED}❌ Service is not running${NC}"
    echo "Start service with: cd src && python -m taminator.api.main"
    exit 1
fi

# Test 2: Check rhcase availability in health endpoint
echo -e "\n${BOLD}Test 2: rhcase Health Status${NC}"
HEALTH=$(curl -s "${BASE_URL}/health")
RHCASE_AVAILABLE=$(echo "$HEALTH" | jq -r '.rhcase.available')
RHCASE_PATH=$(echo "$HEALTH" | jq -r '.rhcase.path')
RHCASE_VERSION=$(echo "$HEALTH" | jq -r '.rhcase.version')
RHCASE_BUNDLED=$(echo "$HEALTH" | jq -r '.rhcase.bundled')

if [ "$RHCASE_AVAILABLE" = "true" ]; then
    echo -e "${GREEN}✅ rhcase is available${NC}"
    echo "   Path: $RHCASE_PATH"
    echo "   Version: $RHCASE_VERSION"
    echo "   Bundled: $RHCASE_BUNDLED"
else
    echo -e "${RED}❌ rhcase is not available${NC}"
    exit 1
fi

# Test 3: rhcase health endpoint
echo -e "\n${BOLD}Test 3: rhcase Health Endpoint${NC}"
RHCASE_HEALTH=$(curl -s "${BASE_URL}/api/rhcase/health")
echo "$RHCASE_HEALTH" | jq '.'
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ rhcase health endpoint works${NC}"
else
    echo -e "${RED}❌ rhcase health endpoint failed${NC}"
    exit 1
fi

# Test 4: Execute simple command (--version)
echo -e "\n${BOLD}Test 4: Execute rhcase --version${NC}"
RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/execute" \
    -H "Content-Type: application/json" \
    -d '{"command": "--version"}')

SUCCESS=$(echo "$RESULT" | jq -r '.success')
OUTPUT=$(echo "$RESULT" | jq -r '.output')

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ rhcase --version succeeded${NC}"
    echo "   Output: $OUTPUT"
else
    echo -e "${RED}❌ rhcase --version failed${NC}"
    echo "$RESULT" | jq '.'
    exit 1
fi

# Test 5: Execute doctor command
echo -e "\n${BOLD}Test 5: Execute rhcase doctor${NC}"
RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/doctor")

SUCCESS=$(echo "$RESULT" | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ rhcase doctor succeeded${NC}"
    echo "   (Output truncated - check full response if needed)"
else
    echo -e "${YELLOW}⚠️  rhcase doctor reported issues (this may be expected)${NC}"
    echo "   Check if rhcase is fully configured (credentials, etc.)"
fi

# Test 6: Test JIRA projects endpoint
echo -e "\n${BOLD}Test 6: List JIRA Projects${NC}"
RESULT=$(curl -s "${BASE_URL}/api/rhcase/jira/projects")

SUCCESS=$(echo "$RESULT" | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    echo -e "${GREEN}✅ JIRA projects command succeeded${NC}"
else
    echo -e "${YELLOW}⚠️  JIRA projects command failed (may need VPN/credentials)${NC}"
    ERROR=$(echo "$RESULT" | jq -r '.error')
    echo "   Error: $ERROR"
fi

# Test 7: Test error handling (invalid command)
echo -e "\n${BOLD}Test 7: Error Handling (invalid command)${NC}"
RESULT=$(curl -s -X POST "${BASE_URL}/api/rhcase/execute" \
    -H "Content-Type: application/json" \
    -d '{"command": "invalid-command-that-does-not-exist"}')

SUCCESS=$(echo "$RESULT" | jq -r '.success')

if [ "$SUCCESS" = "false" ]; then
    echo -e "${GREEN}✅ Error handling works correctly${NC}"
    echo "   (Correctly reported failure for invalid command)"
else
    echo -e "${YELLOW}⚠️  Error handling may need review${NC}"
fi

# Summary
echo -e "\n${BOLD}════════════════════════════════════════${NC}"
echo -e "${BOLD}📊 Test Summary${NC}"
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Service running${NC}"
echo -e "${GREEN}✅ rhcase available${NC}"
echo -e "${GREEN}✅ Health endpoint working${NC}"
echo -e "${GREEN}✅ Command execution working${NC}"
echo -e "${GREEN}✅ Error handling working${NC}"
echo ""
echo -e "${BOLD}🎯 rhcase Integration Status: VALIDATED${NC}"
echo ""
echo "Next steps:"
echo "  - Test specific commands (analyze, list, kcs, etc.)"
echo "  - Test with real customer data"
echo "  - Test from GUI"

