---
wiki-version: "1.0"
type: schema
created: "{{DATE}}"
updated: "{{DATE}}"
maintained-by: llm-wiki
---

# Wiki Schema

The conventions for this wiki. Every operation reads this page before writing. Edit it when the
conventions change — it is the source of truth, not this plugin's defaults.

## Namespace Conventions

- Top-level: {{NAMESPACES}}
- Page naming: Title Case, hyphens for multi-word (`Wiki/Projects/My-Project`)
- Layout: {{LAYOUT_NOTE}}

### Sub-namespaces

A namespace can nest. An entity that accumulates its own material — a client, a person, an initiative —
becomes a folder with its own hub, and can hold sub-namespaces of its own:

```
Wiki/Clients/_index.md                                  hub (top-level namespace)
Wiki/Clients/Acme/_index.md                             hub (the client)
Wiki/Clients/Acme/Overview.md                           page
Wiki/Clients/Acme/Projects/_index.md                    hub (sub-namespace)
Wiki/Clients/Acme/Projects/202607-Data-Migration.md     page
```

**Depth: up to 4 segments below `Wiki/`.** That is enough for namespace → entity → sub-namespace → page,
which is the deepest structure that stays navigable. Past that, the thing you are nesting usually wants
to be its own page with links.

**Every level that contains children carries its own hub with its own `### Index`.** This is what makes
nesting work rather than just look tidy — routing walks down through these indexes, so a folder without
a hub is a dead end and everything beneath it becomes unroutable.

**A routing line pointing at a hub says so**, with `#hub` and a description of what is under it, not of
the entity itself:

```
- [[Wiki/Clients/Acme]] -- #hub · active client: renewal, two projects, staffing #client #active
- [[Wiki/Clients/Acme/Projects]] -- #hub · per-project pages, dated #project
```

That `#hub` marker is what tells a query there is another level worth descending into, rather than a
leaf page to open.

**Promote deliberately.** A client mentioned twice belongs in a log or on one page. A client with its own
projects, staffing and renewal history has earned a folder. When you promote a page to a folder, keep the
page name as the folder's `_index.md` so every existing `[[link]]` still resolves — pages link by name,
and renaming breaks every inbound reference.

## Page Types and Required Properties

### Entity (person, client, tool, service, technology)
```yaml
type: entity
entity-type: person | client | tool | service | technology
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active | inactive | archived
source: ingest | manual | import
sensitivity-flag: high     # optional — see "Sensitivity-flagged people"
```

### Project
```yaml
type: project
status: active | completed | on-hold | cancelled
created: YYYY-MM-DD
updated: YYYY-MM-DD
started: YYYY-MM-DD
completed: YYYY-MM-DD      # if applicable
```

### Knowledge (learning, reference)
```yaml
type: knowledge
domain: tech | business | content | ops
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low | stale
```

### Feedback (lessons learned, gotchas)
```yaml
type: feedback
severity: critical | important | nice-to-know
created: YYYY-MM-DD
verified: YYYY-MM-DD
applies-to: []             # page references to affected systems
```

### Log (append-only chronological source log)
```yaml
type: log
source: meetings | email | chat | tickets | documents
created: YYYY-MM-DD
updated: YYYY-MM-DD
```
Log pages carry one `## YYYY-MM-DD` section per ingest run, newest at the bottom. They are **appended
to, never rewritten**, and they get long — read their tail, not the whole file.

### Timeline (forward-looking schedule)
```yaml
type: timeline
updated: YYYY-MM-DD
```
**Not a log.** Rebuilt each ingest from the current calendar pull, not appended to. Three sections:

- `## Calendar (next 30 days)` — one line per event: `YYYY-MM-DD HH:MM -- #tag -- description`.
  Tags: `#meeting` `#deadline` `#followup` `#ooo` `#travel`. Lines whose date has passed are dropped
  on the next rebuild.
- `## Commitments` — concrete future date-bound commitments surfaced in meetings/email/chat that are
  **not** on anyone's calendar (a stated deadline, a "follow up next week" promise, a target date
  mentioned in passing), each linking back to the log entry it came from. Pruned once the date passes.
