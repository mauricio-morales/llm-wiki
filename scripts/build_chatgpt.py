#!/usr/bin/env python3
"""Build the ChatGPT package of llm-wiki from the Claude plugin.

The Claude plugin (plugins/llm-wiki) is the only source. This script translates it into
plugins/llm-wiki-chatgpt, which is committed so ChatGPT can install it from the repo's marketplace
(.agents/plugins/marketplace.json). Never edit plugins/llm-wiki-chatgpt by hand: change the Claude
source or platforms/chatgpt/, then rebuild.

The committed copy is refreshed only when the ChatGPT package is released, so between releases it is
the last released snapshot and always matches its own version number.

    python3 scripts/build_chatgpt.py            # rebuild plugins/llm-wiki-chatgpt
    python3 scripts/build_chatgpt.py --check    # fail if the committed copy is stale
    python3 scripts/build_chatgpt.py --out DIR  # build somewhere else
"""
import argparse, filecmp, json, re, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "plugins" / "llm-wiki"
PLAT = ROOT / "platforms" / "chatgpt"
DEFAULT_OUT = ROOT / "plugins" / "llm-wiki-chatgpt"

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".html", ".txt", ".json"}
RELEASES = "https://github.com/mauricio-morales/llm-wiki/releases"

# Ordered: earlier rules see the text before later ones.
REPLACEMENTS = [
    ("this plugin's `agents/voice-profiler.md`", "this plugin's `voice-profiler` skill"),
    ("a `CLAUDE.md`", "an `AGENTS.md`"),
    ("a CLAUDE.md", "an AGENTS.md"),
    ("CLAUDE.md", "AGENTS.md"),
    (re.compile(r"\.claude(?![-\w])"), ".agents"),
    ("Cowork session", "ChatGPT desktop session"),
    ("**Cowork** → **Customize** → **Plugins**", "**Plugins**"),
    ("Cowork → Customize → Plugins", "Plugins"),
    ("Customize → Plugins", "Plugins"),
    ("the Claude app", "the ChatGPT desktop app"),
    ("Claude's own", "ChatGPT's own"),
    ("Claude Memory", "ChatGPT Memory"),
    ("Claude's memory", "ChatGPT's memory"),
    ("Claude must know", "ChatGPT must know"),
    ("in a Claude session", "in a chat session"),
    (re.compile(r"(?<![\w/-])/wiki-setup"), "@wiki-setup"),
    (f"{RELEASES}/latest", f"{RELEASES}/tag/chatgpt-latest"),
]

SKILL_HEADER = """> **Running in ChatGPT.** This skill was written for Claude and translated. Read `PLATFORM.md` in this
> skill's folder before acting: it says what the remaining Claude-specific terms mean here, and it wins
> wherever the two disagree.

"""

TASK_NOTE = ("Running in ChatGPT: first read `.agents/skills/wiki/PLATFORM.md` (or `PLATFORM.md` in the "
             "installed `wiki` skill). It says what this prompt's scheduler and question terms mean "
             "in ChatGPT.\n")

# Words that should not survive translation. PLATFORM.md is exempt: it names them on purpose.
FORBIDDEN = ["CLAUDE.md", ".claude/", "Cowork", "AskUserQuestion is a tool"]


def translate(text):
    for old, new in REPLACEMENTS:
        text = old.sub(new, text) if isinstance(old, re.Pattern) else text.replace(old, new)
    return text


def add_skill_header(text):
    """Insert the header right after the SKILL.md frontmatter."""
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    if not m:
        raise SystemExit("SKILL.md without frontmatter")
    return text[: m.end()] + "\n" + SKILL_HEADER + text[m.end():].lstrip("\n")


def add_task_note(text):
    """A task template's prompt opens with its stamp; the note goes on the line after it."""
    return re.sub(r"^(<!-- llm-wiki task: .*\{\{PLUGIN_VERSION\}\}.*-->\n)", r"\1\n" + TASK_NOTE,
                  text, flags=re.M)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build(out):
    version = json.loads((PLAT / "plugin.json").read_text())["version"]
    if out.exists():
        shutil.rmtree(out)
    skills_out = out / "skills"

    # The two skills, translated file by file.
    for skill in ("wiki", "wiki-setup"):
        for f in sorted((SRC / "skills" / skill).rglob("*")):
            if f.is_dir() or f.name == ".DS_Store":
                continue
            rel = f.relative_to(SRC / "skills")
            if rel.name == "CLAUDE.md":
                rel = rel.with_name("AGENTS.md")
            dest = skills_out / rel
            if f.suffix not in TEXT_SUFFIXES:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                continue
            text = translate(f.read_text(encoding="utf-8"))
            if rel.name == "SKILL.md":
                text = add_skill_header(text)
            if rel.parent.name == "references" and rel.name.startswith("task-"):
                text = add_task_note(text)
            write(dest, text)

    # The voice-profiler subagent becomes a skill: ChatGPT plugins carry skills, not agents.
    agent = (SRC / "agents" / "voice-profiler.md").read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", agent, re.S)
    keep = [l for l in m.group(1).splitlines() if l.split(":", 1)[0] in ("name", "description")]
    voice = "---\n" + "\n".join(keep) + "\n---\n" + agent[m.end():]
    write(skills_out / "voice-profiler" / "SKILL.md", add_skill_header(translate(voice)))

    # Every skill carries the platform page, so it works even when a skill is installed on its own.
    platform = (PLAT / "PLATFORM.md").read_text(encoding="utf-8")
    for skill in ("wiki", "wiki-setup", "voice-profiler"):
        write(skills_out / skill / "PLATFORM.md", platform)
    write(skills_out / "wiki-setup" / "VERSION", version + "\n")

    shutil.copy2(PLAT / "plugin.json", out / "plugin.json")
    # Hooks are deliberately not shipped: ChatGPT asks the user to trust each one, and AGENTS.md covers it.

    leftovers = []
    for f in out.rglob("*"):
        if f.is_file() and f.suffix in TEXT_SUFFIXES and f.name != "PLATFORM.md":
            body = f.read_text(encoding="utf-8")
            leftovers += [f"{f.relative_to(out)}: {w}" for w in FORBIDDEN if w in body]
    if leftovers:
        raise SystemExit("Untranslated Claude terms:\n  " + "\n  ".join(leftovers))
    return version


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    # dircmp compares shallowly; compare contents to be sure.
    for name in cmp.common_files:
        if not filecmp.cmp(Path(a) / name, Path(b) / name, shallow=False):
            return False
    return all(same_tree(Path(a) / d, Path(b) / d) for d in cmp.common_dirs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="fail if the committed package is stale")
    args = ap.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            build(Path(tmp) / "pkg")
            if not DEFAULT_OUT.exists() or not same_tree(Path(tmp) / "pkg", DEFAULT_OUT):
                sys.exit("plugins/llm-wiki-chatgpt is stale: run scripts/build_chatgpt.py and commit it.")
        print("plugins/llm-wiki-chatgpt is up to date")
        return
    version = build(args.out)
    print(f"built llm-wiki for ChatGPT {version} -> {args.out}")


if __name__ == "__main__":
    main()
