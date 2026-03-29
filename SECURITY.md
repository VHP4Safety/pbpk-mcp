# Security Policy

## Reporting A Vulnerability

Please do not open a public issue with exploit details for authentication, authorization, audit, or runtime-integrity vulnerabilities.

Prefer one of these routes:

1. GitHub private vulnerability reporting or a GitHub security advisory, if enabled for this repository.
2. Direct contact through the repository owner or organization contact on GitHub if private reporting is unavailable.

Include:

- affected version or commit
- deployment mode
- reproduction steps
- expected impact
- any logs with secrets and identifiers removed

## Response Expectations

PBPK MCP is a scientific infrastructure project, so issues that can widen authority, leak sensitive runtime state, or make trust-bearing outputs easier to overread should be treated as security-relevant even when they are not classic remote-code-execution bugs.

Examples include:

- auth bypass
- role confusion
- confirmation-gate bypass
- public exposure of protected runtime resources
- drift between packaged and live contract surfaces
- trust-bearing summaries losing required caveats or block reasons

## Supported Release Posture

The strongest support target is the latest public release plus the current default branch before the next release cut.

The default local compose profile is development-oriented. Do not expose it beyond localhost without hardened auth, ingress, and runtime controls.
