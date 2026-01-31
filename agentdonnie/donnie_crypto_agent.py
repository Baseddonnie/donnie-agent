#!/usr/bin/env python3
"""
🐵 DONNIE$ - Moltbook-ready AI Terminal Agent
Een full-featured AI agent met Monkey Power en Bankr-wallet integratie.
"""

import os
import sys
import subprocess
import random
import time
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
from wallet import BankrWallet

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
        self.wallet = BankrWallet()
        print(f"💰 Wallet address: {self.wallet.address}")

        # Skills
        self.load_skills()

    # =========================
    # Skills
    # =========================
    def load_skills(self):
        print("✅ Skill loaded: moltbook")

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
        return f"""
📊 DONNIE$ Stats

🍌 Bananas earned : {self.banana_count}
💬 Messages       : {len(self.conversation_history) // 2}
⏱️ Session time   : {session_time.seconds // 60} minutes
💰 Wallet address : {self.wallet.address}
📁 Directory      : {os.getcwd()}
""".strip()

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
                f"🖥️ OS: {subprocess.getoutput('uname -s')}",
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

# =========================
# Daemon loop (systemd)
# =========================
def run_daemon(agent: DonnieAgent):
    print("🚀 DONNIE$ running in daemon mode")

    while True:
        try:
            # Placeholder voor:
            # - Moltbook events
            # - OpenClaw skills
            # - Wallet monitoring
            time.sleep(30)

        except Exception as e:
            print(f"❌ Daemon error: {e}")
            time.sleep(5)

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
    agent = DonnieAgent()

    if sys.stdin.isatty():
        # Interactive mode
        print(f"🚀 DONNIE$ ready in {os.getcwd()}\n")
        while True:
            try:
                user_input = input(f"{agent.emoji['monkey']} DONNIE$ > ").strip()
                if not user_input:
                    continue
                print(agent.handle(user_input))
            except KeyboardInterrupt:
                break
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
