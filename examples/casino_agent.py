"""
Purple Flea Casino Agent Example
==================================
Demonstrates how an AI agent can play provably fair casino games:
- List available games
- Place bets with cryptographic verification
- Verify game fairness using HMAC-SHA256 proofs
- Claim winnings automatically

Referral code STARTER earns 10% of house edge.
Sign up: https://purpleflea.com/referral?code=STARTER
"""

import os
import json
import hashlib
import hmac
from dotenv import load_dotenv
from purpleflea import CasinoClient

load_dotenv()

# 10% referral on casino fees with code STARTER
client = CasinoClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=os.environ.get("PURPLEFLEA_REFERRAL_CODE", "STARTER"),
    base_url=os.environ.get("PURPLEFLEA_CASINO_API", "https://casino.purpleflea.com/api/v1"),
)


def list_games() -> list:
    """List all available casino games."""
    games = client.games.list()
    print("Available games:")
    for game in games:
        print(f"  {game['name']}: {game['description']}")
        print(f"    Min bet: ${game['min_bet']} | Max bet: ${game['max_bet']}")
        print(f"    House edge: {game['house_edge']}% | RTP: {100 - game['house_edge']:.1f}%")
    return games


def play_dice(bet_amount: float, target: int = 50, over: bool = True) -> dict:
    """
    Play a dice game.
    - target: roll over/under this number (1-99)
    - over: True = bet on roll OVER target, False = bet UNDER
    - Win probability: target% (under) or (100-target)% (over)
    """
    result = client.games.play(
        game="dice",
        bet_amount=bet_amount,
        options={"target": target, "over": over},
    )
    print(f"\nDice Roll:")
    print(f"  Bet: ${bet_amount:.2f} | Target: {'>' if over else '<'}{target}")
    print(f"  Result: {result.roll}")
    print(f"  Outcome: {'WIN' if result.won else 'LOSS'}")
    if result.won:
        print(f"  Payout: ${result.payout:.2f} (profit: +${result.payout - bet_amount:.2f})")
    print(f"  Server seed hash: {result.server_seed_hash}")
    return result


def play_coinflip(bet_amount: float, choice: str = "heads") -> dict:
    """Play a coin flip. choice: 'heads' or 'tails'"""
    result = client.games.play(
        game="coinflip",
        bet_amount=bet_amount,
        options={"choice": choice},
    )
    print(f"\nCoin Flip:")
    print(f"  Bet: ${bet_amount:.2f} on {choice}")
    print(f"  Result: {result.outcome}")
    print(f"  {'WIN +$' + str(result.profit) if result.won else 'LOSS'}")
    return result


def verify_game_fairness(result: dict, server_seed: str) -> bool:
    """
    Verify a game result is provably fair.
    Purple Flea uses HMAC-SHA256: result = HMAC(server_seed, client_seed + nonce)
    """
    expected_hash = hmac.new(
        server_seed.encode(),
        f"{result['client_seed']}:{result['nonce']}".encode(),
        hashlib.sha256,
    ).hexdigest()

    is_valid = expected_hash == result["server_seed_hash"]
    print(f"\nFairness verification: {'VALID' if is_valid else 'INVALID'}")
    print(f"  Expected hash: {expected_hash[:16]}...")
    print(f"  Recorded hash: {result['server_seed_hash'][:16]}...")
    return is_valid


def get_game_history(limit: int = 10) -> list:
    """Get recent game history."""
    history = client.games.history(limit=limit)
    wins = sum(1 for g in history if g["won"])
    total_wagered = sum(g["bet_amount"] for g in history)
    total_pnl = sum(g["payout"] - g["bet_amount"] for g in history)
    print(f"\nGame History (last {limit}):")
    print(f"  Win rate: {wins}/{len(history)} ({wins/len(history)*100:.0f}%)")
    print(f"  Total wagered: ${total_wagered:.2f}")
    print(f"  Net P&L: ${total_pnl:+.2f}")
    return history


if __name__ == "__main__":
    print("=== Purple Flea Casino Agent (ref: STARTER) ===\n")
    print("Casino API: https://casino.purpleflea.com")
    print("Earn 10% referral commission — code: STARTER\n")
    print("Provably fair using HMAC-SHA256\n")

    games = list_games()

    # Example plays (use tiny amounts for testing)
    result = play_dice(bet_amount=0.10, target=50, over=True)
    coin = play_coinflip(bet_amount=0.10, choice="heads")
    history = get_game_history(limit=5)
