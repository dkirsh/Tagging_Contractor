"""
yamlshim.py
- Goal: remove external PyYAML dependency from release gates.
- Strategy: try PyYAML; if missing, fall back to a minimal YAML subset parser.

Assumptions (true for our registry YAML):
- mappings, lists, strings, numbers, booleans, null
- indentation with spaces
- no anchors/aliases, no custom tags
If the YAML grows beyond this subset, prefer exporting registry to JSON for contract generation.
"""
from __future__ import annotations
from pathlib import Path
import re

def _coerce_scalar(s: str):
    s = s.strip()
    if s == "null" or s == "Null" or s == "NULL" or s == "~":
        return None
    if s == "true" or s == "True" or s == "TRUE":
        return True
    if s == "false" or s == "False" or s == "FALSE":
        return False
    # quoted
    if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    # int/float
    if re.fullmatch(r"[+-]?\d+", s):
        try: return int(s)
        except: pass
    if re.fullmatch(r"[+-]?\d+\.\d+", s):
        try: return float(s)
        except: pass
    return s

def safe_load(text: str):
    # Minimal indentation-based parser for YAML subset.
    # Supports:
    # key: value
    # key:
    #   nested: value
    # - item
    lines = []
    for raw in text.splitlines():
        # strip comments (naive but ok for our files)
        line = raw.split("#", 1)[0].rstrip("\n")
        if not line.strip():
            continue
        lines.append(line.rstrip())

    root = None
    stack = []  # [{"indent": int, "container": obj, "last_key": str|None}]
    def current():
        return stack[-1]["container"] if stack else None

    for line in lines:
        indent = len(line) - len(line.lstrip(" "))
        s = line.lstrip(" ")
        if s.startswith("- "):
            item = s[2:].strip()
            cont = current()
            if cont is None:
                root = []
                stack = [{"indent": indent, "container": root, "last_key": None}]
                cont = root
            if not isinstance(cont, list):
                # Try to convert the most recent dict placeholder into a list.
                if stack:
                    found = False
                    for entry in reversed(stack):
                        parent = entry["container"]
                        last_key = entry["last_key"]
                        if isinstance(parent, dict) and last_key:
                            cur = parent.get(last_key)
                            if cur == {} or cur is None:
                                parent[last_key] = []
                                cont = parent[last_key]
                                stack.append({"indent": indent, "container": cont, "last_key": None})
                                found = True
                                break
                            if isinstance(cur, list):
                                cont = cur
                                stack.append({"indent": indent, "container": cont, "last_key": None})
                                found = True
                                break
                    if not found:
                        raise ValueError("YAML subset parser: list item under non-list")
                else:
                    raise ValueError("YAML subset parser: list item under non-list")
            # item may be scalar or inline mapping "k: v"
            if ":" in item and not item.startswith('"') and not item.startswith("'"):
                k, v = item.split(":", 1)
                obj = {k.strip(): _coerce_scalar(v)}
                cont.append(obj)
                # allow following indented lines to extend this object
                stack.append({"indent": indent + 2, "container": obj, "last_key": k.strip()})
            else:
                cont.append(_coerce_scalar(item))
            continue

        # mapping line
        if ":" not in s:
            raise ValueError(f"YAML subset parser: expected ':' in line: {s}")
        k, v = s.split(":", 1)
        k = k.strip()
        v = v.strip()

        # unwind stack to correct indent
        while stack and indent < stack[-1]["indent"]:
            stack.pop()

        cont = current()
        if cont is None:
            root = {}
            stack = [{"indent": indent, "container": root, "last_key": None}]
            cont = root

        if not isinstance(cont, dict):
            raise ValueError("YAML subset parser: mapping under non-dict")

        parent_entry = stack[-1] if stack else None
        if v == "":
            # start a nested container; we don't know list vs dict yet.
            # default dict; can be replaced if next line is a list item.
            cont[k] = {}
            if parent_entry is not None:
                parent_entry["last_key"] = k
            stack.append({"indent": indent + 2, "container": cont[k], "last_key": None})
        else:
            cont[k] = _coerce_scalar(v)
            if parent_entry is not None:
                parent_entry["last_key"] = k

    return root

def load(source):
    def _looks_like_path(val: str) -> bool:
        if "\n" in val or len(val) > 255:
            return False
        try:
            return Path(val).exists()
        except OSError:
            return False

    try:
        import yaml  # type: ignore
        if hasattr(source, "read"):
            return yaml.safe_load(source)
        if isinstance(source, str) and _looks_like_path(source):
            with open(source, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return yaml.safe_load(source)
    except ModuleNotFoundError:
        if hasattr(source, "read"):
            return safe_load(source.read())
        if isinstance(source, str) and _looks_like_path(source):
            with open(source, "r", encoding="utf-8") as f:
                return safe_load(f.read())
        return safe_load(str(source))
