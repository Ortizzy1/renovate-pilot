# Pilot runbook (Stage 2 - requires separate explicit authorization)

Nothing below has been executed. Every step that touches GitHub needs the owner's go-ahead.

## 0. Prerequisites
- A GitHub account the owner controls, and a **new, empty, private** repo (suggested name `renovate-pilot`).
- Confirm the plan's feature set (step 3) before relying on branch protection.
- No secrets, tokens or deployment credentials are needed by this repo or its CI.

## 1. Publish the sample (one-time, authorized)
```bash
git remote add origin https://github.com/<owner>/renovate-pilot.git
git push origin pilot/renovate-synthetic-20261109:main
git tag -a frozen-sample-v0 <commit>   # see step 6
git push origin frozen-sample-v0
```
Only this repo is pushed. Check `git remote -v` shows exactly one remote first.

## 2. Install hosted Renovate into ONLY this repo
1. GitHub -> Settings -> Applications -> Install the Renovate GitHub App (Mend Renovate, free tier).
2. Choose **Only select repositories** -> pick `renovate-pilot`. Never "All repositories".
3. Review the permission list shown by GitHub before accepting.
4. Afterwards re-open the installation page and confirm exactly one repository is listed.

## 3. Branch protection / plan check
Private-repo branch protection and rulesets are not available on every plan (historically GitHub Free
private repos lack enforced protection; verify current docs). Check:
Repo -> Settings -> Branches (or Rules -> Rulesets). If "Require ..." options are greyed out with an
upgrade notice, enforcement is NOT available: record that, and treat "human approval" as procedural only.
Do not buy/upgrade anything without separate approval.

If available, protect `main`: require PR, require 1 approval, require status checks
`npm`, `python`, `lockfiles`, `negative-test`, block force pushes, no bypass.

## 4. Review the onboarding PR
Renovate opens "Configure Renovate". Because `renovate.json` already exists, it should be a
config-acknowledgement PR. Check: no new files beyond config; the PR body lists detected
managers `npm` and `pep621` only; no `github-actions`, `docker` or other managers. Do not merge
until CI is green and you have read the diff.

## 5. Validate both update PRs
Expected: two separate PRs.
- `semver` 7.5.4 -> 7.8.6: diff touches only `npm-app/package.json` and `npm-app/package-lock.json`.
- `packaging` 24.0 -> 24.2: diff touches only `py-app/pyproject.toml` and `py-app/uv.lock`.
Verify: not automerged, CI (all 4 jobs) green, lockfile `resolved`/hash entries changed, no major
PR for packaging 25/26, no PR for any other package, at most 2 open PRs. If a lockfile is not
regenerated, record it as a finding (do not hand-edit to hide it).
Merge manually only after human review.

## 6. Frozen sample tag
Record at tagging time: `git rev-parse frozen-sample-v0^{commit}` -> store the SHA off-repo.
After the pilot: `git ls-remote origin refs/tags/frozen-sample-v0*` must show the same SHA, and
`git diff frozen-sample-v0 <base-before-pilot> --stat` must be empty for the baseline commit.
Renovate never touches tags; this proves it.

## 7. Disable / remove
1. GitHub -> Settings -> Applications -> Renovate -> Configure -> remove the repo or Uninstall.
2. Close any open Renovate PRs; delete `renovate/*` branches.
3. Optionally delete or archive the sample repo, and delete the local clone.
4. Confirm: installation list is empty; no webhooks left (Repo -> Settings -> Webhooks).

## Costs and limits
Renovate GitHub App and Actions minutes on a small private repo are free on current tiers, but verify
limits. Hosted behavior (PR titles, lockfile regeneration of `uv.lock` in Mend's sandbox) is untested.
