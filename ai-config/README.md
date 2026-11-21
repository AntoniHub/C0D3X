# AI configuration

Portable copy of the Claude Code setup I use on every machine: global rules and four
subagents. The subagents live in [`.claude/agents`](../.claude/agents), which is the
single source of truth; the installer copies them to the user-level folder so they
are available in every project.

| File | Purpose |
|---|---|
| `CLAUDE.md` | Global rules: code audit standard, comments policy, no emojis, git etiquette, QA mindset |
| `settings.snippet.json` | Settings to merge by hand: no co-author trailers, confirmation before commit and push, `.env` files unreadable |
| `install.ps1`, `install.sh` | Copy the rules and the agents to `~/.claude` |

## Subagents

| Agent | Model | Access | Role |
|---|---|---|---|
| `code-reviewer` | Haiku, medium effort | read only | Reviews changed code against the global rules and language standards |
| `bug-reporter` | Haiku, medium effort | read only | Turns a failed run into a redacted bug report with its classification |
| `security-reviewer` | Sonnet, medium effort | read only | Looks for vulnerabilities and gaps before code reaches the repository |
| `test-planner` | Sonnet, medium effort | writes `docs/test-plans/` | Produces risk-based test plans following ISO/IEC/IEEE 29119-3 |

Read-only agents run on the smaller model to keep token use low. The two that need
judgement or write files use the mid-size model.

## Install

```powershell
./ai-config/install.ps1            # skips files that already differ
./ai-config/install.ps1 -Force     # replaces them and keeps a timestamped backup
```

```bash
./ai-config/install.sh             # or: ./ai-config/install.sh --force
```

Both accept an alternative target: `-ClaudeDir <path>` or `CLAUDE_DIR=<path>`.
