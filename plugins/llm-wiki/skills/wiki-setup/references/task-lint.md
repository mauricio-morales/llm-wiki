# Template: the monthly lint task

---

<!-- llm-wiki task: {{TASK_KIND}} | template version: {{PLUGIN_VERSION}} | generated: {{DATE}} -->

## Before anything: is this the run?

This task is scheduled **every Saturday** (`0 9 * * 6`) so that it can run on the **first Saturday of the
month** — the weekend, when the owner is least likely to need their token budget for anything else.

Check `jobs.lint.schedule` in `llm-wiki.yml`:

- **It is the weekly-Saturday form** (day-of-week `6`, day-of-month `*`) → if today's day of the month is
  **greater than 7**, this is not the first Saturday. **Stop immediately and do nothing** — no reads, no
  update check, no report. A skipped week should cost effectively nothing.
- **It is anything else** — an older wiki still on `0 9 1 * *`, or a schedule the owner chose — **skip this
  check and run normally.** Updates never change a schedule, so a wiki set up before this default still
  fires on its old day; applying the first-Saturday test to it would make the lint silently never run.

Why not a single cron expression: `0 9 1-7 * 6` looks right and is not. When both day-of-month and
day-of-week are set, standard cron fires when **either** matches — so that expression runs on days 1–7
**and** every Saturday. First-Saturday cannot be expressed reliably in cron alone; the weekly schedule
plus this check is the portable way. **Do not "simplify" it back.**

## Step 0 — Adopt any pending update to this prompt

{{TASK_SELF_UPDATE}}

<!-- Setup fills this from references/task-self-update.md. Embed it in full — a scheduled run cannot
     read the reference file. -->

Run the LLM Wiki's health check on the wiki at `{{WIKI_PATH}}`.

Read `llm-wiki.yml` and `Wiki/Schema.md` first, then follow the `wiki` skill's `lint` workflow.

## What to run

1. **`lint {{LINT_FIX_FLAG}}`** — full scan: orphans, stale pages, missing properties, broken refs, hub
   completeness, index drift, missing index descriptions, archived-in-live-index, credential leaks,
   {{PRIVACY_LINT}} empty pages, cross-ref minimum, L1/L2 duplicates.

2. **`prune --months {{PRUNE_MONTHS}}`** — LRU-Demote. Evict cold pages from the live hub index so
   routing stays precise as the wiki grows. Demotion is **not** deletion: the page keeps its file, keeps
   every incoming link, and stays greppable; only its routing line moves from `### Index` to
   `### Archive`. Exempt hubs, Schema, Dashboard, the Access-Log and `status: active` projects.

   {{PRUNE_CONFIRM}}

3. **`status`** — metrics and the cache profile: hot pages, cold pages, live-index size per namespace,
   and the routing-transparency breakdown. A page repeatedly hit by the same grep term rather than by its
   index line is a page with a weak routing description — fix the description, that is the whole point of
   collecting the signal.

4. **Weight check** — total size of `Archives/` and of the wiki folder. Report the numbers every run so
   growth is visible early rather than as a surprise, and flag it sooner if the folder is synced, where
   every megabyte is copied to everyone who has it. Past ~200 MB in `Archives/`, list the largest
   snapshots and propose which to drop; re-archive an oversized page as a text-only snapshot rather than
   deleting the record outright.

   Report `Artifacts/` separately from `Archives/` — it is the folder that actually grows. List artifact
   folders past the `Safe to delete after` date in their `_about.md`, or older than six months and marked
   `Ingested: yes`. **Propose; never delete.** An artifact someone is midway through using looks exactly
   like a stale one, and one still linked from a live wiki page must never go without saying so — a dead
   link to evidence that used to exist is worse than a large folder.

   Flag any artifact folder **missing `_about.md`**, and anything sitting at the **wiki root** that is not
   `llm-wiki.yml`, `CLAUDE.md`, `Wiki/`, `Archives/`, `Artifacts/`, `.claude/` or a `wiki-*-state.json`.
   Root clutter is how a wiki folder becomes unusable, and it accumulates one stray file at a time.

   Also report any **sync conflict copies** in the folder (`... (X's conflicted copy).md`, `*.sync-conflict-*`).
   **Never delete one** — surface it and offer to merge the divergent sections back into the canonical
   page. A conflict copy usually means more than one machine is running the ingest, which is worth saying
   out loud.

