# Staying current — updating the folder's copy of the skills

## The problem

Setup copies the skills into `<wiki folder>/.claude/skills/` so the folder works on its own: sync it and
a teammate needs nothing installed. The cost is a fork. From that moment the folder's copy can drift two
ways at once — the published plugin moves forward, and the local copy gets personalized — and a naive
"just overwrite it" destroys the second while a naive "leave it alone" throws away the first.

## Keep personalizations out of the skill files

**The best fix is to not create the conflict.** The folder already has two files that are yours, that
setup never overwrites, and that every session reads:

- **`CLAUDE.md`** — how this wiki should behave. Standing instructions, house rules, exceptions.
- **`Wiki/Schema.md`** — conventions, page types, privacy rules, the namespace list.

**Anything specific to this wiki belongs in one of those, not in `.claude/skills/`.** A rule written into
`CLAUDE.md` survives every update untouched and takes effect immediately; the same rule written into
`SKILL.md` is a merge conflict waiting to happen. When a user asks to change how the wiki behaves, change
`CLAUDE.md` — reach for the skill files only when the change genuinely belongs to the engine rather than
to this wiki.

Say this out loud when someone proposes editing a skill file directly. It is the difference between a
wiki that updates cleanly for years and one that is stranded on whatever version it was personalized on.

## The baseline

Setup writes the skills twice:

```
.claude/skills/wiki/SKILL.md            the live copy — what actually runs
.claude/skills/.baseline/wiki/SKILL.md  a pristine copy of exactly what was installed
.claude/skills/.llm-wiki-version        the version both came from
```

The baseline is never edited and never read at runtime. It exists so that an update can tell **local
edits** (baseline → live) apart from **upstream changes** (baseline → new version). Without it, the two
are indistinguishable and no safe merge is possible. It costs a few hundred KB of markdown.

## When to check

**No scheduled task.** The check rides along with normal work, throttled so it is nearly free:

- Only in a session where **the llm-wiki plugin is actually present** — that is the only place a newer
  version can be read from. A teammate who has the folder but no plugin gets updates through folder sync
  instead, and should never be prompted about this.
- At most **once every 7 days**. `lastUpdateCheck` in `llm-wiki.yml` records the last one.
- **Never at the start of a task.** Check after the user's actual request is finished, so an update notice
  never delays or derails what they asked for.
- **Never during a scheduled job.** An unattended run must not change the code it is running. Ingest,
  brief and lint skip this entirely.

The check itself is one file read: compare `skills_version` in `llm-wiki.yml` against the running
plugin's `plugin.json`. Same version, or the folder is newer — do nothing, silently, and update
`lastUpdateCheck`.

## Applying an update

**Only the `ingest_owner` applies updates to a shared wiki.** Anyone else who notices one says so and
leaves it; two people merging the same shared folder from different plugin versions is how a synced
folder ends up in conflict.

For each skill file, compare the live copy against the baseline:

**Unmodified locally** — the common case, and the easy one. Replace the file outright with the new
version, refresh the baseline, bump `skills_version`. No merge, no risk, nothing to ask about.

**Modified locally** — a real three-way merge:

1. Compute upstream's changes (baseline → new) and local changes (baseline → live).
2. Apply upstream changes that don't touch locally-modified sections. These land silently.
3. Where both changed the same section, **stop and show the user both versions** — do not guess. Prose
   merges cannot be resolved by heuristics the way code sometimes can, and a silently mis-merged
   instruction is worse than no update: it will be followed.
4. **Never drop a local change to take an upstream one.** If a conflict cannot be resolved, keep the local
   version, report that the file stayed behind, and say exactly which upstream change was not applied.
5. **Offer to relocate the personalization.** A local edit that is really a house rule belongs in
   `CLAUDE.md`, where it stops conflicting forever. Moving it is usually the right resolution, and it
   permanently retires that conflict.

Then update `skills_version`, `wiki_version`, `.llm-wiki-version` and the baseline together — all four, or
the next check reasons from stale information.

## What to say

Keep it to a line or two, after the work is done:

> Your wiki skills are on 1.6.0; 1.8.0 is available. It adds X and Y. Update? (Your two local changes to
> the ingest rules are preserved.)

One line, one question, and it does not come back for another 7 days if declined. **Never present this
before the user's actual request**, and never as a blocking prompt.

If an update was applied, say what changed in a sentence and note that **it takes effect in the next
session** — the current one is already running the old text.

## Never

- **Never update during a scheduled run.** A job that rewrites its own instructions mid-flight is
  unreviewable and unattributable when it misbehaves.
- **Never overwrite a locally-modified file** without showing the conflict.
- **Never touch `CLAUDE.md`, `Wiki/`, or anything outside `.claude/skills/`** as part of an update. Those
  are the user's, permanently.
- **Never downgrade.** If the folder is newer than the plugin, the folder wins — say so, so nobody
  "fixes" it backwards.
