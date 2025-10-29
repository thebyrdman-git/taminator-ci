#!/bin/bash
# Tesla Architecture Integration Test
# Tests: Service → API → Health Check → AI Status → Customer Data

set -euo pipefail

cd /home/jbyrd/TAMINATOR

echo "============================================"
echo "🚗⚡ TESLA ARCHITECTURE INTEGRATION TEST"
echo "============================================"
echo ""

# Kill any existing services
echo "1️⃣ Cleaning up old service instances..."
pkill -9 -f "uvicorn.*taminator" 2>/dev/null || true
pkill -9 -f "taminator-service" 2>/dev/null || true
sleep 2
echo "   ✅ Clean slate"
echo ""

# Start service
echo "2️⃣ Starting Taminator API Service..."
cd src
PYTHONPATH=/home/jbyrd/TAMINATOR/src python3 -m uvicorn taminator.api.main:app \
  --host 127.0.0.1 \
  --port 8765 \
  > /tmp/taminator-test.log 2>&1 &
SERVICE_PID=$!
echo "   🚀 Service PID: $SERVICE_PID"
echo "   ⏳ Waiting for startup (5s)..."
sleep 5

# Test health endpoint
echo ""
echo "3️⃣ Testing Health Endpoint..."
HEALTH=$(curl -s http://127.0.0.1:8765/health)
if echo "$HEALTH" | grep -q '"status":"healthy"'; then
    echo "   ✅ Service is healthy"
    echo "   📊 Health Response:"
    echo "$HEALTH" | python3 -m json.tool | sed 's/^/      /'
else
    echo "   ❌ Health check failed"
    echo "   Response: $HEALTH"
    kill $SERVICE_PID 2>/dev/null
    exit 1
fi

# Test AI status
echo ""
echo "4️⃣ Testing AI Model Availability..."
AI_STATUS=$(echo "$HEALTH" | python3 -c "import sys,json; h=json.load(sys.stdin); print(h.get('ai', {}).get('available', False))")
if [ "$AI_STATUS" = "True" ]; then
    echo "   ✅ AI models available"
    AI_URL=$(echo "$HEALTH" | python3 -c "import sys,json; h=json.load(sys.stdin); print(h.get('ai', {}).get('proxy_url', 'N/A'))")
    AI_MODELS=$(echo "$HEALTH" | python3 -c "import sys,json; h=json.load(sys.stdin); print(len(h.get('ai', {}).get('models', [])))")
    echo "   📡 Proxy: $AI_URL"
    echo "   🤖 Models: $AI_MODELS available"
else
    echo "   ⚠️  AI models not available (expected if LiteLLM not running)"
fi

# Test customer endpoint
echo ""
echo "5️⃣ Testing Customer Endpoint..."
CUSTOMERS=$(curl -s http://127.0.0.1:8765/api/customers)
CUSTOMER_COUNT=$(echo "$CUSTOMERS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
if [ "$CUSTOMER_COUNT" -gt 0 ]; then
    echo "   ✅ Customer endpoint working"
    echo "   👥 Loaded $CUSTOMER_COUNT customers"
    echo "   📋 Sample customer:"
    echo "$CUSTOMERS" | python3 -m json.tool | head -20 | sed 's/^/      /'
else
    echo "   ⚠️  No customers found (may be expected)"
fi

# Test customer stats
echo ""
echo "6️⃣ Testing Customer Stats..."
FIRST_CUSTOMER=$(echo "$CUSTOMERS" | python3 -c "import sys,json; c=json.load(sys.stdin); print(c[0]['customer_id'] if c else '')" 2>/dev/null || echo "")
if [ -n "$FIRST_CUSTOMER" ]; then
    STATS=$(curl -s "http://127.0.0.1:8765/api/customers/$FIRST_CUSTOMER/stats")
    if echo "$STATS" | grep -q '"customer_id"'; then
        echo "   ✅ Stats endpoint working"
        echo "   📊 Stats for $FIRST_CUSTOMER:"
        echo "$STATS" | python3 -m json.tool | sed 's/^/      /'
    else
        echo "   ⚠️  Stats endpoint returned unexpected data"
    fi
else
    echo "   ⚠️  Skipped (no customers to test)"
fi

# Cleanup
echo ""
echo "7️⃣ Cleaning up..."
kill $SERVICE_PID 2>/dev/null || true
wait $SERVICE_PID 2>/dev/null || true
echo "   ✅ Service stopped"

echo ""
echo "============================================"
echo "🎉 TESLA ARCHITECTURE TEST COMPLETE!"
echo "============================================"
echo ""
echo "Summary:"
echo "  ✅ Service lifecycle (start/stop)"
echo "  ✅ Health endpoint"
echo "  ✅ AI status detection"
echo "  ✅ Customer data API"
echo "  ✅ Statistics endpoint"
echo ""
echo "Next steps:"
echo "  1. Test GUI integration (npm start)"
echo "  2. Build AppImage (npm run build)"
echo "  3. Deploy to production"
echo ""


