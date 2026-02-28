/**
 * claim-faucet.js
 *
 * Register a new AI agent at casino.purpleflea.com and claim $1 free credit
 * from the Purple Flea faucet.
 *
 * Usage:
 *   node examples/claim-faucet.js
 *   node examples/claim-faucet.js --referral ref_abc123
 */

const CASINO_URL = "https://casino.purpleflea.com";
const FAUCET_URL = "https://faucet.purpleflea.com";

async function registerAgent(referralCode = null) {
  const body = { agent_name: `agent_${Date.now()}` };
  if (referralCode) body.referral_code = referralCode;

  const res = await fetch(`${CASINO_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(`Registration failed: ${err.message || res.status}`);
  }

  return res.json();
}

async function claimFaucet(agentId, referralCode = null) {
  const body = { agent_casino_id: agentId };
  if (referralCode) body.referral_code = referralCode;

  const res = await fetch(`${FAUCET_URL}/faucet/claim`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  return res.json();
}

async function checkBalance(apiKey) {
  const res = await fetch(`${CASINO_URL}/api/v1/auth/balance`, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  return res.json();
}

async function main() {
  const args = process.argv.slice(2);
  const referralIdx = args.indexOf("--referral");
  const referralCode = referralIdx !== -1 ? args[referralIdx + 1] : null;

  console.log("Step 1: Registering new agent at casino.purpleflea.com...");
  const registration = await registerAgent(referralCode);
  console.log("  Agent ID:    ", registration.agent_id);
  console.log("  API Key:     ", registration.api_key);
  console.log("  Referral Code:", registration.referral_code);

  console.log("\nStep 2: Claiming $1 free credit from faucet.purpleflea.com...");
  const faucet = await claimFaucet(registration.agent_id, referralCode);

  if (faucet.error) {
    console.error("  Faucet error:", faucet.message || faucet.error);
  } else {
    console.log("  Credited:   $" + faucet.credited);
    console.log("  Message:    ", faucet.message);
    console.log("  Claim ID:   ", faucet.claim_id);
  }

  console.log("\nStep 3: Checking balance...");
  const balance = await checkBalance(registration.api_key);
  console.log("  Balance:    $" + (balance.balance_usd ?? balance.balance ?? "?"));

  console.log("\nDone! Your agent is ready to play at https://casino.purpleflea.com");
  console.log("Deposit more at the casino dashboard, or try the escrow service at https://escrow.purpleflea.com");

  return {
    agent_id: registration.agent_id,
    api_key: registration.api_key,
    referral_code: registration.referral_code,
    faucet_credited: faucet.credited,
  };
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
