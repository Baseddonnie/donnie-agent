#!/usr/bin/env python3
"""
🐵 DONNIE$ - Moltbook-ready AI Terminal Agent
A full-featured AI terminal assistant with Monkey Power and safety checks.
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
import random


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

        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.banana_count = 0
        self.session_start = datetime.now()

    # =========================
    # INPUT ROUTER (NEW)
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
    # BASIC COMMAND RESPONSES
    # =========================
    def help_text(self) -> str:
        return f"""
🐵 DONNIE$ Commands

• help / commands  → show this help
• system           → system information
• stats / token    → session statistics
• exit / quit      → quit DONNIE$

You can also just talk naturally or ask for:
• file operations
• code analysis
• shell commands
• automation

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
""".strip()

    # =========================
    # API KEY
    # =========================
    def _get_api_key(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key

        donnie_dir = Path.home() / '.donnie'
        donnie_dir.mkdir(parents=True, exist_ok=True)
        env_file = donnie_dir / '.env'

        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        return line.split('=', 1)[1].strip()

        print(f"\n{self.emoji['monkey']} DONNIE$ needs your API key!")
        api_key = input("API Key: ").strip()
        with open(env_file, 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")

        print(f"{self.emoji['success']} API key saved\n")
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

        system_prompt = f"You are DONNIE$ {self.emoji['monkey']}, an AI terminal agent."

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
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