- `## Waiting on others` and `## I owe` — open commitments in both directions. **Not pruned by date.**
  Each line carries the ask, the stake, the due date (and whether it was stated or defaulted), and a deep
  link. See "Commitment tracking".

### Focus-Area item (inside Log.md / Decisions.md)

Not a page type — a line format. Every item captured for a Focus Area is typed:

```
- [52] 2026-09-12 -- decision -- <what was settled> -- decided by <who>, <authority> -- [[source]]
- [53] 2026-09-12 -- idea -- <the proposal> -- raised by <who> -- [[source]]
- [54] 2026-09-12 -- follow-up -- <what is owed> -- owner <who>, due <date|none> -- [[source]]
- [55] 2026-09-12 -- question -- <what is open> -- blocks <what> -- [[source]]
- [56] 2026-09-12 -- signal -- <the external fact> -- [[source]]
```

**The `[id]` is written here, at ingest, from the same wiki-wide `nextItemId` counter the commitments
use.** It lives on the line in the wiki page — it is not a rendering detail. Reports read it; they never
invent it. An id minted while rendering would differ on every run, so a reply naming it would resolve to
the wrong thing or to nothing.

`decision` without a named decider and authority is incomplete. Where authority is unclear, write
`authority unclear` — never imply it.

### Objectives (the owner's own KPIs / OKRs)

```yaml
type: objectives
updated: YYYY-MM-DD
```

One page, the canonical copy of what the owner is measured on. Each objective records: the statement in
the owner's own words, the measure, baseline and target, the period's start and end, the current value
with the date and **where it came from**, the source (connector, page, person, or `manual`), and which
Focus Areas it maps to.

**Never infer a target.** An objective with no stated number is qualitative and reports as a judgement,
not a percentage. **An objective with no feeding source reports as "not tracked", never as zero** — and
that gap is worth reporting, since an objective nobody can measure is one that gets argued about at
review time.

**At period end, close objectives out with their final attainment and keep them.** Start the new period
below. That history is the most useful thing on the page at the next planning round, and the first thing
anyone is tempted to delete.

### Hub (namespace index)
```yaml
type: hub
namespace: Wiki/NamespaceName
```

## Cross-Reference Rules

- Every page MUST have at least one outgoing `[[Wiki/...]]` link
- Every active page MUST have exactly one routing line in its namespace hub's `### Index`
- When a page mentions an entity that has its own page, link it
- Tags: `#tag` for lightweight categorization
- External links: `[Text](URL)`. For an archived URL, link both: `[Original](URL) ([archived copy](../../Archives/...))`

## Routing-Line Format

`[[Wiki/NS/Page]] -- one-sentence description, under 120 chars #tag #tag`

A line pointing at a sub-hub carries `#hub` and describes what is underneath it, so a query knows to
descend rather than to open a leaf.

The description is the **routing key** — `query` reads only these lines to decide which pages to open.
Terse and distinctive beats complete. "Notes about the client" routes nothing; "Acme renewal — rates,
2027 scope, the open SOW question" routes precisely.

## Content Format Rules

{{FORMAT_RULES}}

- NEVER store credentials, passwords or API tokens in wiki pages
- Dates: ISO 8601 (YYYY-MM-DD)
- Language: {{LANGUAGE}} — every page is written in this language regardless of the source's language

## Folder layout

The wiki root holds exactly: `llm-wiki.yml`, `CLAUDE.md`, `Wiki/`, `Archives/`, `Artifacts/`, `.claude/`
and the `wiki-*-state.json` files. **Nothing else is ever written there.**

- **`Archives/`** — snapshots of URLs that were ingested. Things from elsewhere, saved.
- **`Artifacts/`** — output produced here: analyses, exports, generated documents. One dated folder per
  piece of work, `YYYY-MM-DD-<scope>-<what>/`, each carrying an `_about.md`. Facts an artifact establishes
  are ingested into `Wiki/` with the artifact linked as the source. Artifacts are the only thing in this
  folder that may be deleted — they are derived — but only on a proposal a person accepts.

## Privacy and exclusions

