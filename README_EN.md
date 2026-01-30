# 🐵 DONNIE$ - AI Terminal Agent with Monkey Power! 🍌

A powerful AI-powered terminal assistant that helps you with everything from writing code to system management. With extra monkey attitude!

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-purple)

## 🎯 Two Versions Available

### 1. **Standard Edition** (`donnie_agent_en.py`)
The classic AI terminal agent with all core features.

### 2. **Crypto Edition** (`donnie_crypto_agent.py`) 💰
Enhanced with $DONNIE token integration on Base Network!
- Live token price tracking
- Earn $DONNIE tokens for completing tasks
- Web3 development support
- Crypto-native personality

**$DONNIE Token Contract:** `0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07`  
**Network:** Base (Chain ID: 8453)

## ✨ Features

### 🚀 Core Capabilities

- **🤖 Conversational AI**: Talk to your terminal in natural language
- **📁 Smart File Operations**: Read, write, and analyze files
- **🔍 Code Search**: Search through your entire codebase instantly
- **💻 Shell Command Execution**: Run complex commands with simple questions
- **📊 System Monitoring**: Real-time system information
- **🧠 Context Awareness**: Remembers your conversation for follow-ups
- **🛡️ Safety First**: Built-in safety checks for dangerous commands
- **🍌 Banana Rewards**: Earn bananas for productivity!

### 💰 Crypto Edition Extras

- **📈 Live Price Data**: Real-time $DONNIE token stats from DEX
- **🎁 Token Rewards**: Earn $DONNIE tokens for completing tasks
- **🔗 Web3 Integration**: Smart contract support, Solidity search
- **💎 Degen Personality**: WAGMI, To the moon, Diamond hands!
- **🌐 Base Network**: Built for Base ecosystem development

## 🎬 Quick Start

### Installation

#### Option 1: Automatic (Recommended)

```bash
# Download the installer
curl -sL https://raw.githubusercontent.com/your-username/donnie/main/install_donnie.sh -o install_donnie.sh

# Make it executable
chmod +x install_donnie.sh

# Run installer
./install_donnie.sh

# Choose your version:
# 1 = Standard Edition
# 2 = Crypto Edition
```

#### Option 2: Manual

```bash
# Install dependencies
pip3 install anthropic requests

# For standard version
python3 donnie_agent_en.py

# For crypto version
python3 donnie_crypto_agent.py
```

### First Run

