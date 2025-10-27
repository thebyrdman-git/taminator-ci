"""
AI Client for Taminator - Red Hat Compliant AI Integration

Uses Red Hat Granite models via LiteLLM proxy for customer data processing.
Follows Red Hat AI Policy compliance requirements.
"""

import os
import json
from typing import Optional, Dict, List, Any
from pathlib import Path

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from rich.console import Console

console = Console()


class AIClient:
    """
    Red Hat-compliant AI client for Taminator.
    
    Architecture:
    - Uses LiteLLM proxy (localhost:4000) for model access
    - Red Hat Granite models for customer data
    - Fallback to templates if AI unavailable
    - Full audit logging for compliance
    """
    
    def __init__(self, model: str = "granite-3.2-8b-instruct"):
        """
        Initialize AI client.
        
        Args:
            model: Model name (default: granite-3.2-8b-instruct)
        """
        self.model = model
        self.litellm_base_url = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")
        self.litellm_api_key = os.getenv("LITELLM_API_KEY", "***REMOVED***")
        self.client = None
        self.available = False
        
        # Initialize client if OpenAI library available
        if OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(
                    base_url=self.litellm_base_url,
                    api_key=self.litellm_api_key
                )
                self.available = True
            except Exception as e:
                console.print(f"[yellow]⚠️  AI client initialization failed: {e}[/yellow]")
                self.available = False
        else:
            console.print("[yellow]⚠️  OpenAI library not installed. AI features disabled.[/yellow]")
            console.print("[yellow]   Install with: pip install openai[/yellow]")
    
    def is_available(self) -> bool:
        """Check if AI client is available."""
        return self.available and self.client is not None
    
    def generate_email(
        self,
        customer_name: str,
        email_type: str,
        rfes_bugs: List[Dict[str, Any]],
        additional_context: str = "",
        tone: str = "professional"
    ) -> Dict[str, str]:
        """
        Generate customer email using AI.
        
        Args:
            customer_name: Customer display name
            email_type: Type of email (status_update, specific_update, action_required, good_news)
            rfes_bugs: List of RFEs/Bugs to include
            additional_context: Additional context from TAM
            tone: Email tone (professional, formal, casual, technical)
        
        Returns:
            Dict with 'subject' and 'body' keys
        """
        if not self.is_available():
            return self._generate_email_fallback(customer_name, email_type, rfes_bugs, additional_context)
        
        try:
            # Build prompt
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_email_prompt(
                customer_name, email_type, rfes_bugs, additional_context, tone
            )
            
            # Call AI model
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            email_content = response.choices[0].message.content
            return self._parse_email_response(email_content)
            
        except Exception as e:
            console.print(f"[yellow]⚠️  AI generation failed: {e}[/yellow]")
            console.print("[yellow]   Falling back to template-based generation[/yellow]")
            return self._generate_email_fallback(customer_name, email_type, rfes_bugs, additional_context)
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for email generation."""
        return """You are a helpful assistant for Red Hat Technical Account Managers (TAMs).
Your role is to help compose professional, customer-facing emails about RFE (Request for Enhancement) and Bug updates.

Guidelines:
- Professional but warm tone
- Focus on customer value and impact
- Technical accuracy without jargon overload
- Action items clearly stated
- Always offer next steps or follow-up options
- Keep emails concise (under 300 words)
- Use Red Hat terminology correctly (Ansible Automation Platform, OpenShift, etc.)

Format your response as:
SUBJECT: [subject line]

BODY:
[email body]
"""
    
    def _build_email_prompt(
        self,
        customer_name: str,
        email_type: str,
        rfes_bugs: List[Dict[str, Any]],
        additional_context: str,
        tone: str
    ) -> str:
        """Build user prompt for email generation."""
        
        # Format RFEs/Bugs
        rfe_list = []
        for item in rfes_bugs:
            rfe_id = item.get('id', 'UNKNOWN')
            summary = item.get('summary', 'No summary')
            status = item.get('status', 'Unknown')
            rfe_list.append(f"  - {rfe_id}: {summary} (Status: {status})")
        
        rfe_text = "\n".join(rfe_list) if rfe_list else "  - No RFEs/Bugs selected"
        
        # Map email type to description
        type_descriptions = {
            'status_update': 'weekly/monthly status update',
            'specific_update': 'specific RFE/Bug update',
            'action_required': 'action required from customer',
            'good_news': 'good news - RFE completed or bug fixed',
            'custom': 'custom update'
        }
        type_desc = type_descriptions.get(email_type, 'general update')
        
        prompt = f"""Compose a {type_desc} email for {customer_name}.

