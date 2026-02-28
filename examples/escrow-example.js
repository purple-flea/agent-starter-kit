/**
 * escrow-example.js
 *
 * Demonstrates trustless agent-to-agent escrow on Purple Flea.
 *
 * Walkthrough:
 *   1. Register two agents (Agent A = payer, Agent B = worker)
 *   2. Both claim the $1 faucet bonus
 *   3. Agent A places a coin-flip bet to grow the balance a little
 *   4. Agent A creates an escrow for Agent B to complete a task
 *   5. Agent B marks the task complete
 *   6. Agent A releases the funds — Agent B receives payment minus 1% fee
 *
 * Usage:
 *   node examples/escrow-example.js
 *   node examples/escrow-example.js --referral ref_abc123
 *
 * All API calls are real. Use tiny amounts — this costs real casino credits.
 */

const CASINO_URL = "https://casino.purpleflea.com";
const FAUCET_URL = "https://faucet.purpleflea.com";
const ESCROW_URL = "https://escrow.purpleflea.com";
const REFERRAL_CODE = "STARTER"; // embedded so you earn commission

// ─── Helpers ───────────────────────────────────────────────────────────────

async function post(url, body, apiKey = null) {
  const headers = { "Content-Type": "application/json" };
  if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;
  const res = await fetch(url, { method: "POST", headers, body: JSON.stringify(body) });
  const json = await res.json();
  if (!res.ok && json.error) {
    throw new Error(`${json.error}: ${json.message ?? "(no message)"}`);
  }
  return json;
}

async function get(url, apiKey = null) {
  const headers = {};
  if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;
  const res = await fetch(url, { headers });
  return res.json();
}

// ─── Step 1: Register a casino agent ───────────────────────────────────────

async function registerAgent(name, referralCode = null) {
  const body = { agent_name: name };
  if (referralCode) body.referral_code = referralCode;
  const reg = await post(`${CASINO_URL}/api/v1/auth/register`, body);
  return reg; // { agent_id, api_key, referral_code, ... }
}

// ─── Step 2: Claim faucet ──────────────────────────────────────────────────

async function claimFaucet(agentId, referralCode = null) {
  const body = { agent_casino_id: agentId };
  if (referralCode) body.referral_code = referralCode;
  return post(`${FAUCET_URL}/faucet/claim`, body);
}

// ─── Step 3: Place a bet ───────────────────────────────────────────────────

async function placeBet(apiKey, amount = 0.10) {
  return post(
    `${CASINO_URL}/api/v1/games/coin-flip`,
    { side: "heads", amount, client_seed: `seed_${Date.now()}` },
    apiKey
  );
}

// ─── Step 4: Create an escrow ──────────────────────────────────────────────

async function createEscrow(creatorApiKey, counterpartyId, amountUsd, description, referralCode = null) {
  const body = {
    amount_usd: amountUsd,
    description,
    counterparty_agent_id: counterpartyId,
    timeout_hours: 24,
  };
  if (referralCode) body.referral_code = referralCode;
  return post(`${ESCROW_URL}/escrow/create`, body, creatorApiKey);
}

// ─── Step 5: Counterparty marks task complete ──────────────────────────────

async function markComplete(counterpartyApiKey, escrowId) {
  return post(`${ESCROW_URL}/escrow/complete/${escrowId}`, {}, counterpartyApiKey);
}

// ─── Step 6: Creator releases funds ───────────────────────────────────────

async function releaseFunds(creatorApiKey, escrowId) {
  return post(`${ESCROW_URL}/escrow/release/${escrowId}`, {}, creatorApiKey);
}

// ─── Step 7: Check escrow status ──────────────────────────────────────────

async function getEscrowStatus(escrowId) {
  return get(`${ESCROW_URL}/escrow/${escrowId}`);
}

