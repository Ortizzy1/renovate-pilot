"""Controlled negative test.

Copies npm-app to a temp dir, deliberately breaks isCompatible(), and asserts
the smoke test FAILS. Exit 0 means the safety net works (broken code was caught).
Exit 1 means broken code passed the tests, i.e. the tests are meaningless.
The real source tree is never modified.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "npm-app"
GOOD = "return semver.satisfies(version, range);"
BAD = "return !semver.satisfies(version, range);"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="negtest-") as tmp:
        work = Path(tmp) / "npm-app"
        shutil.copytree(SRC, work, ignore=shutil.ignore_patterns("node_modules"))
        npm = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
                       cwd=work, check=True, capture_output=True)
        # Positive control: the unbroken copy MUST pass, otherwise a later failure proves nothing.
        control = subprocess.run([npm, "test"], cwd=work, capture_output=True, text=True)
        if control.returncode != 0 or "pass 3" not in control.stdout:
            print("negative test setup error: unbroken control did not pass 3 tests", file=sys.stderr)
            print(control.stdout, file=sys.stderr)
            return 2
        target = work / "src" / "version.js"
        text = target.read_text(encoding="utf-8")
        if GOOD not in text:
            print("negative test setup error: mutation anchor not found", file=sys.stderr)
            return 2
        target.write_text(text.replace(GOOD, BAD), encoding="utf-8")
        result = subprocess.run([npm, "test"], cwd=work, capture_output=True, text=True)
        if result.returncode == 0 or "fail 0" in result.stdout:
            print("NEGATIVE TEST FAILED: deliberately broken code passed the smoke test")
            return 1
        print("NEGATIVE TEST OK: broken code was rejected by the smoke test "
              f"(npm test exit {result.returncode})")
        return 0


if __name__ == "__main__":
    sys.exit(main())