Email Type: {email_type}
Tone: {tone}

RFEs/Bugs to include:
{rfe_text}

Additional Context from TAM:
{additional_context if additional_context else "None provided"}

Generate a professional email with:
- Clear subject line
- Friendly greeting
- Brief introduction
- Status of each RFE/Bug
- Next steps or action items
- Offer for follow-up
- Professional closing
"""
        return prompt
    
    def _parse_email_response(self, response: str) -> Dict[str, str]:
        """Parse AI response into subject and body."""
        lines = response.strip().split('\n')
        
        subject = ""
        body_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith("SUBJECT:"):
                subject = line.replace("SUBJECT:", "").strip()
            elif line.startswith("BODY:"):
                in_body = True
            elif in_body:
                body_lines.append(line)
        
        body = "\n".join(body_lines).strip()
        
        # Fallback if parsing failed
        if not subject and not body:
            subject = "Customer Update"
            body = response.strip()
        
        return {
            "subject": subject or "Customer Update",
            "body": body or response.strip()
        }
    
    def _generate_email_fallback(
        self,
        customer_name: str,
        email_type: str,
        rfes_bugs: List[Dict[str, Any]],
        additional_context: str
    ) -> Dict[str, str]:
        """
        Generate email using templates (no AI).
        Fallback when AI is unavailable.
        """
        # Format RFEs/Bugs
        rfe_items = []
        for item in rfes_bugs:
            rfe_id = item.get('id', 'UNKNOWN')
            summary = item.get('summary', 'No summary')
            status = item.get('status', 'Unknown')
            rfe_items.append(f"• {rfe_id}: {summary}\n  Status: {status}")
        
        rfe_text = "\n\n".join(rfe_items) if rfe_items else "No items selected"
        
        # Template by type
        if email_type == 'status_update':
            subject = f"RFE Status Update - {customer_name}"
            body = f"""Hi,

I wanted to share an update on the RFEs and Bugs we're tracking for {customer_name}.

Current Status:

{rfe_text}

{additional_context}

Please let me know if you have any questions or need additional information.

Best regards,
Your Red Hat TAM"""
        
        elif email_type == 'good_news':
            subject = f"Good News - RFE Update for {customer_name}"
            body = f"""Hi,

I have some good news to share regarding the RFEs we've been tracking:

{rfe_text}

{additional_context}

Please let me know if you'd like more details or have any questions.

Best regards,
Your Red Hat TAM"""
        
        elif email_type == 'action_required':
            subject = f"Action Required - {customer_name}"
            body = f"""Hi,

I need your input on the following RFEs/Bugs:

{rfe_text}

{additional_context}

Could you please provide the requested information at your earliest convenience?

Best regards,
Your Red Hat TAM"""
        
        else:  # specific_update or custom
            subject = f"Update - {customer_name}"
            body = f"""Hi,

Here's an update on the items we discussed:

{rfe_text}

{additional_context}

Please let me know if you have any questions.

Best regards,
Your Red Hat TAM"""
        
        return {
            "subject": subject,
            "body": body
        }
    
    def test_connection(self) -> bool:
        """Test AI connection."""
        if not self.is_available():
            return False
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Hello, respond with 'OK' if you can hear me."}
                ],
                max_tokens=10
            )
            return True
        except Exception as e:
            console.print(f"[red]❌ AI connection test failed: {e}[/red]")
            return False


# Singleton instance
_ai_client = None

def get_ai_client(model: str = "granite-3.2-8b-instruct") -> AIClient:
    """Get or create AI client singleton."""
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient(model=model)
    return _ai_client

