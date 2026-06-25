import json
import re
from pathlib import Path

from .file_collector import collect_files
from .ai_client import call_ai

_SYSTEM_PROMPT = (
    "You are an expert OpenAPI specification writer. "
    "Given source files from a REST API project, produce a complete, valid "
    "OpenAPI 3.0.3 specification in JSON. "
    "Respond with ONLY the raw JSON — no markdown fences, no explanation, no commentary."
)


def _build_prompt(files: list[tuple[str, str]], title: str, api_version: str) -> str:
    file_blocks = "\n\n".join(
        f"### {path}\n{content}" for path, content in files
    )
    return (
        f"{_SYSTEM_PROMPT}\n\n"
        f"API title: {title}\n"
        f"API version: {api_version}\n\n"
        f"Source files:\n\n{file_blocks}"
    )


def _parse_json(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"AI response was not valid JSON:\n{raw[:500]}") from exc


def generate_spec(
    project_dir: Path,
    *,
    title: str = "API",
    api_version: str = "1.0.0",
    api_key: str,
    provider: str = "claude",
) -> dict:
    files = collect_files(project_dir)
    prompt = _build_prompt(files, title, api_version)
    raw = call_ai(prompt, api_key, provider)
    return _parse_json(raw)
