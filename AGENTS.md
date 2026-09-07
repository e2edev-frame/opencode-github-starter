# AGENTS.md — test-opencode-github

Test repo for the OpenCode GitHub agent. Small Python demo (`calc.py` + `test_calc.py`).

## Golden rules

1. **Never push directly to `main`.** Branch protection requires a PR + 1 approval.
   A watchdog workflow opens an issue on direct pushes.
2. **Never commit secrets.** API keys live only in GitHub Secrets (`OPENCODE_API_KEY`)
   and local `~/.local/share/opencode/auth.json`. Workflows reference `${{ secrets.* }}`.
3. **Never commit build artifacts** (`__pycache__/`, `*.pyc`, `node_modules/`, `.env`).
   `.gitignore` covers these — keep it updated when adding new stacks.
4. Keep PRs small, one purpose per PR. Squash-merge.

## Workflow commands

- Sanity check demo: `python calc.py` (expect `5`), `python -m pytest` if tests exist.
- GitHub: `gh pr create`, `gh pr view`, `gh issue create`, `gh run list --repo e2edev-frame/test-opencode-github`.

## Docs

- Human setup/troubleshooting guide: `docs/GITHUB-SETUP.md` — read it before touching workflows.
- Installed project skill: `.opencode/skills/pr-flow/SKILL.md` — the PR-only flow every change must follow.
