# mfdballm/llm_client.py

from typing import List, Dict
from pathlib import Path

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router
from mfdballm.session_store import SessionStore


class LLMClient:
    """
    LLM Client

    Supports:
        - Stateless mode (default)
        - Persistent project-isolated sessions (optional)

    Router remains unchanged.
    """

    def __init__(
        self,
        project_path: str | None = None,
        persistent: bool = False,
    ):
        providers = build_providers()
        self.router = Router(providers)

        self.persistent = persistent

        if self.persistent:
            if project_path is None:
                project_path = str(Path.cwd())

            self.session = SessionStore(project_path)
        else:
            self.session = None

    # ============================================================
    # Chat
    # ============================================================

    def chat(self, messages: List[Dict]) -> str:

        if not self.persistent:
            return self.router.chat(messages)

        # Persistent mode

        history = self.session.load()

        full_context = history + messages

        result = self.router.chat(full_context)

        # Append new messages and assistant response

        for msg in messages:
            self.session.append(msg)

        self.session.append({
            "role": "assistant",
            "content": result,
        })

        return result

    # ============================================================
    # Session control
    # ============================================================

    def clear_session(self):
        if self.session:
            self.session.clear()
