import json
import click
from pathlib import Path
from .generator import generate_spec


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--output", "-o", default="openapi.json", show_default=True, help="Output file path.")
@click.option("--title", default="API", show_default=True, help="API title.")
@click.option("--version", "api_version", default="1.0.0", show_default=True, help="API version.")
@click.option(
    "--api-key",
    envvar="OPENAPI_GEN_API_KEY",
    required=True,
    help="AI provider API key (or set OPENAPI_GEN_API_KEY).",
)
@click.option(
    "--provider",
    type=click.Choice(["claude", "openai"]),
    default="claude",
    show_default=True,
    help="AI provider to use.",
)
def main(path: Path, output: str, title: str, api_version: str, api_key: str, provider: str) -> None:
    """Generate an OpenAPI specification for a REST API project directory."""
    click.echo(f"Scanning {path} ...")
    spec = generate_spec(path, title=title, api_version=api_version, api_key=api_key, provider=provider)
    output_path = Path(output)
    output_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    click.echo(f"Wrote JSON spec to {output_path}")
