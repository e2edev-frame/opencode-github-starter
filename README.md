# opencode-github-starter

A hardened starter for running the [opencode](https://opencode.ai/docs/github/) GitHub agent —
from zero to an agent that writes code, pushes branches, and opens PRs by itself.
Built by debugging every failure for real; the scars are documented below.

## How it works — 3 contributors

| Who | Role |
|---|---|
| **Owner** (you) | Gives orders, approves, merges. The only human. |
| **Local agent** | Works on your machine, commits signed, opens PRs via `gh`. |
| **Cloud agent** (`opencode-agent[bot]`) | Lives in GitHub Actions. Comment `/opencode <task>` on any issue/PR and it implements, pushes, and opens a PR. |

## Automation (4 workflows)

| Workflow | Trigger | Job |
|---|---|---|
| `opencode.yml` | `/opencode` or `/oc` comment, **OWNER only** | Implement + push branch + open PR |
| `opencode-review.yml` | PR opened/updated | Auto-review every PR |
| `direct-push-watchdog.yml` | Push to `main` | Opens an issue if anyone bypasses PRs |
| `ci.yml` | PR / push | `pytest` must stay green |

Rules live in [`AGENTS.md`](AGENTS.md), the contribution flow in
[`.opencode/skills/pr-flow/SKILL.md`](.opencode/skills/pr-flow/SKILL.md),
and the full setup/troubleshooting log in [`docs/GITHUB-SETUP.md`](docs/GITHUB-SETUP.md).

## Quickstart (reuse this in your own repo, ~20 min)

1. Install the [opencode-agent app](https://github.com/apps/opencode-agent) on your repository.
2. Add the `OPENCODE_API_KEY` Actions secret (your own Zen key).
3. Repo **Settings → Actions → General → Workflow permissions** → check
   **"Allow GitHub Actions to create and approve pull requests"** → Save.
   (No API for this — it must be clicked. Without it the agent gets
   `403: GitHub Actions is not permitted to create pull requests`.)
4. Protect `main`: require a PR + 1 approval, forbid force-push/deletion.
5. Open an issue, comment `/opencode <task>`, watch the agent open a PR.

If your repo is private, also check your Actions minutes quota (public repos are unlimited).
Solo devs: widen the trigger to `MEMBER`/`COLLABORATOR` only when the team grows;
you cannot approve your own PRs, so merge your own with `gh pr merge --admin`.

## Lessons learned the hard way

1. **Read-only token can't deliver.** The agent implemented code but couldn't push —
   the job needs `contents: write` + `pull-requests: write` + `issues: write`.
2. **Public repo + open trigger = free compute for strangers.** Lock the trigger to
   `OWNER` (`author_association`), and match precisely with `' /oc'`/`startsWith`
   instead of substring `contains` (which also matches words like `/october`).
3. **No keyboard on the runner.** A `gh pr create` missing `--head` waited on an
   interactive prompt for **19 minutes**. Every CLI command must be fully explicit
   with stdin closed (`< /dev/null`) so a forgotten prompt fails fast.
4. **Pin your actions.** `@latest`/floating tags are a supply-chain risk —
   pin to SHAs (see `opencode.yml`).

Details, dead ends, and fixes: [`docs/GITHUB-SETUP.md`](docs/GITHUB-SETUP.md).

## Repo layout

```
calc.py / test_calc.py   demo code (the agent wrote subtract/divide itself)
AGENTS.md                rules incl. cloud-agent discipline
docs/GITHUB-SETUP.md     setup guide + troubleshooting from real incidents
.github/workflows/      the 4 workflows above
.opencode/skills/        pr-flow skill: branch → PR → review → squash-merge
```

## License

MIT — see [LICENSE](LICENSE).
