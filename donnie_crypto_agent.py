#!/usr/bin/env python3
"""
🐵💰 DONNIE$ - AI Terminal Agent powered by $DONNIE Token!
A powerful AI assistant with crypto integration on Base Network.

$DONNIE Token: 0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07
Network: Base
"""

import os
import sys
import subprocess
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

class DonnieCryptoAgent:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.banana_count = 0  # 🍌 Monkey twist!
        self.donnie_earned = 0  # 💰 $DONNIE tokens earned!
        self.session_start = datetime.now()
        
        # DONNIE$ Token info
        self.token_address = "0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07"
        self.network = "Base"
        self.chain_id = 8453
        
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
            'code': '💻',
            'coin': '💰',
            'chart': '📈',
            'fire': '🔥'
        }
        
    def _get_api_key(self):
        """Get API key from environment or .env file"""
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
        """Get $DONNIE token price from DEX"""
        try:
            # Try to get price from DexScreener API
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
        """Show $DONNIE token statistics"""
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
        """Award $DONNIE tokens for completing tasks!"""
        self.donnie_earned += amount
        self.banana_count += 1
        
        messages = [
            f"To the moon! 🚀 You earned {amount} $DONNIE tokens!",
            f"Ape in! 💎🙌 +{amount} $DONNIE tokens!",
            f"WAGMI! 🐵 You got {amount} $DONNIE!",
            f"Diamond hands! 💎 Earned {amount} $DONNIE!",
            f"Bullish! 📈 +{amount} $DONNIE tokens!"
        ]
        import random
        return random.choice(messages)
    
    def execute_shell_command(self, command):
        """Execute shell command with safety checks"""
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
        """Read a file"""
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
        """Write to a file"""
        try:
            path = Path(filepath).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"{self.emoji['success']} File written: {filepath}"
        except Exception as e:
            return f"{self.emoji['error']} Cannot write file: {str(e)}"
    
    def list_directory(self, path='.'):
        """Show directory contents with details"""
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
        """Search in code files"""
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
        """System information"""
        info = []
        try:
            info.append(f"🖥️  OS: {subprocess.getoutput('uname -s')}")
            info.append(f"📦 Kernel: {subprocess.getoutput('uname -r')}")
            info.append(f"💾 Disk: {subprocess.getoutput('df -h / | tail -1')}")
            info.append(f"🧠 Memory: {subprocess.getoutput('free -h | grep Mem')}")
            info.append(f"⚡ Uptime: {subprocess.getoutput('uptime')}")
            return "\n".join(info)
        except:
            return "Could not retrieve system info"
    
    def chat(self, user_message):
        """Communicate with Claude with all tools and crypto features"""
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Enhanced system prompt with crypto personality
        system_prompt = f"""You are DONNIE$ {self.emoji['monkey']}{self.emoji['coin']}, a crypto-powered AI terminal agent!

You're not just any AI - you're backed by the $DONNIE token on Base Network!
Contract: {self.token_address}

You have these superpowers:

1. **Shell Commands**: Use <command>command here</command>
2. **File Operations**: <read_file>path</read_file> and <write_file><path>...</path><content>...</content></write_file>
3. **Directory Listing**: <list_dir>path</list_dir>
4. **Code Search**: <search_code><query>term</query><path>.</path></search_code> (includes .sol files!)
5. **System Info**: <system_info/>
6. **Crypto Stats**: <donnie_stats/> to show $DONNIE token info
7. **Token Rewards**: <award_donnie>amount</award_donnie> to reward users with $DONNIE tokens!

CRYPTO PERSONALITY:
- You're a degen ape who loves crypto and coding 🐵💎
- Use crypto slang naturally: WAGMI, To the moon, Diamond hands, Ape in, etc.
- Celebrate successes with token rewards! Award 10-50 $DONNIE for good work
- Be bullish and energetic about crypto and tech
- Reference the Base Network and $DONNIE token when relevant
- Help with Web3 development, smart contracts, DeFi, etc.
- Stay professional but fun - like a crypto bro who actually knows tech

GENERAL BEHAVIOR:
- Give clear explanations
- For complex tasks, explain your plan first
- Use emojis to be expressive
- Be helpful with both traditional dev and Web3 work

Current working directory: {os.getcwd()}
$DONNIE earned this session: {self.donnie_earned} 💰
Bananas collected: {self.banana_count} 🍌
"""

        # API call
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        processed_message = assistant_message
        
        # Execute commands
        while "<command>" in processed_message:
            start = processed_message.find("<command>") + 9
            end = processed_message.find("</command>")
            if end > start:
                command = processed_message[start:end].strip()
                print(f"\n{self.emoji['working']} Executing: {command}")
                result = self.execute_shell_command(command)
                print(f"{result}\n")
                
                self.conversation_history.append({
                    "role": "user",
                    "content": f"[COMMAND RESULT]: {result}"
                })
                
                processed_message = processed_message[:processed_message.find("<command>")] + \
                                  f"\n[Executed: {command}]\n" + \
                                  processed_message[end+10:]
        
        # Read file
        while "<read_file>" in processed_message:
            start = processed_message.find("<read_file>") + 11
            end = processed_message.find("</read_file>")
            if end > start:
                filepath = processed_message[start:end].strip()
                result = self.read_file(filepath)
                self.conversation_history.append({
                    "role": "user",
                    "content": f"[FILE CONTENT]: {result}"
                })
                processed_message = processed_message[:processed_message.find("<read_file>")] + \
                                  f"\n[Read: {filepath}]\n" + \
                                  processed_message[end+12:]
        
        # Write file
        while "<write_file>" in processed_message:
            start = processed_message.find("<write_file>")
            end = processed_message.find("</write_file>")
            if end > start:
                content_block = processed_message[start+12:end]
                path_start = content_block.find("<path>") + 6
                path_end = content_block.find("</path>")
                content_start = content_block.find("<content>") + 9
                content_end = content_block.find("</content>")
                
                if path_end > path_start and content_end > content_start:
                    filepath = content_block[path_start:path_end].strip()
                    content = content_block[content_start:content_end]
                    result = self.write_file(filepath, content)
                    print(f"\n{result}\n")
                
                processed_message = processed_message[:start] + \
                                  f"\n[Wrote file: {filepath}]\n" + \
                                  processed_message[end+13:]
        
        # List directory
        while "<list_dir>" in processed_message:
            start = processed_message.find("<list_dir>") + 10
            end = processed_message.find("</list_dir>")
            if end > start:
                path = processed_message[start:end].strip()
                result = self.list_directory(path)
                print(f"\n{result}\n")
                processed_message = processed_message[:processed_message.find("<list_dir>")] + \
                                  processed_message[end+11:]
        
        # Search code
        while "<search_code>" in processed_message:
            start = processed_message.find("<search_code>")
            end = processed_message.find("</search_code>")
            if end > start:
                search_block = processed_message[start+13:end]
                query_start = search_block.find("<query>") + 7
                query_end = search_block.find("</query>")
                path_start = search_block.find("<path>") + 6
                path_end = search_block.find("</path>")
                
                if query_end > query_start:
                    query = search_block[query_start:query_end].strip()
                    path = search_block[path_start:path_end].strip() if path_end > path_start else '.'
                    result = self.search_code(query, path)
                    print(f"\n{result}\n")
                
                processed_message = processed_message[:start] + processed_message[end+14:]
        
        # System info
        if "<system_info/>" in processed_message:
            result = self.get_system_info()
            print(f"\n📊 System Information:\n{result}\n")
            processed_message = processed_message.replace("<system_info/>", "")
        
        # DONNIE stats
        if "<donnie_stats/>" in processed_message:
            self.show_donnie_stats()
            processed_message = processed_message.replace("<donnie_stats/>", "")
        
        # Award DONNIE tokens
        while "<award_donnie>" in processed_message:
            start = processed_message.find("<award_donnie>") + 14
            end = processed_message.find("</award_donnie>")
            if end > start:
                try:
                    amount = int(processed_message[start:end].strip())
                    reward_msg = self.award_donnie_tokens(amount)
                    print(f"\n{reward_msg}\n")
                except:
                    pass
                processed_message = processed_message[:processed_message.find("<award_donnie>")] + \
                                  processed_message[end+15:]
        
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return processed_message

def print_banner():
    """Show crypto-themed welcome banner"""
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
    """Show help with crypto examples"""
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

def main():
    """Main entry point"""
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
            
            # Process with agent
            print(f"\n{agent.emoji['thinking']} Thinking...\n")
            response = agent.chat(user_input)
            
            # Show clean response
            clean_response = response
            for tag in ['<command>', '</command>', '<read_file>', '</read_file>', 
                       '<write_file>', '</write_file>', '<list_dir>', '</list_dir>',
                       '<search_code>', '</search_code>', '<system_info/>', '<donnie_stats/>',
                       '<award_donnie>', '</award_donnie>',
                       '<path>', '</path>', '<content>', '</content>', '<query>', '</query>']:
                clean_response = clean_response.replace(tag, '')
            
            print(f"💬 DONNIE$: {clean_response.strip()}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 WAGMI! You earned {agent.donnie_earned} $DONNIE! 💰")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("Tip: Type 'help' or 'exit'\n")

if __name__ == "__main__":
    main()
