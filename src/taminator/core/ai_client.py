"""
AI Client for LiteLLM Integration

Wrapper for calling LiteLLM proxy with Red Hat approved models
"""

import httpx
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AIClient:
    """
    LiteLLM client for AI-powered features
    
    Features:
    - Automatic proxy detection (localhost or rhgrimm)
    - Model selection (Red Hat approved only)
    - Rate limiting
    - Error handling with graceful degradation
    """
    
    # LiteLLM proxy endpoints
    LITELLM_URLS = [
        "http://localhost:4000",  # Local proxy
        "http://rhgrimm:4000"     # Remote grimm machine
    ]
    
    # Red Hat approved models (in fallback order: fastest → most compatible)
    RED_HAT_MODELS = [
        "granite-3.2-8b-instruct",    # Primary: Latest, fastest
        "granite-3.1-8b-instruct",    # Fallback 1: Stable
        "mistral-7b-instruct",        # Fallback 2: Alternative
        "granite-8b-code-instruct",   # Fallback 3: Code-focused (still works for text)
    ]
    
    # Model fallback chain (try in this order)
    MODEL_FALLBACK_CHAIN = RED_HAT_MODELS
    
    def __init__(self):
        """Initialize AI client"""
        self.proxy_url: Optional[str] = None
        self.available_models: List[str] = []
        self._last_check: Optional[datetime] = None
        
        logger.info("🤖 AIClient initialized")
    
    async def is_available(self) -> bool:
        """Check if AI service is available"""
        
        # Cache check result for 1 minute
        if self._last_check and datetime.now() - self._last_check < timedelta(minutes=1):
            return self.proxy_url is not None
        
        # Try to connect to proxy
        async with httpx.AsyncClient(timeout=2.0) as client:
            for url in self.LITELLM_URLS:
                try:
                    response = await client.get(f"{url}/health")
                    if response.status_code == 200:
                        self.proxy_url = url
                        self._last_check = datetime.now()
                        
                        # Get available models
                        await self._fetch_models()
                        
                        logger.info(f"✅ Connected to LiteLLM: {url}")
                        return True
                        
                except Exception as e:
                    logger.debug(f"⚠️  LiteLLM not available at {url}: {e}")
                    continue
        
        self.proxy_url = None
        self._last_check = datetime.now()
        return False
    
    async def _fetch_models(self):
        """Fetch available models from proxy"""
        if not self.proxy_url:
            return
        
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.proxy_url}/models")
                if response.status_code == 200:
                    all_models = response.json().get("data", [])
                    # Filter to Red Hat approved models
                    self.available_models = [
                        m["id"] for m in all_models
                        if any(rh in m["id"] for rh in ["granite", "mistral"])
                    ]
                    logger.debug(f"Available models: {self.available_models}")
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to fetch models: {e}")
            self.available_models = self.RED_HAT_MODELS  # Fallback to default list
    
    async def generate(
        self,
        prompt: str,
        model: str = "granite-3.2-8b-instruct",
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using AI model with automatic fallback
        
        Tries models in fallback order if primary model fails:
        1. granite-3.2-8b-instruct (primary)
        2. granite-3.1-8b-instruct (fallback)
        3. mistral-7b-instruct (alternative)
        4. granite-8b-code-instruct (last resort)
        
        Args:
            prompt: User prompt
            model: Preferred model (default: granite-3.2-8b-instruct)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
            
        Raises:
            RuntimeError: If all models unavailable
        """
        # Check availability
        if not await self.is_available():
            raise RuntimeError("AI service not available. Check LiteLLM proxy.")
        
        # Build models to try (preferred first, then fallback chain)
        models_to_try = []
        if model in self.RED_HAT_MODELS:
            models_to_try.append(model)
        
        # Add fallback chain (skip if already in list)
        for fallback_model in self.MODEL_FALLBACK_CHAIN:
            if fallback_model not in models_to_try:
                models_to_try.append(fallback_model)
        
        # Build request messages
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Try models in order until one succeeds
        last_error = None
        
        for try_model in models_to_try:
            try:
                logger.debug(f"🤖 Trying model: {try_model}")
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.proxy_url}/chat/completions",
                        json={
                            "model": try_model,
                            "messages": messages,
                            "max_tokens": max_tokens,
                            "temperature": temperature
                        }
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    # Extract generated text
                    generated_text = result["choices"][0]["message"]["content"]
                    
                    logger.info(f"✅ Generated {len(generated_text)} chars using {try_model}")
                    return generated_text
                    
            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                logger.warning(f"⚠️  Model {try_model} failed ({status}), trying next model")
                last_error = e
                continue
            
            except Exception as e:
                logger.warning(f"⚠️  Model {try_model} error: {e}, trying next model")
                last_error = e
                continue
        
        # All models failed
        error_msg = f"All AI models failed. Last error: {last_error}"
        logger.error(f"❌ {error_msg}")
        raise RuntimeError(error_msg)
    
    def get_status(self) -> Dict[str, Any]:
        """Get AI service status"""
        return {
            "available": self.proxy_url is not None,
            "proxy_url": self.proxy_url,
            "models": self.available_models,
            "last_check": self._last_check.isoformat() if self._last_check else None
        }


# Global singleton
_ai_client: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """Get global AIClient instance"""
    global _ai_client
    
    if _ai_client is None:
        _ai_client = AIClient()
    
    return _ai_client
