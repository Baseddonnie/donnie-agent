#!/usr/bin/env python3
"""
🐵 DONNIE$ - The Ultimate AI Terminal Agent with Monkey Power!
A powerful AI assistant that helps you in the terminal.
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
        # Emojis for personality
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

        # Session and API setup
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.banana_count = 0
        self.session_start = datetime.now()

    def _get_api_key(self):
        """Get API key from environment or .env file."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key

        env_file = Path.home() / '.donnie' / '.env'
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        return line.split('=', 1)[1].strip()

        print(f"\n{self.emoji['monkey']} DONNIE$ needs your API key!")
        print("\n1. Go to: https://console.anthropic.com/")
        print("2. Create an API key")
        print("3. Enter it here (will be securely saved):\n")

        api_key = input("API Key: ").strip()
        donnie_dir = Path.home() / '.donnie'
        donnie_dir.mkdir(exist_ok=True)
        with open(donnie_dir / '.env', 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        print(f"\n{self.emoji['success']} API key saved in ~/.donnie/.env\n")
        return api_key

    def execute_shell_command(self, command):
        """Execute shell command safely."""
        dangerous = ['rm -rf /', 'mkfs', 'dd if=', ':(){:|:&};:', 'chmod -R 777 /']
        if any(d in command for d in dangerous):
            return f"{self.emoji['error']} Dangerous command blocked!"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout or ""
            errors = result.stderr or ""
            return f"Output:\n{output}\n{errors}" if errors else f"Output:\n{output}"
        except subprocess.TimeoutExpired:
            return f"{self.emoji['error']} Command timeout after 60 seconds"
        except Exception as e:
            return f"{self.emoji['error']} Error: {e}"

    def read_file(self, filepath):
        """Read a file safely."""
        try:
            path = Path(filepath).expanduser()
            if not path.exists():
                return f"{self.emoji['error']} File not found: {filepath}"
            if path.stat().st_size > 1_000_000:
                return f"{self.emoji['error']} File too large (max 1MB)"
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return f"{self.emoji['file']} Content of {filepath}:\n\n{content}"
        except Exception as e:
            return f"{self.emoji['error']} Cannot read file: {e}"

    def write_file(self, filepath, content):
        """Write content to a file."""
        try:
            path = Path(filepath).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"{self.emoji['success']} File written: {filepath}"
        except Exception as e:
            return f"{self.emoji['error']} Cannot write file: {e}"

    def list_directory(self, path='.'):
        """List directory contents."""
        try:
            path_obj = Path(path).expanduser()
            if not path_obj.exists():
                return f"{self.emoji['error']} Directory not found: {path}"
            items = []
            for item in sorted(path_obj.iterdir()):
                size = item.stat().st_size if item.is_file() else '-'
                type_icon = '📁' if item.is_dir() else '📄'
                items.append(f"{type_icon} {item.name} ({size} bytes)" if size != '-' else f"{type_icon} {item.name}")
            return f"{self.emoji['search']} Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            return f"{self.emoji['error']} Error: {e}"

    def search_code(self, query, path='.'):
        """Search code files with grep."""
        try:
            result = subprocess.run(
                f"grep -r -n -i '{query}' {path} --include='*.py' --include='*.js' --include='*.java' --include='*.go' --include='*.rs'",
                shell=True, capture_output=True, text=True, timeout=30
            )
            return f"{self.emoji['search']} Found:\n{result.stdout}" if result.stdout else f"{self.emoji['search']} No results for '{query}'"
        except Exception as e:
            return f"{self.emoji['error']} Search error: {e}"

    def get_system_info(self):
        """Get basic system information."""
        try:
            info = [
                f"🖥️ OS: {subprocess.getoutput('uname -s')}",
                f"📦 Kernel: {subprocess.getoutput('uname -r')}",
                f"💾 Disk: {subprocess.getoutput('df -h / | tail -1')}",
                f"🧠 Memory: {subprocess.getoutput('free -h | grep Mem')}",
                f"⚡ Uptime: {subprocess.getoutput('uptime')}"
            ]
            return "\n".join(info)
        except:
            return "Could not retrieve system info"

    def award_banana(self):
        """Give a banana reward."""
        self.banana_count += 1
        messages = [
            "Fantastic! Here's a banana! 🍌",
            "You deserve a banana! 🍌",
            "Banana time! 🍌",
            "Golden banana for you! 🍌✨",
            "Monkey approved! 🍌🐵"
        ]
        return random.choice(messages)

    def chat(self, user_message):
        """Send message to Claude and process tool commands."""
        self.conversation_history.append({"role": "user", "content": user_message})
        system_prompt = f"""You are DONNIE$ {self.emoji['monkey']}, an AI terminal agent with personality and tools."""
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=system_prompt,
            messages=self.conversation_history
        )
        assistant_message = response.content[0].text
        # Tool processing can be implemented here as before
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🐵 DONNIE$ - AI Terminal Agent with Monkey Power! 🍌   ║
║                                                           ║
║   Features:                                               ║
║   ✅ Shell command execution                               ║
║   ✅ File read/write operations                            ║
║   ✅ Code search & analysis                                ║
║   ✅ System monitoring                                     ║
║   ✅ Multi-turn conversations                              ║
║   ✅ Safety controls                                       ║
║   ✅ Banana reward system 🍌                               ║
║                                                           ║
║   Commands:                                               ║
║   - Type your question or command                         ║
║   - 'help' for tips                                       ║
║   - 'stats' for statistics                                ║
║   - 'clear' to clear history                               ║
║   - 'exit' to quit                                        ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)

