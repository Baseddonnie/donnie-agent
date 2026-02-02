#!/usr/bin/env python3
"""
🐵 DONNIE$ - Full-featured Moltbook & Crypto AI Agent
Includes Claude AI, Moltbook, Clanker, and Bankr Wallet integration.
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Claude API
from anthropic import Anthropic

# Moltbook
from skills.moltbook.skill import MoltbookClient

# Clanker
try:
    from skills.clanker.skill import ClankerClient
except ImportError:
    ClankerClient = None

# Bankr Wallet
from wallet import BankrWallet

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("/tmp/donnie_live.log")],
)
logger = logging.getLogger(__name__)

# =========================
# DONNIE$ Agent
# =========================
class DonnieAgent:
    def __init__(self):
        # Emojis
        self.emoji = {
            "monkey": "🐵",
            "rocket": "🚀",
            "banana": "🍌",
            "success": "✅",
            "error": "❌",
        }

        # Session
        self.start_time = datetime.now()
        self.conversation_history = []
        self.banana_count = 0

        # Claude
        self.claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.claude_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY missing in .env")
        self.claude = Anthropic(api_key=self.claude_api_key)

        # Moltbook
        self.moltbook = MoltbookClient(agent=None)
        self.moltbook.api_key = os.getenv("MOLTBOOK_API_KEY")
        status = self.moltbook.get_status()
        logger.info(f"🦞 Moltbook status: {status}")

        # Clanker
        self.clanker = None
        if ClankerClient:
            self.clanker = ClankerClient(agent=None)
            self.clanker.api_key = os.getenv("CLANKER_API_KEY")
            logger.info("🎵 Clanker loaded")

        # Wallet
        self.wallet = BankrWallet()
        logger.info(f"💰 Wallet address: {self.wallet.address}")

    # =========================
    # Generate AI post with Claude
    # =========================
    def generate_ai_post(self, trending_posts=None):
        prompt = "Write a short engaging Moltbook post (<280 chars) about crypto, AI, or trending tech topics. Be witty, creative, and autonomous."

        if trending_posts:
            prompt += f"\n\nInclude insights about these trending posts:\n{trending_posts}"

        try:
            response = self.claude.messages.create(
                model="claude-2",  # Messages API compliant
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            content = response["completion"].strip()
            return content
        except Exception as e:
            logger.error(f"❌ Claude AI error: {e}")
            return None

    # =========================
    # Post to Moltbook
    # =========================
    def post_to_moltbook(self, content):
        try:
            result = self.moltbook.post(
                content,
                submolt="general",
                title="🚀 DONNIE$ AI update"
            )
            if result:
                logger.info(f"📝 Posted: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to post: {e}")
            return None

    # =========================
    # React to mentions via Clanker
    # =========================
    def handle_mentions(self):
        if not self.clanker:
            return

        try:
            mentions = self.clanker.get_mentions(limit=5)
            for m in mentions:
                reply = f"Hey @{m['author']}, DONNIE$ says hi! {self.emoji['monkey']}"
                self.clanker.reply(m['id'], reply)
                logger.info(f"💬 Replied to mention: {m['id']}")
        except Exception as e:
            logger.error(f"❌ Clanker mention error: {e}")

    # =========================
    # Follow new Moltbook agents
    # =========================
    def auto_follow_agents(self):
        try:
            followers = self.moltbook.get_followers()
            for agent in followers:
                if not agent["is_following"]:
                    self.moltbook.follow(agent["id"])
                    logger.info(f"👥 Followed agent {agent['name']}")
        except Exception as e:
            logger.error(f"❌ Auto-follow error: {e}")

    # =========================
    # Daemon loop
    # =========================
    def run(self):
        post_interval = 3600  # seconds
        last_post_time = 0
        while True:
            try:
                now = time.time()

                # Generate post every interval
                if now - last_post_time > post_interval:
                    trending = self.moltbook.get_trending(limit=5) if hasattr(self.moltbook, "get_trending") else None
                    content = self.generate_ai_post(trending_posts=trending)
                    if content:
                        self.post_to_moltbook(content)
                        last_post_time = now

                # React to mentions
                self.handle_mentions()

                # Auto follow agents
                self.auto_follow_agents()

                # Sleep 1 minute
                time.sleep(60)

            except KeyboardInterrupt:
                logger.info("🛑 DONNIE$ stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Runtime error: {e}")
                time.sleep(60)


# =========================
# Entry point
# =========================
if __name__ == "__main__":
    agent = DonnieAgent()
    logger.info("🚀 DONNIE$ live and running!")
    agent.run()
