import json
from pathlib import Path
from mfdballm.llm_client import LLMClient


class Orchestrator:

    SYSTEM_PLANNER = """You are a senior software architect.
Break the task into JSON array:
[
  {"path": "relative/path/file.ext", "description": "what to generate"}
]
Return ONLY valid JSON.
"""

    SYSTEM_EXECUTOR = """You are a senior backend engineer.
Generate full file content.
Return ONLY raw code.
No explanations.
"""

    def __init__(self):
        self.client = LLMClient()

    def _clean_json(self, raw: str) -> str:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
        return raw.strip()

    def build(self, spec_path: str, overwrite=False):

        spec_file = Path(spec_path)
        spec = json.loads(spec_file.read_text())

        plan_prompt = json.dumps(spec, indent=2)

        plan_raw = self.client.chat([
            {"role": "system", "content": self.SYSTEM_PLANNER},
            {"role": "user", "content": plan_prompt},
        ], max_tokens=1200)

        files = json.loads(self._clean_json(plan_raw))

        for file in files:
            path = Path(file["path"])
            desc = file["description"]

            if path.exists() and not overwrite:
                continue

            file_prompt = f"""
Project spec:
{plan_prompt}

File path:
{path}

Description:
{desc}
"""

            content = self.client.chat([
                {"role": "system", "content": self.SYSTEM_EXECUTOR},
                {"role": "user", "content": file_prompt},
            ], max_tokens=2500)

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content.strip())
