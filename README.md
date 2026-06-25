# OpenAPI Generator

A pip-installable CLI tool that uses AI to generate OpenAPI 3.0.3 specifications for any REST API project directory.

## Overview

Point this tool at any REST API project and it will scan the source files, send them to an AI model (Claude or OpenAI), and produce a valid OpenAPI 3.0.3 JSON specification.

## Installation

```bash
# With Claude support (default)
pip install "openapi-generator[claude]"

# With OpenAI support
pip install "openapi-generator[openai]"

# Both providers
pip install "openapi-generator[all]"
```

## Usage

```bash
openapi-gen <path-to-project> --api-key <your-api-key>
```

The API key can also be provided via the `OPENAPI_GEN_API_KEY` environment variable:

```bash
export OPENAPI_GEN_API_KEY=sk-ant-...
openapi-gen <path-to-project>
```

### Options

| Option | Default | Description |
|---|---|---|
| `<path>` | _(required)_ | Path to the REST API project directory |
| `--api-key` | `OPENAPI_GEN_API_KEY` env var | AI provider API key |
| `--provider` | `claude` | AI provider: `claude` or `openai` |
| `--output`, `-o` | `openapi.json` | Output file path |
| `--title` | `API` | API title in the spec |
| `--version` | `1.0.0` | API version in the spec |

### Examples

```bash
# Generate a spec using Claude (default)
export OPENAPI_GEN_API_KEY=sk-ant-...
openapi-gen ./my-api

# Generate a spec using OpenAI
openapi-gen ./my-api --provider openai --api-key sk-...

# Specify title, version, and output path
openapi-gen ./my-api --title "My REST API" --version "2.0.0" --output ./docs/openapi.json
```

## Output

The generated file follows the [OpenAPI 3.0.3 specification](https://spec.openapis.org/oas/v3.0.3) and can be used directly with tools like Swagger UI, Postman, or any OpenAPI-compatible client generator.

## Supported Languages

The tool scans files with the following extensions: `.py`, `.js`, `.ts`, `.go`, `.java`, `.rb`, `.php`, `.cs`

## Development

```bash
git clone https://github.com/your-org/openapi-generator
cd openapi-generator
pip install -e ".[dev]"
pytest
```

## License

MIT
