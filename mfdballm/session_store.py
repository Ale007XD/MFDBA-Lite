# mfdballm/session_store.py

import json
import hashlib
from pathlib import Path
from typing import List, Dict
from threading import RLock


class SessionStore:
    """
    Persistent project-isolated session storage.

    Root:
        ~/.mfdballm/sessions/{project_hash}/session.json

    Thread-safe.
    Atomic writes.
    """

    def __init__(self, project_path: str):
        self._lock = RLock()

        project = Path(project_path).resolve()
        project_hash = hashlib.sha256(
            str(project).encode()
        ).hexdigest()[:16]

        self.base_dir = (
            Path.home()
            / ".mfdballm"
            / "sessions"
            / project_hash
        )

        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.session_file = self.base_dir / "session.json"

    # ============================================================
    # Core operations
    # ============================================================

    def load(self) -> List[Dict]:
        with self._lock:
            if not self.session_file.exists():
                return []

            try:
                return json.loads(
                    self.session_file.read_text()
                )
            except Exception:
                # corrupted file protection
                return []

    def save(self, messages: List[Dict]):
        with self._lock:
            tmp_file = self.session_file.with_suffix(".tmp")

            tmp_file.write_text(
                json.dumps(messages, indent=2)
            )

            tmp_file.replace(self.session_file)

    def append(self, message: Dict):
        with self._lock:
            messages = self.load()
            messages.append(message)
            self.save(messages)

    def clear(self):
        with self._lock:
            if self.session_file.exists():
                self.session_file.unlink()
