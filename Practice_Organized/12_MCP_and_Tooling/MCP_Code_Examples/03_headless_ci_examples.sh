#!/usr/bin/env bash
# Headless idfc-coder usage — for CI jobs, pre-commit hooks, or one-off
# scripting where you don't want the interactive TUI.
#
# Credentials must be present in the environment (or CI secret store):
#   AD_USERNAME, AD_PASSWORD

set -euo pipefail

# 1. Simple prompt, plain text output
idfc-coder -p "What files are in this project?"

# 2. Structured output — parse tool calls / results programmatically
#    (each line is a JSON object; good for CI logs or piping into jq)
idfc-coder -p "Refactor the main module" --output-format stream-json \
  | jq -c 'select(.type == "assistant")'

# 3. Plan-only phase — get a proposed plan without letting it touch files.
#    Good for a "dry run" step in a PR pipeline before a human approves.
idfc-coder -p "How would you add auth to this service?" --phase plan

# 4. Point at a specific project directory (e.g. in a monorepo CI job)
idfc-coder -p "Add tests for the changed files" --cwd /path/to/project

# 5. Pin a specific version for reproducible CI runs
IDFC_CODER_VERSION=0.10.7 curl -fsSL \
  https://artifactory.idfcfirstbank.com/artifactory/idfc-binaries/idfc-coder/install.sh \
  | bash