**Audience: {{AUDIENCE}}**

{{PRIVACY_RULES}}

## Sensitivity-flagged people

Individuals where a single new item usually connects to a long-running thread, so treating it as a
standalone event is how expectations get broken. Their page carries `sensitivity-flag: high`.

When a source surfaces one: read their full page first, route the fact into the right existing section
(the page is a dossier, not a log), re-evaluate its "Open items", surface it at the top of the run
report, and flag any contradiction rather than overwriting it.

### Sensitivity-flagged list

_(none yet — add people here deliberately; ingest runs never add or remove them on their own)_

## Commitment tracking

An ask that goes out and never comes back, or one accepted and never delivered, is the most expensive
thing a wiki can lose. Both directions are tracked in the ingest state file until closed, and rendered in
the daily brief.

**The owner is always one of the two parties.** Commitments between other people are not tracked — the
owner can neither chase nor close them, and a ledger padded with other people's obligations stops being
read. Delegation is the exception that proves it: work handed to someone else is still the owner's
commitment, because the owner still answers for it.

**Two directions, never merged:**

- `theirs` — someone owes the owner something
- `mine` — the owner owes someone something, **and agreed to it**. A request nobody accepted is not a
  commitment; the agreement is the trigger.

**Every entry carries:** `id`, `direction`, `withWhom`, `subject` (what was asked or agreed), `stake`
(what is blocked while it sits), `impact` (`high`/`medium`/`low`, judged at capture), `link` (to the
source message, never to a summary), `asked`, `due`, `dueIsExplicit`, `status`.

**The brief ranks by impact first, then urgency**, and shows at most five per section — a high-impact item
due Thursday outranks a low-impact one a month overdue. Age alone measures how long something has been
ignorable.

**`due` is never empty.** If a date was stated, that is it — resolved to an absolute date against the
*message's* date, at capture time. If none was stated, `due` = `asked` + 7 days and `dueIsExplicit` is
`false`: a nudge date, not a promise, and the brief must say which it is.

**Surfacing:** an open commitment appears in the brief when `due` is today or earlier, and **every day
after until it closes.** Anything the owner owes with a real stated deadline also gets one heads-up the
previous working day — being told on the morning it is due is often too late to produce it.

**Closing:** only on evidence, never on age. `theirs` closes when the answer or artifact arrives; `mine`
closes when the owner produced it. Also `withdrawn` or `superseded`, recorded as such rather than deleted.

## Timeline sections

`Timeline.md` carries **"Waiting on others"** and **"I owe"**, mirroring the two directions. Neither is
pruned by date — unlike the calendar and commitment lines, an open commitment stays until it is closed.

## L1/L2 Architecture

**L1 = Claude Memory** (auto-loaded every session): feedback rules, quick gotchas, identity,
credentials. Everything Claude must know at the START of every session.

**L2 = this wiki** (on-demand): projects, workflows, research, deep knowledge, business intelligence.

Routing rule: *"Would a mistake without this knowledge be dangerous or embarrassing? -> L1. Merely
inconvenient? -> L2."* Credentials are always L1 — this wiki is plain files in a folder that may be
synced and shared.

## Lint Rules

Orphans · stale (`updated` > 90d with `confidence: high`) · missing properties · broken refs · hub
completeness · index drift · missing index description · archived-in-live-index · credential leak ·
privacy leak · empty pages · cross-ref minimum · L1/L2 duplicates · `Archives/` size.

## No version control

This wiki is plain files in a folder. There is no git and no history, so:

- **Append, never overwrite.** An overwrite is unrecoverable.
- **Never delete a page** outside an explicit instruction. `prune` demotes; it does not delete.

---

## Credits

This schema — its page types, hub-index routing lines and access-log format — derives from
[llm-wiki](https://github.com/MehmetGoekce/llm-wiki) by Mehmet Gökçe, MIT licensed, via the
[llm-wiki plugin](https://github.com/mauricio-morales/llm-wiki) that generated this wiki.
The pattern it implements — a persistent, LLM-maintained wiki with ingest, query and lint as its core
operations — was proposed by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Edit this page freely; it is yours now.
