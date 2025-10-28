"""
Gmail Draft Assistant with AI Enhancement

Features:
- Read clipboard content (Clippy integration)
- AI-enhanced draft generation
- Automatic Gmail draft creation
- Context-aware responses
- Template support
"""

import logging
import base64
from email.mime.text import MIMEText
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .google_auth import get_google_auth_manager
from .token_manager import get_token_manager
from .ai_client import get_ai_client

logger = logging.getLogger(__name__)


class GmailAssistant:
    """
    Smart Gmail draft assistant with AI enhancement
    
    Workflow:
    1. User copies text to clipboard (customer email, case notes, etc.)
    2. Clippy detects content and context
    3. AI generates professional draft response
    4. Draft saved to Gmail
    5. User opens Gmail to review and send
    
    Features:
    - Context-aware responses (RFE, Bug, Customer Update)
    - Professional tone matching
    - Template library
    - Red Hat branding
    - Signature management
    """
    
    # Email templates for common scenarios
    TEMPLATES = {
        "rfe_update": {
            "subject": "RFE Update: {issue_key} - {summary}",
            "tone": "professional",
            "style": "technical_update"
        },
        "bug_report": {
            "subject": "Bug Report: {issue_key} - {summary}",
            "tone": "urgent",
            "style": "technical_detailed"
        },
        "customer_response": {
            "subject": "Re: {subject}",
            "tone": "friendly_professional",
            "style": "supportive"
        },
        "weekly_update": {
            "subject": "Weekly TAM Update - {customer_name} - {date}",
            "tone": "professional",
            "style": "executive_summary"
        },
        "portal_announcement": {
            "subject": "New Content Posted: {title}",
            "tone": "informative",
            "style": "announcement"
        }
    }
    
    def __init__(self, token_manager=None):
        """Initialize Gmail Assistant"""
        self.token_manager = token_manager or get_token_manager()
        self.ai_client = get_ai_client()  # LiteLLM client
        
        logger.info("📧 GmailAssistant initialized")
    
    def _get_gmail_service(self):
        """Get authenticated Gmail service"""
        auth_manager = get_google_auth_manager(self.token_manager)
        
        if not auth_manager.has_valid_token():
            raise ValueError("Not authenticated with Google. Please sign in first.")
        
        # Gmail API needs specific scope
        creds = auth_manager.creds
        return build('gmail', 'v1', credentials=creds)
    
    async def create_draft_from_clipboard(
        self,
        clipboard_content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create Gmail draft from clipboard content
        
        Args:
            clipboard_content: Raw clipboard text
            context: Additional context (customer, issue, etc.)
            
        Returns:
            Draft metadata (ID, URL)
        """
        logger.info("📋 Creating draft from clipboard")
        
        # Detect context if not provided
        if not context:
            context = await self._detect_context(clipboard_content)
        
        # Generate draft using AI
        draft_content = await self._generate_draft(clipboard_content, context)
        
        # Create draft in Gmail
        draft_id = await self._save_to_gmail(draft_content)
        
        return {
            "draft_id": draft_id,
            "draft_url": f"https://mail.google.com/mail/u/0/#drafts/{draft_id}",
            "subject": draft_content["subject"],
            "preview": draft_content["body"][:200] + "...",
            "context": context
        }
    
    async def _detect_context(self, content: str) -> Dict[str, Any]:
        """
        Detect context from clipboard content
        
        Uses pattern matching + AI to determine:
        - Email type (RFE update, bug report, customer response)
        - Customer name (if present)
        - Issue keys (JIRA IDs)
        - Urgency level
        """
        import re
        
        context = {
            "type": "general",
            "customer": None,
            "issue_keys": [],
            "urgency": "normal",
            "detected_patterns": []
        }
        
        # Detect JIRA issue keys
        jira_pattern = r'(RHEL|RFE|RHBZ)-\d+'
        issue_keys = re.findall(jira_pattern, content)
        if issue_keys:
            context["issue_keys"] = issue_keys
            context["detected_patterns"].append("jira_issues")
        
        # Detect customer names (common patterns)
        customer_patterns = [
            r'(?:for|at|with)\s+([A-Z][A-Za-z\s]+(?:Bank|Financial|Insurance|Inc\.|Corp\.|Company))',
            r'Customer:\s*(.+)',
            r'Account:\s*(.+)'
        ]
        
        for pattern in customer_patterns:
            matches = re.findall(pattern, content)
            if matches:
                context["customer"] = matches[0].strip()
                context["detected_patterns"].append("customer_name")
                break
        
        # Detect email type
        if any(word in content.lower() for word in ['rfe', 'enhancement request', 'feature request']):
            context["type"] = "rfe_update"
            context["detected_patterns"].append("rfe")
        elif any(word in content.lower() for word in ['bug', 'issue', 'defect', 'error']):
            context["type"] = "bug_report"
            context["detected_patterns"].append("bug")
        elif any(word in content.lower() for word in ['weekly update', 'status report', 'progress']):
            context["type"] = "weekly_update"
            context["detected_patterns"].append("weekly_update")
        
        # Detect urgency
        if any(word in content.lower() for word in ['urgent', 'critical', 'sev 1', 'emergency']):
            context["urgency"] = "high"
        
        logger.debug(f"Detected context: {context}")
        return context
    
    async def _generate_draft(
        self,
        clipboard_content: str,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate email draft using AI
        
        Args:
            clipboard_content: Raw clipboard text
            context: Detected context
            
        Returns:
            Draft content (subject, body, signature)
        """
        logger.info(f"🤖 Generating draft for type: {context['type']}")
        
        # Get template
        template = self.TEMPLATES.get(context["type"], self.TEMPLATES["customer_response"])
        
        # Build AI prompt
        prompt = self._build_draft_prompt(clipboard_content, context, template)
        
        # Call AI model
        try:
            ai_response = await self.ai_client.generate(
                prompt=prompt,
                model="granite-3.2-8b-instruct",  # Red Hat approved model
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse AI response
            draft = self._parse_ai_response(ai_response, context)
            
        except Exception as e:
            logger.warning(f"⚠️  AI generation failed, using template: {e}")
            # Fallback to template-based generation
            draft = self._generate_from_template(clipboard_content, context, template)
        
        # Add Red Hat signature
        draft["body"] += self._get_signature()
        
        return draft
    
    def _build_draft_prompt(
        self,
        content: str,
        context: Dict[str, Any],
        template: Dict[str, str]
    ) -> str:
        """Build AI prompt for draft generation"""
        
        prompt = f"""You are a professional Red Hat Technical Account Manager (TAM) writing an email.

CONTEXT:
- Email Type: {context['type']}
- Customer: {context.get('customer', 'N/A')}
- JIRA Issues: {', '.join(context.get('issue_keys', []))}
- Urgency: {context['urgency']}
- Tone: {template['tone']}
- Style: {template['style']}

SOURCE CONTENT (from clipboard):
{content}

TASK:
Generate a professional email draft with:
1. Clear, concise subject line
2. Professional greeting
3. Main content based on source material
4. Call to action (if appropriate)
5. Professional closing

OUTPUT FORMAT:
SUBJECT: [subject line]

BODY:
[email body - 3-5 paragraphs]

GUIDELINES:
- Use professional TAM voice
- Be clear and concise
- Include relevant JIRA links if applicable
- Match the specified tone and style
- Do NOT include signature (added separately)
"""
        
        return prompt
    
    def _parse_ai_response(
        self,
        ai_response: str,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """Parse AI-generated draft"""
        
        lines = ai_response.strip().split('\n')
        
        # Extract subject
        subject = "Update"
        for line in lines:
            if line.startswith("SUBJECT:"):
                subject = line.replace("SUBJECT:", "").strip()
                break
        
        # Extract body (everything after BODY: or first blank line)
        body_started = False
        body_lines = []
        
        for line in lines:
            if line.startswith("BODY:"):
                body_started = True
                continue
            if body_started:
                body_lines.append(line)
        
        body = '\n'.join(body_lines).strip()
        
        return {
            "subject": subject,
            "body": body
        }
    
    def _generate_from_template(
        self,
        content: str,
        context: Dict[str, Any],
        template: Dict[str, str]
    ) -> Dict[str, str]:
        """Fallback template-based generation (no AI)"""
        
        # Simple template expansion
        subject = template["subject"].format(
            issue_key=context.get("issue_keys", ["N/A"])[0] if context.get("issue_keys") else "N/A",
            summary="Update",
            customer_name=context.get("customer", "Customer"),
            date=datetime.now().strftime("%Y-%m-%d")
        )
        
        body = f"""Hello,

{content}

Please let me know if you have any questions or need additional information.

"""
        
        return {
            "subject": subject,
            "body": body
        }
    
    def _get_signature(self) -> str:
        """Get Red Hat TAM signature"""
        
        # TODO: Load from user preferences
        return """
--
Jimmy Byrd
Senior Technical Account Manager
Red Hat, Inc.
jbyrd@redhat.com
"""
    
    async def _save_to_gmail(self, draft_content: Dict[str, str]) -> str:
        """
        Save draft to Gmail
        
        Args:
            draft_content: Subject and body
            
        Returns:
            Draft ID
        """
        logger.info("💾 Saving draft to Gmail")
        
        try:
            gmail = self._get_gmail_service()
            
            # Create message
            message = MIMEText(draft_content["body"])
            message['subject'] = draft_content["subject"]
            message['from'] = 'me'  # Gmail uses 'me' as sender
            
            # Encode message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Create draft
            draft = gmail.users().drafts().create(
                userId='me',
                body={
                    'message': {
                        'raw': encoded_message
                    }
                }
            ).execute()
            
            logger.info(f"✅ Draft created: {draft['id']}")
            return draft['id']
            
        except HttpError as e:
            logger.error(f"❌ Failed to create draft: {e}")
            raise
    
    async def create_draft_manual(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> str:
        """
        Create Gmail draft manually (no AI)
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            
        Returns:
            Draft ID
        """
        logger.info(f"📧 Creating manual draft to: {to}")
        
        gmail = self._get_gmail_service()
        
        # Create message
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)
        
        # Encode and create draft
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        draft = gmail.users().drafts().create(
            userId='me',
            body={'message': {'raw': encoded_message}}
        ).execute()
        
        return draft['id']
    
    def list_drafts(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        List existing Gmail drafts
        
        Args:
            max_results: Maximum number of drafts to return
            
        Returns:
            List of draft metadata
        """
        logger.info("📋 Listing Gmail drafts")
        
        gmail = self._get_gmail_service()
        
        try:
            results = gmail.users().drafts().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            drafts = results.get('drafts', [])
            
            return [
                {
                    "id": draft['id'],
                    "snippet": gmail.users().drafts().get(
                        userId='me',
                        id=draft['id']
                    ).execute().get('message', {}).get('snippet', '')
                }
                for draft in drafts
            ]
            
        except HttpError as e:
            logger.error(f"❌ Failed to list drafts: {e}")
            return []
    
    def delete_draft(self, draft_id: str):
        """Delete a Gmail draft"""
        logger.info(f"🗑️  Deleting draft: {draft_id}")
        
        gmail = self._get_gmail_service()
        
        try:
            gmail.users().drafts().delete(
                userId='me',
                id=draft_id
            ).execute()
            
            logger.info("✅ Draft deleted")
            
        except HttpError as e:
            logger.error(f"❌ Failed to delete draft: {e}")
            raise


# Global singleton
_gmail_assistant: Optional[GmailAssistant] = None


def get_gmail_assistant() -> GmailAssistant:
    """Get global GmailAssistant instance"""
    global _gmail_assistant
    
    if _gmail_assistant is None:
        _gmail_assistant = GmailAssistant()
    
    return _gmail_assistant

