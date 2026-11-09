# Working in this repository

This repo is **llm-wiki** — a plugin that turns a folder into a self-maintaining knowledge base, packaged
for **Claude** and for **ChatGPT**. It is published open-source at `mauricio-morales/llm-wiki` and
installed by others.

**Nearly nothing here is code.** The product is prompt content: Markdown skills, Markdown templates, one
HTML report shell, one shell hook. The one script, `scripts/build.py`, assembles each app's package from
that content. There are no dependencies and no test suite, so **you cannot run a change to find out
whether it works**. The only real test is
installing it and running a setup against a throwaway folder. Bear that in mind before a change that
"obviously" works.

## This file is the development one. There is another, and it is not this.

**`./CLAUDE.md` — the file you are reading — is for working on the plugin.** It is never shipped: the
packages are built from `core/` and `platforms/`, and the release workflows add only `README.md`, the
app's changelog and `LICENSE`. Nobody who installs the plugin ever sees this.

This is the single easiest thing to get wrong here, because the plugin's whole job is to *write* a
CLAUDE.md into someone else's folder.

- **The plugin** — this repo. What gets published and installed.
- **A wiki** — what the plugin *creates* in a user's folder, from the templates in
  `core/skills/wiki-setup/templates/`.

So there are two instruction files and they are unrelated:

| File | What it is |
|---|---|
| `./CLAUDE.md` | **This file.** Instructions for working in this repo. Never shipped. |
| `core/skills/wiki-setup/templates/INSTRUCTIONS.md` | A **template**. Built into `CLAUDE.md` for Claude and `AGENTS.md` for ChatGPT; setup fills it in and writes it into a user's wiki folder, where it tells their sessions how to behave. |

Before editing either, check which one the request is actually about. **"Add a rule to CLAUDE.md" almost
always means the template** — the behavior users get — not this file. A rule meant for users that lands
here reaches nobody; a development note that lands in the template ships to everyone.

### This folder is not a wiki

If the llm-wiki plugin is installed while you work here, its skills may look relevant. They are not:
there is no `llm-wiki.yml` and no `Wiki/` here, because this repo is the plugin, not a wiki made by it.
The engine skill should decline, and the SessionStart hook stays silent by design. Do not run
`/wiki-setup` in this repo — it would scaffold a wiki on top of the source.

## Spec Kit is installed here — and it means three different `skills` directories

