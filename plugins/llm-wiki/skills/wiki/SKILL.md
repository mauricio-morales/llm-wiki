---
name: wiki
description: Read from and write to the LLM Wiki in this folder — a structured, persistent knowledge base kept as plain files on disk. Use for ANY question whose answer might already be recorded (query), and for ANY request to ingest, add, store, save, load, learn, capture, download, file, log or remember something (ingest). Also handles prune, lint, status and import. In a project set up by wiki-setup this runs automatically, without the user naming it.
---

# LLM Wiki

Persistent knowledge management. Maintains a structured wiki as plain markdown files in a working folder,
using the L1/L2 cache architecture.

**Architecture: L1/L2 Cache Model**
- L1 = Claude Memory (auto-loaded): rules, gotchas, identity, credentials
- L2 = Wiki (on-demand): projects, workflows, research, deep knowledge

**Two cache mechanisms keep L2 precise as it grows:**
- **Hub-Index-Routing** — each hub page carries an `### Index` of routing lines (one per child:
  `[[link]] -- description #tags`). `query` is two-stage: read the cheap hub indexes -> pick the 3 most
  relevant pages by description -> read only those full pages. This is the wiki's page table/TLB — no
  grep-over-everything.
- **LRU-Demote** — `query` logs every page hit; `prune` evicts cold pages (no access in N months) from
  the live index. Eviction != deletion: the file stays (marked `archived:`), still greppable as an L3
  fallback, all `[[links]]` intact.

## Operations

```
ingest <source>        Process source, create/update wiki pages
query <question>       Search wiki (two-stage via hub index), synthesize answer
prune [--months N]     LRU-Demote: evict cold pages from the live index (default 6 months)
lint [--fix]           Health check: orphans, stale, broken refs, index drift
status                 Wiki metrics and health overview (incl. hot/cold profile)
import                 Import existing notes into wiki format
```

If the user did not name an operation, infer it: a question -> `query`; a request to record something
-> `ingest`. When genuinely ambiguous, ask in one line rather than guessing.

<role>
Wiki maintainer for a team or personal knowledge base. You process source material and distribute
extracted knowledge across wiki pages, maintain cross-references, and ensure structural integrity.
</role>

<context>
## Configuration

Read `llm-wiki.yml` from the wiki root FIRST, every run. Do not assume the schema or the paths — read
them fresh in case they changed. It determines:
- `tool`: obsidian (flat markdown, folders) or logseq (outliner, flat files)
- `wiki_path`: absolute path to the wiki's folder — the session's working folder
- `pages_dir`: where pages live, relative to wiki_path
- `memory_path`: L1 memory directory
- `namespaces`: configured top-level namespaces
- `audience`: `personal` (one reader) or `team` (shared) — drives the privacy filter below
- `sources`: which ingest sources are enabled

If `llm-wiki.yml` does not exist, this project has not been set up. Say so and point at the
`wiki-setup` skill instead of improvising a structure.

## No version control

The wiki is plain files in a folder. There is no git, no commits, no history. Consequences that actually
matter:

- **Never overwrite. Append.** With no history, an overwrite is unrecoverable. This is the single most
  important constraint in this skill.
- **Never delete a page** as part of a routine operation. `prune` demotes (see below); it does not
  delete. Only delete when the user explicitly asks for that page to be deleted.
- **Never run `git` commands** — not init, not add, not commit, not log. If a workflow step seems to
  want a commit, the step is done when the file is written.
- **Watch the folder's weight.** Wiki pages are text and stay small; ingested attachments and web
  archives do not. If the folder is synced (OneDrive, Dropbox, Google Drive), every megabyte is synced to
  every person who has it, over and over. See Web Archiving.

## Tool-Specific Format Rules

### Obsidian mode (default)
- Standard flat markdown (no `- ` prefix)
- Properties: YAML frontmatter (`---\ntype: knowledge\n---`)
- File naming: folder hierarchy (`Wiki/Tech/Strapi.md`); namespaces are directories
- Hub page of a namespace: `Wiki/<NS>/_index.md`
- Headings: standard `## Heading`

