# Base — Data Governance
[ID: base-data-governance]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for data classification, retention, privacy, and ownership.
Applies to any project that stores or processes user data, business
data, or regulated information.

## Data classification
[ID: data-governance-classification]

- Classify every data field into one of four tiers:
  - **Public** — safe to expose (product names, documentation)
  - **Internal** — business-sensitive, not for external use
    (internal metrics, cost data)
  - **Confidential** — restricted access (customer PII, financial
    records, API keys)
  - **Restricted** — highest sensitivity (passwords, payment card
    data, health records)
- Classification MUST be documented in the schema or data dictionary
- Access controls MUST match the classification tier — confidential
  and restricted data require role-based access

## PII handling
[ID: data-governance-pii]

- Identify all personally identifiable information (PII) fields
  in the schema — name, email, phone, address, IP, device IDs
- PII MUST be encrypted at rest and in transit
- Minimize PII collection — do not store what you do not need
- Provide a mechanism for data deletion (right to erasure) —
  hard delete or anonymize, never just soft-delete PII
- PII MUST NOT appear in application logs, error messages, or stack
  traces; the audit trail is a separate store, not a log
- Mask or redact PII in non-production environments

## Retention
[ID: data-governance-retention]

- Define a retention policy for each data category — document
  how long data is kept and when it is purged
- Retention periods MUST comply with applicable regulations
  (GDPR, CCPA, HIPAA, industry-specific)
- Implement automated purging — do not rely on manual cleanup
- Audit logs and backups are subject to retention policies too —
  do not retain backups indefinitely
- Document the purge mechanism: soft delete → hard delete after
  N days, or direct hard delete

## Data ownership
[ID: data-governance-ownership]

- Every data domain (users, orders, inventory) MUST have a
  designated owner — a team or individual accountable for quality,
  access, and lifecycle
- The data owner approves schema changes and access grants
- Cross-domain data access MUST go through defined interfaces
  (APIs, views) — not direct table access
- Document data ownership in the schema or data dictionary

## Audit trail
[ID: data-governance-audit]

- Changes to confidential and restricted data MUST be logged:
  who changed what, when, and the previous value
- Keep the audit trail in its own store, never in application logs,
  with access restricted to the tier of the data it records
- Audit logs MUST be append-only — never editable or deletable
  by application code
- Audit logs MUST be retained according to the retention policy
- Include the actor (user ID or service identity), timestamp,
  action (create, update, delete), and affected record
