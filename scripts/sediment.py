#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, time
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
OBJ_DIR = REPO_ROOT / "_archive" / "sedimentary" / "objects"
MF_DIR  = REPO_ROOT / "_archive" / "sedimentary" / "manifests"

EXCLUDE_DIRS = {
  "_archive", ".venv", "__pycache__", ".git", "release_artifacts"
}
EXCLUDE_FILES = {".DS_Store"}

def sha256_file(p: Path) -> str:
  h = hashlib.sha256()
  with p.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
      h.update(chunk)
  return h.hexdigest()

def should_skip(p: Path) -> bool:
  rel = p.relative_to(REPO_ROOT)
  parts = rel.parts
  if any(part in EXCLUDE_DIRS for part in parts):
    return True
  if p.name in EXCLUDE_FILES:
    return True
  return False

def sediment(system_version: str, core_version: str) -> Path:
  OBJ_DIR.mkdir(parents=True, exist_ok=True)
  MF_DIR.mkdir(parents=True, exist_ok=True)

  files = {}
  total_bytes = 0
  for p in REPO_ROOT.rglob("*"):
    if p.is_dir():
      continue
    if should_skip(p):
      continue
    rel = str(p.relative_to(REPO_ROOT))
    digest = sha256_file(p)
    size = p.stat().st_size
    total_bytes += size

    obj_path = OBJ_DIR / digest
    if not obj_path.exists():
      obj_path.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(p, obj_path)

    files[rel] = {"sha256": digest, "bytes": size}

  manifest = {
    "schema": "sedimentary.manifest.v1",
    "written_at": datetime.now(timezone.utc).isoformat(),
    "system_version": system_version,
    "core_version": core_version,
    "file_count": len(files),
    "total_bytes": total_bytes,
    "files": files,
  }

  out = MF_DIR / f"{system_version}.manifest.json"
  out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
  return out

def main():
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("--system", required=True)
  ap.add_argument("--core", required=True)
  args = ap.parse_args()
  out = sediment(args.system, args.core)
  print(f"OK: wrote {out} ({len(json.loads(out.read_text())['files'])} files)")

if __name__ == "__main__":
  main()
