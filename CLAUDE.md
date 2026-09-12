# Working in this repository

This repo is **the llm-wiki plugin** — a Claude Code plugin that turns a folder into a self-maintaining
knowledge base. It is published open-source at `mauricio-morales/llm-wiki` and installed by others.

**Nothing here is code.** Every file is prompt content: Markdown skills, Markdown templates, one HTML
report shell, one shell hook. There is no build, no dependencies, and no test suite. A change is a text
edit — which also means **you cannot run it to find out whether it works**. The only real test is
installing it and running a setup against a throwaway folder. Bear that in mind before a change that
"obviously" works.

## This file is the development one. There is another, and it is not this.

**`./CLAUDE.md` — the file you are reading — is for working on the plugin.** It is never shipped: the
release workflow copies `.claude-plugin`, `skills`, `hooks`, `README.md`, `CHANGELOG.md` and `LICENSE`,
and nothing else. Nobody who installs the plugin ever sees this.

This is the single easiest thing to get wrong here, because the plugin's whole job is to *write* a
CLAUDE.md into someone else's folder.

- **The plugin** — this repo. What gets published and installed.
- **A wiki** — what the plugin *creates* in a user's folder, from the templates in
  `skills/wiki-setup/templates/`.

So there are two `CLAUDE.md` files and they are unrelated:

| File | What it is |
|---|---|
| `./CLAUDE.md` | **This file.** Instructions for working in this repo. Never shipped — the release workflow does not copy it. |
| `skills/wiki-setup/templates/CLAUDE.md` | A **template**. Setup fills it in and writes it into a user's wiki folder, where it tells their sessions how to behave. |

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

**They are tooling, not product.** They do not ship: the release workflow copies `.claude-plugin`,
`skills`, `hooks`, `README.md`, `CHANGELOG.md` and `LICENSE`, so nothing under `.specify/` or `.claude/`
reaches a user.

That leaves three directories with "skills" in the path. Confusing them is the most likely way to break
something here:

| Path | What it is | Ships? |
|---|---|---|
| `skills/` | **The plugin's skills.** The product. `wiki` and `wiki-setup`. | Yes |
| `skills/wiki-setup/templates/` | Templates written into a *user's* wiki folder — including a copy of the engine skill. | Yes, as templates |
| `.claude/skills/speckit-*` | **Spec Kit's** commands for working in this repo. Nothing to do with the plugin. | No |

Editing a `speckit-*` skill changes how you work on the plugin. Editing `skills/wiki/SKILL.md` changes
the plugin. They look alike in a file listing and are completely unrelated.

Spec Kit is also configured with `context_file: CLAUDE.md` (see `.specify/init-options.json`), so its
commands may read and update **this file**. If a Spec Kit command rewrites sections here, check that it
has not flattened the distinctions above — they are the thing this file exists to preserve.

## Layout

```
.claude-plugin/plugin.json       the plugin manifest
.claude-plugin/marketplace.json  makes this repo installable as a marketplace (source: "./")
skills/wiki/SKILL.md             the engine: query, ingest, prune, lint, status, import
skills/wiki-setup/SKILL.md       the setup wizard — the only command a user types
skills/wiki-setup/references/    loaded by the wizard as needed: source catalog, backfill protocol,
                                 the scheduled-task prompt templates, update/merge protocol
skills/wiki-setup/templates/     what gets written into a user's folder
.github/workflows/release.yml    builds the zip on tag, attaches it to a Release
```

`references/` holds detail the wizard reads on demand, keeping `SKILL.md` navigable. When a section grows
past roughly a screen and is only needed in one phase, move it to `references/` and link it.

## Releasing

**Releases happen on tag. Nothing else publishes.** Pushing to `main` publishes nothing.

1. Land changes on `main` with an entry under `## Unreleased` in `CHANGELOG.md`. Every user-facing change
   gets one, written as what changed and **why it mattered** — a reader deciding whether to update needs
   the consequence, not the diff.
2. When ready to cut a release, in one commit:
   - Bump `version` in **both** `.claude-plugin/plugin.json` **and** `.claude-plugin/marketplace.json`.
     They are separate files and drift silently; CI fails the release if they disagree.
   - Rename `## Unreleased` to `## X.Y.Z — YYYY-MM-DD`.
3. `git tag -a vX.Y.Z -m "..."` and `git push origin vX.Y.Z`.
4. CI verifies the tag matches both manifests, builds the zip, and publishes the Release.
5. Verify by downloading the published asset, not by trusting the green tick.

**Versioning**: patch for wording and fixes; minor for new behavior; major for anything that changes how a
wiki is set up or invalidates an existing one.

**Never commit the zip.** It is generated from this repo, so a committed copy duplicates the source and
goes stale on the next edit. `.gitignore` excludes it.

Repo-internal changes that do not ship — this file, workflow tweaks — need no version bump and no
CHANGELOG entry.

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
notice and must keep doing so. Credits appear in the README, both skills, the CHANGELOG header and the
generated `Wiki/Schema.md`. Do not thin them out.

**Every `{{PLACEHOLDER}}` must be filled by setup.** A template shipped with one still in it is a silent,
permanent bug — a task prompt containing `{{SKIP_LOGIC}}` does not error, it just behaves strangely every
night forever. `skills/wiki-setup/SKILL.md` carries a checklist and a final grep; add to it when you add a
placeholder.

**The generated wiki has no version control.** Its rules follow from that and must not be softened:
append never overwrite, never delete a page outside an explicit instruction, never run git in a user's
wiki folder.

**Users personalize `CLAUDE.md` and `Wiki/Schema.md`, never the skill files** — those are replaced by
updates. If a change would invite someone to edit a skill file in their folder, it belongs somewhere else.

## Writing style for skill content

These files are read by a model as instructions, and they are long. What works here:

- **Say why, not just what.** A rule with its reason survives contact with a situation it did not
  anticipate; a bare imperative gets pattern-matched and misapplied.
- **Name the failure the rule prevents**, concretely, ideally with the real case that motivated it. The
  routing, skip-logic and double-routing sections all read this way and it is deliberate.
- **State the default and the exception separately.** "File it, and ask only when X" beats a paragraph of
  hedging.
- **Prefer a worked ❌/✅ example over more prose** where a rule is about judgment rather than mechanics.
