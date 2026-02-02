import requests
import os
import logging

MOLTBOOK_API = "https://www.moltbook.com/api/v1"

logger = logging.getLogger(__name__)

def register(agent):
    """Register the Moltbook skill with the agent"""
    agent.moltbook = MoltbookClient(agent)
    logger.info(f"✅ Moltbook skill loaded")

class MoltbookClient:
    def __init__(self, agent):
        self.agent = agent
        # Your actual agent ID from Moltbook registration
        self.agent_id = "341cb075-738b-40cc-a9e6-520162e13250"
        self.api_key = os.getenv("MOLTBOOK_API_KEY", "moltbook_sk_Q73cYorPjS-a7P2ZBWmobRokP8r2lIob")
        
        if not self.api_key:
            logger.warning("⚠️ MOLTBOOK_API_KEY not found in environment")
        else:
            logger.info(f"💚 Moltbook client initialized with agent_id: {self.agent_id}")
    
    def _get_headers(self):
        """Get authorization headers for API requests"""
        if not self.api_key:
            raise ValueError("MOLTBOOK_API_KEY not set")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_status(self):
        """Check agent claim status"""
        try:
            r = requests.get(
                f"{MOLTBOOK_API}/agents/status",
                headers=self._get_headers()
            )
            r.raise_for_status()
            status = r.json()
            logger.info(f"📊 Agent status: {status}")
            return status
        except Exception as e:
            logger.error(f"❌ Failed to get status: {e}")
            return None
    
    def get_me(self):
        """Get current agent profile"""
        try:
            r = requests.get(
                f"{MOLTBOOK_API}/agents/me",
                headers=self._get_headers()
            )
            r.raise_for_status()
            profile = r.json()
            logger.info(f"👤 Agent profile loaded: {profile.get('name')}")
            return profile
        except Exception as e:
            logger.error(f"❌ Failed to get agent profile: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def post(self, content, submolt="general", title=None):
        """Create a post on Moltbook"""
        # Check if claimed first
        status = self.get_status()
        if status and not status.get('claimed'):
            logger.warning("⚠️ Agent not claimed yet! Posts may not appear.")
            logger.info(f"📋 Claim URL: https://moltbook.com/claim/moltbook_claim_VjHZZFw8CKzu6bVnBtMDH3gysQFxnEM-")
        
        # If no title provided, use first 60 chars of content
        if not title:
            title = content[:60] + ("..." if len(content) > 60 else "")
        
        payload = {
            "submolt": submolt,
            "title": title,
            "content": content
        }
        
        try:
            logger.info(f"📤 Posting to /{submolt}: {title}")
            r = requests.post(
                f"{MOLTBOOK_API}/posts",
                json=payload,
                headers=self._get_headers()
            )
            r.raise_for_status()
            result = r.json()
            logger.info(f"✅ Posted successfully: post_id={result.get('id')}")
            logger.info(f"🔗 View at: https://moltbook.com/u/DONNIE_AGENT")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to post: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            return None
    
    def get_feed(self, sort="hot", limit=25):
        """Get posts from feed"""
        try:
            r = requests.get(
                f"{MOLTBOOK_API}/feed?sort={sort}&limit={limit}",
                headers=self._get_headers()
            )
            r.raise_for_status()
            feed = r.json()
            logger.info(f"📥 Fetched {len(feed) if isinstance(feed, list) else 0} posts from feed")
            return feed
        except Exception as e:
            logger.error(f"❌ Failed to get feed: {e}")
            return None
    
    def comment_on_post(self, post_id, content):
        """Comment on a post"""
        try:
            r = requests.post(
                f"{MOLTBOOK_API}/posts/{post_id}/comments",
                json={"content": content},
                headers=self._get_headers()
            )
            r.raise_for_status()
            result = r.json()
            logger.info(f"✅ Commented on post {post_id}")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to comment: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def upvote_post(self, post_id):
        """Upvote a post"""
        try:
            r = requests.post(
                f"{MOLTBOOK_API}/posts/{post_id}/upvote",
                headers=self._get_headers()
            )
            r.raise_for_status()
            logger.info(f"⬆️ Upvoted post {post_id}")
            return r.json()
        except Exception as e:
            logger.error(f"❌ Failed to upvote: {e}")
            return None
