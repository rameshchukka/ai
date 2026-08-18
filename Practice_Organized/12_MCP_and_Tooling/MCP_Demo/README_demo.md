# idfc-coder Demo — SDK + MCP (Jira, Confluence, Bitbucket)

## What this demonstrates
- Python SDK driving a multi-turn agent session
- Built-in Atlassian MCP integration (Jira + Confluence) — auto-enabled by env vars
- Custom MCP server for self-hosted Bitbucket, wired via `mcp.demo.json`
- `phase="plan"` — the whole demo is read-only, so nothing gets modified live

## Setup (do this before the demo, not during it)

1. Copy the env template and fill in real values — **never** in chat, never committed:
   ```bash
   cp .env.demo.example .env.demo
   # edit .env.demo with your real AD creds, Atlassian token, Bitbucket token
   ```

2. Load them into your shell:
   ```bash
   set -a; source .env.demo; set +a
   ```

3. Install the SDK:
   ```bash
   pip install idfc-coder --index-url \
     https://artifactory.idfcfirstbank.com/artifactory/api/pypi/idfc-pypi-local/simple
   ```

4. Install the Bitbucket MCP server once so the demo doesn't pay npx download
   latency live:
   ```bash
   npm install -g mcp-bitbucket
   ```

5. Edit the three constants at the top of `demo_atlassian_bitbucket.py`
   (`JIRA_TICKET`, `BITBUCKET_PROJECT`, `BITBUCKET_REPO`) to point at real
   items you want to show.

6. Dry-run it once, off-stage, to confirm all three integrations connect:
   ```bash
   python demo_atlassian_bitbucket.py
   ```
   Check `~/.idfc-coder/logs/idfc-coder.log` for:
   ```
   idfc_coder.mcp - INFO - Connected to 'bitbucket' (N tools)
   ```
   and confirm no `ERROR` lines for Atlassian.

## Running it live
```bash
python demo_atlassian_bitbucket.py
```
It walks: Jira ticket → linked Confluence doc → open Bitbucket PRs →
a synthesized status summary — printing each tool call as it happens so
the audience can see what's being fetched, not just the final answer.

## CLI fallback (if the SDK script has an issue mid-demo)
The same flow works headless, one prompt at a time:
```bash
idfc-coder -p "Look up Jira ticket PROJ-1234 and summarize it" --phase plan
idfc-coder -p "List open PRs in PROJ/backend-api" --phase plan
```

## Safety notes for the demo
- Everything runs in `phase="plan"` — read-only tools only, nothing writes
  back to Jira, Confluence, or Bitbucket.
- Atlassian's MCP server is allowlisted to read-only tools by default at
  the idfc-coder level too (belt and suspenders).
- Rotate the Bitbucket personal access token and Atlassian API token after
  the demo if they were created solely for it.
- Double-check `.env.demo` is in `.gitignore` before you `git add .` anything
  in this folder.
