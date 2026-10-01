"""
Preset contract configurations for quick drafting and testing in LegalEase.
"""

PRESETS = {
    "Custom (Blank)": {
        "doc_type": "Mutual Non-Disclosure Agreement (NDA)",
        "jurisdiction": "State of Delaware, United States",
        "party1_name": "",
        "party1_role": "Disclosing Party",
        "party2_name": "",
        "party2_role": "Receiving Party",
        "duration": "2 years from Effective Date",
        "payment_terms": "N/A (Mutual exchange of proprietary information)",
        "bias": "Balanced & Mutual",
        "custom_clauses": ""
    },
    "🤝 Mutual NDA (Tech Startup & Partner)": {
        "doc_type": "Mutual Non-Disclosure Agreement (NDA)",
        "jurisdiction": "State of Delaware, United States",
        "party1_name": "Apex Cloud Systems Inc.",
        "party1_role": "Disclosing & Receiving Party",
        "party2_name": "NexGen AI Labs LLC",
        "party2_role": "Disclosing & Receiving Party",
        "duration": "3 years from Effective Date",
        "payment_terms": "Mutual consideration of evaluating potential commercial partnership",
        "bias": "Balanced & Mutual",
        "custom_clauses": "Standard carve-outs for publicly known information. Mandatory return or certified destruction of confidential information within 14 days of written notice. Expedited injunctive relief without requirement to post bond."
    },
    "💻 Independent Software Developer Agreement": {
        "doc_type": "Independent Contractor Agreement",
        "jurisdiction": "State of California, United States",
        "party1_name": "VentureFlow Studios Inc.",
        "party1_role": "Client / Company",
        "party2_name": "Alex Chen",
        "party2_role": "Contractor / Full-Stack Engineer",
        "duration": "6 months (renewable upon written agreement)",
        "payment_terms": "$85.00 USD per hour, invoiced bi-weekly, net 15 payment terms",
        "bias": "Favorable to Party 1 (Client)",
        "custom_clauses": "Complete work-for-hire intellectual property assignment. Contractor retains pre-existing tools and open-source libraries. Non-solicitation of company employees for 12 months post-termination. 14 days notice for termination without cause."
    },
    "🏢 Commercial Office Lease Agreement": {
        "doc_type": "Commercial Lease Agreement",
        "jurisdiction": "State of New York, United States",
        "party1_name": "Hudson Commercial Properties REIT",
        "party1_role": "Landlord",
        "party2_name": "Beacon Media Group LLC",
        "party2_role": "Tenant",
        "duration": "36 months commencing on the Effective Date",
        "payment_terms": "$6,500.00 USD per month payable on the 1st of each calendar month, with a $13,000 security deposit",
        "bias": "Balanced & Mutual",
        "custom_clauses": "Tenant responsible for interior non-structural maintenance and electrical utilities. Landlord maintains exterior envelope and HVAC. 60 days advance written notice required prior to lease expiration for renewal option."
    },
    "🌐 Website Terms of Service & Privacy Policy": {
        "doc_type": "Website Terms of Service & Privacy Policy",
        "jurisdiction": "State of California, United States (with GDPR & CCPA compliance)",
        "party1_name": "CloudSync Platform Inc.",
        "party1_role": "Platform Operator / Service Provider",
        "party2_name": "End User / Registered Account Holder",
        "party2_role": "User / Customer",
        "duration": "Perpetual until account termination by either party",
        "payment_terms": "Tiered monthly subscription fees billed automatically via Stripe",
        "bias": "Favorable to Party 1 (Company)",
        "custom_clauses": "Mandatory individual binding arbitration with class action waiver. Liability capped at the total amount paid by user in preceding 12 months. CCPA and GDPR data subject request compliance."
    }
}
