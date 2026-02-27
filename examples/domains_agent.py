"""
Purple Flea Domains Agent Example
====================================
Demonstrates how an AI agent can autonomously register and manage domains:
- Search domain availability
- Register domains
- Configure DNS records
- List and manage owned domains

Referral code STARTER earns 15% of registration fees.
Sign up: https://purpleflea.com/referral?code=STARTER
"""

import os
from dotenv import load_dotenv
from purpleflea import DomainsClient

load_dotenv()

# 15% referral on domain registrations with code STARTER
client = DomainsClient(
    api_key=os.environ["PURPLEFLEA_API_KEY"],
    referral_code=os.environ.get("PURPLEFLEA_REFERRAL_CODE", "STARTER"),
    base_url=os.environ.get("PURPLEFLEA_DOMAINS_API", "https://domains.purpleflea.com/api/v1"),
)


def search_domains(name: str, tlds: list[str] = None) -> list:
    """Search domain availability across multiple TLDs."""
    if tlds is None:
        tlds = [".com", ".io", ".ai", ".xyz", ".org", ".net"]

    results = client.domains.search(name=name, tlds=tlds)
    print(f"\nDomain search for '{name}':")
    for result in results:
        status = "AVAILABLE" if result["available"] else "taken"
        price = f"${result['price']:.2f}/yr" if result["available"] else ""
        print(f"  {result['domain']}: {status} {price}")
    available = [r for r in results if r["available"]]
    return available


def register_domain(
    domain: str,
    years: int = 1,
    auto_renew: bool = True,
    privacy: bool = True,
) -> dict:
    """Register a domain name."""
    registration = client.domains.register(
        domain=domain,
        years=years,
        auto_renew=auto_renew,
        whois_privacy=privacy,
    )
    print(f"\nDomain registered:")
    print(f"  Domain: {registration.domain}")
    print(f"  Expires: {registration.expires_at}")
    print(f"  Auto-renew: {registration.auto_renew}")
    print(f"  Nameservers: {', '.join(registration.nameservers)}")
    return registration


def set_dns_records(domain: str, records: list[dict]) -> dict:
    """Configure DNS records for a domain."""
    result = client.dns.set_records(domain=domain, records=records)
    print(f"\nDNS records updated for {domain}:")
    for record in records:
        print(f"  {record['type']} {record['name']} → {record['value']}")
    return result


def point_to_server(domain: str, ip_address: str) -> dict:
    """Point a domain to a server IP address."""
    return set_dns_records(domain, [
        {"type": "A", "name": "@", "value": ip_address, "ttl": 300},
        {"type": "A", "name": "www", "value": ip_address, "ttl": 300},
    ])


def list_owned_domains() -> list:
    """List all domains owned by this agent."""
    domains = client.domains.list()
    print(f"\nOwned domains ({len(domains)} total):")
    for domain in domains:
        days_left = domain["days_until_expiry"]
        status = "EXPIRING SOON" if days_left < 30 else "active"
        print(f"  {domain['domain']}: expires in {days_left} days [{status}]")
    return domains


def renew_expiring_domains(days_threshold: int = 30) -> list:
    """Auto-renew domains expiring within threshold."""
    domains = list_owned_domains()
    renewed = []
    for domain in domains:
        if domain["days_until_expiry"] < days_threshold:
            result = client.domains.renew(domain["domain"], years=1)
            print(f"  Renewed {domain['domain']} for 1 year")
            renewed.append(result)
    return renewed


if __name__ == "__main__":
    print("=== Purple Flea Domains Agent (ref: STARTER) ===\n")
    print("Domains API: https://domains.purpleflea.com")
    print("Earn 15% referral commission — code: STARTER\n")

    # Search for domain availability
    available = search_domains("my-ai-agent", tlds=[".com", ".io", ".ai"])

    # List owned domains
    owned = list_owned_domains()

    # Auto-renew anything expiring soon
    if owned:
        renewed = renew_expiring_domains(days_threshold=30)

    # Example: register the first available domain (commented out)
    # if available:
    #     reg = register_domain(available[0]["domain"])
    #     point_to_server(reg.domain, "1.2.3.4")