This repo has [Spec Kit](https://github.com/github/spec-kit) (v0.8.9) installed for developing the
plugin. `.specify/` and `.claude/skills/speckit-*` are its files, committed deliberately so the workflow
is reproducible.

**They are tooling, not product.** They do not ship: packages are built only from `core/` and
`platforms/`, so nothing under `.specify/` or `.claude/` reaches a user.

That leaves several directories with "skills" in the path. Confusing them is the most likely way to break
something here:

| Path | What it is | Ships? |
|---|---|---|
| `core/skills/` | **The product.** `wiki`, `wiki-setup`, `voice-profiler`, written for no app in particular. Edit here. | Yes, through the build |
| `core/skills/wiki-setup/templates/` | Templates written into a *user's* wiki folder — including a copy of the engine skill. | Yes, as templates |
| `plugins/llm-wiki*/skills/` | **Generated** packages. Overwritten by every build. Never edit. | They are what ships |
| `.claude/skills/speckit-*` | **Spec Kit's** commands for working in this repo. Nothing to do with the plugin. | No |

Editing a `speckit-*` skill changes how you work on the plugin. Editing `core/skills/wiki/SKILL.md`
changes the plugin. They look alike in a file listing and are completely unrelated.

Spec Kit is also configured with `context_file: CLAUDE.md` (see `.specify/init-options.json`), so its
commands may read and update **this file**. If a Spec Kit command rewrites sections here, check that it
has not flattened the distinctions above — they are the thing this file exists to preserve.

## Layout

**The wiki is written once, in `core/`, and built into one package per app.** Everything else in this repo
is development tooling that must never reach a user.

```
core/skills/                       <- THE PRODUCT. Edit here.
  wiki/SKILL.md                      the engine: query, ingest, prune, lint, status, import
  wiki-setup/SKILL.md                the setup wizard — the only command a user types
  wiki-setup/references/             loaded by the wizard on demand: source catalog, backfill
                                     protocol, scheduled-task templates, update/merge protocol
  wiki-setup/templates/              what gets written into a user's folder (INSTRUCTIONS.md becomes
                                     CLAUDE.md or AGENTS.md)
  voice-profiler/SKILL.md            builds the owner's email voice (an agent on Claude, a skill on ChatGPT)

platforms/<app>/                   what makes it that app's package
  platform.json                      vocabulary, package directory, how the voice profiler ships
  files/                             copied in as-is: the manifest (holds the version), Claude's hook
  CHANGELOG.md                       that package's history

scripts/build.py                   core/ + platforms/<app>/ -> plugins/<package>/
plugins/llm-wiki/                  GENERATED Claude package (committed: the marketplace installs it)
plugins/llm-wiki-chatgpt/          GENERATED ChatGPT package (committed, same reason)
.claude-plugin/marketplace.json    Claude's marketplace; points at ./plugins/llm-wiki
.agents/plugins/marketplace.json   ChatGPT's marketplace; points at ./plugins/llm-wiki-chatgpt
.github/workflows/                 release.yml (v* tags, Claude), release-chatgpt.yml (chatgpt-v* tags),
                                   check.yml (every push: core/ builds for every app)
docs/setup-claude.md, docs/setup-chatgpt.md   the per-app setup pages the README links to
README.md LICENSE CHANGELOG.md     repo root; CHANGELOG.md only points at the two app changelogs
CLAUDE.md                          this file — development only, never shipped
.specify/ .claude/                 Spec Kit tooling — development only, never shipped
```

**Why packages live in subdirectories:** a package's root is what an installer sees. When the repo root
was the plugin root, everything beside it — Spec Kit's `.specify/` and `.claude/skills/speckit-*` — sat
inside the plugin's boundary. Nesting makes the separation structural, and the release workflows fail the
build if dev tooling ever appears in a zip.

**Anything added to the repo root is development tooling by default.** If a new file should reach users,
it belongs in `core/` (every app) or `platforms/<app>/files/` (one app).

`references/` holds detail the wizard reads on demand, keeping `SKILL.md` navigable. When a section grows
past roughly a screen and is only needed in one phase, move it to `references/` and link it.

## Writing for every app at once

Core text says what the wiki does, not which app it runs in. Where an app matters, use the build markers
(full syntax at the top of `scripts/build.py`):

- **`{{@term}}`** for a word or phrase each app says differently: `{{@instructions_file}}` (CLAUDE.md /
  AGENTS.md), `{{@dot_dir}}`, `{{@ask_tool}}`, `{{@the_app}}`, `{{@setup_command}}`… Every app's
  `platform.json` must define every term; the build fails otherwise.
- **`{{@claude:…}}`** for a short phrase only one app keeps.
- **`<!-- @if chatgpt -->` … `<!-- @endif -->`** for whole lines only one app keeps: a procedure that
  differs, like how a scheduled task is created in ChatGPT.

Plain `{{PLACEHOLDERS}}` are not build markers: setup fills them in the user's folder.

**Never name an app, its menus or its tools in plain core text.** Writing "`AskUserQuestion`" or "the
Claude app" straight into `core/` ships a Claude instruction to ChatGPT. Grep the ChatGPT package for
`Claude`, `CLAUDE`, `Cowork` after a change; the only expected hit is an upstream author's repo name in
the voice profiler's credits.

**The Claude package must not change by accident.** After editing core, `python3 scripts/build.py claude
--check` shows whether the Claude package differs from what is committed. Differences you didn't intend
are a marker mistake.

## Releasing

**Releases happen on tag. Nothing else publishes.** Pushing to `main` publishes nothing; `check.yml` only
builds every package into a scratch directory to catch a broken `core/`.

**Each app is released separately, with its own version.** `v*` tags release Claude; `chatgpt-v*` tags
release ChatGPT. A change in `core/` reaches each app at that app's next release. **A committed package is
rebuilt only when that app is released**, so between releases it stays the last released snapshot and
matches its own version number. Don't run `scripts/build.py` for an app you aren't releasing.

1. Land changes in `core/` (or `platforms/<app>/`) on `main`, with an entry under `## Unreleased` in each
   affected app's `platforms/<app>/CHANGELOG.md`. Every user-facing change gets one, written as what
   changed and **why it mattered** — a reader deciding whether to update needs the consequence, not the diff.
2. To release an app, in one commit:
   - Bump its version: **Claude** in both `platforms/claude/files/.claude-plugin/plugin.json` **and**
     `.claude-plugin/marketplace.json` (they drift silently; CI fails the release if they disagree).
     **ChatGPT** in `platforms/chatgpt/files/plugin.json`.
   - Rename `## Unreleased` to `## X.Y.Z — YYYY-MM-DD`.
   - Run `python3 scripts/build.py <app>` and commit the rebuilt package.
3. Tag and push: `git tag vX.Y.Z` (Claude) or `git tag chatgpt-vX.Y.Z` (ChatGPT).
4. CI verifies the tag against the manifest, that the committed package matches `core/` (`--check`),
   builds the zip and publishes the release. ChatGPT releases are never marked "latest", so
   `/releases/latest` stays the Claude plugin, whose zip the Claude setup page links to.
5. Verify by downloading the published asset, not by trusting the green tick.

**Versioning**: patch for wording and fixes; minor for new behavior; major for anything that changes how a
wiki is set up or invalidates an existing one.

**How each app installs it.** Claude: the repo's Claude marketplace, or the release zip uploaded in the
app. ChatGPT: a workspace admin imports this repository once (Admin → Plugins → Import marketplace),
which reads `.agents/plugins/marketplace.json`; users then add it from Plugins.

**Never commit a zip.** It is generated, so a committed copy goes stale on the next edit. `.gitignore`
excludes it.

Repo-internal changes that do not ship — this file, workflow tweaks, the build script — need no version
bump and no CHANGELOG entry.

## Conventions that are not negotiable

**No personal or organizational specifics.** This plugin is deliberately generic; the wizard learns who
the user is from their connectors and environment. Examples use fictional names and `example.com`. This
rule exists because it was broken once: guidance written from one person's calendar habits ("many people
keep a standing evening block") taught the model to go hunting for that pattern in everyone's calendar.
The fix was to make the rule structural — coverage of the working day, never entry names. **Prefer rules
that hold for any user over rules describing how one user works.**

**Attribution is a license obligation, not a courtesy.** Substantial parts — the L1/L2 architecture,
hub-index routing, LRU-demote, and the schema/hub/dashboard/access-log templates — derive from
[llm-wiki](https://github.com/MehmetGoekce/llm-wiki) by Mehmet Gökçe, MIT. `LICENSE` reproduces that
notice and must keep doing so. Credits appear in the README, both skills, both app CHANGELOG headers and
the generated `Wiki/Schema.md`. Do not thin them out.

**Every `{{PLACEHOLDER}}` must be filled by setup.** A template shipped with one still in it is a silent,
permanent bug — a task prompt containing `{{SKIP_LOGIC}}` does not error, it just behaves strangely every
night forever. `core/skills/wiki-setup/SKILL.md` carries a checklist and a final grep; add to it when you add a
placeholder.

**The generated wiki has no version control.** Its rules follow from that and must not be softened:
append never overwrite, never delete a page outside an explicit instruction, never run git in a user's
wiki folder.

**Users personalize their folder's `CLAUDE.md` / `AGENTS.md` and `Wiki/Schema.md`, never the skill files** — those are replaced by
updates. If a change would invite someone to edit a skill file in their folder, it belongs somewhere else.

## New optional features must be registered

Any feature that only exists if the owner switches it on — like Focus Areas, Objectives, news — gets a row
in `core/skills/wiki-setup/references/features.md`, **in the release that ships it**, with the
Claude version it shipped in.

That registry is the only way an upgrade knows a feature exists. Leave it out and every wiki set up before
that release never hears about the feature — and the fallback is a recommendation in a closing paragraph,
which in practice nobody reads. Upgrades ask about registered features as real questions.

## Writing style for skill content

These files are read by a model as instructions, and they are long. What works here:

- **Say why, not just what.** A rule with its reason survives contact with a situation it did not
  anticipate; a bare imperative gets pattern-matched and misapplied.
- **Name the failure the rule prevents**, concretely, ideally with the real case that motivated it. The
  routing, skip-logic and double-routing sections all read this way and it is deliberate.
- **State the default and the exception separately.** "File it, and ask only when X" beats a paragraph of
  hedging.
- **Prefer a worked ❌/✅ example over more prose** where a rule is about judgment rather than mechanics.
