import os
from pathlib import Path

_INCLUDE_EXTENSIONS = {".py", ".js", ".ts", ".go", ".java", ".rb", ".php", ".cs"}
_SKIP_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", ".eggs"}


def collect_files(project_dir: Path, max_bytes: int = 400_000) -> list[tuple[str, str]]:
    """Walk *project_dir* and return (relative_path, content) for each source file.

    Stops collecting once the total accumulated size exceeds *max_bytes* to
    avoid exceeding AI model context limits.
    """
    results: list[tuple[str, str]] = []
    total = 0

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]

        for filename in sorted(files):
            if Path(filename).suffix not in _INCLUDE_EXTENSIONS:
                continue

            abs_path = Path(root) / filename
            try:
                content = abs_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            total += len(content.encode("utf-8"))
            if total > max_bytes:
                return results

            rel_path = abs_path.relative_to(project_dir).as_posix()
            results.append((rel_path, content))

    return results
