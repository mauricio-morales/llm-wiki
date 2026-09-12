# Template: the ingest task

Setup fills the `{{...}}` placeholders and passes the result as the `prompt` of a scheduled task.
Every run starts with no memory of the setup conversation, so the prompt must be **fully self-contained**:
paths, connector names, scope, filters, destinations. Do not write "as discussed" into a task prompt.

**Substitute the owner's real details from `llm-wiki.yml`'s `owner:` block when filling this template.**
The task prompt must name them explicitly — a scheduled run has no signed-in context to infer "me" from,
and an unqualified "me" in a task prompt resolves to nobody.

---

Ingest new content into the LLM Wiki at `{{WIKI_PATH}}`.

Read `llm-wiki.yml` and `Wiki/Schema.md` first — do not assume the schema, read it fresh each run in
case it changed. Then follow the `wiki` skill's `ingest` workflow.

## Adaptive time window — read this before touching any source

Job state lives at the storage root, next to `llm-wiki.yml`: `wiki-ingest-state.json`. It holds
`lastSuccessfulRun` (ISO timestamp), per-source dedup cursors, `frequentContacts` (rolling interaction
scores), `channelActivity` (per-channel post/reaction counts, used to tell conversation channels from
announcement channels) and `pendingOutboundRequests`. It holds cursors and tracking data — never
credentials.

Compute the window for **every** source below:

- `windowStart = state.lastSuccessfulRun` if present.
- If the state file or `lastSuccessfulRun` is missing (first run), default to 24 hours ago and say so
  plainly in the report.
- This is the entire catch-up mechanism. A normal run covers ~24h; if yesterday's run failed or was
  skipped, `lastSuccessfulRun` is still two or more days old, so this run automatically pulls the whole
  gap. **Do not cap or truncate a wide gap** — if it has been a week, ingest the week and say so.
- Write a new `lastSuccessfulRun` **only at the very end**, and only if the run completed end to end (all
  sources processed or explicitly reported unavailable). A partial or failed run must leave it untouched
  so the next run's window widens to retry the gap.

## Sources

{{SOURCE_BLOCKS}}

A source that is configured but has no connector authorized in this environment: **report it clearly as
pending, do not silently skip it, and do not substitute another source for it.**

## Focus Areas — first-class, every source

{{FOCUS_BLOCK}}

Where Focus Areas are configured, this rule outranks everything else in this job:

- **Double-route.** Anything relating to a Focus Area, however loosely, is written to **both** its normal
  home (the day's log, the client page, the person's page) **and** the Focus Area's own pages. An item
  that exists only in a chronological log has not been captured — it is findable only by someone who
  already knows when it happened.
- **Never light-touch.** Other material can be a line. A Focus Area item is captured in full: what
  happened, who was involved, what was decided or proposed, what it changes.
- **Type and attribute every item**: `decision` (with **who decided and on what authority**), `idea`
  (who raised it), `follow-up` (owner, and date if stated), `question`, `signal`. Untyped items produce a
  report that is a list of things that happened, which is not a report. Where authority for a decision is
  unclear, record it as unclear — never imply it.
- Match against the Focus Area's **statement** in its hub, not just its name. The statement is the routing
  key and is deliberately broader than the title.
- `Decisions.md` is a **live state page**: resolve open threads in place, mark superseded decisions
  against what replaced them. `Log.md` is the append-only record. Keep the two distinct — conflating them
  is what makes a report unable to say what changed.

If the window held nothing for a Focus Area, **say so explicitly in the report** rather than omitting the
section. Silence and "nothing happened" must never look the same.

## Outbound request tracking

Cuts across every message-carrying source. Scan what the wiki owner **sent** — sent mail, their own chat
messages, their ticket comments — for asks that need an answer back. For each new one, add an entry to
`pendingOutboundRequests` in the state file with all four fields:

