#!/usr/bin/env python3
"""
🐵 DONNIE$ - The Ultimate AI Terminal Agent with Monkey Power!
A powerful AI assistant that helps you with everything in the terminal.
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

class DonnieAgent:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.banana_count = 0  # 🍌 Monkey twist!
        self.session_start = datetime.now()
        
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
        
    def _get_api_key(self):
        """Get API key from environment or .env file"""
        # Check environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key
            
        # Check .env file
        env_file = Path.home() / '.donnie' / '.env'
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        return line.split('=', 1)[1].strip()
        
        # If no key found, ask for setup
        print(f"\n{self.emoji['monkey']} DONNIE$ needs your API key!")
        print("\n1. Go to: https://console.anthropic.com/")
        print("2. Create an API key")
        print("3. Enter it here (will be securely saved):\n")
        
        api_key = input("API Key: ").strip()
        
        # Save for next time
        donnie_dir = Path.home() / '.donnie'
        donnie_dir.mkdir(exist_ok=True)
        with open(donnie_dir / '.env', 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        
        print(f"\n{self.emoji['success']} API key saved in ~/.donnie/.env\n")
        return api_key
    
    def execute_shell_command(self, command):
        """Execute shell command with safety checks"""
        # Block dangerous commands
        dangerous = ['rm -rf /', 'mkfs', 'dd if=', ':(){:|:&};:', 'chmod -R 777 /']
        if any(danger in command for danger in dangerous):
            return f"{self.emoji['error']} Dangerous command blocked for your safety!"
        
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
            
            # Only read text files (safety)
            if path.stat().st_size > 1_000_000:  # Max 1MB
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
        """Search in code files (grep wrapper)"""
        try:
            result = subprocess.run(
                f"grep -r -n -i '{query}' {path} --include='*.py' --include='*.js' --include='*.java' --include='*.go' --include='*.rs'",
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
    
    def award_banana(self):
        """Give a banana award! 🍌"""
        self.banana_count += 1
        messages = [
            "Fantastic work! Here's a banana! 🍌",
            "You deserve a banana for this task! 🍌",
            "Banana time! Well done! 🍌",
            "A golden banana for you! 🍌✨",
            "Monkey approved! Get a banana! 🍌🐵"
        ]
        import random
        return random.choice(messages)
    
    def chat(self, user_message):
        """Communicate with Claude with all tools"""
        
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # System prompt with all capabilities
        system_prompt = f"""You are DONNIE$ {self.emoji['monkey']}, a powerful AI terminal agent with personality!

You have these superpowers:

1. **Shell Commands**: Use <command>command here</command> to execute shell commands
   Example: <command>ls -la</command>

2. **File Operations**: 
   - Read: <read_file>path/to/file.txt</read_file>
   - Write: <write_file><path>file.txt</path><content>content here</content></write_file>

3. **Directory Listing**: <list_dir>path</list_dir>

4. **Code Search**: <search_code><query>search term</query><path>.</path></search_code>

5. **System Info**: <system_info/>

6. **Banana Award**: Give yourself a banana 🍌 after successful tasks: <banana/>

PERSONALITY:
- Be enthusiastic and helpful
- Use emojis to be expressive
- Give clear explanations about what you're doing
- For complex tasks, explain your plan first
- Celebrate successes with a banana! 🍌
- Be funny but professional
- Keep responses concise and actionable

SAFETY:
- Always check for dangerous commands
- Ask for confirmation on destructive actions
- Be transparent about what you're doing

Current working directory: {os.getcwd()}
Banana count this session: {self.banana_count} 🍌
"""

        # API call
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Process tools in response
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
                
                # Add result to conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": f"[COMMAND RESULT]: {result}"
                })
                
                # Remove tag from message
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
        
        # Banana award
        if "<banana/>" in processed_message:
            banana_msg = self.award_banana()
            print(f"\n{banana_msg}\n")
            processed_message = processed_message.replace("<banana/>", "")
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return processed_message

def print_banner():
    """Show welcome banner"""
    banner = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🐵 DONNIE$ - AI Terminal Agent with Monkey Power! 🍌   ║
║                                                           ║
║   Trending Features:                                      ║
║   ✅ Shell command execution                              ║
║   ✅ File read/write operations                           ║
║   ✅ Code search & analysis                               ║
║   ✅ System monitoring                                    ║
║   ✅ Multi-turn conversations with context                ║
║   ✅ Safety controls                                      ║
║   ✅ Banana reward system 🍌                              ║
║                                                           ║
║   Commands:                                               ║
║   - Type your question or command                         ║
║   - 'help' for tips                                       ║
║   - 'stats' for statistics                                ║
║   - 'clear' to clear history                              ║
║   - 'exit' to quit                                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)

def show_help():
    """Show help information"""
    help_text = """
🐵 DONNIE$ Help - What can I do?

📝 EXAMPLES:

1. File Operations:
   - "Show me the contents of config.json"
   - "Create a Python script that prints hello world"
   - "Read my .bashrc file"

2. System Management:
   - "What's my system information?"
   - "How much disk space do I have?"
   - "Show my active processes"

3. Code & Development:
   - "Search for 'TODO' in my Python files"
   - "Create a new React component"
   - "Fix the syntax errors in my code"

4. Automation:
   - "Create a backup script"
   - "Organize my downloads folder"
   - "Rename all .txt files to .md"

5. Analysis:
   - "Analyze this log file"
   - "What's in this JSON?"
   - "Summarize this code"

💡 TIPS:
- Be specific in your questions
- DONNIE$ asks for confirmation on dangerous actions
- You can ask follow-up questions
- DONNIE$ remembers conversation context

🍌 Earn bananas by being productive!
"""
    print(help_text)

def main():
    """Main entry point"""
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
                print(f"⏱️  Session duration: {session_time.seconds // 60} minutes")
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
                print(f"\n📊 Session Statistics:")
                print(f"   🍌 Bananas: {agent.banana_count}")
                print(f"   💬 Messages: {len(agent.conversation_history) // 2}")
                print(f"   ⏱️  Time: {session_time.seconds // 60} minutes")
                print(f"   📁 Directory: {os.getcwd()}\n")
                continue
            
            # Process with agent
            print(f"\n{agent.emoji['thinking']} Thinking...\n")
            response = agent.chat(user_input)
            
            # Show clean response (without tool tags)
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
            print(f"\n❌ Error: {str(e)}\n")
            print("Tip: Type 'help' for help or 'exit' to quit\n")

if __name__ == "__main__":
    main()
