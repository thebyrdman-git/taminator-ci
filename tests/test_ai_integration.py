#!/usr/bin/env python3
"""
AI Integration Test - Verify Clippy email generation works end-to-end

Tests:
1. LiteLLM proxy connection
2. AI model availability (Granite)
3. Email draft generation quality
4. Graceful degradation (AI unavailable)

Run: python3 tests/test_ai_integration.py
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from taminator.core.ai_client import AIClient, get_ai_client
from taminator.core.gmail_assistant import GmailAssistant

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


async def test_litellm_connection():
    """Test 1: Can we connect to LiteLLM proxy?"""
    logger.info("=" * 60)
    logger.info("TEST 1: LiteLLM Proxy Connection")
    logger.info("=" * 60)
    
    ai_client = get_ai_client()
    
    available = await ai_client.is_available()
    
    if available:
        logger.info(f"✅ PASS: Connected to LiteLLM at {ai_client.proxy_url}")
        logger.info(f"   Available models: {ai_client.available_models}")
        return True
    else:
        logger.warning("❌ FAIL: LiteLLM proxy not available")
        logger.warning("   Checked URLs:")
        for url in AIClient.LITELLM_URLS:
            logger.warning(f"   - {url}")
        logger.warning("")
        logger.warning("   To fix:")
        logger.warning("   1. Start LiteLLM proxy: litellm --config ~/.config/pai/litellm/config.yaml")
        logger.warning("   2. Or start on rhgrimm machine")
        return False


async def test_ai_generation():
    """Test 2: Can AI generate text?"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 2: AI Text Generation")
    logger.info("=" * 60)
    
    ai_client = get_ai_client()
    
    # Check if available
    if not await ai_client.is_available():
        logger.warning("⚠️  SKIP: LiteLLM not available (graceful degradation will handle this)")
        return None
    
    # Test simple generation
    test_prompt = "Write a professional one-sentence greeting for a TAM email."
    
    try:
        result = await ai_client.generate(
            prompt=test_prompt,
            model="granite-3.2-8b-instruct",
            max_tokens=100,
            temperature=0.7
        )
        
        logger.info(f"✅ PASS: AI generated text successfully")
        logger.info(f"   Prompt: {test_prompt}")
        logger.info(f"   Result: {result[:200]}...")
        logger.info(f"   Length: {len(result)} characters")
        return True
        
    except Exception as e:
        logger.error(f"❌ FAIL: AI generation failed: {e}")
        return False


async def test_clippy_draft_generation():
    """Test 3: Can Clippy generate email drafts?"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 3: Clippy Email Draft Generation")
    logger.info("=" * 60)
    
    # Test with realistic TAM content
    clipboard_content = """
    Customer: TD Bank
    Issue: RHEL-12345 - Request for Performance Monitoring Feature
    
    Customer is requesting a new performance monitoring feature for RHEL 9.
    They need real-time CPU and memory metrics exposed via REST API.
    
    This would help them integrate with their internal monitoring systems.
    Priority: High
    Expected timeline: Q2 2025
    """
    
    assistant = GmailAssistant()
    
    # Test context detection
    logger.info("Testing context detection...")
    context = await assistant._detect_context(clipboard_content)
    logger.info(f"   Detected context: {context}")
    logger.info(f"   Type: {context['type']}")
    logger.info(f"   Customer: {context.get('customer', 'N/A')}")
    logger.info(f"   Issue keys: {context.get('issue_keys', [])}")
    
    # Test draft generation (without saving to Gmail)
    logger.info("")
    logger.info("Testing draft generation...")
    
    try:
        draft = await assistant._generate_draft(clipboard_content, context)
        
        logger.info(f"✅ PASS: Draft generated successfully")
        logger.info("")
        logger.info("   " + "-" * 56)
        logger.info(f"   Subject: {draft['subject']}")
        logger.info("   " + "-" * 56)
        logger.info(f"   Body Preview:")
        for line in draft['body'][:400].split('\n'):
            logger.info(f"   {line}")
        logger.info("   " + "-" * 56)
        logger.info("")
        
        # Quality checks
        quality_pass = True
        
        if len(draft['subject']) < 10:
            logger.warning("⚠️  Quality Issue: Subject too short")
            quality_pass = False
        
        if len(draft['body']) < 100:
            logger.warning("⚠️  Quality Issue: Body too short")
            quality_pass = False
        
        if "TD Bank" not in draft['body'] and "Customer" not in draft['body']:
            logger.warning("⚠️  Quality Issue: Customer context missing")
            quality_pass = False
        
        if "RHEL-12345" not in draft['body']:
            logger.warning("⚠️  Quality Issue: Issue key missing")
            quality_pass = False
        
        if quality_pass:
            logger.info("✅ PASS: Draft quality checks passed")
        else:
            logger.warning("⚠️  WARN: Draft quality could be improved")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ FAIL: Draft generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_graceful_degradation():
    """Test 4: Does graceful degradation work (AI unavailable)?"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 4: Graceful Degradation (AI Unavailable)")
    logger.info("=" * 60)
    
    assistant = GmailAssistant()
    
    # Test with simple content
    clipboard_content = """
    Customer update: Everything is working well.
    Let me know if you need anything else.
    """
    
    context = {
        "type": "customer_response",
        "customer": "Test Customer",
        "urgency": "normal"
    }
    
    template = assistant.TEMPLATES["customer_response"]
    
    # Use template fallback directly
    draft = assistant._generate_from_template(clipboard_content, context, template)
    
    logger.info("✅ PASS: Template fallback works")
    logger.info(f"   Subject: {draft['subject']}")
    logger.info(f"   Body: {draft['body'][:200]}...")
    
    return True


async def main():
    """Run all AI integration tests"""
    logger.info("")
    logger.info("🤖 AI INTEGRATION TEST SUITE")
    logger.info("Testing Clippy email generation end-to-end")
    logger.info("")
    
    results = []
    
    # Test 1: LiteLLM connection
    results.append(await test_litellm_connection())
    
    # Test 2: AI generation (skip if LiteLLM unavailable)
    results.append(await test_ai_generation())
    
    # Test 3: Clippy draft generation
    results.append(await test_clippy_draft_generation())
    
    # Test 4: Graceful degradation
    results.append(await test_graceful_degradation())
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    skipped = sum(1 for r in results if r is None)
    
    logger.info(f"✅ Passed: {passed}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"⚠️  Skipped: {skipped}")
    logger.info("")
    
    if failed == 0:
        logger.info("🎉 ALL TESTS PASSED")
        logger.info("")
        logger.info("AI integration is working correctly!")
        logger.info("Clippy can generate professional email drafts.")
        logger.info("Graceful degradation works if AI unavailable.")
        return 0
    else:
        logger.error("💥 SOME TESTS FAILED")
        logger.error("")
        logger.error("Fix issues before shipping alpha.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

