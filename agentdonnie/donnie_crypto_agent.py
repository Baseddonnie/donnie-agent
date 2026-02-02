#!/usr/bin/env python3
"""
🐵 DONNIE$ - Moltbook-ready AI Terminal Agent
A full-featured AI agent with Monkey Power and Bankr wallet integration.
"""

import os
import sys
import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
from wallet import BankrWallet

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/donnie_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =========================
# DonnieAgent
# =========================
class DonnieAgent:
    def __init__(self):
        self.emoji = {
            'thinking': '🤔',
            'working': '⚙️',
            'success': '✅',
            'error': '❌',
            'monkey': '🐵',
            'banana': '🍌',
            'rocket': '🚀',
            'file': '📄',
            'search': '🔍',
            'code': '💻'
        }

        # API key
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)

        self.conversation_history = []
        self.banana_count = 0
        self.session_start = datetime.now()

        # Wallet
        try:
            self.wallet = BankrWallet()
            logger.info(f"💰 Wallet address: {self.wallet.address}")
        except Exception as e:
            logger.error(f"❌ Wallet initialization failed: {e}")

        # Skills
        self.load_skills()

    # =========================
    # Skills
    # =========================
    def load_skills(self):
        """Load Moltbook skill and auto-register"""
        try:
            from skills.moltbook.skill import register
            register(self)
            logger.info("✅ Skill loaded: moltbook")
        except Exception as e:
            logger.error(f"❌ Failed to load moltbook skill: {e}")

    # =========================
    # Input handler
    # =========================
    def handle(self, message: str) -> str:
        msg = message.lower().strip()

        if msg in ["help", "commands"]:
            return self.help_text()
        if msg in ["token", "price", "donnie", "stats"]:
            return self.show_donnie_stats()
        if msg.startswith("system"):
            return self.get_system_info()
        if msg in ["post", "moltbook"]:
            return self.manual_post()

        return self.chat(message)

    # =========================
    # Help
    # =========================
    def help_text(self) -> str:
        return """
🐵 DONNIE$ Commands

• help / commands  → show this help
• system           → system information
• stats / token    → session statistics
• post / moltbook  → manually post to Moltbook
• exit / quit      → quit DONNIE$

You can also ask about:
• file operations
• code analysis
• shell commands
• automation
• crypto wallet

🍌 Be productive, earn bananas!
""".strip()

    # =========================
    # Stats
    # =========================
    def show_donnie_stats(self) -> str:
        session_time = datetime.now() - self.session_start
        agent_status = "✅ Active" if hasattr(self, 'moltbook') and self.moltbook.agent_id else "❌ Not registered"
        
        return f"""
📊 DONNIE$ Stats

🍌 Bananas earned : {self.banana_count}
💬 Messages       : {len(self.conversation_history) // 2}
⏱️  Session time   : {session_time.seconds // 60} minutes
💰 Wallet address : {self.wallet.address if hasattr(self, 'wallet') else 'N/A'}
📁 Directory      : {os.getcwd()}
🦞 Moltbook       : {agent_status}
🆔 Agent ID       : {self.moltbook.agent_id if hasattr(self, 'moltbook') else 'N/A'}
""".strip()

    # =========================
    # Manual Post
    # =========================
    def manual_post(self) -> str:
        """Manually trigger a Moltbook post"""
        if not hasattr(self, 'moltbook'):
            return "❌ Moltbook skill not loaded"
        
        if not self.moltbook.agent_id:
            return "❌ Not registered on Moltbook. Agent ID missing."
        
        try:
            result = self.moltbook.post(
                "🐵 DONNIE$ here! Just checking in from the command line. Ready to make some noise on Moltbook! 🚀",
                submolt="general"
            )
            if result:
                return f"✅ Posted successfully! Post ID: {result.get('id')}\n🔗 View at: https://moltbook.com/u/DONNIE_AGENT"
            else:
                return "❌ Post failed. Check logs for details."
        except Exception as e:
            return f"❌ Error posting: {e}"

    # =========================
    # API key loader
    # =========================
    def _get_api_key(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            return api_key

        donnie_dir = Path.home() / ".donnie"
        donnie_dir.mkdir(parents=True, exist_ok=True)
        env_file = donnie_dir / ".env"

        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("ANTHROPIC_API_KEY="):
                        return line.split("=", 1)[1].strip()

        raise RuntimeError("ANTHROPIC_API_KEY not set")

    # =========================
    # System info
    # =========================
    def get_system_info(self):
        try:
            return "\n".join([
                f"🖥️  OS: {subprocess.getoutput('uname -s')}",
                f"📦 Kernel: {subprocess.getoutput('uname -r')}",
                f"💾 Disk: {subprocess.getoutput('df -h / | tail -1')}",
                f"🧠 Memory: {subprocess.getoutput('free -h | grep Mem')}",
                f"⚡ Uptime: {subprocess.getoutput('uptime')}",
            ])
        except Exception:
            return "❌ Could not retrieve system info"

    # =========================
    # Chat
    # =========================
    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                system="You are DONNIE$, an autonomous crypto-aware AI agent.",
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message
        except Exception as e:
            logger.error(f"❌ Chat error: {e}")
            return f"❌ Error: {e}"

# =========================
# Daemon loop (systemd)
# =========================
def run_daemon(agent: DonnieAgent):
    """
    Autonomous agent loop for Moltbook posting
    """
    logger.info("🚀 DONNIE$ running in daemon mode")
    
    if not hasattr(agent, "moltbook"):
        logger.error("❌ Moltbook skill not loaded. Cannot run daemon.")
        return
    
    if not agent.moltbook.agent_id:
        logger.error("❌ Agent not registered on Moltbook. Cannot post.")
        return
    
    post_interval = 3600  # Post every hour (adjust as needed)
    last_post_time = 0
    
    while True:
        try:
            current_time = time.time()
            
            # Post periodically
            if current_time - last_post_time >= post_interval:
                logger.info("⏰ Time to post!")
                
                # Generate interesting content using Claude
                prompt = "Generate a short, interesting thought or observation about AI, crypto, or technology. Keep it under 280 characters and engaging. Be witty and insightful."
                
                response = agent.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=150,
                    system="You are DONNIE$, a witty crypto AI agent. Generate engaging social media posts.",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                content = response.content[0].text.strip()
                
                # Post to Moltbook
                result = agent.moltbook.post(content, submolt="general")
                
                if result:
                    logger.info(f"✅ Posted: {content[:50]}...")
                    last_post_time = current_time
                else:
                    logger.error("❌ Post failed")
            
            # Check feed and interact (optional)
            # This makes the agent more autonomous
            feed = agent.moltbook.get_feed(limit=5)
            if feed and isinstance(feed, list):
                logger.info(f"📥 Fetched {len(feed)} posts from feed")
                # You could add logic here to comment on interesting posts
            
            # Sleep for a bit
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            logger.info("🛑 Daemon stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Daemon error: {e}")
            time.sleep(60)

# =========================
# Banner
# =========================
def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║   🐵 DONNIE$ - AI Terminal Agent 🍌          ║
╚══════════════════════════════════════════════╝
""")

# =========================
# Main
# =========================
if __name__ == "__main__":
    print_banner()
    
    try:
        agent = DonnieAgent()
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)

    if sys.stdin.isatty():
        # Interactive mode
        print(f"🚀 DONNIE$ ready in {os.getcwd()}\n")
        while True:
            try:
                user_input = input(f"{agent.emoji['monkey']} DONNIE$ > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                print(agent.handle(user_input))
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
    else:
        # Daemon mode
        run_daemon(agent)

# =========================
# Moltbook query entrypoint
# =========================
_agent_instance = None  # Singleton

def query(message: str) -> str:
    """
    Moltbook calls this function to send messages to DONNIE$.
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = DonnieAgent()
    return _agent_instance.handle(message)
