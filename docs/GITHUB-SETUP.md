# GitHub + OpenCode setup — opencode-github-starter

> Start with the [README](../README.md) for the big picture; this file is the deep log.

Owner: `e2edev-frame` · Visibility: **public** · Default branch: `main`

## What is installed

| Piece | File / place | Purpose |
|---|---|---|
| Agent trigger | `.github/workflows/opencode.yml` | Reply to `/opencode` or `/oc` in issue/PR comments (model `opencode/big-pickle` via Zen) |
| Auto review | `.github/workflows/opencode-review.yml` | Reviews every opened/updated PR automatically |
| Push watchdog | `.github/workflows/direct-push-watchdog.yml` | Opens an issue if commits reach `main` without a merged PR |
| Reviewers | `CODEOWNERS` (`* @e2edev-frame`) | Auto-requests owner review on every PR |
| Hygiene | `.gitignore`, `.gitattributes` | No artifacts/secrets, LF line endings |
| Branch protection | repo settings (API) | PR + 1 approval required, no force-push/deletion |
| Secret | `OPENCODE_API_KEY` (Actions secret) | Zen key, also stored locally in `~/.local/share/opencode/auth.json` |
| GitHub App | `opencode-agent` | Installed on this repo only |

## Everyday use

- Issue/PR comment: `/opencode fix this`, `/opencode explain this issue`, `/oc add error handling here`
- Local: `gh issue create`, `gh pr create`, `gh run list --repo e2edev-frame/opencode-github-starter`

## Troubleshooting (all hit for real during setup)

| Symptom | Cause | Fix |
|---|---|---|
| `unauthorized` / wrong account | `gh` logged in as someone else | `gh auth login --hostname github.com --git-protocol https --web`, verify with `gh api user --jq .login` |
| Checkout `Repository not found` in runner | job `permissions:` lacks `contents: read` (private repos mask as 404) | add `contents: read` (see `opencode.yml`) |
| `User opencode-agent[bot] does not have write permissions` | bot's own reply re-triggered the workflow (self-loop via `/oc` substring) | guard `if:` with `github.event.comment.user.type != 'Bot'` |
| Review posts `fatal: could not read Username` | `persist-credentials: false` leaves git without auth for the action's `git fetch` | keep persisted credentials + `fetch-depth: 0` in review workflow |
| Review can't post comment (403) | review job needs write to comment | `pull-requests: write`, `issues: write` |
| Agent replies "done" but no branch/PR appears | `opencode` job is read-only (`contents: read`), push denied | `contents: write` + `pull-requests: write`, trigger locked to `OWNER` (see `opencode.yml`) |
| Can't approve own PR / can't merge | GitHub forbids self-approval; solo devs merge own PRs via `gh pr merge --admin` | approve bot PRs normally; `--admin` only for your own |
| Branch protection 403 on private repo | requires GitHub Pro | this repo is public, so real protection is on; watchdog remains as backup |

## Worth reading (short list)

- OpenCode: `https://opencode.ai/docs/github/`, `/docs/zen/`, `/docs/skills/`, `/docs/troubleshooting/`
- GitHub: Actions permissions, branch protection, CODEOWNERS, `gh` CLI manual

## Solo-dev rules

1. Agent PRs → review → approve → squash-merge.
2. Your own PRs → `--admin` merge (you cannot self-approve, by design).
3. Reviews are advisory — the agent was wrong at least once here (it suggested
   restoring `persist-credentials: false`, which breaks its own `git fetch`).
