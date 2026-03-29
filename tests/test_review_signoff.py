from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcp.session_registry import SessionRegistry  # noqa: E402
from mcp_bridge.adapter.schema import SimulationHandle  # noqa: E402
from mcp_bridge.app import create_app  # noqa: E402
from mcp_bridge.audit import LocalAuditTrail  # noqa: E402
from mcp_bridge.config import AppConfig  # noqa: E402
from mcp_bridge.review_signoff import (  # noqa: E402
    attach_operator_review_signoff,
    build_operator_review_governance,
    build_operator_review_signoff_history,
    build_operator_review_signoff_summary,
    record_operator_review_signoff,
    revoke_operator_review_signoff,
)
from mcp_bridge.security.auth import AuthContext  # noqa: E402
from mcp_bridge.security.simple_jwt import jwt  # noqa: E402


class ReviewSignoffTests(unittest.TestCase):
    def test_record_and_revoke_summary_survive_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            audit = LocalAuditTrail(tmpdir, enabled=True)
            auth = AuthContext(subject="operator-a", roles=["operator"], token_id="tok-a")

            record_operator_review_signoff(
                audit,
                auth=auth,
                simulation_id="sim-1",
                scope="export_oecd_report",
                disposition="approved-for-bounded-use",
                rationale="Reviewed against declared context of use and retained bounded-use limits.",
                limitations_accepted=["Adult human reference_compound context only"],
                review_focus=["Context of use", "Population support"],
                service_version="0.4.2-test",
            )
            recorded = build_operator_review_signoff_summary(
                audit,
                simulation_id="sim-1",
                scope="export_oecd_report",
            )
            self.assertEqual(recorded["status"], "recorded")
            self.assertEqual(recorded["disposition"], "approved-for-bounded-use")
            self.assertEqual(recorded["recordedBy"]["subject"], "operator-a")
            self.assertIn("does not change qualification state", recorded["plainLanguageSummary"].lower())

            revoke_operator_review_signoff(
                audit,
                auth=auth,
                simulation_id="sim-1",
                scope="export_oecd_report",
                rationale="The supporting review context changed and the earlier bounded-use sign-off is no longer current.",
                service_version="0.4.2-test",
            )
            revoked = build_operator_review_signoff_summary(
                audit,
                simulation_id="sim-1",
                scope="export_oecd_report",
            )
            self.assertEqual(revoked["status"], "revoked")
            self.assertEqual(revoked["revokedBy"]["subject"], "operator-a")
            self.assertIn("treat the output as unsigned", revoked["plainLanguageSummary"].lower())

            history = build_operator_review_signoff_history(
                audit,
                simulation_id="sim-1",
                scope="export_oecd_report",
                limit=10,
            )
            self.assertEqual(history["status"], "available")
            self.assertEqual(history["latestStatus"], "revoked")
            self.assertEqual(history["returnedEntryCount"], 2)
            self.assertEqual(history["entries"][0]["action"], "revoked")
            self.assertEqual(history["entries"][1]["action"], "recorded")
            self.assertEqual(history["entries"][1]["actor"]["subject"], "operator-a")

    def test_operator_review_governance_explicitly_disables_override_semantics(self) -> None:
        governance = build_operator_review_governance("export_oecd_report")
        self.assertEqual(governance["workflowStatus"], "descriptive-signoff-only")
        self.assertFalse(governance["supportsOverride"])
        self.assertFalse(governance["supportsAdjudication"])
        self.assertFalse(governance["signoffChangesQualificationState"])
        self.assertFalse(governance["signoffConfersDecisionAuthority"])
        self.assertTrue(governance["externalAuthorityRequiredForOverrides"])

    def test_attach_operator_review_signoff_augments_report_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            audit = LocalAuditTrail(tmpdir, enabled=True)
            auth = AuthContext(subject="operator-b", roles=["operator"], token_id="tok-b")
            record_operator_review_signoff(
                audit,
                auth=auth,
                simulation_id="sim-2",
                scope="export_oecd_report",
                disposition="acknowledged",
                rationale="Reviewed for bounded interpretation and traceable human-review context.",
                service_version="0.4.2-test",
            )

            payload = {
                "simulationId": "sim-2",
                "report": {
                    "humanReviewSummary": {
                        "humanReviewRequired": True,
                    }
                },
            }
            attach_operator_review_signoff(
                payload,
                audit=audit,
                tool_name="export_oecd_report",
            )

            self.assertIn("operatorReviewSignoff", payload)
            self.assertIn("operatorReviewGovernance", payload)
            self.assertEqual(payload["operatorReviewSignoff"]["status"], "recorded")
            self.assertFalse(payload["operatorReviewGovernance"]["supportsOverride"])
            self.assertEqual(
                payload["report"]["humanReviewSummary"]["operatorReviewSignoff"]["status"],
                "recorded",
            )
            self.assertFalse(
                payload["report"]["humanReviewSummary"]["operatorReviewGovernance"]["supportsAdjudication"]
            )

    def test_review_signoff_route_requires_operator_confirmation_and_is_viewer_readable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AppConfig.model_validate(
                {
                    "environment": "development",
                    "auth_allow_anonymous": False,
                    "auth_dev_secret": "test-dev-secret",
                    "audit_enabled": True,
                    "audit_storage_path": tmpdir,
                    "service_version": "0.4.2-test",
                }
            )

            def auth_headers(role: str) -> dict[str, str]:
                token = jwt.encode(
                    {
                        "sub": f"review-signoff-{role}",
                        "roles": [role],
                        "iat": int(time.time()),
                        "exp": int(time.time()) + 3600,
                    },
                    "test-dev-secret",
                    algorithm="HS256",
                )
                return {"Authorization": f"Bearer {token}"}

            with TestClient(create_app(config=config)) as client:
                registry: SessionRegistry = client.app.state.session_registry
                registry.register(
                    SimulationHandle(simulation_id="sim-3", file_path="/tmp/test.pkml")
                )

                viewer_denied = client.post(
                    "/review_signoff",
                    headers=auth_headers("viewer"),
                    json={
                        "simulationId": "sim-3",
                        "scope": "export_oecd_report",
                        "disposition": "approved-for-bounded-use",
                        "rationale": "Reviewed for bounded report use with retained caveats.",
                        "confirm": True,
                    },
                )
                self.assertEqual(viewer_denied.status_code, 403)

                operator_needs_confirmation = client.post(
                    "/review_signoff",
                    headers=auth_headers("operator"),
                    json={
                        "simulationId": "sim-3",
                        "scope": "export_oecd_report",
                        "disposition": "approved-for-bounded-use",
                        "rationale": "Reviewed for bounded report use with retained caveats.",
                    },
                )
                self.assertEqual(operator_needs_confirmation.status_code, 428)

                recorded = client.post(
                    "/review_signoff",
                    headers=auth_headers("operator"),
                    json={
                        "simulationId": "sim-3",
                        "scope": "export_oecd_report",
                        "disposition": "approved-for-bounded-use",
                        "rationale": "Reviewed for bounded report use with retained caveats.",
                        "limitationsAccepted": ["Illustrative example only"],
                        "reviewFocus": ["Claim boundaries"],
                        "confirm": True,
                    },
                )
                self.assertEqual(recorded.status_code, 200)
                summary = recorded.json()["operatorReviewSignoff"]
                self.assertEqual(summary["status"], "recorded")
                self.assertEqual(summary["disposition"], "approved-for-bounded-use")
                governance = recorded.json()["operatorReviewGovernance"]
                self.assertEqual(governance["workflowStatus"], "descriptive-signoff-only")
                self.assertFalse(governance["supportsOverride"])

                viewer_read = client.get(
                    "/review_signoff",
                    headers=auth_headers("viewer"),
                    params={"simulationId": "sim-3", "scope": "export_oecd_report"},
                )
                self.assertEqual(viewer_read.status_code, 200)
                self.assertEqual(
                    viewer_read.json()["operatorReviewSignoff"]["recordedBy"]["subject"],
                    "review-signoff-operator",
                )
                self.assertFalse(viewer_read.json()["operatorReviewGovernance"]["supportsAdjudication"])

                viewer_history = client.get(
                    "/review_signoff/history",
                    headers=auth_headers("viewer"),
                    params={"simulationId": "sim-3", "scope": "export_oecd_report", "limit": 10},
                )
                self.assertEqual(viewer_history.status_code, 200)
                history = viewer_history.json()["operatorReviewSignoffHistory"]
                self.assertEqual(history["returnedEntryCount"], 1)
                self.assertEqual(history["entries"][0]["action"], "recorded")
                self.assertEqual(
                    history["entries"][0]["actor"]["subject"],
                    "review-signoff-operator",
                )
                self.assertFalse(
                    viewer_history.json()["operatorReviewGovernance"]["signoffConfersDecisionAuthority"]
                )


if __name__ == "__main__":
    unittest.main()
