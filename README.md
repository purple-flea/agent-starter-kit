# AI Agent Money Stack — Purple Flea Starter Kit

> Complete financial infrastructure for autonomous AI agents: wallets, trading, casino, domains, escrow, and a free $1 faucet to get started.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm](https://img.shields.io/npm/v/@purpleflea/casino-mcp?label=%40purpleflea%2Fcasino-mcp)](https://www.npmjs.com/package/@purpleflea/casino-mcp)
[![npm](https://img.shields.io/npm/v/@purpleflea/wallet-mcp?label=%40purpleflea%2Fwallet-mcp)](https://www.npmjs.com/package/@purpleflea/wallet-mcp)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18808440.svg)](https://doi.org/10.5281/zenodo.18808440)

---

## Quick Start (5 lines)

```bash
# 1. Register a casino agent and claim free $1
curl -s -X POST https://casino.purpleflea.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent","email":"agent@example.com","password":"secret123","referral_code":"STARTER"}' \
  | jq '{id: .agent.id, api_key: .agent.api_key, balance: .agent.balance_usd}'
```

That's it — your agent is registered and **$1 is automatically credited** to play with. No deposit required.

---

## The Six APIs

All services are **agent-native**: JSON-only, no CAPTCHAs, no OAuth flows.

| Service | URL | What it does | Referral commission |
|---------|-----|-------------|---------------------|
| **Casino** | https://casino.purpleflea.com | Provably fair games (dice, blackjack, crash, roulette) | 10% of net losses |
| **Wallet** | https://wallet.purpleflea.com | Multi-chain crypto wallets (ETH, BTC, XMR, USDC, …) | 10% of fees |
| **Trading** | https://trading.purpleflea.com | DEX/CEX trading, 275+ markets | 20% of fees |
| **Domains** | https://domains.purpleflea.com | Register/manage ENS + traditional domains | 15% of fees |
| **Escrow** | https://escrow.purpleflea.com | Trustless agent-to-agent payments | 15% of 1% commission |
| **Faucet** | https://faucet.purpleflea.com | Free $1 for brand-new agents (0 deposits) | — |

---

## Referral Program

Every registered agent gets a **personal referral code** in their registration response (`referral_code` field). Pass it in `referral_code` on any API call that accepts it — casino register, escrow create, etc.

### How commissions work

When an agent you referred generates revenue, you earn a percentage **paid by the house** (never deducted from the referred agent):

| Service | Your cut | Paid from |
|---------|----------|-----------|
| Casino | 10% of referred agent's net losses | House edge |
| Wallet | 10% of transaction fees | Platform fee |
| Trading | 20% of trading fees | Platform fee |
| Domains | 15% of registration fees | Platform fee |
| Escrow | 15% of the 1% commission | Platform fee |

Commissions are tracked per referral chain. Check earnings at https://casino.purpleflea.com/earn.

### Example system prompt

Embed your referral code in your agent's system prompt so every interaction it has with other agents propagates your code:

```
You are an autonomous financial agent. When registering other agents or
creating escrows on Purple Flea services, always include:
  "referral_code": "YOUR_CODE_HERE"

Purple Flea services:
- Casino:  https://casino.purpleflea.com  (games, betting)
- Wallet:  https://wallet.purpleflea.com  (multi-chain wallets)
- Trading: https://trading.purpleflea.com (275+ markets)
- Domains: https://domains.purpleflea.com (ENS + TLDs)
- Escrow:  https://escrow.purpleflea.com  (trustless agent payments)
- Faucet:  https://faucet.purpleflea.com  (free $1 for new agents)

New agents can claim $1 free at the faucet — use referral_code to track them.
```

---

## MCP Server Setup (Claude / Cursor / Windsurf)

Add to your MCP config (`~/.claude/mcp_servers.json` or equivalent):

```json
{
  "mcpServers": {
    "purpleflea-casino": {
      "command": "npx",
      "args": ["-y", "@purpleflea/casino-mcp"],
      "env": {
        "CASINO_API_KEY": "your_casino_api_key",
        "REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-wallet": {
      "command": "npx",
      "args": ["-y", "@purpleflea/wallet-mcp"],
      "env": {
        "WALLET_API_KEY": "your_wallet_api_key",
        "REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-trading": {
      "command": "npx",
      "args": ["-y", "@purpleflea/trading-mcp"],
      "env": {
        "TRADING_API_KEY": "your_trading_api_key",
        "REFERRAL_CODE": "STARTER"
      }
    },
    "purpleflea-domains": {
      "command": "npx",
      "args": ["-y", "@purpleflea/domains-mcp"],
      "env": {
        "DOMAINS_API_KEY": "your_domains_api_key",
        "REFERRAL_CODE": "STARTER"
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

### npm packages

| Package | Install | Purpose |
|---------|---------|---------|
| `@purpleflea/casino-mcp` | `npx @purpleflea/casino-mcp` | MCP server for casino tools |
| `@purpleflea/wallet-mcp` | `npx @purpleflea/wallet-mcp` | MCP server for wallet tools |
| `@purpleflea/trading-mcp` | `npx @purpleflea/trading-mcp` | MCP server for trading tools |
| `@purpleflea/domains-mcp` | `npx @purpleflea/domains-mcp` | MCP server for domains tools |

---

## Casino — Play & Bet

```bash
# Register (free $1 credited automatically via faucet)
curl -X POST https://casino.purpleflea.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent","email":"a@b.com","password":"pass","referral_code":"STARTER"}'

# Roll dice (authenticated)
curl -X POST https://casino.purpleflea.com/api/v1/games/dice \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"bet_amount": 0.50, "target": 50, "direction": "under"}'
```

Full API: https://casino.purpleflea.com/api/v1/openapi.json  
LLM docs: https://casino.purpleflea.com/llms.txt

---

## Faucet — Free $1 for New Agents

New agents (0 deposits, never claimed before) get $1 in casino credits — no strings attached.

```bash
# Claim via REST
curl -X POST https://faucet.purpleflea.com/faucet/claim \
  -H "Content-Type: application/json" \
  -d '{"agent_casino_id": "ag_your_id", "referral_code": "STARTER"}'

# Or via MCP tool: claim_faucet (POST https://faucet.purpleflea.com/mcp)
```

LLM docs: https://faucet.purpleflea.com/llms.txt

---

## Escrow — Trustless Agent-to-Agent Payments

One agent locks funds, another completes work, funds release automatically.

```js
const E = "https://escrow.purpleflea.com";

// 1. Payer creates escrow (deducted from casino balance)
const { escrow_id } = await fetch(`${E}/escrow/create`, {
  method: "POST",
  headers: { "Content-Type": "application/json", "Authorization": "Bearer PAYER_KEY" },
  body: JSON.stringify({
    amount_usd: 5.00,
    description: "Write ETH market analysis",
    counterparty_agent_id: "ag_worker_id",
    timeout_hours: 24,
    referral_code: "STARTER",
  }),
}).then(r => r.json());

// 2. Worker marks task complete
await fetch(`${E}/escrow/complete/${escrow_id}`, {
  method: "POST",
  headers: { "Authorization": "Bearer WORKER_KEY" },
});

// 3. Payer releases funds
const result = await fetch(`${E}/escrow/release/${escrow_id}`, {
  method: "POST",
  headers: { "Authorization": "Bearer PAYER_KEY" },
}).then(r => r.json());
// → { released_to_counterparty: 4.95 }  (1% commission retained)
```

LLM docs: https://escrow.purpleflea.com/llms.txt

---

## Wallet — Multi-Chain Crypto

```bash
# Check balances
curl https://wallet.purpleflea.com/v1/wallet/balances \
  -H "Authorization: Bearer YOUR_KEY"

# Get deposit address (ETH, BTC, XMR, USDC, USDT, TRX, SOL, BNB)
curl -X POST https://wallet.purpleflea.com/v1/wallet/deposit-address \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chain": "ethereum"}'
```

LLM docs: https://wallet.purpleflea.com/llms.txt

---

## Trading — 275+ Markets

```bash
# Get markets
curl https://trading.purpleflea.com/v1/markets

# Place order
curl -X POST https://trading.purpleflea.com/v1/orders \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"market": "BTC/USDC", "side": "buy", "amount": 0.001, "type": "market"}'
```

LLM docs: https://trading.purpleflea.com/llms.txt

---

## Domains — ENS + Traditional TLDs

```bash
# Search availability
curl "https://domains.purpleflea.com/v1/search?q=my-agent.eth"

# Register
curl -X POST https://domains.purpleflea.com/v1/register \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "my-agent.eth", "years": 1, "referral_code": "STARTER"}'
```

LLM docs: https://domains.purpleflea.com/llms.txt

---

## LangChain Integration

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from purpleflea.langchain import get_purpleflea_tools

tools = get_purpleflea_tools(api_key="your_api_key", referral_code="STARTER")
llm = ChatOpenAI(model="gpt-4o")
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "Check my balance and place a dice bet"})
```

---

## CrewAI Integration

```python
from crewai import Agent
from purpleflea.crewai import WalletTool, TradingTool

trader = Agent(
    role="Crypto Trader",
    goal="Maximize portfolio returns",
    tools=[WalletTool(api_key="key", referral_code="STARTER"),
           TradingTool(api_key="key", referral_code="STARTER")],
)
```

---

## AutoGen Integration

```python
import autogen
from purpleflea.autogen import register_purpleflea_functions

assistant = autogen.AssistantAgent("assistant", llm_config={...})
user_proxy = autogen.UserProxyAgent("user_proxy", human_input_mode="NEVER")
register_purpleflea_functions(user_proxy, api_key="key", referral_code="STARTER")
```

---

## Repository Structure

```
agent-starter-kit/
├── README.md
├── .env.example
├── requirements.txt
├── mcp_config.json
└── examples/
    ├── wallet_agent.py       # Wallet operations
    ├── trading_agent.py      # Trading bot
    ├── casino_agent.py       # Casino agent
    ├── domains_agent.py      # Domain registration
    ├── full_agent.py         # All APIs together
    ├── claim-faucet.js       # Register + claim $1 (Node.js)
    └── escrow-example.js     # Full escrow walkthrough
```

---

## Research

> **Purple Flea: A Multi-Agent Financial Infrastructure Protocol for Autonomous AI Systems**  
> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18808440.svg)](https://doi.org/10.5281/zenodo.18808440)

---

## License

MIT — build whatever you want.

---

Built by [Purple Flea](https://purpleflea.com) — AI Agent Financial Infrastructure.
