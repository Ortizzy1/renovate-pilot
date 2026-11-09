# Pilot runbook (Stage 2 - requires separate explicit authorization)

Nothing below has been executed. Every step that touches GitHub needs the owner's explicit,
separate authorization. Do not assume any GitHub plan, feature or permission: verify each one
in the GitHub UI or official docs at the time.

The order matters. **Branch protection is configured and verified BEFORE Renovate is installed.**

## Frozen sample tag (read first)

- `frozen-sample-v0` is an existing **lightweight** tag at `b8b35c4040148dcba2932e839f24fc2aceaa8ee0`,
  the originally accepted sample commit.
- Stage 2 **pushes and verifies the existing tag only**. Never create, recreate, move, delete,
  or force-update it, and never use `git tag -f`, `git push --force`, or `git push --tags`
  with a replaced tag.
- The remote tag must keep pointing at `b8b35c4...` even after later corrective commits are
  published on the branch. The branch HEAD will differ from the tag; that is expected.

## 0. Prerequisites
- A GitHub account the owner controls.
- No secrets, tokens or deployment credentials are needed by this repo or its CI.
- Re-check local state first: branch `pilot/renovate-synthetic-20261109`, clean status,
  `git remote -v` empty, `git rev-parse frozen-sample-v0` = `b8b35c4040148dcba2932e839f24fc2aceaa8ee0`.

## 1. Create the repository (separate owner authorization required)
Create a new, empty, **private** repository containing no README/license/gitignore, named for the
synthetic pilot only. Do not reuse any existing repository. Record owner, name, and visibility.
Do not buy or upgrade any plan without separate approval.

## 2. Publish the approved commit and the existing frozen tag
1. Confirm `git remote` is empty, then add exactly one remote for the new repo.
2. Push the approved pilot branch commit to the remote `main` (the branch HEAD at the time of
   authorization, including any corrective successor commit).
3. Push the existing tag by explicit name, with no force:
   ```bash
   git push origin refs/tags/frozen-sample-v0:refs/tags/frozen-sample-v0
   ```

## 3. Verify the remote branch and exact tag target
```bash
git ls-remote origin refs/heads/main "refs/tags/frozen-sample-v0*"
```
- `refs/heads/main` must equal the local approved HEAD.
- `refs/tags/frozen-sample-v0` must equal `b8b35c4040148dcba2932e839f24fc2aceaa8ee0`
  (lightweight tag: no `^{}` peeled line). Any other value: stop and report; do not fix by re-tagging.

## 4. Establish baseline CI
Confirm the `ci` workflow ran on `main` and that all four jobs pass: `npm`, `python`, `lockfiles`,
`negative-test`. Confirm the workflow ran with read-only `contents` permission and no secrets, and
that both `setup-uv` steps used uv `0.12.15`. If any check fails, stop and diagnose; do not
install Renovate on a red baseline.

## 5. Configure and verify branch protection BEFORE installing Renovate
Check what the account and plan actually allow (Repo -> Settings -> Branches, and Rules -> Rulesets;
consult current GitHub docs for private-repository support on this plan). Do not assume availability.

If enforcement is available, configure for `main`:
- require a pull request before merging, with at least 1 approving review
- require status checks `npm`, `python`, `lockfiles`, `negative-test` to pass (and be up to date)
- block force pushes and branch deletion; no bypass actors
- restrict who can merge to the owner

Then **verify it is actually enforced**, not just saved: attempt (without merging anything you care
about) a direct push to `main` and confirm it is rejected, and confirm a PR with a failing or
pending check cannot be merged. Record the evidence.

## 6. If private branch protection cannot be enforced: STOP
If settings are missing, greyed out, show an upgrade prompt, or the verification in step 5 fails:
- Stop here. Do not install Renovate.
- Report the limitation to the owner and the options, for example: upgrade the plan (owner's
  decision, cost not assumed), make the synthetic repo public (it contains no sensitive data, but
  that is the owner's call and permanent exposure of the history), use a different account or
  organization with the needed features, or abandon the hosted test.
- Manual or procedural review is **not** enforced protection and must not be described as such.
  Proceeding without enforcement requires an explicit, informed owner decision recorded in writing.

## 7. Install the Renovate GitHub App for the single repository
Only after steps 3-5 pass:
1. Install the Renovate GitHub App and choose **Only select repositories**, selecting just the
   synthetic pilot repo. Never "All repositories".
2. Review the permissions GitHub shows before accepting.
3. Re-open the installation page and confirm exactly one repository is listed.

## 8. Onboarding behavior
Because `renovate.json` is already committed, Renovate normally treats the repo as onboarded and
skips the "Configure Renovate" onboarding PR. If an onboarding PR does appear, or Renovate reports
the config invalid, treat it as a finding: read the PR/log, do not merge until understood.

## 9. Confirm the expected dependency PRs and CI
Expected (not yet observed on hosted Renovate): two separate PRs.
- `semver` 7.5.4 -> 7.8.6: touches only `npm-app/package.json` and `npm-app/package-lock.json`.
- `packaging` 24.0 -> 24.2: touches only `py-app/pyproject.toml` and `py-app/uv.lock`.

Verify: no automerge; all four CI checks run and pass on each PR; lockfiles regenerated by
Renovate (not hand-edited); no major PR for `packaging` 25/26; no PR for any other package or
manager; at most 2 open Renovate PRs. If a lockfile is not regenerated, record a finding.
Versions may drift as new releases ship; compare against registries at test time.

## 10. Manual review and merge authorization
Read each diff. Merge only after (a) CI is green, (b) a human has reviewed, and (c) the owner has
explicitly authorized that specific merge. No automerge, no merge by bots.

## 11. Verify the frozen tag is unchanged
After PRs are handled:
```bash
git ls-remote origin "refs/tags/frozen-sample-v0*"
```
Must still show `b8b35c4040148dcba2932e839f24fc2aceaa8ee0`. Renovate does not touch tags.

## 12. Revoke access and tear down
1. GitHub -> Settings -> Applications -> Installed GitHub Apps -> Renovate -> Configure:
   remove the repository, or Uninstall. Reload and confirm the repository list is empty/app gone.
2. Close open Renovate PRs; delete `renovate/*` branches.
3. Check Repo -> Settings -> Webhooks and Integrations for leftovers.
4. Optionally archive or delete the synthetic repo (owner's decision; deletion is irreversible)
   and delete local clones.
5. Do not delete or move the frozen tag unless the owner separately decides to destroy the whole repo.

## Costs and limits
Plan features and any cost are unverified. Hosted Renovate behavior (PR creation, `uv.lock`
regeneration in Renovate's environment, onboarding skip) is untested until Stage 2.
