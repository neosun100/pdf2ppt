#!/bin/bash

# PDF2PPT Test Suite
# Tests CLI, API, and Docker functionality

set -e

echo "🧪 PDF2PPT Test Suite"
echo "===================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((FAILED++))
    fi
}

# Test 1: CLI Installation
echo "Test 1: CLI Installation"
pdf2ppt --version > /dev/null 2>&1
test_result $? "CLI tool is installed"
echo ""

# Test 2: CLI Conversion
echo "Test 2: CLI Conversion"
cd demo
pdf2ppt latex-demo.pdf /tmp/cli-test.pptx --force --pages 1-2 > /dev/null 2>&1
test_result $? "CLI conversion works"
[ -f /tmp/cli-test.pptx ]
test_result $? "Output file created"
echo ""

# Test 3: Start API Server
echo "Test 3: API Server"
cd ..
python -m uvicorn web.app:app --host 127.0.0.1 --port 8889 > /tmp/api-server.log 2>&1 &
SERVER_PID=$!
sleep 3

# Test 4: Health Check
echo "Test 4: Health Check"
curl -s http://127.0.0.1:8889/health | grep -q "healthy"
test_result $? "Health check endpoint"
echo ""

# Test 5: Web UI
echo "Test 5: Web UI"
curl -s http://127.0.0.1:8889/ | grep -q "PDF2PPT"
test_result $? "Web UI loads"
echo ""

# Test 6: API Documentation
echo "Test 6: API Documentation"
curl -s http://127.0.0.1:8889/docs | grep -q "Swagger"
test_result $? "Swagger docs available"
echo ""

# Test 7: API Conversion
echo "Test 7: API Conversion"
curl -X POST http://127.0.0.1:8889/api/convert \
  -F "file=@demo/latex-demo.pdf" \
  -F 'options={"pages":"1","parallel":1}' \
  2>/dev/null | grep -q "completed"
test_result $? "API conversion works"
echo ""

# Test 8: Download Endpoint
echo "Test 8: Download Endpoint"
sleep 2
curl -s http://127.0.0.1:8889/api/download/latex-demo.pptx -o /tmp/api-download.pptx
[ -f /tmp/api-download.pptx ] && [ -s /tmp/api-download.pptx ]
test_result $? "File download works"
echo ""

# Test 9: MCP Server
echo "Test 9: MCP Server"
python -c "from mcp import mcp_server" > /dev/null 2>&1
test_result $? "MCP server imports"
echo ""

# Cleanup
kill $SERVER_PID 2>/dev/null || true
rm -f /tmp/cli-test.pptx /tmp/api-download.pptx

# Summary
echo ""
echo "===================="
echo "Test Summary"
echo "===================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
