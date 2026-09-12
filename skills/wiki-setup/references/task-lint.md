# Template: the monthly lint task

---

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

   Drift is not an error and must not be reported as one — a wiki a version behind works fine. It is
   reported because on a synced folder there is otherwise **no signal at all** that a teammate has been
   running last month's logic.

7. **Backfill status** — if `wiki-backfill-state.json` exists and is in progress, report
   `unitsDone / unitsTotal`, the date reached, and any permanently failed units.

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
