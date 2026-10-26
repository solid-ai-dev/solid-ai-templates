# Base — Deployment
[ID: base-deployment]

Deployment rules that hold on any target: certificates, load balancing,
service discovery, registries, secrets, and network assumptions. The
products and topology a team adopts belong in its own stack or platform
template.

## Deployment targets
[ID: base-deployment-targets]
[LOAD: generate-context]

- Declare each deployment target in the project's context file: cloud,
  hybrid, offline (air-gapped), or another the project names
- Note which configuration differs per target

## Certificates and PKI
[ID: base-deployment-certs]

- Automate certificate issuance and renewal — never rely on a manual expiry
  reminder alone
- Treat a certificate expiring without renewal as an incident
- Distribute every trusted root certificate through configuration
  management or the base image, never by hand
- Renew certificates and check revocation against endpoints the target can
  reach

## Load balancing and reverse proxy
[ID: base-deployment-lb]

- Route public ingress through a load balancer or reverse proxy that
  health-checks its backends; never make an instance directly
  internet-routable

## Service discovery and DNS
[ID: base-deployment-dns]

- Resolve services by DNS name or service discovery — never hardcode IPs
- Confirm every hostname a service needs resolves on its target before
  deployment
- Sync every node's clock from a time source the target can reach — clock
  skew breaks certificate validation and distributed systems

## Artifact registries
[ID: base-deployment-registries]
[LOAD: release]

- Sign every deployable artifact and scan it for vulnerabilities before
  promotion to production

## Secrets management
[ID: base-deployment-secrets]

- Inject secrets at runtime from a secrets service; never bake them into a
  deployable artifact
- Rotate secrets automatically; alert on rotation failures
- Authenticate services to the secrets service by platform identity — no
  static tokens in configuration files
- Keep the secrets service's recovery free of anything the target cannot
  reach
- Document a break-glass procedure for the secrets service

## Network assumptions
[ID: base-deployment-network]

- Route traffic that crosses a network boundary through a defined ingress
  or egress point
- Keep firewall rules in version control beside the service
- Make every required endpoint reachable before the service starts

### Recording network assumptions
[LOAD: generate-context]

- Document network assumptions in the project's context file: which
  segments reach the internet, and the internal endpoints a service needs
  (DNS, NTP, registry, CA, OCSP)
