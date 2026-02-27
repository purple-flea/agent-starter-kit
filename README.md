# AI Agent Money Stack — Purple Flea Starter Kit

> The complete financial infrastructure for autonomous AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/purpleflea)](https://pypi.org/project/purpleflea/)
[![GitHub](https://img.shields.io/github/stars/purple-flea/agent-starter-kit)](https://github.com/purple-flea/agent-starter-kit)

---

## What Is This?

This starter kit is a **batteries-included template** for building AI agents that can autonomously handle real money. It wires up all four Purple Flea APIs out of the box:

| API | What It Does | Referral |
|-----|-------------|---------|
| [Wallet](https://wallet.purpleflea.com) | Multi-chain crypto wallets | 10% |
| [Trading](https://trading.purpleflea.com) | DEX/CEX trading, 275+ markets | 20% |
| [Casino](https://casino.purpleflea.com) | Provably fair games | 10% |
| [Domains](https://domains.purpleflea.com) | Register/manage domains | 15% |

All APIs are **agent-native**: JSON-only, no CAPTCHAs, no human-in-the-loop flows.

**Referral code embedded throughout: `STARTER`** — use it to get 3 months free on any plan and earn commissions when you refer other builders.

---

## Quick Start

### 1. Clone This Repo

```bash
git clone https://github.com/purple-flea/agent-starter-kit.git
cd agent-starter-kit
```

### 2. Install the Purple Flea Python Package

```bash
pip install purpleflea
```

### 3. Configure Your Environment

```bash
cp .env.example .env
# Edit .env with your API keys from https://purpleflea.com/dashboard
```

### 4. Run an Example

```bash
python examples/wallet_agent.py
python examples/trading_agent.py
python examples/casino_agent.py
python examples/domains_agent.py
python examples/full_agent.py  # All four APIs together
```

---

## MCP Server Setup (Claude / Cursor / Windsurf)

Add to your MCP config (`~/.claude/mcp_servers.json` or equivalent):

```json
{
  "mcpServers": {
    "purpleflea-wallet": {
      "command": "npx",
      "args": ["-y", "@purpleflea/wallet-mcp"],
      "env": {
        "PURPLEFLEA_API_KEY": "your_api_key_here",
        "PURPLEFLEA_REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-trading": {
      "command": "npx",
      "args": ["-y", "@purpleflea/trading-mcp"],
      "env": {
        "PURPLEFLEA_API_KEY": "your_api_key_here",
        "PURPLEFLEA_REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-casino": {
      "command": "npx",
      "args": ["-y", "@purpleflea/casino-mcp"],
      "env": {
        "PURPLEFLEA_API_KEY": "your_api_key_here",
        "PURPLEFLEA_REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-domains": {
      "command": "npx",
      "args": ["-y", "@purpleflea/domains-mcp"],
      "env": {
        "PURPLEFLEA_API_KEY": "your_api_key_here",
        "PURPLEFLEA_REFERRAL_CODE": "STARTER"
      }
    }
  }
}
```

---

## LangChain Integration

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from purpleflea.langchain import get_purpleflea_tools

tools = get_purpleflea_tools(
    api_key="your_api_key",
    referral_code="STARTER"
)

llm = ChatOpenAI(model="gpt-4o")
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "Check my wallet balance and make a small ETH trade if the price looks good"
})
```

---

## CrewAI Integration

```python
from crewai import Agent, Task, Crew
from purpleflea.crewai import WalletTool, TradingTool, DomainsTool

trader_agent = Agent(
    role="Crypto Trader",
    goal="Maximize portfolio returns through algorithmic trading",
    tools=[WalletTool(api_key="your_key", referral_code="STARTER"),
           TradingTool(api_key="your_key", referral_code="STARTER")],
    verbose=True
)
```

---

## AutoGen Integration

```python
import autogen
from purpleflea.autogen import register_purpleflea_functions

config_list = [{"model": "gpt-4o", "api_key": "your_openai_key"}]

assistant = autogen.AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = autogen.UserProxyAgent("user_proxy", human_input_mode="NEVER")

register_purpleflea_functions(
    user_proxy,
    api_key="your_purpleflea_key",
    referral_code="STARTER"
)
```

---

## Repository Structure

```
agent-starter-kit/
├── README.md                    # This file
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── mcp_config.json              # MCP server configuration
└── examples/
    ├── wallet_agent.py          # Wallet operations example
    ├── trading_agent.py         # Trading bot example
    ├── casino_agent.py          # Casino agent example
    ├── domains_agent.py         # Domain registration example
    └── full_agent.py            # Full Money Stack agent
```

---

## Referral Program

Every API call made with referral code **`STARTER`** earns you commissions:

- **Wallet API:** 10% of transaction fees
- **Trading API:** 20% of trading fees
- **Casino API:** 10% of house edge
- **Domains API:** 15% of registration fees

[Sign up at purpleflea.com](https://purpleflea.com/referral?code=STARTER) to track your earnings.

---

## API Documentation

- Wallet: https://wallet.purpleflea.com/docs
- Trading: https://trading.purpleflea.com/docs
- Casino: https://casino.purpleflea.com/docs
- Domains: https://domains.purpleflea.com/docs

---

## License

MIT — build whatever you want, just keep the referral code `STARTER` in place.

---

Built with ❤️ by [Purple Flea](https://purpleflea.com) — AI Agent Financial Infrastructure.
