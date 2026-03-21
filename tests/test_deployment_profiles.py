from __future__ import annotations

import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DEV_COMPOSE = WORKSPACE_ROOT / "docker-compose.celery.yml"
HARDENED_COMPOSE = WORKSPACE_ROOT / "docker-compose.hardened.yml"
HARDENED_DEPLOY = WORKSPACE_ROOT / "scripts" / "deploy_hardened_stack.sh"


class DeploymentProfileTests(unittest.TestCase):
    def test_development_compose_keeps_explicit_dev_default(self) -> None:
        text = DEV_COMPOSE.read_text(encoding="utf-8")
        self.assertIn('AUTH_ALLOW_ANONYMOUS: "true"', text)
        self.assertIn("ENVIRONMENT: development", text)
        self.assertIn("./schemas:/app/schemas:ro", text)
        self.assertIn("./docs:/app/docs:ro", text)

    def test_hardened_overlay_disables_anonymous_access_and_requires_auth_env(self) -> None:
        text = HARDENED_COMPOSE.read_text(encoding="utf-8")
        self.assertIn('AUTH_ALLOW_ANONYMOUS: "false"', text)
        self.assertIn("ENVIRONMENT: production", text)
        self.assertIn("${AUTH_ISSUER_URL:?", text)
        self.assertIn("${AUTH_AUDIENCE:?", text)
        self.assertIn("${AUTH_JWKS_URL:?", text)
        self.assertIn('${PBPK_BIND_HOST:-127.0.0.1}:${PBPK_BIND_PORT:-8000}:8000', text)

    def test_hardened_deploy_uses_overlay_and_waits_for_bound_base_url(self) -> None:
        text = HARDENED_DEPLOY.read_text(encoding="utf-8")
        self.assertIn("docker-compose.celery.yml", text)
        self.assertIn("docker-compose.hardened.yml", text)
        self.assertIn('PBPK_BIND_HOST:-127.0.0.1', text)
        self.assertIn('PBPK_BIND_PORT:-8000', text)
        self.assertIn('wait_for_runtime_ready.py" --base-url "${base_url}"', text)


if __name__ == "__main__":
    unittest.main()
