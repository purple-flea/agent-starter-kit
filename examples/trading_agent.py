"""
Purple Flea Trading Agent Example
===================================
Demonstrates how an AI agent can autonomously trade crypto:
- Query market prices for 275+ markets
- Place market and limit orders
- Manage open positions
- Set stop-loss and take-profit

Referral code STARTER earns 20% of trading fees.
Sign up: https://purpleflea.com/referral?code=STARTER
"""

import os
from dotenv import load_dotenv
from purpleflea import TradingClient

load_dotenv()

# 20% referral on all trading fees with code STARTER
client = TradingClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=os.environ.get("PURPLEFLEA_REFERRAL_CODE", "STARTER"),
    base_url=os.environ.get("PURPLEFLEA_TRADING_API", "https://trading.purpleflea.com/api/v1"),
)


def get_market_price(symbol: str) -> dict:
    """Get current price and 24h stats for a market."""
    market = client.markets.get(symbol)
    print(f"\n{symbol}:")
    print(f"  Price: ${market.price:,.2f}")
    print(f"  24h Change: {market.change_24h:+.2f}%")
    print(f"  24h Volume: ${market.volume_24h:,.0f}")
    print(f"  Funding Rate: {market.funding_rate:.4f}%")
    return market


def scan_opportunities(min_volume_usd: float = 1_000_000) -> list:
    """Scan all markets for high-volume opportunities."""
    markets = client.markets.list(min_volume=min_volume_usd)
    movers = sorted(markets, key=lambda m: abs(m["change_24h"]), reverse=True)[:10]
    print(f"\nTop 10 movers (>{min_volume_usd/1e6:.0f}M volume):")
    for m in movers:
        print(f"  {m['symbol']}: {m['change_24h']:+.1f}% | ${m['price']:,.2f} | Vol: ${m['volume_24h']/1e6:.1f}M")
    return movers


def place_market_order(
    symbol: str,
    side: str,  # "buy" or "sell"
    size_usd: float,
    leverage: int = 1,
) -> dict:
    """Place a market order for an asset."""
    order = client.orders.create(
        symbol=symbol,
        side=side,
        type="market",
        size_usd=size_usd,
        leverage=leverage,
    )
    print(f"\nOrder placed:")
    print(f"  Symbol: {order.symbol}")
    print(f"  Side: {order.side.upper()}")
    print(f"  Size: ${size_usd:.2f} at {leverage}x leverage")
    print(f"  Fill price: ${order.fill_price:,.2f}")
    print(f"  Order ID: {order.id}")
    return order


def place_limit_order(
    symbol: str,
    side: str,
    size_usd: float,
    limit_price: float,
    stop_loss: float = None,
    take_profit: float = None,
) -> dict:
    """Place a limit order with optional stop-loss and take-profit."""
    order = client.orders.create(
        symbol=symbol,
        side=side,
        type="limit",
        size_usd=size_usd,
        limit_price=limit_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
    )
    print(f"\nLimit order placed:")
    print(f"  {order.side.upper()} {order.symbol} @ ${limit_price:,.2f}")
    if stop_loss:
        print(f"  Stop-loss: ${stop_loss:,.2f}")
    if take_profit:
        print(f"  Take-profit: ${take_profit:,.2f}")
    print(f"  Order ID: {order.id}")
    return order


def get_portfolio() -> dict:
    """Get current open positions and P&L."""
    portfolio = client.portfolio.get()
    print(f"\nPortfolio Summary:")
    print(f"  Total Value: ${portfolio.total_value:,.2f}")
    print(f"  Unrealized P&L: ${portfolio.unrealized_pnl:+,.2f}")
    print(f"  Today's P&L: ${portfolio.daily_pnl:+,.2f}")
    print(f"\n  Open Positions:")
    for pos in portfolio.positions:
        print(f"    {pos['symbol']}: {pos['side']} ${pos['size_usd']:.0f} | PnL: ${pos['unrealized_pnl']:+.2f}")
    return portfolio


def close_position(position_id: str) -> dict:
    """Close an open position at market price."""
    result = client.positions.close(position_id)
    print(f"\nClosed position {position_id}")
    print(f"  Realized P&L: ${result.realized_pnl:+.2f}")
    return result


if __name__ == "__main__":
    print("=== Purple Flea Trading Agent (ref: STARTER) ===\n")
    print("Trading API: https://trading.purpleflea.com")
    print("Earn 20% referral commission — code: STARTER\n")
    print("275+ markets: BTC, ETH, SOL, TSLA, NVDA, GOLD, EUR/USD...\n")

    btc = get_market_price("BTC-PERP")
    eth = get_market_price("ETH-PERP")
    movers = scan_opportunities(min_volume_usd=10_000_000)
    portfolio = get_portfolio()

    # Example limit order (commented out to avoid accidental execution)
    # order = place_limit_order("BTC-PERP", "buy", 100.0, btc.price * 0.99, stop_loss=btc.price * 0.97)
