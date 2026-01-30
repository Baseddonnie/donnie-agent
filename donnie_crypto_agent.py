#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DONNIE$ - AI Terminal Agent powered by $DONNIE Token!
A powerful AI assistant with crypto integration on Base Network.

$DONNIE Token: 0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07
Network: Base
"""

import os
import sys
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
import random

class DonnieCryptoAgent:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.banana_count = 0
        self.donnie_earned = 0
        self.session_start = datetime.now()
        
        self.token_address = "0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07"
        self.network = "Base"
        self.chain_id = 8453
        
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
            'code': '💻',
            'coin': '💰',
            'chart': '📈',
            'fire': '🔥'
        }

    def _get_api_key(self):
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

    def get_donnie_price(self):
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{self.token_address}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('pairs'):
                    pair = data['pairs'][0]
                    price = float(pair.get('priceUsd', 0))
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
                    volume = float(pair.get('volume', {}).get('h24', 0))
                    price_change = float(pair.get('priceChange', {}).get('h24', 0))
                    return {
                        'price': price,
                        'liquidity': liquidity,
                        'volume_24h': volume,
                        'price_change_24h': price_change,
                        'success': True
                    }
            return {'success': False, 'error': 'Could not fetch price'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def show_donnie_stats(self):
        print(f"\n{self.emoji['chart']} $DONNIE Token Stats:")
        print(f"   {self.emoji['coin']} Contract: {self.token_address}")
        print(f"   {self.emoji['rocket']} Network: {self.network} (Chain ID: {self.chain_id})")
        
        price_data = self.get_donnie_price()
        if price_data['success']:
            price = price_data['price']
            change = price_data['price_change_24h']
            change_emoji = '📈' if change > 0 else '📉'
            print(f"   {self.emoji['fire']} Price: ${price:.8f}")
            print(f"   {change_emoji} 24h Change: {change:+.2f}%")
            print(f"   💧 Liquidity: ${price_data['liquidity']:,.2f}")
            print(f"   📊 Volume 24h: ${price_data['volume_24h']:,.2f}")
        else:
            print(f"   ⚠️  Live price data unavailable")
        print(f"\n   🍌 Your session earnings: {self.donnie_earned} $DONNIE\n")

    def award_donnie_tokens(self, amount=10):
        self.donnie_earned += amount
        self.banana_count += 1
        messages = [
            f"To the moon! 🚀 You earned {amount} $DONNIE tokens!",
            f"Ape in! 💎🙌 +{amount} $DONNIE tokens!",
            f"WAGMI! 🐵 You got {amount} $DONNIE!",
            f"Diamond hands! 💎 Earned {amount} $DONNIE!",
            f"Bullish! 📈 +{amount} $DONNIE tokens!"
        ]
        return random.choice(messages)

    def execute_shell_command(self, command):
        dangerous = ['rm -rf /', 'mkfs', 'dd if=', ':(){:|:&};:', 'chmod -R 777 /']
        if any(danger in command for danger in dangerous):
            return f"{self.emoji['error']} Dangerous command blocked!"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=os.getcwd()
            )
            output = result.stdout if result.stdout else ""
            errors = result.stderr if result.stderr else ""
            return f"Output:\n{output}\n{errors if errors else ''}"
        except subprocess.TimeoutExpired:
            return f"{self.emoji['error']} Command timeout after 60 seconds"
        except Exception as e:
            return f"{self.emoji['error']} Error: {str(e)}"

    def read_file(self, filepath):
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
            return f"{self.emoji['error']} Cannot read file: {str(e)}"

    def write_file(self, filepath, content):
        try:
            path = Path(filepath).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"{self.emoji['success']} File written: {filepath}"
        except Exception as e:
            return f"{self.emoji['error']} Cannot write file: {str(e)}"

    def list_directory(self, path='.'):
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
            return f"{self.emoji['error']} Error: {str(e)}"

    def search_code(self, query, path='.'):
        try:
            result = subprocess.run(
                f"grep -r -n -i '{query}' {path} --include='*.py' --include='*.js' --include='*.java' --include='*.go' --include='*.rs' --include='*.sol'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.stdout:
                return f"{self.emoji['search']} Found:\n{result.stdout}"
            else:
                return f"{self.emoji['search']} No results for '{query}'"
        except Exception as e:
            return f"{self.emoji['error']} Search error: {str(e)}"

    def get_system_info(self):
        try:
            info = []
            info.append(f"🖥️ OS: {subprocess.getoutput('uname -s')}")
            info.append(f"📦 Kernel: {subprocess.getoutput('uname -r')}")
            info.append(f"💾 Disk: {subprocess.getoutput('df -h / | tail -1')}")
            info.append(f"🧠 Memory: {subprocess.getoutput('free -h | grep Mem')}")
            info.append(f"⚡ Uptime: {subprocess.getoutput('uptime')}")
            return "\n".join(info)
        except:
            return "Could not retrieve system info"

# --- Banner & Help ---
def print_banner():
    banner = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🐵💰 DONNIE$ - Crypto AI Terminal Agent! 🚀            ║
║                                                           ║
║   Powered by $DONNIE Token on Base Network               ║
║   Contract: 0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07  ║
║                                                           ║
║   Features:                                               ║
║   ✅ Shell command execution                              ║
║   ✅ File operations & code search                        ║
║   ✅ Web3 & smart contract support                        ║
║   ✅ Live $DONNIE token stats                             ║
║   ✅ Earn $DONNIE tokens for tasks! 💎                    ║
║   ✅ Crypto-native personality                            ║
║                                                           ║
║   Commands:                                               ║
║   - Ask anything in natural language                      ║
║   - 'token' - Show $DONNIE stats                          ║
║   - 'stats' - Your earnings & session info                ║
║   - 'help' - Usage tips                                   ║
║   - 'exit' - Quit                                         ║
║                                                           ║
║   WAGMI! 🐵💎🙌                                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)

def show_help():
    help_text = """
