#!/usr/bin/env python3
"""Copy allowlisted MIT-licensed Skill files from upstream without copying restricted image assets."""
import json
import re
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "library" / "skills"
ROOT_FILES = ("SKILL.md", "README.md", "README.zh.md", "REFERENCES.md", "CHANGELOG.md", "LICENSE", "ASSET-LICENSE.md")
SUBDIRS = ("design-system", "scripts", "swatches")
EXTENSIONS = {".md", ".json", ".py", ".svg", ".txt", ".yml", ".yaml"}
MAX_SIZE = 2_000_000

def git(*argv):
    return subprocess.check_output(["git", *argv], text=True).strip()

def update_files(source, dest):
    for filename in ROOT_FILES:
        src = source / filename
        dst = dest / filename
        if src.is_file():
            if src.stat().st_size > MAX_SIZE or src.is_symlink():
                raise ValueError(f"Unsafe upstream file: {src}")
            shutil.copy2(src, dst)
        elif dst.exists():
            dst.unlink()
    for subdir in SUBDIRS:
        src = source / subdir
        dst = dest / subdir
        if dst.exists():
            shutil.rmtree(dst)
        if not src.is_dir():
            continue
        for file in src.rglob("*"):
            if file.is_symlink():
                raise ValueError(f"Symlink rejected: {file}")
            if not file.is_file():
                continue
            if file.suffix.lower() not in EXTENSIONS or file.stat().st_size > MAX_SIZE:
                raise ValueError(f"Disallowed upstream file: {file}")
            out = dst / file.relative_to(src)
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, out)

def sync(folder):
    path = folder / "upstream.json"
    conf = json.loads(path.read_text(encoding="utf-8"))
    url = conf["url"].rstrip("/")
    branch = conf.get("branch", "main")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", url):
        raise ValueError("Only trusted github.com repository URLs may be synced")
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", branch):
        raise ValueError("Invalid Git branch")
    mode = conf.get("sync_mode", "allowlisted-mit-text")
    if mode == "link-only":
        # Track the latest upstream commit without copying unlicensed source files.
        output = git("ls-remote", "--heads", url + ".git", branch)
        matches = [line.split()[0] for line in output.splitlines() if line.strip()]
        if len(matches) != 1 or not re.fullmatch(r"[0-9a-f]{40}", matches[0]):
            raise ValueError(f"{folder.name}: cannot resolve upstream branch")
        sha = matches[0]
        if sha == conf.get("sha"):
            print(f"{folder.name}: external source unchanged ({sha[:12]})")
            return False
        conf["sha"] = sha
        conf["last_synced"] = date.today().isoformat()
        path.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{folder.name}: upstream link updated ({sha[:12]}); no source files mirrored")
        return True
    if mode == "approved-text-mirror":
        # User-confirmed redistribution permission; retain upstream license notices.
        # Only mirror text, config and scripts; never execute upstream code or copy art.
        allowed_roots = ("SKILL.md", "README.md", "LICENSE", "LICENSE.md", "COMMERCIAL.md")
        allowed_dirs = ("agents", "references", "scripts")
        allowed_ext = EXTENSIONS | {".toml", ".sh", ".js", ".ts"}
        with tempfile.TemporaryDirectory() as tmp:
            upstream = Path(tmp) / "upstream"
            subprocess.run([
                "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                "--single-branch", "--branch", branch, url + ".git", str(upstream)
            ], check=True)
            subprocess.run(["git", "-C", str(upstream), "sparse-checkout", "set", *allowed_dirs], check=True)
            sha = git("-C", str(upstream), "rev-parse", "HEAD")
            if sha == conf.get("sha"):
                print(f"{folder.name}: already current ({sha[:12]})")
                return False
            if not (upstream / "SKILL.md").is_file():
                raise ValueError(f"{folder.name}: upstream SKILL.md missing")
            for filename in allowed_roots:
                src, dst = upstream / filename, folder / filename
                if src.is_symlink():
                    raise ValueError(f"Symlink rejected: {src}")
                if src.is_file():
                    if src.stat().st_size > MAX_SIZE:
                        raise ValueError(f"File too large: {src}")
                    shutil.copy2(src, dst)
                elif dst.exists():
                    dst.unlink()
            for dirname in allowed_dirs:
                src, dst = upstream / dirname, folder / dirname
                if dst.exists():
                    shutil.rmtree(dst)
                if not src.is_dir():
                    continue
                for file in src.rglob("*"):
                    if file.is_symlink():
                        raise ValueError(f"Symlink rejected: {file}")
                    if not file.is_file() or file.suffix.lower() not in allowed_ext:
                        continue
                    if file.stat().st_size > MAX_SIZE:
                        raise ValueError(f"File too large: {file}")
                    output = dst / file.relative_to(src)
                    output.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, output)
            conf["sha"] = sha
            conf["last_synced"] = date.today().isoformat()
            path.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{folder.name}: synced approved upstream text ({sha[:12]}); artwork excluded")
            return True
    if mode != "allowlisted-mit-text":
        raise ValueError(f"{folder.name}: unsupported sync mode {mode}")
    with tempfile.TemporaryDirectory() as tmp:
        upstream = Path(tmp) / "upstream"
        subprocess.run([
            "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
            "--single-branch", "--branch", branch, url + ".git", str(upstream)
        ], check=True)
        subprocess.run(["git", "-C", str(upstream), "sparse-checkout", "set", *SUBDIRS], check=True)
        sha = git("-C", str(upstream), "rev-parse", "HEAD")
        if sha == conf.get("sha"):
            print(f"{folder.name}: already current ({sha[:12]})")
            return False
        license_file = upstream / "LICENSE"
        if not license_file.exists() or "MIT License" not in license_file.read_text(encoding="utf-8"):
            raise ValueError(f"{folder.name}: upstream license not recognized as MIT")
        if not (upstream / "SKILL.md").exists():
            raise ValueError(f"{folder.name}: upstream SKILL.md missing")
        update_files(upstream, folder)
        conf["sha"] = sha
        conf["last_synced"] = date.today().isoformat()
        path.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{folder.name}: synced {sha[:12]} (restricted original artwork excluded)")
        return True

def main():
    if not SKILLS.exists():
        return
    for folder in sorted(SKILLS.iterdir()):
        if folder.is_dir() and (folder / "upstream.json").is_file():
            sync(folder)

if __name__ == "__main__":
    main()
