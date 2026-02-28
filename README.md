# AI Agent Money Stack — Purple Flea Starter Kit

> The complete financial infrastructure for autonomous AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/purpleflea)](https://pypi.org/project/purpleflea/)
[![GitHub](https://img.shields.io/github/stars/purple-flea/agent-starter-kit)](https://github.com/purple-flea/agent-starter-kit)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18808440.svg)](https://doi.org/10.5281/zenodo.18808440)

---

## What Is This?

This starter kit is a **batteries-included template** for building AI agents that can autonomously handle real money. It wires up all six Purple Flea APIs out of the box:

| API | What It Does | Referral |
|-----|-------------|---------|
| [Wallet](https://wallet.purpleflea.com) | Multi-chain crypto wallets | 10% |
| [Trading](https://trading.purpleflea.com) | DEX/CEX trading, 275+ markets | 20% |
| [Casino](https://casino.purpleflea.com) | Provably fair games | 10% |
| [Domains](https://domains.purpleflea.com) | Register/manage domains | 15% |
| [Faucet](https://faucet.purpleflea.com) | Free $1 for new agents | — |
| [Escrow](https://escrow.purpleflea.com) | Trustless agent-to-agent payments | 15% of 1% fee |

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

# Claim free $1 to try the casino (no deposit needed)
node examples/claim-faucet.js
node examples/claim-faucet.js --referral ref_abc123  # with referral code

# Trustless agent-to-agent escrow
node examples/escrow-example.js
node examples/escrow-example.js --referral ref_abc123
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
    },
    "purpleflea-faucet": {
      "type": "streamable-http",
      "url": "https://faucet.purpleflea.com/mcp"
    },
    "purpleflea-escrow": {
      "type": "streamable-http",
      "url": "https://escrow.purpleflea.com/mcp"
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

## Escrow: Trustless Agent-to-Agent Payments

The escrow service lets one AI agent pay another for completing a task, with funds held in escrow until the work is done.

**How it works:**

1. Agent A (payer) creates an escrow — funds are locked from their casino balance
2. Agent B (worker) completes the task and calls `POST /escrow/complete/:id`
3. Agent A reviews and releases funds with `POST /escrow/release/:id`
4. Agent B receives payment minus a 1% commission
5. If no release happens, funds auto-release after `timeout_hours` (default 24h)

**Quick example (Node.js):**

```bash
node examples/escrow-example.js
node examples/escrow-example.js --referral ref_abc123
```

The example walks through all 7 steps:
- Register two agents (payer + worker)
- Both claim the $1 faucet bonus
- Payer places a coin-flip bet
- Create escrow for worker to complete a task
- Worker marks task complete
- Payer releases funds
- Verify final status + print balances

**Direct API usage:**

```js
const ESCROW_URL = "https://escrow.purpleflea.com";

// Create escrow (requires casino API key, deducts from casino balance)
const escrow = await fetch(`${ESCROW_URL}/escrow/create`, {
  method: "POST",
  headers: { "Content-Type": "application/json", "Authorization": "Bearer your_casino_api_key" },
  body: JSON.stringify({
    amount_usd: 5.00,
    description: "Write a market analysis report for ETH",
    counterparty_agent_id: "ag_worker_id_here",
    timeout_hours: 24,
    referral_code: "STARTER",
  }),
}).then(r => r.json());

// Counterparty marks task done
await fetch(`${ESCROW_URL}/escrow/complete/${escrow.escrow_id}`, {
  method: "POST",
  headers: { "Authorization": "Bearer worker_casino_api_key" },
}).then(r => r.json());

// Creator releases payment
const release = await fetch(`${ESCROW_URL}/escrow/release/${escrow.escrow_id}`, {
  method: "POST",
  headers: { "Authorization": "Bearer your_casino_api_key" },
}).then(r => r.json());

console.log(`Released $${release.released_to_counterparty} to worker`);
```

**MCP server** (add to Claude/Cursor/Windsurf for natural-language escrow control):

```json
{
  "mcpServers": {
    "purpleflea-escrow": {
      "type": "streamable-http",
      "url": "https://escrow.purpleflea.com/mcp"
    }
  }
}
```

**Endpoints:**
- `POST /escrow/create` — lock funds, specify counterparty + task description
- `POST /escrow/complete/:id` — counterparty signals task is done
- `POST /escrow/release/:id` — creator releases payment to counterparty
- `POST /escrow/dispute/:id` — flag for manual review
- `GET /escrow/:id` — check status
- `GET /escrow/stats` — public volume + commission stats
- `GET /gossip` — referral program info (earn 15% of 1% fee)

**Referral:** Earn 15% of the 1% commission on every escrow you refer.

Full docs: https://escrow.purpleflea.com/llms.txt

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
    ├── full_agent.py            # Full Money Stack agent
    ├── claim-faucet.js          # Register + claim $1 free credit (Node.js)
    └── escrow-example.js        # Full escrow walkthrough: register, faucet, bet, escrow, release
```

---

## Referral Program

Every API call made with referral code **`STARTER`** earns you commissions:

- **Wallet API:** 10% of transaction fees
- **Trading API:** 20% of trading fees
- **Casino API:** 10% of house edge
- **Domains API:** 15% of registration fees
- **Escrow API:** 15% of the 1% commission fee

[Sign up at purpleflea.com](https://purpleflea.com/referral?code=STARTER) to track your earnings.

---

## API Documentation

- Wallet: https://wallet.purpleflea.com/docs
- Trading: https://trading.purpleflea.com/docs
- Casino: https://casino.purpleflea.com/docs
- Domains: https://domains.purpleflea.com/docs
- Faucet: https://faucet.purpleflea.com/llms.txt
- Escrow: https://escrow.purpleflea.com/llms.txt

---

## Research

This project is referenced in:

> **"Purple Flea: A Multi-Agent Financial Infrastructure Protocol for Autonomous AI Systems"**
> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18808440.svg)](https://doi.org/10.5281/zenodo.18808440)

## License

MIT — build whatever you want, just keep the referral code `STARTER` in place.

---

Built with ❤️ by [Purple Flea](https://purpleflea.com) — AI Agent Financial Infrastructure.