🐵💰 DONNIE$ Help - Your Crypto Dev Companion

📝 EXAMPLES:

1. General Development:
   - "Create a Python script for data analysis"
   - "Search for TODO comments in my code"
   - "What's my system info?"

2. Web3 & Crypto:
   - "Write a basic ERC-20 token contract"
   - "Explain how to deploy on Base Network"
   - "Create a Web3.js interaction script"
   - "Show me how to interact with my token"

3. DeFi & Smart Contracts:
   - "Review my Solidity contract for issues"
   - "Create a simple staking contract"
   - "Explain gas optimization techniques"

4. Token Operations:
   - "Show $DONNIE token stats"
   - "Explain how to add liquidity"
   - "What's the current price?"

💡 CRYPTO TIPS:
- DONNIE$ understands Web3 dev and crypto
- Earn $DONNIE tokens by completing tasks!
- Get real-time token stats with 'token' command
- Perfect for Base Network development

🚀 LFG! To the moon! 🌙
"""
    print(help_text)

# --- Main loop ---
def main():
    print_banner()
    try:
        agent = DonnieCryptoAgent()
    except Exception as e:
        print(f"❌ Could not start agent: {e}")
        sys.exit(1)
    print(f"🚀 DONNIE$ is ready! Let's build on Base! 💎\n")
    
    while True:
        try:
            user_input = input(f"{agent.emoji['monkey']}{agent.emoji['coin']} DONNIE$ > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'bye']:
                session_time = datetime.now() - agent.session_start
                print(f"\n👋 WAGMI anon! You earned {agent.donnie_earned} $DONNIE tokens! 💰")
                print(f"🍌 Bananas collected: {agent.banana_count}")
                print(f"⏱️  Session: {session_time.seconds // 60} minutes")
                print(f"🚀 To the moon! 🌙\n")
                break
            if user_input.lower() == 'help':
                show_help()
                continue
            if user_input.lower() in ['token', 'donnie', 'price']:
                agent.show_donnie_stats()
                continue
            if user_input.lower() == 'clear':
                agent.conversation_history = []
                print("🧹 Conversation history cleared!")
                continue
            if user_input.lower() == 'stats':
                session_time = datetime.now() - agent.session_start
                print(f"\n📊 Session Statistics:")
                print(f"   💰 $DONNIE Earned: {agent.donnie_earned}")
                print(f"   🍌 Bananas: {agent.banana_count}")
                print(f"   💬 Messages: {len(agent.conversation_history) // 2}")
                print(f"   ⏱️  Time: {session_time.seconds // 60} minutes")
                print(f"   📁 Directory: {os.getcwd()}")
                print(f"   🌐 Network: {agent.network}\n")
                continue

        except KeyboardInterrupt:
            print(f"\n\n👋 WAGMI! You earned {agent.donnie_earned} $DONNIE! 💰")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("Tip: Type 'help' or 'exit'\n")

if __name__ == "__main__":
    main()