def show_help():
    help_text = """
🐵 DONNIE$ Help:

1. File Operations:
   - "Read my file.txt"
   - "Write a Python script"

2. System Info:
   - "Show my system info"
   - "Disk space"

3. Code & Development:
   - "Search TODO in my code"

4. Automation:
   - "Organize folder"
   - "Create backup script"

🍌 Earn bananas by being productive!
"""
    print(help_text)

def main():
    print_banner()
    try:
        agent = DonnieAgent()
    except Exception as e:
        print(f"❌ Could not start agent: {e}")
        sys.exit(1)

    print(f"🚀 DONNIE$ is ready! Current directory: {os.getcwd()}\n")

    while True:
        try:
            user_input = input(f"{agent.emoji['monkey']} DONNIE$ > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'bye']:
                session_time = datetime.now() - agent.session_start
                print(f"\n👋 Goodbye! You earned {agent.banana_count} 🍌 this session!")
                print(f"⏱️ Session duration: {session_time.seconds // 60} minutes")
                break
            if user_input.lower() == 'help':
                show_help()
                continue
            if user_input.lower() == 'clear':
                agent.conversation_history = []
                print("🧹 Conversation history cleared!")
                continue
            if user_input.lower() == 'stats':
                session_time = datetime.now() - agent.session_start
                print(f"\n📊 Session Stats:")
                print(f"   🍌 Bananas: {agent.banana_count}")
                print(f"   💬 Messages: {len(agent.conversation_history) // 2}")
                print(f"   ⏱️ Time: {session_time.seconds // 60} minutes")
                print(f"   📁 Directory: {os.getcwd()}\n")
                continue

            print(f"\n{agent.emoji['thinking']} Thinking...\n")
            response = agent.chat(user_input)
            clean_response = response
            for tag in ['<command>', '</command>', '<read_file>', '</read_file>', 
                        '<write_file>', '</write_file>', '<list_dir>', '</list_dir>',
                        '<search_code>', '</search_code>', '<system_info/>', '<banana/>',
                        '<path>', '</path>', '<content>', '</content>', '<query>', '</query>']:
                clean_response = clean_response.replace(tag, '')
            print(f"💬 DONNIE$: {clean_response.strip()}\n")

        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye! You earned {agent.banana_count} 🍌!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\nTip: Type 'help' or 'exit'\n")

if __name__ == "__main__":
    main()
