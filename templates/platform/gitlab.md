# Platform — GitLab
[ID: platform-gitlab]
[DEPENDS ON: templates/core/quality-gates.md]

GitLab-specific CI and security integration. Maps quality gate categories
to GitLab CI/CD pipelines and GitLab-native features.

---

## CI
[ID: platform-gitlab-ci]

- Pipeline definitions: `.gitlab-ci.yml`
- Trigger: merge request pipelines for validation, branch pipelines for main
- Reusable configuration via `include:` and `extends:`

---

## SAST
[ID: platform-gitlab-sast]

- **Semgrep OSS** — open-source, free for all repositories
- Runs as `semgrep ci` in a pipeline job
- Supports: JavaScript, TypeScript, Python, Go, Java, C/C++, Ruby, and more
- Community rules cover OWASP Top 10 and language-specific patterns
- Stack-specific SAST supplements (Bandit, govulncheck) run as pipeline jobs
- GitLab Ultimate includes built-in SAST, but Semgrep OSS avoids the
  tier dependency

---

## Secret detection
[ID: platform-gitlab-secrets]

- **gitleaks** — `gitleaks detect` in a pipeline job
- GitLab Ultimate includes native secret detection, but gitleaks avoids
  the tier dependency
- MUST run on every merge request pipeline

---

## Quality gate integration
[ID: platform-gitlab-gates]

| Category | Tool / Integration |
|----------|--------------------|
| SAST | Semgrep OSS (pipeline job) |
| SAST (Python) | + Bandit (pipeline job) |
| SAST (Go) | + govulncheck (pipeline job) |
| Secret detection | gitleaks (pipeline job) |
| Site quality | `@lhci/cli` (pipeline job) |
| Link checking | lychee CLI (pipeline job) |
| All lint/format/type/test | Language-specific CLI in pipeline jobs |
