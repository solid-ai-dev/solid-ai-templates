# Base — Deployment
[ID: base-deployment]

Cross-cutting deployment rules. Covers deployment targets, certificates, load
balancing, service discovery, registries, secrets, and network assumptions.
Applies to every service regardless of language or framework.

---

## Deployment targets
[ID: base-deployment-targets]

Declare the deployment target explicitly in every project's context file.
All other rules in this document are qualified by target.

| Target | Description |
|--------|-------------|
| `cloud` | Public cloud (AWS, GCP, Azure) — managed services, external CA, public DNS |
| `hybrid` | On-premises + cloud — private CA for internal traffic, public CA for external |
| `offline` | Air-gapped — no internet access; all dependencies pre-mirrored internally |

A project may support more than one target. List all that apply and note
which sections of configuration differ per target.

---

## Certificates and PKI
[ID: base-deployment-certs]

**Cloud**
- Use a managed CA: AWS ACM, GCP Certificate Manager, or Let's Encrypt via
  ACME — do not manage certificates manually
- Automate renewal — never set a manual expiry reminder as the sole safeguard
- Terminate TLS at the load balancer or ingress; internal service-to-service
  traffic may use mTLS via a service mesh

**Hybrid**
- Run an internal CA (Smallstep `step-ca`, HashiCorp Vault PKI, or CFSSL)
  for all internal services
- Use a public CA (Let's Encrypt, ACM) for externally reachable endpoints only
- Distribute the internal root CA cert to all nodes via configuration
  management — never distribute it manually
- Automate internal certificate rotation; treat certificates expiring without
  renewal as an incident

**Offline**
- Internal CA is the only CA — no ACME against public endpoints
- Run an internal ACME server (Smallstep `step-ca` supports this) so services
  can renew certificates automatically without internet access
- Pre-distribute the root CA cert in the base OS image or via configuration
  management before first deployment
- Certificate revocation via internal CRL or OCSP responder — no external OCSP

---

## Load balancing and reverse proxy
[ID: base-deployment-lb]

**Cloud**
- Use the cloud provider's managed load balancer (AWS ALB/NLB, GCP Load
  Balancing, Azure Application Gateway)
- Prefer application-layer (L7) load balancing for HTTP services — enables
  path-based routing, header inspection, and health checks
- Do not run a self-managed reverse proxy in front of a managed LB unless
  there is a specific requirement (e.g. custom WAF rules)

**Hybrid**
- External traffic: managed cloud LB or hardware appliance (F5, Citrix ADC)
  at the network boundary
- Internal traffic: software reverse proxy (NGINX, HAProxy, Traefik) or
  service mesh (Istio, Linkerd) for east-west routing
- Ensure the internal LB is aware of both on-prem and cloud service endpoints

**Offline**
- Software load balancer only: HAProxy, NGINX, or Traefik — all run fully
  offline with static or service-discovery-driven configuration
- Hardware appliances: F5 BIG-IP, Citrix ADC — common in government and
  defence networks; configure via local management plane, not cloud APIs
- Kubernetes bare-metal: use MetalLB for `LoadBalancer` service type;
  configure address pools from the local IP range

---

## Service discovery and DNS
[ID: base-deployment-dns]

**Cloud**
- Use the cloud provider's DNS service (Route 53, Cloud DNS, Azure DNS)
- Use cloud-native service discovery where available (AWS Cloud Map,
  Kubernetes CoreDNS)
- Services should resolve each other by DNS name — never hardcode IPs

**Hybrid**
- Internal DNS: BIND or CoreDNS — authoritative for all internal zones
- Split-horizon DNS: internal zones resolve to private IPs; public zones
  resolve to public IPs
- Dynamic service registration: Consul or etcd, integrated with DNS via
  Consul DNS or CoreDNS plugins

**Offline**
- Internal DNS is the only DNS — no public resolver fallback
- All hostnames must resolve within the internal DNS zone before deployment
- Dynamic service discovery: Consul or etcd running on internal infrastructure
- NTP: sync all nodes from an internal time server — clock skew causes
  certificate validation failures and distributed system bugs

---

## Container and artifact registries
[ID: base-deployment-registries]

**Cloud**
- Use a managed registry: AWS ECR, GCP Artifact Registry, GitHub Container
  Registry, or Docker Hub (private)
- Enforce image signing and scan all images for vulnerabilities before
  promotion to production

**Hybrid**
- Internal registry (Harbor, JFrog Artifactory, Sonatype Nexus) proxies and
  caches images from public registries
- Air-gapped segments pull from the internal registry only — no direct
  internet access from those segments
- Mirror required base images and dependencies into the internal registry
  as part of the build pipeline

**Offline**
- All images and packages must be mirrored before the system is air-gapped:
  - Container images → Harbor, Artifactory, or Nexus
  - Go modules → Athens module proxy
  - Python packages → devpi or Artifactory PyPI proxy
  - npm packages → Verdaccio or Artifactory npm proxy
- Set `GOPROXY`, `PIP_INDEX_URL`, and `.npmrc` to point to internal mirrors
  in all build environments
- Scan and approve all dependencies at the boundary before mirroring —
  treat the mirror as a trusted internal supply chain artefact

---

## Secrets management
[ID: base-deployment-secrets]

**Cloud**
- Use the cloud provider's secrets service (AWS Secrets Manager, GCP Secret
  Manager, Azure Key Vault) or HashiCorp Vault with a cloud backend
- Never pass secrets as environment variables baked into images — inject at
  runtime via the secrets service or a Kubernetes `Secret` mounted as a volume
- Rotate secrets automatically; alert on rotation failures

**Hybrid**
- HashiCorp Vault with a replicated backend spanning on-prem and cloud, or
  separate Vault clusters with cross-cluster replication
- Services authenticate to Vault using platform identity (IAM role, K8s
  service account) — no static Vault tokens in configuration files

**Offline**
- HashiCorp Vault (runs fully offline), CyberArk, or a hardware HSM
- Vault unsealing must not depend on an external KMS — use Shamir secret
  sharing with a defined key custodian process, or an internal HSM for
  auto-unseal
- Establish a documented break-glass procedure for Vault recovery

---

## Network assumptions
[ID: base-deployment-network]

Document network assumptions explicitly in the project context file.
Do not rely on implicit network access that may not exist in all targets.

**Cloud**
- Outbound internet access available unless restricted by VPC policy
- Public ingress via load balancer; services are not directly internet-routable
- Assume DNS, NTP, and package registries are reachable

**Hybrid**
- Define which network segments have internet access and which do not
- Services crossing the boundary must go through a defined ingress/egress point
- Firewall rules must be documented and version-controlled alongside the service

**Offline**
- No outbound internet access — any code that calls an external URL will fail
- Audit all dependencies for hidden external calls (telemetry, update checks,
  licence validation) — disable or patch before deployment
- All required endpoints (DNS, NTP, registry, CA, OCSP) must be reachable
  within the internal network before the service starts
- Document the full list of required internal endpoints in the project README