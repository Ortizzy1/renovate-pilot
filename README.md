# renovate-pilot

Entirely **synthetic** repository for validating how [Renovate](https://docs.renovatebot.com/)
proposes npm and Python/uv dependency updates, regenerates lockfiles, and triggers independent CI.
It contains no real code, data, secrets or links to any other project.

> Status: **local preparation only.** Hosted Renovate has NOT been installed or tested.
> No GitHub remote exists. Nothing here proves hosted behavior until Stage 2 is run.

## Layout

| Path | Purpose |
|---|---|
| `npm-app/` | npm project; `semver` pinned `7.5.4`; `package-lock.json` committed |
| `py-app/` | uv project; `packaging==24.0` pinned; `uv.lock` committed |
| `renovate.json` | Renovate config (deny-by-default, 2 allowed deps) |
| `.github/workflows/ci.yml` | CI: both smoke tests, lockfile check, negative test |
| `scripts/check_lockfiles.sh` | Lockfile-vs-manifest consistency check |
| `scripts/negative_test.py` | Breaks a *copy* of the code, expects tests to fail |
| `docs/PILOT_RUNBOOK.md` | Stage 2 procedure and teardown |

## Expected Renovate behavior

| Dep | Baseline | Expected PR | Blocked |
|---|---|---|---|
| `semver` (npm) | 7.5.4 | 7.5.4 -> 7.8.6 (minor), edits `package.json` + `package-lock.json` | 8.x, if ever released |
| `packaging` (uv) | 24.0 | 24.0 -> 24.2 (minor), edits `pyproject.toml` + `uv.lock` | 25.x / 26.x (major) |

Versions verified against npm / PyPI registries on 2026-11-09 (latest: semver 7.8.6, packaging 26.3).
`packaging` 25/26 are classed as major by Renovate, which demonstrates the major-upgrade gate.
Each dependency gets its own branch/PR; `prConcurrentLimit` is 2; automerge is off.

## Local checks

```bash
(cd npm-app && npm ci --ignore-scripts && npm test)
(cd py-app && uv sync --locked && uv run --locked python -m unittest discover -s tests)
bash scripts/check_lockfiles.sh
python scripts/negative_test.py
npx --yes --package renovate@44.224.2 -- renovate-config-validator --strict
```
