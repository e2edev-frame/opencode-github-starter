# Vercel + GitHub — opencode-github-starter

> This repo is a Python demo, so Vercel does not deploy it. This doc is the
> runbook for wiring Vercel into this repo's GitHub flow (and your real projects).
> Local Vercel CLI here is logged in as `dev-2693`.

## 1. Connect the repo (one time, on vercel.com)

1. Vercel dashboard → **Add New → Project → Import** `e2edev-frame/opencode-github-starter`.
2. Set Framework Preset (e.g. Next.js for your real project), add **Environment Variables**.
3. Deploy. Every future PR then gets an automatic **Preview Deployment** with its own URL,
   and Vercel posts the link on the PR.

## 2. Make Vercel checks mandatory (repo Settings → Branches → main)

After the first Vercel deployment, add its check (named `Vercel`) to
**Require status checks to pass before merging**, alongside the `ci` check.
Effect: broken builds and failed previews block merging — same bar as our
1-approval rule. (CLI/API change: `gh api -X PUT .../branches/main/protection`.)

## 3. Useful CLI (already installed: `vercel@54`)

- `vercel login` / `vercel whoami` — auth (currently `dev-2693`)
- `vercel link` — link a local folder to a Vercel project (run inside the real project, not here)
- `vercel env pull` — pull env vars for local dev (never commit `.env*`)
- `vercel --prod` — deploy production from local (prefer GitHub merges instead)

## 4. How it fits our flow

`push/PR → ci (pytest) → opencode-review → Vercel Preview → approve → squash-merge → Vercel Production`

Preview URLs let reviewers (human + agent) click through the real change before approving.
