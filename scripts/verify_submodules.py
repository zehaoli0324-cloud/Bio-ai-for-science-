#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((root / "projects.json").read_text())
failed = []
for project in manifest["projects"]:
    path = root / project["path"]
    if not (path / ".git").exists():
        failed.append(project["path"] + ": not initialized")
        continue
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=path, text=True).strip()
    if actual != project["sha"]:
        failed.append(project["path"] + ": commit mismatch")
if failed:
    print("\n".join(failed), file=sys.stderr)
    sys.exit(1)
print(f"PASS: {len(manifest['projects'])} submodule versions match")