5. **Ingest health** — read `wiki-ingest-state.json`. How old is `lastSuccessfulRun`? If it is more than
   a few days stale, the ingest job has been failing or not running, and that is the single most important
   line in this report. Also report any source that has been reporting itself unavailable run after run —
   a connector that quietly stopped working looks exactly like a quiet month.

6. **Version drift** — compare three things: `wiki_version` and `skills_version` in `llm-wiki.yml`, the
   line in `.claude/skills/.llm-wiki-version`, and the version of whatever llm-wiki plugin is running in
   this session (if one is).

   - Plugin **newer** than the folder copy → the folder is stale. Report it and say the fix: the wiki's
     owner re-runs `/wiki-setup` in reconfigure mode, which re-copies the skills and re-stamps them. On a
     synced wiki that one action updates everyone.
   - Folder copy **newer** than the plugin → this person's plugin is behind. The folder copy is the
     authority; say so, so nobody "fixes" it backwards.
   - Any of them `unknown` or missing → report exactly that. Do not infer a version from behavior.
   - **Baseline present and matching?** `.claude/skills/.baseline/` must exist and hold the same version
     as the live copies. Missing or mismatched, a future update cannot tell a local edit from an upstream
     change and has no safe merge available — report it, and offer to re-stamp the baseline from the
     current version **only if the live files are unmodified**. Re-stamping modified files would silently
     adopt local edits as though they were upstream, permanently losing the distinction.
   - **Locally modified skill files** — list any live file differing from its baseline. Not a fault; it is
     what the merge exists for. But say which, because each one is a future conflict, and note that a
     personalization is usually better moved into `CLAUDE.md` where it stops conflicting forever.

   **The lint never applies an update.** It reports; a person decides.

   Drift is not an error and must not be reported as one — a wiki a version behind works fine. It is
   reported because on a synced folder there is otherwise **no signal at all** that a teammate has been
   running last month's logic.

7. **Suspected capped sweeps** — scan `wiki-ingest-state.json` and recent run reports for per-source
   retrieved counts sitting at a round page size (100, 50, 25, 200, 1000), and especially the same number
   recurring. That is the signature of a sweep that stops at its page cap and reports the remainder as a
   quiet window. Flag the source and the affected windows, and state the fix: narrow the window and
   re-ingest that period.

   This check exists because the failure is otherwise undetectable — once written to the wiki, a
   truncated window and a genuinely empty one are indistinguishable.

8. **Uneven coverage** — compare `backfilled_through` across enabled sources in `llm-wiki.yml`. Flag any
   source with `null`, or whose history starts materially later than the others. That is a wiki that will
   answer across a gap without noticing: ask what was agreed with a client, and the part of the record
   that lived in the late-added source is simply missing. Offer to backfill it to match; never start one
   unprompted, since it spends tokens the owner did not choose to spend.

9. **Backfill status** — if `wiki-backfill-state.json` exists and is in progress, report
   `unitsDone / unitsTotal`, the date reached, any permanently failed units, and **any unit still marked
   `truncated`** — windows that were seen but not captured, and the likeliest source of a silent hole.

## Rules

- **Never delete a page.** Not as a fix, not as cleanup. If a fix would require removing content, report
  it and let the user decide.
- **Never run git.**
- Auto-fix is limited to: adding missing hub entries, backfilling routing lines from page titles and
  first content blocks, cleaning index drift, downgrading stale confidence, creating stubs for broken
  links, and adding obvious cross-references.
- Update the Dashboard page with the run's metrics and timestamp.

## Report

Findings by severity, with counts and per-issue suggested fixes. Lead with anything that means the wiki
is not being fed: a stale ingest cursor, a dead connector, a failed backfill. Those matter more than a
hundred missing cross-references.
