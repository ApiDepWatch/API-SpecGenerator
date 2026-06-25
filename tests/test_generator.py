import json
import pytest
from pathlib import Path
from unittest.mock import patch

from openapi_generator.file_collector import collect_files
from openapi_generator.generator import generate_spec


# --- file_collector tests ---

def test_collect_files_filters_extensions(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("# python")
    (tmp_path / "README.md").write_text("# docs")
    (tmp_path / "logo.png").write_bytes(b"\x89PNG")

    files = collect_files(tmp_path)
    paths = [p for p, _ in files]
    assert "app.py" in paths
    assert "README.md" not in paths
    assert "logo.png" not in paths


def test_collect_files_respects_max_bytes(tmp_path: Path) -> None:
    # "a_small.py" sorts before "z_big.py", so small is collected first;
    # adding big would exceed the budget, so we stop with exactly 1 file.
    (tmp_path / "a_small.py").write_text("y" * 100)
    (tmp_path / "z_big.py").write_text("x" * 300)

    files = collect_files(tmp_path, max_bytes=250)
    assert len(files) == 1
    assert files[0][0] == "a_small.py"


def test_collect_files_skips_excluded_dirs(tmp_path: Path) -> None:
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "dep.js").write_text("module.exports = {}")
    (tmp_path / "index.js").write_text("const x = 1")

    files = collect_files(tmp_path)
    paths = [p for p, _ in files]
    assert "index.js" in paths
    assert not any("node_modules" in p for p in paths)


# --- generator tests ---

def test_generate_spec_calls_ai_and_parses_result(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("# flask app")
    fake_spec = {
        "openapi": "3.0.3",
        "info": {"title": "Test API", "version": "0.1.0"},
        "paths": {},
    }

    with patch("openapi_generator.generator.call_ai", return_value=json.dumps(fake_spec)):
        spec = generate_spec(tmp_path, title="Test API", api_version="0.1.0", api_key="fake", provider="claude")

    assert spec["openapi"] == "3.0.3"
    assert spec["info"]["title"] == "Test API"
    assert spec["info"]["version"] == "0.1.0"
    assert "paths" in spec


def test_generate_spec_strips_markdown_fences(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("# flask app")
    fake_spec = {"openapi": "3.0.3", "info": {"title": "A", "version": "1"}, "paths": {}}
    raw = f"```json\n{json.dumps(fake_spec)}\n```"

    with patch("openapi_generator.generator.call_ai", return_value=raw):
        spec = generate_spec(tmp_path, title="A", api_version="1", api_key="fake", provider="claude")

    assert spec["openapi"] == "3.0.3"


def test_generate_spec_raises_on_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("# flask app")

    with patch("openapi_generator.generator.call_ai", return_value="not json at all"):
        with pytest.raises(ValueError, match="not valid JSON"):
            generate_spec(tmp_path, title="A", api_version="1", api_key="fake", provider="claude")
