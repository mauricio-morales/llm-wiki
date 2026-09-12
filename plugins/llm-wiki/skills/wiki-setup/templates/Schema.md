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
- `## Waiting on a reply` — asks that have gone out and not come back. **Not pruned by date.** Each
  line carries the ask, the stake, the age and a deep link. See "Outbound request tracking".

### Focus-Area item (inside Log.md / Decisions.md)

Not a page type — a line format. Every item captured for a Focus Area is typed:

```
- 2026-09-12 -- decision -- <what was settled> -- decided by <who>, <authority> -- [[source]]
- 2026-09-12 -- idea -- <the proposal> -- raised by <who> -- [[source]]
- 2026-09-12 -- follow-up -- <what is owed> -- owner <who>, due <date|none> -- [[source]]
- 2026-09-12 -- question -- <what is open> -- blocks <what> -- [[source]]
- 2026-09-12 -- signal -- <the external fact> -- [[source]]
```

`decision` without a named decider and authority is incomplete. Where authority is unclear, write
`authority unclear` — never imply it.

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

## Outbound request tracking

An ask that goes out and never comes back is the most expensive thing a wiki can lose. Every ask the
wiki owner sends — in email, chat or a ticket — is tracked in the ingest state file until it is answered,
and rendered in the daily brief.

Each tracked ask carries four fields, and **all four are mandatory**:

1. **`subject`** — what was actually asked, specific enough to act on without opening the link
2. **`stake`** — what is blocked, at risk or undecided while it sits, with a date when one exists
3. **`link`** — a deep link to the source message itself, never to the wiki page summarizing it
4. **`whoseMove`** — `them` or `us`. "He owes you the estimate" and "you owe him an answer" are
   opposite instructions and must never be blurred

Ageing: `#waiting` at 7-13 days, `#waiting-overdue` at 14+. **Rank by stake, not by age** — an 11-day
ask blocking a dated client call outranks a 21-day courtesy chase.

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
Edit this page freely; it is yours now.