1. Start DONNIE$: `donnie` (or run the script directly)
2. On first launch, enter your Anthropic API key
3. Get your key at: [https://console.anthropic.com/](https://console.anthropic.com/)
4. Ready to go! 🎉

## 💡 Examples

### Basic Usage

```
DONNIE$ > What's my current directory?
💬 DONNIE$: You're in /home/user/projects!

DONNIE$ > Show me all Python files
💬 DONNIE$: [displays list of .py files]
```

### File Operations

```
DONNIE$ > Create a Python script that prints "Hello Monkey"
💬 DONNIE$: Sure! Creating hello_monkey.py...
[creates file]
🍌 Banana time! Well done!

DONNIE$ > Read my config.json and explain what it does
💬 DONNIE$: [reads file and provides explanation]
```

### Code & Development

```
DONNIE$ > Search for all TODOs in my project
💬 DONNIE$: Found 3 TODOs: [list of results]

DONNIE$ > Create a React component for a login form
💬 DONNIE$: [creates component file]

DONNIE$ > Fix the syntax errors in script.py
💬 DONNIE$: I see 2 errors, let me fix those...
```

### Crypto Edition Features 💰

```
DONNIE$ > Show $DONNIE token stats
📈 $DONNIE Token Stats:
   💰 Contract: 0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07
   🚀 Network: Base (Chain ID: 8453)
   🔥 Price: $0.00012345
   📈 24h Change: +15.67%

DONNIE$ > Create an ERC-20 token contract
💬 DONNIE$: Let's build that token! [creates Solidity contract]
🚀 To the moon! You earned 25 $DONNIE tokens!

DONNIE$ > Explain how to add liquidity on Base
💬 DONNIE$: [provides detailed explanation]
💎 Diamond hands! +15 $DONNIE!
```

## 🛠️ Commands

- `help` - Show detailed help
- `stats` - Session statistics (bananas, time, messages)
- `token` - (Crypto edition) Show $DONNIE token info
- `clear` - Clear conversation history
- `exit` / `quit` - Stop DONNIE$

## 🎨 Features in Detail

### 1. Shell Command Execution
DONNIE$ can execute virtually any shell command:
```
DONNIE$ > Show me the 5 largest files in this folder
[executes: du -ah . | sort -rh | head -5]
```

### 2. File Read/Write
Read and write files directly:
```
DONNIE$ > Create a Python script that calculates fibonacci numbers
[creates fibonacci.py with complete code]
```

### 3. Code Search
Search through your codebase (includes .sol files in crypto edition):
```
DONNIE$ > Find where I use the function 'calculate_total'
[grep through all code files]
```

### 4. System Info
Real-time system monitoring:
```
DONNIE$ > What's my memory usage?
[shows detailed memory info]
```

### 5. Multi-turn Conversations
DONNIE$ remembers context:
```
DONNIE$ > Create a Python script
💬 DONNIE$: [creates script.py]

DONNIE$ > Now add error handling
💬 DONNIE$: [updates the same script]

DONNIE$ > And add logging
💬 DONNIE$: [adds logging to script]
```

### 6. Crypto Features (Crypto Edition) 💰

**Token Economics:**
- Earn 10-50 $DONNIE per completed task
- Live price tracking from DexScreener
- Real-time liquidity and volume data

**Web3 Development:**
- Smart contract creation and review
- Solidity code search
- Gas optimization tips
- Base Network deployment guides

## 🔒 Security

DONNIE$ has built-in safety features:

- ✅ Blocks dangerous commands (`rm -rf /`, etc.)
- ✅ Asks for confirmation on destructive actions
- ✅ Timeout for long-running commands
- ✅ File size limits (max 1MB per file)
- ✅ Only text files are automatically read
- ✅ API key securely stored in `~/.donnie/.env`

## 📊 Requirements

- Python 3.8+
- `anthropic` library
- `requests` library (for crypto edition)
- Anthropic API key (free tier available)
- Linux, macOS, or WSL

## 🤝 Contributing

Want to contribute? Awesome! 🎉

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Tips & Tricks

1. **Be Specific**: The more specific your question, the better DONNIE$ can help
2. **Follow-ups**: DONNIE$ remembers context, feel free to ask follow-up questions
3. **Experiment**: Try different things, DONNIE$ is versatile!
4. **Check Stats**: Type `stats` to see your banana count 🍌
5. **Token Info**: (Crypto edition) Type `token` for live $DONNIE stats 💰

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip3 install anthropic requests --break-system-packages
```

### "API key not found"
DONNIE$ will automatically ask for your API key on first run.  
Get one at: https://console.anthropic.com/

### "Permission denied"
```bash
chmod +x donnie_agent_en.py
chmod +x donnie_crypto_agent.py
```

### Shell alias not working
Restart your terminal or:
```bash
source ~/.bashrc  # or ~/.zshrc
```

## 🗺️ Roadmap

### Standard Edition
- [ ] Web search integration
- [ ] Git operations
- [ ] Docker management
- [ ] Database queries
- [ ] API testing tools
- [ ] Custom plugins system

### Crypto Edition
- [ ] Multi-chain support (Ethereum, Polygon, Arbitrum)
- [ ] NFT operations
- [ ] DeFi protocol interactions
- [ ] Wallet integration
- [ ] Token swap functionality
- [ ] Real on-chain rewards system
- [ ] DAO governance tools

## 📄 License

MIT License - Use freely!

## 🙏 Credits

- Built with [Anthropic's Claude API](https://www.anthropic.com/)
- Powered by [$DONNIE Token](https://basescan.org/token/0xa2a21af3a9a6cd40e29046082dbb7a8337de5b07) on Base Network
- Inspired by the best AI terminal agents
- Extra monkey power by you! 🐵

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/your-username/donnie/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/donnie/discussions)
- 🐦 Twitter: [@DonnieToken](https://twitter.com/DonnieToken)
- 💬 Telegram: [DONNIE$ Community](https://t.me/donniecoin)

---

**Made with 🍌 and 🐵 by the DONNIE$ Team**

⭐ Star this repo if you like DONNIE$!  
💰 Buy $DONNIE on Base Network!  
🚀 LFG! WAGMI! 🌙
