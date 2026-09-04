"""Append-only, privacy-conscious local audit evidence for manual sessions."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


GENESIS_HASH = "0" * 64


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def safe_event(event):
    """Keep identifiers and decisions, never tool-result or answer content."""
    action = event.get("action") if isinstance(event.get("action"), dict) else {}
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": {key: action[key] for key in ("tool", "path", "ticket_id") if key in action},
        "resource": event.get("resource"),
        "status": event.get("status"),
        "authorized": event.get("authorized"),
        "reason": event.get("reason"),
        "result_sha256": digest(event.get("result")),
    }


class AuditLog:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event):
        previous_hash = GENESIS_HASH
        if self.path.exists() and self.path.stat().st_size:
            last_line = self.path.read_text(encoding="utf-8").splitlines()[-1]
            previous_hash = json.loads(last_line)["entry_hash"]
        record = safe_event(event)
        record["previous_hash"] = previous_hash
        record["entry_hash"] = digest(record)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(record) + "\n")
        return record


def verify(path):
    previous_hash = GENESIS_HASH
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return False, f"audit log okunamadi: {exc}"
    for number, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
            entry_hash = record.pop("entry_hash")
        except (ValueError, KeyError, TypeError):
            return False, f"satir {number}: gecersiz kayit"
        if record.get("previous_hash") != previous_hash or digest(record) != entry_hash:
            return False, f"satir {number}: zincir veya ozet uyusmuyor"
        previous_hash = entry_hash
    return True, f"{len(lines)} kayit dogrulandi; son ozet: {previous_hash}"