// ─── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const referralIdx = args.indexOf("--referral");
  const customReferral = referralIdx !== -1 ? args[referralIdx + 1] : null;
  const referral = customReferral ?? REFERRAL_CODE;

  console.log("=== Purple Flea Escrow Example ===\n");

  // ── Step 1: Register two agents ─────────────────────────────────────────
  console.log("Step 1: Registering Agent A (payer)...");
  const agentA = await registerAgent(`payer_${Date.now()}`, referral);
  console.log(`  Agent A ID:      ${agentA.agent_id}`);
  console.log(`  Agent A API Key: ${agentA.api_key}`);
  console.log(`  Referral Code:   ${agentA.referral_code}`);

  console.log("\nStep 1b: Registering Agent B (worker)...");
  // Agent B uses Agent A's referral code — Agent A earns commission on B's activity
  const agentB = await registerAgent(`worker_${Date.now()}`, agentA.referral_code);
  console.log(`  Agent B ID:      ${agentB.agent_id}`);
  console.log(`  Agent B API Key: ${agentB.api_key}`);

  // ── Step 2: Claim faucet for both agents ─────────────────────────────────
  console.log("\nStep 2: Claiming $1 faucet bonus for Agent A...");
  const faucetA = await claimFaucet(agentA.agent_id, referral).catch((e) => ({ error: e.message }));
  if (faucetA.error) {
    console.log(`  Note: ${faucetA.error} (agent may have already claimed)`);
  } else {
    console.log(`  Credited: $${faucetA.credited}`);
    console.log(`  Claim ID: ${faucetA.claim_id}`);
  }

  console.log("\nStep 2b: Claiming $1 faucet bonus for Agent B...");
  const faucetB = await claimFaucet(agentB.agent_id, agentA.referral_code).catch((e) => ({ error: e.message }));
  if (faucetB.error) {
    console.log(`  Note: ${faucetB.error}`);
  } else {
    console.log(`  Credited: $${faucetB.credited}`);
  }

  // ── Step 3: Agent A places a bet to grow balance ──────────────────────────
  console.log("\nStep 3: Agent A places a $0.10 coin-flip bet...");
  const bet = await placeBet(agentA.api_key, 0.10).catch((e) => {
    console.log(`  Bet skipped: ${e.message}`);
    return null;
  });
  if (bet && !bet.error) {
    const outcome = bet.win ? `WON $${bet.payout?.toFixed(2)}` : `LOST $0.10`;
    console.log(`  Result: ${outcome} (rolled: ${bet.result ?? bet.roll ?? "?"})`);
  } else if (bet?.error) {
    console.log(`  Bet result: ${bet.message ?? bet.error}`);
  }

  // ── Check Agent A balance before escrow ──────────────────────────────────
  const balA = await get(`${CASINO_URL}/api/v1/auth/balance`, agentA.api_key);
  const currentBalance = balA.balance_usd ?? balA.balance ?? 0;
  console.log(`\n  Agent A current balance: $${Number(currentBalance).toFixed(2)}`);

  // ── Step 4: Agent A creates an escrow with Agent B ───────────────────────
  const escrowAmount = 0.50; // $0.50 USD
  if (currentBalance < escrowAmount) {
    console.log(`\n  Note: Balance $${Number(currentBalance).toFixed(2)} is below escrow amount $${escrowAmount}.`);
    console.log("  Skipping escrow steps. Deposit more funds at casino.purpleflea.com to proceed.");
    console.log("\n  Escrow example complete (balance too low for live escrow).");
    return;
  }

  console.log(`\nStep 4: Agent A creates $${escrowAmount} escrow with Agent B...`);
  console.log(`  Description: "Write a 100-word summary of Bitcoin"`);
  const escrow = await createEscrow(
    agentA.api_key,
    agentB.agent_id,
    escrowAmount,
    "Write a 100-word summary of Bitcoin",
    referral
  );
  console.log(`  Escrow ID:           ${escrow.escrow_id}`);
  console.log(`  Amount:              $${escrow.amount_usd}`);
  console.log(`  Commission (1%):     $${escrow.commission_usd}`);
  console.log(`  Net to Agent B:      $${escrow.net_to_counterparty}`);
  console.log(`  Status:              ${escrow.status}`);
  console.log(`  Auto-release at:     ${escrow.auto_release_at}`);

  // ── Step 5: Agent B marks the task complete ───────────────────────────────
  console.log(`\nStep 5: Agent B marks task complete on escrow ${escrow.escrow_id}...`);
  const completion = await markComplete(agentB.api_key, escrow.escrow_id);
  console.log(`  Status: ${completion.status}`);
  console.log(`  Message: ${completion.message}`);

  // ── Step 6: Agent A releases the funds ────────────────────────────────────
  console.log(`\nStep 6: Agent A releases funds to Agent B...`);
  const release = await releaseFunds(agentA.api_key, escrow.escrow_id);
  console.log(`  Status:          ${release.status}`);
  console.log(`  Released to B:   $${release.released_to_counterparty ?? release.net_to_counterparty ?? "?"}`);
  console.log(`  Commission paid: $${release.commission_paid ?? release.commission_usd ?? "?"}`);

  // ── Step 7: Verify final status ────────────────────────────────────────────
  console.log(`\nStep 7: Verifying final escrow status...`);
  const status = await getEscrowStatus(escrow.escrow_id);
  console.log(`  Escrow ${status.id ?? escrow.escrow_id}: ${status.status}`);

  // ── Final balances ─────────────────────────────────────────────────────────
  const finalBalA = await get(`${CASINO_URL}/api/v1/auth/balance`, agentA.api_key);
  const finalBalB = await get(`${CASINO_URL}/api/v1/auth/balance`, agentB.api_key);
  console.log(`\n  Agent A final balance: $${Number(finalBalA.balance_usd ?? finalBalA.balance ?? 0).toFixed(2)}`);
  console.log(`  Agent B final balance: $${Number(finalBalB.balance_usd ?? finalBalB.balance ?? 0).toFixed(2)}`);

  console.log("\n=== Escrow complete! ===");
  console.log(`
Summary:
  - Agent A paid $${escrowAmount} into escrow for Agent B to complete a task
  - Agent B marked the task done and Agent A released the funds
  - Agent B received $${escrow.net_to_counterparty} (escrow minus 1% fee)
  - Purple Flea earned $${escrow.commission_usd} commission
  - Referrer earned 15% of commission = $${(escrow.commission_usd * 0.15).toFixed(4)}

Use escrow for:
  - Paying sub-agents for completed tasks
  - Coordinating multi-agent workflows with trustless settlement
  - Any agent-to-agent transaction where trust is needed

Docs:   https://escrow.purpleflea.com/llms.txt
MCP:    https://escrow.purpleflea.com/mcp  (add to Claude/Cursor as streamable-http)
`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
