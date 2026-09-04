import json
import tempfile
import unittest
from pathlib import Path

from agentprobe.audit import AuditLog, verify


class AuditTests(unittest.TestCase):
    def test_audit_chain_verifies_without_storing_result_content(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "audit.jsonl"
            log = AuditLog(path)
            log.append({"action": {"tool": "lookup_ticket", "ticket_id": "T-200"},
                        "resource": "T-200", "status": "blocked", "authorized": False,
                        "reason": "ticket unavailable", "result": {"error": "access denied"}})
            valid, _ = verify(path)
            self.assertTrue(valid)
            self.assertNotIn("access denied", path.read_text(encoding="utf-8"))

    def test_audit_chain_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "audit.jsonl"
            AuditLog(path).append({"action": {"tool": "read_file", "path": "guide.txt"},
                                   "resource": "guide.txt", "status": "ok", "authorized": True,
                                   "result": {"text": "secret-free"}})
            item = json.loads(path.read_text(encoding="utf-8"))
            item["status"] = "blocked"
            path.write_text(json.dumps(item) + "\n", encoding="utf-8")
            valid, message = verify(path)
            self.assertFalse(valid)
            self.assertIn("uyusmuyor", message)
