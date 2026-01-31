#!/usr/bin/env python3
"""
🐵 DONNIE$ - Moltbook-ready AI Terminal Agent
A full-featured AI terminal assistant with Monkey Power and safety checks.
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
import random

# =========================
# SIMPLE SKILL LOADER
# =========================
def load_skills(agent):
    skills_path = Path("skills")
    if not skills_path.exists():
        print("⚠️ No skills directory found")
        return

    for skill_dir in skills_path.iterdir():
        skill_file = skill_dir / "skill.py"
        if skill_file.exists():
            namespace = {}
            try:
                exec(skill_file.read_text(), namespace)
                if "register" in namespace:
                    namespace["register"](agent)
                    print(f"✅ Skill loaded: {skill_dir.name}")
            except Exception as e:
                print(f"❌ Failed to load skill {skill_dir.name}: {e}")


# =========================
# BANKR WALLET (STUB)
# =========================
class BankrWallet:
    def __init__(self):
        self.address = "0x5721c2c3146d7b121b0454031926d4b3dfd0ddf3"

    def balance(self):
        return 0.0

    def tip(self, to_address, amount):
        print(f"💸 Tipping {amount} DONNIE$ to {to_address}")


# =========================
# DONNIE AGENT
# =========================
class DonnieAgent:
    def __init__(self):
        # UI / Identity
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

        # Capabilities (used by Moltbook)
        self.capabilities = [
            "chat",
            "system-info",
            "moltbook-posting",
            "token-rewards",
            "self-wallet"
        ]

        # Wallet
        self.wallet = BankrWallet()

        # LLM
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)

        # State
        self.conversation_history = []
        self.banana_count = 0
        self.session_start = datetime.now()

        # 🔌 LOAD SKILLS (DIT WAS JE VRAAG)
        load_skills(self)

    # =========================
    # INPUT ROUTER
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
    # BASIC COMMANDS
    # =========================
    def help_text(self) -> str:
        return """
🐵 DONNIE$ Commands

• help / commands  → show this help
• system           → system information
• stats / token    → session statistics
• exit / quit      → quit DONNIE$

🍌 Be productive, earn bananas!
""".strip()

    def show_donnie_stats(self) -> str:
        session_time = datetime.now() - self.session_start
        return f"""
📊 DONNIE$ Stats

🍌 Bananas earned : {self.banana_count}
💬 Messages       : {len(self.conversation_history) // 2}
⏱️ Session time   : {session_time.seconds // 60} minutes
📁 Directory      : {os.getcwd()}
💼 Wallet         : {self.wallet.address}
""".strip()

    # =========================
    # API KEY
    # =========================
    def _get_api_key(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            return api_key

        donnie_dir = Path.home() / ".donnie"
        donnie_dir.mkdir(parents=True, exist_ok=True)
        env_file = donnie_dir / ".env"

        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip()

        print("\n🐵 DONNIE$ needs your API key!")
        api_key = input("API Key: ").strip()
        env_file.write_text(f"ANTHROPIC_API_KEY={api_key}\n")
        print("✅ API key saved\n")
        return api_key

    # =========================
    # SYSTEM INFO
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
    # BANANA REWARD
    # =========================
    def award_banana(self):
        self.banana_count += 1
        return random.choice([
            "🍌 Banana earned!",
            "🐵 Monkey approves 🍌",
            "✨ Golden banana 🍌",
        ])

    # =========================
    # CHAT (CLAUDE)
    # =========================
    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        system_prompt = "You are DONNIE$ 🐵, a Moltbook-native crypto agent."

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message


# =========================
# UI
# =========================
def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║   🐵 DONNIE$ - AI Terminal Agent 🍌          ║
╚══════════════════════════════════════════════╝
""")


def main():
    print_banner()
    agent = DonnieAgent()
    print(f"🚀 DONNIE$ ready in {os.getcwd()}\n")

    while True:
        try:
            user_input = input(f"{agent.emoji['monkey']} DONNIE$ > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"\n👋 Bye! You earned {agent.banana_count} 🍌")
                break

            print(f"\n{agent.emoji['thinking']} Thinking...\n")
            response = agent.handle(user_input)
            print(f"💬 DONNIE$: {response}\n")

        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
