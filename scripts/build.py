#!/usr/bin/env python3
"""Build an app's llm-wiki package from the platform-neutral core.

    core/skills/            the wiki: written once, for no app in particular
    platforms/<app>/        what makes it that app's package:
      platform.json           vocabulary, where the package goes, how the voice profiler ships
      files/                  copied into the package as-is (manifest, hooks)
      CHANGELOG.md            that package's own history and version line

Core text marks what differs between apps in three ways, all resolved here:

    {{@name}}                         a vocabulary term, from platform.json "vocab"
    {{@claude:text}}                  text that only one app's package keeps (inline)
    <!-- @if chatgpt --> … <!-- @endif -->   whole lines that only one app's package keeps

Plain {{NAME}} placeholders are not ours: setup fills them in a user's folder, so they pass through.

    python3 scripts/build.py claude            # rebuild plugins/llm-wiki
    python3 scripts/build.py chatgpt --check   # fail if the committed package is stale
    python3 scripts/build.py all --out DIR     # build both under DIR (CI uses this to validate core)
"""
import argparse, filecmp, json, re, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "core" / "skills"
PLATFORMS = ROOT / "platforms"
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".html", ".txt", ".json"}

BLOCK = re.compile(r"^<!-- @if (\w+) -->\n(.*?)^<!-- @endif -->\n", re.S | re.M)
INLINE = re.compile(r"\{\{@(\w+):(.*?)\}\}", re.S)
TERM = re.compile(r"\{\{@(\w+)\}\}")


def platforms():
    return sorted(p.name for p in PLATFORMS.iterdir() if (p / "platform.json").exists())


def render(text, app, vocab, where):
    known = set(platforms())

    def block(m):
        if m.group(1) not in known:
            raise SystemExit(f"{where}: unknown app in '@if {m.group(1)}'")
        return m.group(2) if m.group(1) == app else ""

    def inline(m):
        if m.group(1) not in known:
            raise SystemExit(f"{where}: unknown app in '{{{{@{m.group(1)}:…}}}}'")
        return m.group(2) if m.group(1) == app else ""

    def term(m):
        if m.group(1) not in vocab:
            raise SystemExit(f"{where}: '{m.group(0)}' is not in platforms/{app}/platform.json")
        return vocab[m.group(1)]

    text = BLOCK.sub(block, text)
    text = INLINE.sub(inline, text)
    text = TERM.sub(term, text)
    if "{{@" in text or "<!-- @if" in text or "<!-- @endif" in text:
        raise SystemExit(f"{where}: unresolved build marker")
    return text


def build(app, out):
    conf = json.loads((PLATFORMS / app / "platform.json").read_text())
    vocab = conf["vocab"]
    if out.exists():
        shutil.rmtree(out)

    for f in sorted(CORE.rglob("*")):
        if f.is_dir() or f.name == ".DS_Store":
            continue
        rel = f.relative_to(CORE)
        if rel.parts[0] == "voice-profiler":
            continue
        if rel.name == "INSTRUCTIONS.md" and rel.parent.name == "templates":
            rel = rel.with_name(vocab["instructions_file"])
        dest = out / "skills" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix in TEXT_SUFFIXES:
            dest.write_text(render(f.read_text(encoding="utf-8"), app, vocab, rel), encoding="utf-8")
        else:
            shutil.copy2(f, dest)

    # The voice profiler: an agent where the app packages agents, a skill where it does not.
    vp = conf["voice_profiler"]
    text = render((CORE / "voice-profiler" / "SKILL.md").read_text(encoding="utf-8"), app, vocab,
                  "voice-profiler/SKILL.md")
    m = re.match(r"(---\n.*?\n)(---\n)", text, re.S)
    extra = "".join(f"{k}: {v}\n" for k, v in vp.get("frontmatter", {}).items())
    text = m.group(1) + extra + m.group(2) + text[m.end():]
    dest = out / ("agents/voice-profiler.md" if vp["as"] == "agent" else "skills/voice-profiler/SKILL.md")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")

    files = PLATFORMS / app / "files"
    for f in sorted(files.rglob("*")):
        if f.is_file() and f.name != ".DS_Store":
            dest = out / f.relative_to(files)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
    return conf


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b, ignore=[".DS_Store"])
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    if any(not filecmp.cmp(Path(a) / n, Path(b) / n, shallow=False) for n in cmp.common_files):
        return False
    return all(same_tree(Path(a) / d, Path(b) / d) for d in cmp.common_dirs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app", help="an app under platforms/, or 'all'")
    ap.add_argument("--out", type=Path, help="build here instead of the app's package_dir")
    ap.add_argument("--check", action="store_true", help="fail if the committed package is stale")
    args = ap.parse_args()
    apps = platforms() if args.app == "all" else [args.app]
    for app in apps:
        if app not in platforms():
            sys.exit(f"no platforms/{app}/platform.json")
        package_dir = ROOT / json.loads((PLATFORMS / app / "platform.json").read_text())["package_dir"]
        if args.check:
            with tempfile.TemporaryDirectory() as tmp:
                build(app, Path(tmp) / "pkg")
                if not package_dir.exists() or not same_tree(Path(tmp) / "pkg", package_dir):
                    sys.exit(f"{package_dir.relative_to(ROOT)} is stale: run scripts/build.py {app} and commit it.")
            print(f"{package_dir.relative_to(ROOT)} is up to date")
        else:
            out = args.out / app if args.out else package_dir
            build(app, out)
            print(f"built {app} -> {out}")


if __name__ == "__main__":
    main()