- `subject` — what was actually asked, specific enough to act on without opening the link
- `stake` — what is blocked, at risk or undecided while it sits, with a date when one exists
- `link` — a deep link to the source message itself, never to a wiki page summarizing it
- `whoseMove` — `them` or `us`

Capture the link **at ingest time**, when you already have the message in hand. Hunting for it later, in
the brief, costs far more. Techniques: Slack search returns a permalink on every hit; email search on the
Sent folder returns a web link; **Teams chat search returns a null `webUrl` whenever a date filter is
set** — the date filter forces a per-chat scan path that omits the field, so run it with **no date
filter** and narrow with distinctive keywords from the message text instead.

Each run, check whether any pending ask has since been answered — a reply in the thread, a ticket
transition, the thing simply arriving. Close those out. Age the rest: `#waiting` at 7-13 days,
`#waiting-overdue` at 14+. Mirror the open list into `Wiki/{{PRIMARY_NS}}/Timeline.md`'s
"Waiting on a reply" section.

**An ask is not closed because it is old.** It is closed because it was answered or withdrawn.

## Follow shared links once

If a message shares a link or carries an attachment, open it once and record what it was about — one hop
only, no chasing links inside the linked document. Capture what it is, who sent it, roughly what it
contains, and any figure, date, name or commitment on its face. A short paragraph is the target, not a
deep read. Escalate to a full ingest only if it independently clears the bar (a contract, a client
proposal, a live deliverable with a near-term date).

Record the pointer even when the content is thin or unreadable — *"opened, it's the bare template with
nothing filled in"* is a useful finding. If a file cannot be opened at all, say so and say why.

Do **not** follow credential-gated third-party links, unsubscribe or tracking URLs, or anything shaped
like a phishing probe. Note that the link exists and was deliberately not opened, and why.

{{ATTACHMENT_POLICY}}

## Routing

Route into `Wiki/{{PRIMARY_NS}}` unless a fact clearly belongs elsewhere. Give each source its own dated
log page, continuing its chronological log on later runs rather than duplicating structure:

{{LOG_PAGE_MAP}}

`Timeline.md` is **not a log** — it is rebuilt each run from the calendar pull, plus commitments
surfaced in other sources that aren't on anyone's calendar, plus the (never date-pruned) waiting list.

Create a page for a person only once a genuinely reusable pattern emerges — a recurring 1:1, an ongoing
thread of decisions. Otherwise leave them in the log. Create new topic pages only when a genuinely new,
reusable topic emerges that doesn't fit an existing page.

Maintain the `### Index` routing line in the hub for every page touched. Add `[[cross-references]]`
between affected pages; never leave a page with zero outgoing links. Set `updated` on every touched page.

## Rules

- **Append, never overwrite.** No version history exists — an overwrite is unrecoverable.
- **Never run git.** This project is not a repository.
- Never write credentials into wiki content.
- Extract entities, facts, decisions and action items — never paste raw transcripts or message logs.
- Figures from speech-to-text are low-confidence: the "-teen"/"-ty" pairs (15/50, 16/60, 13/30…) are
  routinely misheard. Reconcile against context, note the artifact, and never attribute the error to the
  speaker.
- Write every wiki page in {{LANGUAGE}} regardless of the source's language.
- {{PRIVACY_LINE}}

## Backfill drain

After the forward window is complete, check `wiki-backfill-state.json`. If it exists with
`status: in_progress`, process **2-4 backfill units**, oldest pending first, following the backfill
protocol: mark each `in_progress` before starting, checkpoint after each one, stop early if context gets
heavy. Forward ingest always comes first — never let the backfill starve today's data. Report progress as
`unitsDone / unitsTotal` with the date reached.

## Report

Open the summary with a **Focus Areas** section when any are configured — new decisions and who made
them, new ideas, threads opened and closed, signals — before anything else. Then: pages created and
updated, notable decisions and action items, newly opened
and newly closed outbound asks, any source that was unavailable, backfill progress if a backfill is
running, and the window actually used if it was wider than 24h because of a missed run.
