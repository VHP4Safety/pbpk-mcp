# Contributing

Thanks for contributing to PBPK MCP.

## Scope

This repository is a public PBPK MCP server with a published contract surface, live runtime checks, and release evidence gates. Contributions should preserve:

- contract clarity
- conservative scientific boundaries
- explicit auth and runtime safety
- reproducible release behavior

## Pull Requests

Before opening a pull request:

- run the relevant local tests for the area you changed
- update docs when behavior, contracts, or workflow expectations change
- avoid widening scientific or regulatory claims without explicit evidence and matching tests
- keep temporary files, credentials, machine-local paths, and generated runtime artifacts out of the patch

For release-facing or trust-surface changes, review:

- `docs/github_publication_checklist.md`
- `docs/hardening_migration_notes.md`
- `docs/pbk_reviewer_signoff_checklist.md`
- `docs/post_release_audit_plan.md`

## Model And Contract Changes

If you change:

- MCP tools or routes
- public schemas or examples
- trust-bearing summaries
- release or readiness checks

also update the matching tests and generated contract artifacts.

## Security And Scientific Claims

Do not:

- commit secrets, bearer tokens, or local credentials
- present runtime readiness as scientific adequacy
- present illustrative examples as regulatory-ready evidence
- remove caveats, block reasons, or scope boundaries from trust-bearing outputs without replacing them with something stronger

## Communication

Use issues and pull requests for normal changes. For sensitive security problems, follow `SECURITY.md` instead of opening a public issue with exploit details.
