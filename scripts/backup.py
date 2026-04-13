#!/usr/bin/env python3
from __future__ import annotations
import os, shutil
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]
REPOS_DIR = REPO_ROOT.parent
BACKUPS   = REPOS_DIR / "Backups"

def main():
  BACKUPS.mkdir(parents=True, exist_ok=True)
  ts = datetime.now().strftime("%Y%m%d_%H%M%S")
  dest = BACKUPS / f"{REPO_ROOT.name}_backup_{ts}"
  if dest.exists():
    raise SystemExit(f"Refusing to overwrite existing backup: {dest}")
  print(f"Backing up repo to: {dest}")
  shutil.copytree(REPO_ROOT, dest, symlinks=True)
  print("GO")

if __name__ == "__main__":
  main()
