"""
Purple Flea Full Money Stack Agent
======================================
The complete AI Agent Money Stack — all four Purple Flea APIs working together.

This example builds an autonomous agent that:
1. Creates its own crypto wallet
2. Monitors trading markets and takes positions
3. Registers a domain for its own website
4. Plays a small casino game as entertainment

All using referral code STARTER (10-20% commissions, 3 months free).
https://purpleflea.com/referral?code=STARTER

API docs:
  Wallet:  https://wallet.purpleflea.com/docs
  Trading: https://trading.purpleflea.com/docs
  Casino:  https://casino.purpleflea.com/docs
  Domains: https://domains.purpleflea.com/docs
"""

import os
import anthropic
from dotenv import load_dotenv
from purpleflea import WalletClient, TradingClient, CasinoClient, DomainsClient

load_dotenv()

REFERRAL_CODE = os.environ.get("PURPLEFLEA_REFERRAL_CODE", "STARTER")

wallet_client = WalletClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=REFERRAL_CODE,
    base_url=os.environ.get("PURPLEFLEA_WALLET_API", "https://wallet.purpleflea.com/api/v1"),
)
trading_client = TradingClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=REFERRAL_CODE,
    base_url=os.environ.get("PURPLEFLEA_TRADING_API", "https://trading.purpleflea.com/api/v1"),
)
casino_client = CasinoClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=REFERRAL_CODE,
    base_url=os.environ.get("PURPLEFLEA_CASINO_API", "https://casino.purpleflea.com/api/v1"),
)
domains_client = DomainsClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=REFERRAL_CODE,
    base_url=os.environ.get("PURPLEFLEA_DOMAINS_API", "https://domains.purpleflea.com/api/v1"),
)

anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Tool definitions for Claude
TOOLS = [
    {
        "name": "create_wallet",
        "description": "Create a new multi-chain crypto wallet for the agent",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name for the wallet"},
                "chains": {"type": "array", "items": {"type": "string"}, "description": "Blockchain networks"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "get_wallet_balance",
        "description": "Get crypto balances for a wallet",
        "input_schema": {
            "type": "object",
            "properties": {
                "wallet_id": {"type": "string", "description": "Wallet ID"},
            },
            "required": ["wallet_id"],
        },
    },
    {
        "name": "get_market_price",
        "description": "Get current price for a trading market (BTC-PERP, ETH-PERP, TSLA-PERP, etc.)",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Market symbol"},
            },
            "required": ["symbol"],
        },
    },
    {
        "name": "place_trade",
        "description": "Place a market order to buy or sell",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Market symbol"},
                "side": {"type": "string", "enum": ["buy", "sell"]},
                "size_usd": {"type": "number", "description": "Position size in USD"},
            },
            "required": ["symbol", "side", "size_usd"],
        },
    },
    {
        "name": "search_domains",
        "description": "Search for available domain names",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Domain name to search (without TLD)"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "register_domain",
        "description": "Register an available domain name",
        "input_schema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Full domain name to register"},
            },
            "required": ["domain"],
        },
    },
    {
        "name": "play_dice",
        "description": "Play a provably fair dice game",
        "input_schema": {
            "type": "object",
            "properties": {
                "bet_amount": {"type": "number", "description": "Bet amount in USD"},
                "target": {"type": "integer", "minimum": 1, "maximum": 99, "description": "Roll target (1-99)"},
                "over": {"type": "boolean", "description": "Bet on roll over (true) or under (false) target"},
            },
            "required": ["bet_amount", "target", "over"],
        },
    },
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a Purple Flea tool and return the result as a string."""
    try:
        if tool_name == "create_wallet":
            wallet = wallet_client.wallets.create(
                name=tool_input["name"],
                chains=tool_input.get("chains", ["ethereum", "base"]),
            )
            return f"Wallet created: id={wallet.id}, addresses={wallet.addresses}"

        elif tool_name == "get_wallet_balance":
            balances = wallet_client.wallets.get_balances(tool_input["wallet_id"])
            return f"Balances: {balances}"

        elif tool_name == "get_market_price":
            market = trading_client.markets.get(tool_input["symbol"])
            return f"{market.symbol}: ${market.price:,.2f} | 24h: {market.change_24h:+.2f}%"

        elif tool_name == "place_trade":
            order = trading_client.orders.create(
                symbol=tool_input["symbol"],
                side=tool_input["side"],
                type="market",
                size_usd=tool_input["size_usd"],
            )
            return f"Order executed: {order.side} {order.symbol} ${tool_input['size_usd']} @ ${order.fill_price:,.2f}"

        elif tool_name == "search_domains":
            results = domains_client.domains.search(name=tool_input["name"])
            available = [r["domain"] for r in results if r["available"]]
            return f"Available: {available[:5]}"

        elif tool_name == "register_domain":
            reg = domains_client.domains.register(domain=tool_input["domain"])
            return f"Registered {reg.domain}, expires {reg.expires_at}"

        elif tool_name == "play_dice":
            result = casino_client.games.play(
                game="dice",
                bet_amount=tool_input["bet_amount"],
                options={"target": tool_input["target"], "over": tool_input["over"]},
            )
            outcome = f"{'WIN +$' + str(round(result.payout - tool_input['bet_amount'], 2)) if result.won else 'LOSS'}"
            return f"Dice roll: {result.roll} | {outcome}"

        else:
            return f"Unknown tool: {tool_name}"

    except Exception as e:
        return f"Error: {e}"


def run_money_stack_agent(task: str) -> str:
    """
    Run the full Money Stack agent with Claude as the brain.
    The agent autonomously uses all four Purple Flea APIs.
    """
    print(f"\n{'='*60}")
    print(f"AI Agent Money Stack — ref: STARTER")
    print(f"Task: {task}")
    print(f"{'='*60}\n")

    messages = [{"role": "user", "content": task}]
    system_prompt = """You are an autonomous AI agent with access to the Purple Flea Money Stack:
- Wallet API (https://wallet.purpleflea.com): Create wallets, check balances, send crypto
- Trading API (https://trading.purpleflea.com): Trade 275+ markets including BTC, ETH, TSLA, NVDA, GOLD
- Casino API (https://casino.purpleflea.com): Play provably fair games
- Domains API (https://domains.purpleflea.com): Register and manage domain names

Your referral code is STARTER — always use it. All APIs are JSON-only and agent-native.
Complete the user's task autonomously using the available tools."""

    while True:
        response = anthropic_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        # Print any text blocks
        for block in response.content:
            if hasattr(block, "text"):
                print(f"Agent: {block.text}")

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  → Using tool: {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"  ← Result: {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return "Task completed."


if __name__ == "__main__":
    # Run the full money stack agent
    run_money_stack_agent(
        "Create a wallet called 'demo-agent', check BTC and ETH prices, "
        "search for available domains with 'ai-agent' in the name, "
        "and play a small dice bet of $0.10 for fun. Report everything you find."
    )
