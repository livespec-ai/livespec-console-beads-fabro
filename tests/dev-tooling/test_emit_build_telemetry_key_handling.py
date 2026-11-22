"""emit-build-telemetry.sh refuses xtrace and keeps the Honeycomb key out of curl's argv."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / ".github" / "scripts" / "emit-build-telemetry.sh"
_KEY = "SENTINEL-honeycomb-ingest-key-0123"
_SHIM = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$SHIM_ARGV"
prev=""
out=""
for a in "$@"; do
  [ "$prev" = "--config" ] && cat "$a" >> "$SHIM_CONFIG"
  [ "$prev" = "-o" ] && out="$a"
  prev="$a"
done
[ -n "$out" ] && echo '{}' > "$out"
printf 200
"""


def _env(tmp_path: Path, **extra: str) -> dict[str, str]:
    shim_dir = tmp_path / "bin"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "curl"
    shim.write_text(_SHIM, encoding="utf-8")
    shim.chmod(0o755)
    env = {
        "PATH": f"{shim_dir}{os.pathsep}{os.environ['PATH']}",
        "HOME": os.environ.get("HOME", "/"),
        "HONEYCOMB_BUILD_INGEST_KEY": _KEY,
        "BUILD_ENV": "ci",
        "BUILD_PHASE": "test",
        "BUILD_REPO": "o/r",
        "BUILD_GIT_COMMIT_SHA": "0" * 40,
        "BUILD_TOOLCHAIN_VER": "1.92.0",
        "BUILD_SPAN_NAME": "build.check",
        "BUILD_START_NANO": "1",
        "BUILD_END_NANO": "2",
        "SHIM_ARGV": str(tmp_path / "argv.log"),
        "SHIM_CONFIG": str(tmp_path / "config.log"),
    }
    env.update(extra)
    return env


def _run(env: dict[str, str], *shell_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", *shell_args, str(_SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_bash_x_is_refused_and_prints_no_key(tmp_path: Path) -> None:
    result = _run(_env(tmp_path), "-x")
    assert result.returncode == 2
    assert _KEY not in result.stdout + result.stderr


def test_shellopts_xtrace_is_refused_and_prints_no_key(tmp_path: Path) -> None:
    result = _run(_env(tmp_path, SHELLOPTS="xtrace"))
    assert result.returncode == 2
    assert _KEY not in result.stdout + result.stderr


def test_key_reaches_curl_through_a_config_and_is_in_no_argv(tmp_path: Path) -> None:
    result = _run(_env(tmp_path))
    assert result.returncode == 0, result.stderr
    argv = (tmp_path / "argv.log").read_text(encoding="utf-8")
    assert argv.strip()
    assert _KEY not in argv
    assert f"x-honeycomb-team: {_KEY}" in (tmp_path / "config.log").read_text(encoding="utf-8")


def test_missing_key_still_fails(tmp_path: Path) -> None:
    env = _env(tmp_path)
    del env["HONEYCOMB_BUILD_INGEST_KEY"]
    assert _run(env).returncode != 0
