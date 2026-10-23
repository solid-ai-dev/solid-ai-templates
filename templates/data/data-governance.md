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
- Document the classification in the schema or data dictionary (MUST)
- Match access controls to the classification tier (MUST)
- Require role-based access for confidential and restricted data

## PII handling
[ID: data-governance-pii]

- Identify all personally identifiable information (PII) fields
  in the schema — name, email, phone, address, IP, device IDs
- Encrypt PII at rest and in transit (MUST)
- Minimize PII collection — do not store what you do not need
- Provide a mechanism for data deletion (right to erasure) —
  hard delete or anonymize, never just soft-delete PII
- Never put PII in application logs, error messages, or stack traces
  (MUST NOT); the audit trail is a separate store, not a log
- Keep the client IP, the one PII field a security log may hold, in that
  log alone, access-restricted and purged when its retention ends
- Mask or redact PII in non-production environments

## Retention
[ID: data-governance-retention]

- Define a retention policy for each data category — document
  how long data is kept and when it is purged
- Comply with applicable regulations (GDPR, CCPA, HIPAA,
  industry-specific) in every retention period (MUST)
- Implement automated purging — do not rely on manual cleanup
- Apply retention policies to audit logs and backups too
- Never retain backups indefinitely
- Document the purge mechanism: soft delete → hard delete after
  N days, or direct hard delete

## Data ownership
[ID: data-governance-ownership]

- Designate an owner for every data domain (users, orders, inventory)
  (MUST) — a team or individual accountable for quality, access, and
  lifecycle
- Have the data owner approve schema changes and access grants
- Route cross-domain data access through defined interfaces (APIs,
  views), not direct table access (MUST)
- Document data ownership in the schema or data dictionary

## Audit trail
[ID: data-governance-audit]

- Log every change to confidential and restricted data (MUST):
  who changed what, when, and the previous value
- Keep the audit trail in its own store, never in application logs,
  with access restricted to the tier of the data it records
- Make audit logs append-only (MUST); never let application code edit
  or delete them
- Retain audit logs according to the retention policy (MUST)
- Include the actor (user ID or service identity), timestamp,
  action (create, update, delete), and affected record
