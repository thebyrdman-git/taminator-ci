#!/bin/bash
# Create GitLab Release v2.1.2
# Requires: GITLAB_TOKEN environment variable

set -e

PROJECT_ID="jbyrd%2Ftaminator"
TAG="v2.1.2"
RELEASE_NAME="TAMINATOR v2.1.2 - CI/CD & Automation Preview"
GITLAB_API="https://gitlab.cee.redhat.com/api/v4"

# Check for token
if [ -z "$GITLAB_TOKEN" ]; then
    echo "❌ Error: GITLAB_TOKEN environment variable not set"
    echo ""
    echo "To set your GitLab token:"
    echo "  export GITLAB_TOKEN='your-gitlab-token'"
    echo ""
    echo "Get your token from:"
    echo "  https://gitlab.cee.redhat.com/-/profile/personal_access_tokens"
    exit 1
fi

# Read release notes
if [ ! -f "GITLAB-RELEASE-v2.1.2.md" ]; then
    echo "❌ Error: GITLAB-RELEASE-v2.1.2.md not found"
    exit 1
fi

DESCRIPTION=$(cat GITLAB-RELEASE-v2.1.2.md | tail -n +3)  # Skip title

echo "🚀 Creating GitLab Release v2.1.2..."
echo ""

# Create release
RESPONSE=$(curl -s -w "\n%{http_code}" \
    --request POST \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    --header "Content-Type: application/json" \
    --data "{
        \"name\": \"$RELEASE_NAME\",
        \"tag_name\": \"$TAG\",
        \"description\": $(echo "$DESCRIPTION" | jq -Rs .)
    }" \
    "$GITLAB_API/projects/$PROJECT_ID/releases")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 201 ]; then
    echo "✅ Release created successfully!"
    echo ""
    echo "Release URL:"
    echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/$TAG"
    echo ""
    echo "📦 Now upload release assets:"
    echo "  1. Go to the release URL above"
    echo "  2. Click 'Edit'"
    echo "  3. Upload:"
    echo "     - release/v2.1.2/Taminator-2.1.2.AppImage"
    echo "     - release/v2.1.2/Taminator-2.1.2.dmg"
    echo "     - release/v2.1.2/SHA256SUMS"
else
    echo "❌ Failed to create release (HTTP $HTTP_CODE)"
    echo ""
    echo "Response:"
    echo "$BODY" | jq .
    exit 1
fi

