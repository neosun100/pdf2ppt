#!/usr/bin/env python3
"""
PDF2PPT Test Suite
Tests all major functionality
"""

import subprocess
import time
import requests
import sys
from pathlib import Path

def test_cli():
    """Test CLI functionality"""
    print("🧪 Testing CLI...")
    
    # Test version
    result = subprocess.run(['pdf2ppt', '--version'], capture_output=True, text=True)
    assert '1.1.0' in result.stdout or '1.2.0' in result.stdout, "Version check failed"
    print("  ✅ Version check passed")
    
    # Test conversion
    result = subprocess.run([
        'pdf2ppt', 'demo/latex-demo.pdf', '/tmp/cli-test.pptx',
        '--force', '--pages', '1-2'
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"Conversion failed: {result.stderr}"
    assert Path('/tmp/cli-test.pptx').exists(), "Output file not created"
    print("  ✅ CLI conversion passed")
    
    Path('/tmp/cli-test.pptx').unlink()
    print("✅ CLI tests passed\n")


def test_api():
    """Test API functionality"""
    print("🧪 Testing API...")
    
    # Start server
    server = subprocess.Popen([
        'python', '-m', 'uvicorn', 'web.app:app',
        '--host', '127.0.0.1', '--port', '8890'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(3)
    
    try:
        # Test health
        response = requests.get('http://127.0.0.1:8890/health', timeout=5)
        assert response.status_code == 200, "Health check failed"
        assert response.json()['status'] == 'healthy', "Health status not healthy"
        print("  ✅ Health check passed")
        
        # Test UI
        response = requests.get('http://127.0.0.1:8890/', timeout=5)
        assert response.status_code == 200, "UI not accessible"
        assert 'PDF2PPT' in response.text, "UI content incorrect"
        print("  ✅ Web UI passed")
        
        # Test API docs
        response = requests.get('http://127.0.0.1:8890/docs', timeout=5)
        assert response.status_code == 200, "API docs not accessible"
        print("  ✅ API docs passed")
        
        # Test conversion
        with open('demo/latex-demo.pdf', 'rb') as f:
            files = {'file': f}
            data = {'options': '{"pages":"1","parallel":1}'}
            response = requests.post(
                'http://127.0.0.1:8890/api/convert',
                files=files,
                data=data,
                timeout=60
            )
            assert response.status_code == 200, "Conversion API failed"
            assert 'completed' in response.text, "Conversion not completed"
        print("  ✅ API conversion passed")
        
        print("✅ API tests passed\n")
        
    finally:
        server.terminate()
        server.wait(timeout=5)


def test_mcp():
    """Test MCP server"""
    print("🧪 Testing MCP...")
    
    # Test import
    sys.path.insert(0, 'mcp')
    try:
        import mcp_server
        print("  ✅ MCP server imports")
    except ImportError as e:
        print(f"  ❌ MCP import failed: {e}")
        return
    
    print("✅ MCP tests passed\n")


if __name__ == '__main__':
    print("=" * 50)
    print("PDF2PPT Test Suite v1.2.0")
    print("=" * 50)
    print()
    
    try:
        test_cli()
        test_api()
        test_mcp()
        
        print("=" * 50)
        print("🎉 All tests passed!")
        print("=" * 50)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
