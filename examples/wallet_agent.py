"""
Purple Flea Wallet Agent Example
=================================
Demonstrates how an AI agent can autonomously manage crypto wallets:
- Create a new multi-chain wallet
- Check balances across chains
- Send transactions
- List transaction history

Referral code STARTER is embedded — earn 10% of transaction fees.
Sign up: https://purpleflea.com/referral?code=STARTER
"""

import os
from dotenv import load_dotenv
from purpleflea import WalletClient

load_dotenv()

# Initialize the client — referral code STARTER earns you 10% of fees
client = WalletClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=os.environ.get("PURPLEFLEA_REFERRAL_CODE", "STARTER"),
    base_url=os.environ.get("PURPLEFLEA_WALLET_API", "https://wallet.purpleflea.com/api/v1"),
)


def create_agent_wallet(agent_name: str, chains: list[str] = None) -> dict:
    """Create a new multi-chain wallet for an AI agent."""
    if chains is None:
        chains = ["ethereum", "base", "solana", "bitcoin"]

    wallet = client.wallets.create(
        name=f"agent-{agent_name}",
        chains=chains,
        metadata={"agent": agent_name, "starter_kit": True}
    )
    print(f"Created wallet for agent '{agent_name}':")
    for chain, address in wallet.addresses.items():
        print(f"  {chain}: {address}")
    return wallet


def check_balances(wallet_id: str) -> dict:
    """Get token balances across all chains."""
    balances = client.wallets.get_balances(wallet_id)
    print(f"\nBalances for wallet {wallet_id}:")
    for chain, tokens in balances.items():
        for token in tokens:
            if float(token["balance"]) > 0:
                print(f"  {chain} {token['symbol']}: {token['balance']} (${token['usd_value']:.2f})")
    return balances


def send_payment(wallet_id: str, to_address: str, amount: str, token: str = "USDC", chain: str = "base") -> dict:
    """Send a crypto payment autonomously."""
    tx = client.wallets.send(
        wallet_id=wallet_id,
        to=to_address,
        amount=amount,
        token=token,
        chain=chain,
    )
    print(f"\nTransaction submitted:")
    print(f"  Hash: {tx.hash}")
    print(f"  Status: {tx.status}")
    print(f"  Explorer: {tx.explorer_url}")
    return tx


def get_transaction_history(wallet_id: str, limit: int = 10) -> list:
    """Retrieve recent transaction history."""
    txns = client.wallets.list_transactions(wallet_id, limit=limit)
    print(f"\nRecent transactions (last {limit}):")
    for tx in txns:
        print(f"  {tx['timestamp']} | {tx['type']} | {tx['amount']} {tx['token']} | {tx['status']}")
    return txns


if __name__ == "__main__":
    print("=== Purple Flea Wallet Agent (ref: STARTER) ===\n")
    print("Wallet API: https://wallet.purpleflea.com")
    print("Earn 10% referral commission — code: STARTER\n")

    # Example usage (would use real wallet IDs in production)
    wallet = create_agent_wallet("my-first-agent")
    balances = check_balances(wallet.id)

    # Example send (commented out to avoid accidental transactions)
    # tx = send_payment(wallet.id, "0xRecipientAddress", "1.00", "USDC", "base")
