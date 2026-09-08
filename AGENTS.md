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
- Upstream docs (read before changing agent behavior): `https://opencode.ai/docs/github/`,
  `https://opencode.ai/docs/permissions/`.

## Cloud agent (GitHub Actions) rules

The `/opencode` / `/oc` comment trigger runs `anomalyco/opencode/github` on `ubuntu-latest`
(see `.github/workflows/opencode.yml`). The runner has **no keyboard**: any command that
waits on an interactive prompt hangs until the job is cancelled (this bit us for real —
`gh pr create` without `--head` sat silent for 19 minutes). OpenCode's `doom_loop` guard
only catches identical repeated calls, NOT one hanging call, so discipline is on us.

1. **Trigger stays OWNER-only.** This repo is public; anyone can comment. The workflow
   `if:` requires `author_association == 'OWNER'` so strangers can't spend our Actions
   minutes or touch code. Keep it that way.
2. **Auth model (don't "simplify" this without reading the docs).** Push/comments work
   through the `opencode-agent` GitHub App via OIDC (default mode, `use_github_token`
   unset) — the App must stay installed on this repo. Separately, the job exposes
   `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` so the agent's own shell `gh` commands
   authenticate. Both halves are load-bearing.
3. **Job permissions are `contents:write`, `pull-requests:write`, `issues:write`.**
   That is the documented minimum for an agent expected to push branches and open PRs
   (see upstream "schedule" guidance). Do not widen (no `actions:write`, no `admin`).
4. **Every CLI command must be fully non-interactive.** Always pass explicit
   `--repo e2edev-frame/test-opencode-github --head <branch> --base main`
   (`--title/--body` for `gh pr create`), and always close stdin with `< /dev/null`
   so a forgotten prompt fails fast instead of hanging. Prefer `gh ... --jq` output
   over parsing human text.
5. **Timeout discipline.** If a command produces no output for ~2 minutes, kill it and
   report — do not wait it out. Break work into small steps; keep PRs single-purpose
   with `Closes #N` in the body so issues auto-close on merge.
6. **Known limits (don't re-learn these).** Agent commits are **unsigned** (runner has
   no SSH key) — never enable required-signed-commits while the agent writes code.
   Runs bill Zen credits — a `CreditsError: No payment method` in logs means fix
   billing at opencode.ai, not the workflow.