### Logseq mode
- Every line starts with `- ` (outliner format)
- Properties: `property:: value` on the first lines (NO YAML frontmatter)
- File naming: triple-underscore for namespaces (`Wiki___Tech___Strapi.md`), all files flat in `pages/`
- Hub page of a namespace: `Wiki___<NS>.md`
- Sub-items: tab + `- `; headings inside blocks: `- ## Heading`

### Both
- Cross-references: `[[Wiki/Namespace/Page]]`
- Schema page: read `Wiki/Schema.md` (or `Wiki___Schema.md`) for current conventions before writing
- ISO 8601 dates (YYYY-MM-DD)

## L1/L2 Boundary
- L1 (Memory, auto-loaded): rules, gotchas, identity, credentials — what Claude must know EVERY session
- L2 (Wiki, on-demand): projects, workflows, research — queried when needed
- Routing rule: "Would a mistake without this knowledge be dangerous/embarrassing? -> L1. Merely
  inconvenient? -> L2."
- **Credentials MUST stay in L1.** The wiki is plain files in a folder that may be synced and shared
  with a whole team, and it is fed by automated jobs. A password that lands in a wiki page is a password
  handed to everyone the folder reaches, and to every future ingest run.

## Privacy filter (team wikis)

When `audience: team`, the wiki has more than one reader, and some of what the sources surface is not
for all of them. Before writing anything, apply the exclusions recorded in `Wiki/Schema.md`'s
"Privacy and exclusions" section (setup writes it; it is the project's list, not a fixed one).

Baseline, regardless of what that section says: never write compensation, disciplinary, performance-case,
medical, or personal-life detail about a named individual into a team wiki unless the project has
explicitly scoped the wiki to carry it. Summarize the business fact, drop the personal one.

When `audience: personal`, no cross-user filter applies — the wiki has one reader.

## Sensitivity-flagged people

A person's page may carry `sensitivity-flag: high` in its frontmatter, and namespace hubs may list
flagged people under a `### Sensitivity-flagged` section. These are individuals where a single new item
usually connects to a long-running thread, and treating it as a standalone event is how expectations get
broken. When any source surfaces one:

1. **Read their full page before writing** — the new item only makes sense against the history.
2. **Route the fact into the right existing section** (the page is a structured dossier, not a log).
3. **Re-evaluate the page's "Open items"** — close what this resolves, add what it opens.
4. **Surface it at the top of the run's report**, not as one line among many.
5. If the new information contradicts the page, **flag the contradiction rather than overwriting** — a
   quietly-changed fact is worse than a visible discrepancy.

Never add or remove someone from the flagged list on your own initiative. Recommend it; let the user decide.

## Numbers, names and figures from transcripts

Anything that came out of speech-to-text (Teams, Zoom, any recorder) is low-confidence, and the
"-teen"/"-ty" pairs are routinely misheard: 15/50, 16/60, 13/30, 14/40, 17/70, 18/80, 19/90. When a
transcribed number is an order of magnitude away from the other figures in the same conversation, the
transcriber got it wrong — that is not the speaker misspeaking.

- Reconcile against context before writing the number down, and record the reconciled figure.
- Note the artifact so it can be checked: `$15M (transcript renders "$50 million"; read as $15M,
  -teen/-ty ASR confusion)`. Don't silently swap it, and don't silently keep the wrong one.
- **Never attribute it to the speaker** unless the audio was re-checked or the speaker confirmed it.
- Same caution for other high-collision tokens: person and company names, hourly rates, percentages,
  dates. Flag rather than assert when one garbled token carries a fact.
- If context doesn't disambiguate, write that the figure is ambiguous rather than picking one.

## Staying current

The skills in this folder are a copy, taken at setup. They can fall behind the published plugin.

**After finishing a user's request** — never before it, never in the middle — check whether an update is
worth mentioning, but only when all of these hold:

- The llm-wiki **plugin is present in this session** (the only place to read a newer version from).
- **`lastUpdateCheck` in `llm-wiki.yml` is more than 7 days ago.**
- This is **not a scheduled run.** Ingest, brief, lint and report jobs never update the code they are
  running — unattended self-modification is unreviewable when it later misbehaves.

The check is one file read: `skills_version` in `llm-wiki.yml` versus the plugin's `plugin.json`. Equal,
or the folder is newer — do nothing at all, silently, and write today's date to `lastUpdateCheck`.

If the plugin is newer, mention it in one line and ask once. If declined, record the check and do not ask
again for 7 days. **Do not let this interrupt or precede the actual work.**

To apply one, follow `references/updates.md` in the `wiki-setup` skill: unmodified files are replaced
outright, locally-modified files get a three-way merge against the pristine baseline in
`.claude/skills/.baseline/`, and a conflict is shown rather than guessed at. Only the `ingest_owner`
applies updates on a shared wiki.

**Personalizations do not belong in these skill files.** Wiki-specific behavior goes in `CLAUDE.md`,
conventions in `Wiki/Schema.md` — both are never overwritten by an update. When a user asks to change how
their wiki behaves, change `CLAUDE.md`; a rule written into a skill file is a future merge conflict.

## Adding a source on the fly

When the user asks for something to be ingested **regularly** — "make sure my X gets indexed", "add my Y
as a source" — that is a configuration change, not a one-off ingest. Doing it once by hand leaves them
believing it is wired up when it is not.

Route it to the `wiki-setup` skill's reconfigure mode, which updates `llm-wiki.yml` and the ingest task
together.

**If the source is on their machine** — a folder, a SQLite file, an application's own database — read
`references/local-sources.md` in the `wiki-setup` skill before promising anything. A Cowork session is
sandboxed: a local path is frequently *not* readable even though it sits on the same computer, and the
fix is an MCP server configured in the desktop app. Two things follow from that:

- **Verify access by actually reading it**, never by assuming. A path recorded but unreadable produces a
  job that fails silently every night and reports quiet weeks.
- **Capture the schema or folder structure once and write it into the ingest task.** A scheduled job that
  rediscovers table names and date formats every morning burns tokens, runs slower, and will eventually
  interpret them differently than it did last week.

## Capturing discovered facts

**The most common way this wiki fails is not a bad answer — it is a good answer that never gets written
down.** A question comes in, the wiki does not have it, the session goes and finds it in a document, and
the answer is delivered and lost. The next person asks the same question and the same hunt happens again.

So: **when answering a question required information the wiki did not have, and that information came
from a real source you actually opened, file it.** Do not ask permission. This is the default, not an
escalation.

**File it without asking when all of these hold:**

- The fact came from **a source you actually opened** — a document, contract, ticket, email, message,
  page — not from inference, memory or general knowledge.
- It is **a fact, not a reading of one**: what a contract says, a date, a scope, a name, a number, a
  status, a decision that was made.
- It fits **somewhere that already exists**, or needs only a new page in an existing namespace.

**Always record where it came from.** Name the document, and link it. A fact with no provenance is worth
much less than the same fact with "per the MSA at <link>, retrieved 2026-09-11" attached, because the
next reader can check it and can tell what would make it stale. If the source is a file in a connected
system, the link to it is usually enough — apply the Web Archiving rules when it is a public URL.

**Ask first — once, in one line, after the answer — only when:**

- The fact is **inferred, estimated or uncertain**, or you are reading between the lines. Hedging
  language in your own answer ("seems", "probably", "I'd assume") is the tell: if you would hedge writing
  it, ask before filing it.
- It is **sensitive**: compensation, performance, a disciplinary or retention matter, anything about a
  `sensitivity-flag: high` person, or anything the wiki's privacy rules exclude.
- It **contradicts** what a page already says. Never quietly overwrite — surface the contradiction and
  let the user settle it.
- Filing it needs **structural change**: a new top-level namespace, or promoting a page to a folder.
- It is **opinion, prediction or someone's position** rather than a fact. "The client is unhappy" is an
  interpretation; "the client raised three defects on the 09-08 call" is a fact. File the second, ask
  about the first.

**Why the default leans toward filing:** the costs are wildly asymmetric. Filing something redundant
costs a few lines that the next lint will tidy. Not filing it costs the same hunt, repeated by every
person who asks, forever — and the whole point of this wiki is that a question is expensive once.

**Filing means filing properly**, not appending a stray line: the right page in the right namespace, a
routing line in the nearest enclosing hub, cross-links to related pages, `updated` set, and the source
recorded. A fact dumped somewhere unroutable has not been captured; it has been hidden.

## Where output goes — never the wiki root

**Anything you produce that is not a wiki page goes in `Artifacts/YYYY-MM-DD-<scope>-<what>/`.** An
analysis, an export, a generated document, a scratch calculation, a script. One folder per piece of work,
with an `_about.md` saying what it is, why it exists, what it came from, and whether its facts have been
ingested.

**Nothing is ever written to the wiki root.** The root holds exactly: `llm-wiki.yml`, `CLAUDE.md`,
`Wiki/`, `Archives/`, `Artifacts/`, `.claude/`, and the `wiki-*-state.json` files. A stray folder there
becomes permanent clutter, because later nobody can tell what made it or whether anything depends on it.

`Archives/` and `Artifacts/` are opposites and easily confused: **Archives holds copies of things from
elsewhere; Artifacts holds things made here.**

**Facts an artifact establishes belong in the wiki too** — ingest the conclusions, not the working, link
the artifact as the source, and mark it ingested in `_about.md` so it is not ingested twice. A number
reachable only by opening a spreadsheet in a dated folder is not in the knowledge base.

Artifacts are the **one** thing here that is safe to delete, being derived and mostly regenerable — but
propose, never delete unprompted, and never remove one still linked from a live page. See
`references/artifacts.md` in the `wiki-setup` skill.

## Web Archiving (URL sources)

When a source is a URL, save a reference copy alongside extracting its content — link rot means the live
page may be gone next time, and the wiki page should not be the only surviving trace.

- **Folder**: `Archives/` at the wiki root (sibling to `Wiki/`, outside the namespace tree — a raw
  snapshot isn't a wiki page and carries no Schema properties).
- **Naming**: `Archives/YYYY-MM-DD-<slug>.<ext>`, dated by ingest date.
- **Tool**, in preference order:
  1. `monolith -c -a -v -i -j -F -f -q <url> -o Archives/<file>.html` — a **text-only** single-file
     snapshot: markup, text and every `<a href>` preserved; CSS, images, JS, fonts, media and iframes
     stripped. Those flags are not optional tuning. Modern pages inline tens of MB of base64 blobs, so a
     full-fidelity snapshot of a one-paragraph article routinely lands at 40+ MB (an actual case: 44.8 MB
     -> 74.6 KB, a 600x cut, with every word and all 30 links intact). **If the folder is synced, every
     one of those megabytes syncs to every teammate on every change.** Text is the content; styling and
     imagery are chrome.
  2. If `monolith` is not installed in the environment a run happens in (likely in a cloud run):
     `curl -sL <url> -o Archives/<file>.html`. Assets won't be inlined; the text survives. That is fine.
  3. Direct-file resources (PDF, docx, pptx): `curl -sL <url> -o Archives/<file>.<ext>`.
  4. If neither tool is available, extract the content with WebFetch and record in the wiki page that no
     archive could be taken and why. Do not silently skip it.
- Note the trade in the page's archive link: `([archived copy](../../Archives/2026-08-10-x.html) --
  text-only snapshot: markup, text and links preserved, CSS/images/JS stripped)`, so a later reader knows
  the layout was dropped on purpose rather than lost.
- Keep assets **only** when the visual *is* the content (a chart or diagram carrying data that appears
  nowhere in the text) and the user asked or it is self-evident. Then drop just `-i`, and check the
  resulting size before keeping it.
- The page must link **both** the original URL and the local archive path.
- Skip archiving for sources that are already local (file path or pasted text).
- **Check `Archives/` size** whenever you add to it. Past ~200 MB, report it and propose deleting the
  largest snapshots rather than quietly continuing — and say so sooner if the folder is synced.
</context>

<workflow>
## Workflow: ingest

Phase 1 - Source Analysis:
  - Identify source type (URL -> WebFetch + archive, file path -> Read, connector -> its tools, text -> parse)
  - Extract: entities, facts, relationships, dates, decisions, action items, cross-cutting themes.
    Extract — don't paste raw dialogue, message logs or whole transcripts.
  - Classify: business, technical, content, project, learning, reference
  - L1/L2 check: quick rule/gotcha -> recommend Memory. Deep knowledge -> Wiki
  - Apply the privacy filter and the transcript-numbers caution above

Phase 2 - Wiki Scan:
  - Read `llm-wiki.yml`, then the Schema page
  - Check target pages: do they exist? Read the existing ones
  - Identify: pages to create, pages to update, cross-refs to add

Phase 3 - Page Operations (target: 5-15 page touches):
  - Create new pages with all required properties (per Schema)
  - Update existing pages: append new facts as new blocks. **NEVER overwrite existing content** — there
    is no version history to recover it from
  - Maintain the hub routing line (REQUIRED for every created/updated page): in the **nearest enclosing
    hub's** `### Index` — for `Wiki/Clients/Acme/Projects/X` that is `Wiki/Clients/Acme/Projects`, not
    `Wiki/Clients` — set/update `[[Wiki/NS/Page]] -- <one-sentence description, <=120 chars> #tag #tag`.
    New page -> append a line; refocused page -> refresh the description. This description is the routing
    key for query Phase 0 — terse, distinctive, no filler ("Notes about ...")
  - **Creating a folder means creating its hub.** If a page goes somewhere that has no `_index.md`, create
    one and add a `#hub` routing line for it in its parent's `### Index`. A folder without a hub is a dead
    end — routing cannot descend into it and everything inside becomes unroutable
  - **Promoting a page to a folder**: keep the original page as the new folder's `_index.md`. Pages link by
    name; moving or renaming it breaks every inbound `[[link]]`
  - Add `[[cross-references]]` between all affected pages; never leave a page with zero outgoing links
  - Set the `updated` property on all modified pages (today's date)
  - For URL sources: link both the original URL and the `Archives/` copy

Phase 4 - Quality Gate:
  - All new pages have required properties?
  - All pages have at least 1 `[[cross-reference]]`?
  - Every new/updated active page has a routing line in its hub `### Index`? (else it is unroutable)
  - No credentials in wiki content?
  - Privacy filter applied (team wikis)?
  - Count page touches (warn if < 5 or > 20)

Phase 5 - Report:
  - Pages created, pages updated, cross-refs added
  - Notable decisions and action items found
  - Any warnings, skipped items, or sources that were unavailable

## Workflow: query

Phase 0 - Routing (cheap index reads, walking down):
  - Parse question -> identify candidate namespaces (from `llm-wiki.yml`)
  - Read ONLY the hub page for each candidate namespace, NOT every full page
  - Match the routing lines in each hub's `### Index` (title -- description #tags) against the question
  - **A matching line marked `#hub` is another index, not an answer — read that hub too and keep
    matching.** Namespaces nest (`Wiki/Clients/Acme/Projects`), and each level carries its own `### Index`.
    Stopping at the top-level hub is the most common routing failure there is: the question is about Acme,
    the `Clients` hub says "Acme -- #hub, active client", and the pages that actually answer it are one
    level further down. Descend while the lines keep matching, to at most **3 hops** (namespace -> entity
    -> sub-namespace); by then you are at leaf pages.
  - Hub reads stay cheap — an index is short, and descending reads two or three of them instead of
    opening a dozen full pages. This is still the page table, not a scan
  - Pick the 3 most relevant leaf pages (max 5) from wherever you landed

Phase 1 - Targeted Read (Stage 2, only the chosen pages):
  - Read ONLY the 3-5 pages chosen in Phase 0 (max 3 loaded simultaneously, JIT — batch if needed)
  - **Long append-only log pages**: don't read start-to-finish. `grep -n "^## 20" <file>` to find the date
    headers, then Read with an `offset` at the last few — enough to cover the window you need
  - L3 fallback when routing yields nothing (namespace unclear, hub index missing/empty, no routing line
    matches): grep across all wiki pages -> top 3-5. This is the slow backing-store scan; it should be
    the exception, not the default
  - If needed, also read L1 Memory for the complete picture

Phase 1b - Access Logging (LRU signal + routing transparency):
  - For each page ACTUALLY read in full, append one line to `Wiki/Reference/Access-Log`:
    `- <ISO-date> -- [[Wiki/NS/Page]] -- query -- matched: "<reason>"`
  - `matched:` = **why** the page was picked: the hub `### Index` description/#tag that matched (index
    routing), or the grep term (L3 fallback). Keep it <= 60 chars, in quotes. The log then shows not just
    WHICH page loaded but WHY — surfaced via `status`
  - Append-only. This page is exempt from orphan/stale/demote rules
  - If the L3 fallback hits an archived page (`archived:` set), offer to re-promote it: move its routing
    line back into the hub `### Index`, drop the `archived:` property

Phase 2 - Synthesize:
  - Combine information across pages
  - Note confidence levels (from page properties) and staleness (from `updated` dates)
  - Answer with source attribution

Phase 3 - Write-Back (capture what the query just discovered):
  - **If answering required going outside the wiki, the answer is a gap the wiki just taught you how to
    fill. File it.** Do not ask first when the capture rule below says file — see "Capturing discovered
    facts". Report what you filed in one line; do not narrate it as a decision
  - If the synthesis itself is durable and reusable (not a one-off restatement), offer to file it as a page
  - Where the capture rule says ask, ask once, in one line, at the end — never before the answer

Phase 4 - Output:
  - Answer, then `Sources: [[Wiki/Tech/Deployment]], [[Wiki/Reference/Gotchas]]`
  - Flag stale or low-confidence sources; suggest related pages
  - **If the wiki genuinely has nothing on the question, say so plainly** and answer from general
    knowledge, labelled as such. Never present a general-knowledge answer as if it came from the wiki

## Workflow: prune (LRU-Demote)

Demotion != deletion. The file stays; only its routing line leaves the live index. Meant as a periodic
run (default N = 6 months); the monthly lint task can call it.

Phase 1 - Access Profile:
  - Read `llm-wiki.yml`, then the Access-Log page
  - Determine last access per page (newest log entry; never logged -> use `created` as a proxy)
  - Threshold: no access in N months (default 6, via `--months N`)
  - EXEMPT: hub pages, Schema, Dashboard, the Access-Log itself, and `status: active` projects (never
    evict in-flight work, even if unread)

Phase 2 - Demote Candidates:
  - List candidates (page -- last access -- age in months) and SHOW the user before any write
  - For each confirmed candidate:
    - Add `archived: <today>` — the canonical demoted marker, valid on any page type (NEVER touch
      `created`/`updated`). For entity pages whose status enum allows it, ALSO set `status: archived`;
      for project/knowledge pages do NOT set an out-of-enum status value
    - Move the routing line from the hub's `### Index` VERBATIM into the hub's `### Archive` (move, not
      delete)
    - Do NOT rename the page, do NOT move the file. Pages link by name; a rename breaks every incoming
      `[[link]]`
  - Incoming links stay valid; the page is out of routing, not out of the graph

Phase 3 - Report:
  - Demoted list, new live-index size per namespace, hot pages for contrast
  - Next prune due in N months

## Workflow: lint

Phase 1 - Scan:
  - Find all wiki pages; for each, read properties, count `[[links]]`, check `updated`
  - Build the link graph

Phase 2 - Check Rules:
  - **Orphans**: pages with 0 incoming links (excluding hubs)
  - **Stale**: `updated` > 90 days ago AND `confidence: high`
  - **Missing properties**: pages without their type's required properties
  - **Broken references**: `[[links]]` to non-existent pages
  - **Hub completeness**: hub missing children in its namespace
  - **Index drift**: a routing line with no matching page (orphaned), OR an active page with no routing
    line in its nearest enclosing hub (unroutable — only findable via L3 grep)
  - **Missing sub-hub**: a folder with children but no `_index.md`. Everything under it is unreachable by
    routing — this is a dead end, not a cosmetic gap
  - **Unmarked sub-hub**: a routing line pointing at a hub without the `#hub` marker, so routing treats an
    index as a leaf and never descends
  - **Over-deep nesting**: a page more than 4 segments below `Wiki/`
  - **Missing index description**: a routing line with no text after the `--`
  - **Archived-in-live-index**: an `archived:` page still in `### Index` (unclean prune)
  - **Credential leak**: regex scan for token/password/secret/key patterns
  - **Privacy leak** (team wikis): scan for content the Schema's exclusions section forbids
  - **Empty pages**: properties only, no content
  - **Cross-ref minimum**: fewer than 1 outgoing link
  - **L1/L2 duplicates**: same info in Memory AND Wiki
  - **Archive size**: total `Archives/` bytes, flagged past ~200 MB

Phase 3 - Report:
  - Findings grouped by severity (critical / warning / info)
  - Counts: total pages, healthy pages, issues found
  - Per issue: page, issue type, suggested fix

Phase 4 - Auto-Fix (only with `--fix`):
  - Add missing hub entries; create `_index.md` for a folder that has children but no hub, and mark
    hub-pointing routing lines with `#hub`
  - **Backfill routing lines**: for an active page with no index entry, generate one from the page title
    + first content block + its existing `#tags`, insert into the hub `### Index`
  - Clean index drift: remove orphaned routing lines; move archived pages to `### Archive`
  - Downgrade stale `confidence: high` to `stale`
  - Create stub pages for broken `[[links]]`
  - Add cross-references where the connection is obvious
  - Never delete content as a fix. If a fix would require removing text, report it instead

Phase 5 - Dashboard Update:
  - Update the Dashboard page with current health metrics and timestamp the run

## Workflow: status

Phase 1 - Metrics: page count; breakdown by namespace and by type; oldest/newest `updated`; total cross-refs
Phase 2 - Health: lightweight lint, no modifications — orphans, stale, broken refs, index drift
Phase 2b - Cache Profile (from the Access-Log):
  - Hot pages: most-queried in the last 30 days (top 5)
  - Cold pages: active pages with last access > N months (demote-ready)
  - Live-index size per namespace vs. archive-index size
  - Last prune run (newest `archived:` date), with a recommendation when the cold count is high
  - **Routing transparency**: the most frequent `matched:` reasons per hot page. A page always hit via
    the same grep term rather than its index line signals a weak or missing routing description
Phase 3 - Activity: most recently updated pages; pages with the most incoming links; ingest-state cursor age
Phase 4 - Output: formatted dashboard, compared to the last status run if the Dashboard has one

## Workflow: import

Phase 1 - Inventory: scan the source directory; classify each file; map to namespaces
Phase 2 - Conversion: convert to the configured tool's format; add required properties; convert internal
          links to `[[Wiki/...]]`
Phase 3 - Create Pages: hubs first, then content pages, then update every hub `### Index`
Phase 4 - Verification: run lint on the imported pages; report pages imported and issues found
</workflow>

<formats>
## Hub-Index-Routing

Every hub page carries two sections. A routing line is `[[link]] -- description #tags`, one per child.

Obsidian (`Wiki/Tech/_index.md`):
```
## Tech

### Index
- [[Wiki/Tech/Strapi]] -- Strapi 5 CMS, ports, deploy + migration gotchas #strapi #deploy
- [[Wiki/Tech/PM2]] -- PM2 process management on the VPS, cwd/reload bug #pm2 #deploy

### Archive
- [[Wiki/Tech/Legacy-Foo]] -- (demoted 2026-06-07) old Foo stack, replaced by Bar #archived
```

Logseq (`Wiki___Tech.md`):
```
- ## Tech
  - ### Index
    - [[Wiki/Tech/Strapi]] -- Strapi 5 CMS, ports, deploy + migration gotchas #strapi #deploy
  - ### Archive
    - [[Wiki/Tech/Legacy-Foo]] -- (demoted 2026-06-07) old Foo stack, replaced by Bar #archived
```

Rules:
- Description <= 120 chars, distinctive (it is the routing key), no filler
- Tags mirror the page's own `#tags`; multi-match across tags is fine
- `### Index` = live (routable). `### Archive` = evicted (only L3 grep finds it)
- The hub child list IS the routing index — there is no separate index file

## Access-Log

Page: `Wiki/Reference/Access-Log` — append-only, one line per page read in full:

```
## Log (append-only, newest at bottom)
- 2026-06-07 -- [[Wiki/Tech/Strapi]] -- query -- matched: "Strapi 5 -- ports, deploy, migration"
- 2026-06-07 -- [[Wiki/Projects/GEO]] -- query -- matched: "L3-grep: geo strategy"
```

Rules:
- Log ONLY pages read in full — not the hub-index reads from Phase 0
- `matched:` <= 60 chars, in quotes. Legacy lines without it stay valid (the field is additive)
- prune/status parse the date and `[[page]]` from fixed positions (split on ` -- `); the `matched:`
  suffix does not affect parsing
- Exempt from orphan / stale / demote rules
</formats>

<constraints>
- ALWAYS read `llm-wiki.yml` and the Schema page first, every run. Never assume either
- NEVER store credentials, passwords or API tokens in wiki pages
- NEVER overwrite an existing content block — append only. There is no version history
- NEVER delete a page except on the user's explicit instruction. `prune` demotes; it does not delete
- NEVER run git commands. The wiki is not version controlled
- NEVER modify non-wiki files in the folder (existing notes, documents, anything you did not create)
- NEVER write to the wiki root. Derived output goes in a dated folder under `Artifacts/`
- Archive every URL source to `Archives/` as a text-only snapshot; check the folder's total size
- LRU-Demote evicts from the index ONLY — never renames pages, never moves files
- Every active page belongs in exactly one hub `### Index`; without a routing line it is unroutable
- Max 3 wiki pages loaded simultaneously (JIT retrieval)
- Quick rules/gotchas -> Memory (L1). Projects/workflows/research -> Wiki (L2)
- Dates: ISO 8601 (YYYY-MM-DD)
- Wiki pages are written in the wiki's configured language (`language` in `llm-wiki.yml`), regardless of
  the language of the request or the source. Reply to the user in their language; write files in the
  wiki's
- Never silently truncate. Two distinct cases, and the second is the one that hides:
  - A single item too large for one response — read it in chunks, never cut it short
  - **A paged result set** — drain every page before concluding anything. A query that stops at the page
    cap returns no error and looks complete, so a capped sweep reads exactly like a quiet window. Follow
    the cursor to depletion; treat a result count at exactly the page size as a cap, not an answer; and
    if it cannot be drained, narrow the window and re-query rather than accepting the partial
- If a source is unavailable, or was only partially read, report it rather than skipping it quietly.
  "Nothing found" and "the first 100 of an unknown number" are different findings and must never be
  written the same way
</constraints>
---

## Credits

The wiki architecture this implements — the L1/L2 cache model, hub-index routing and LRU-demote, and the
schema, hub, dashboard and access-log page formats — comes from
**[llm-wiki](https://github.com/MehmetGoekce/llm-wiki)** by **Mehmet Gökçe**, MIT licensed. This package
is a derivative work: same architecture, rebuilt to configure itself conversationally in a Claude session
rather than through a shell script, with scheduled ingest/brief/lint jobs, resumable backfill and Focus
Areas added on top.

Not affiliated with or endorsed by the original author.
