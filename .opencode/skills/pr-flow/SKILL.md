---
name: pr-flow
description: Enforce the PR-only contribution flow with checks and review on this repo
---

## What I do

Enforce how every change lands in this repo: branch, PR, checks, review, squash-merge.
No direct pushes to `main` — ever.

## When to use me

Use me before making ANY code change in this repo, or when asked about
contributing, merging, or releasing.

## The flow

1. Create a branch from latest `main`: `git checkout -b <type>/short-name`.
2. Make the change. Run the sanity check (`python calc.py`, plus tests if present).
3. Verify `git status` shows no secrets or build artifacts (`__pycache__/`, `*.pyc`, `.env`).
4. Push the branch and open a PR with `gh pr create`. The `opencode-review` workflow
   reviews automatically, and `CODEOWNERS` requests the owner.
5. Address review comments. Re-request review if needed.
6. Merge only when checks are green and the owner approved. Squash-merge,
   delete the branch.

## Never

- Push directly to `main` (branch protection + watchdog enforce this).
- Approve your own PR or bypass protection without saying so explicitly.
- Commit `OPENCODE_API_KEY` or any token value — `${{ secrets.* }}` references only.
