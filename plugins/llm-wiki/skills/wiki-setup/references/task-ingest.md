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
announcement channels) and `commitments` (open asks in both directions). It holds cursors and
tracking data — never
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

## Paged sources: drain every page, and never call a cap "quiet"

Most connectors return results a page at a time. **A paged query is not finished when the first page
comes back — it is finished when the source says there are no more pages.** Stopping early does not
raise an error; it returns a plausible-looking result set, and the run reports a quiet window over data
it never looked at. This has already happened once: an unscoped mail sweep returned its first 100
records, more existed, and the run called the window quiet.

**Follow the cursor to depletion.** Whatever the source calls it — `nextLink`, `@odata.nextLink`,
`next_cursor`, `cursor`, `has_more`, `offset`, `page` — keep requesting until it is absent or false.
Count what you actually retrieved and carry that number into the report.

**Treat a round-numbered result count as truncated until proven otherwise.** Exactly 100, 50, 25, 20,
200, 1000 records is almost never the real answer; it is the cap. A genuine count is a ragged number. If
a sweep returns exactly the page size, assume there is more and prove otherwise before moving on.

**When a source will not give you the rest** — no cursor, a hard cap, rate limiting — do not accept the
partial result. **Narrow and re-query**: split the window in half and run both halves, recursing until
each returns comfortably under the cap. A month that caps at 100 becomes four weeks that return 30 each.
Tighten scope the same way, per mailbox, folder or channel, when the window cannot usefully shrink.

**If it still cannot be drained, say so explicitly and precisely.** "Email: reached the 100-record cap
for 2026-09-01..09-07 and could not page further; this window is incomplete" is a usable finding. "Email:
nothing notable" for the same window is a false statement that no one will ever catch, because an empty
result and a truncated one look identical in a wiki.

**Report retrieved counts per source, every run**, even when the run went fine. A source reporting
exactly its page size week after week is a capped sweep that nobody noticed, and the count is the only
place that shows.

**Never write `lastSuccessfulRun` after a run with an undrained source.** Leaving it unchanged widens the
next window and retries the gap; advancing it past data that was never read makes the gap permanent and
invisible.

## Sources

{{SOURCE_BLOCKS}}

A source that is configured but has no connector authorized in this environment: **report it clearly as
pending, do not silently skip it, and do not substitute another source for it.**

Every source below that returns lists is a paged source. The drain rule above applies to all of them.

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

## Commitment tracking — both directions

Cuts across every message-carrying source. **The purpose is that no ball gets dropped in either
direction**: things the owner is waiting on from other people, and things other people are waiting on
from the owner. Both live in `commitments` in the state file.

### What to capture

**Outbound — they owe the owner.** Scan what the owner **sent** (sent mail, their own chat messages,
their ticket comments) for asks that need something back: a decision, an answer, a document, an action.

**Inbound — the owner owes them.** Scan what the owner **received**, and capture a commitment **only
when the owner accepted it.** An unanswered request from someone else is not yet a commitment. Acceptance
looks like: "I'll send that", "yes, will do", "on it", "by Friday", taking assignment of a ticket, or
saying they'll bring something to a meeting. The agreement is the trigger, not the request.

If a request was made of the owner and they **never responded at all**, that is not a commitment — but
flag it once in the run report so it does not simply vanish. An unacknowledged ask is a decision not yet
made, not a task.

### Fields — all of them, every entry

- `direction` — `theirs` (they owe the owner) or `mine` (the owner owes them)
- `withWhom` — the other party, by name
- `subject` — what was asked or agreed, specific enough to act on without opening the link
- `stake` — what is blocked, at risk or undecided while it sits
- `link` — a deep link to the source message, never to a wiki page summarizing it
- `asked` — ISO date the ask was made or the commitment accepted
- `due` — ISO date. **See below; this is never left empty.**
- `dueIsExplicit` — `true` if a date was actually stated, `false` if defaulted
- `status` — `open` · `fulfilled` · `withdrawn` · `superseded`

### Setting `due` — the rule that makes this work

**If a date was stated, that is the due date.** Resolve relative wording against the **message's own
date**, not today's: "by Friday" in a message sent on 2026-09-02 is 2026-09-04. "End of the month",
"before the board meeting on the 12th", "next Tuesday" all resolve to an absolute ISO date at capture
time. Set `dueIsExplicit: true`.

**If no date was stated, `due` = `asked` + 7 days**, and `dueIsExplicit: false`. This is a nudge date,
not a real deadline, and the brief says so — but it guarantees that every open commitment surfaces
eventually instead of quietly ageing forever.

Resolve the date **at capture time, while the message is in hand.** Deriving it later from a summary is
how "by Friday" becomes the wrong Friday.

### Closing them out

Each run, check every `open` commitment for fulfilment. **Never close on age** — only on evidence.

**`theirs`** is fulfilled when: a reply lands in the thread answering it, the document or decision
arrives, a ticket transitions, or someone states it is done. Record `fulfilled` with the date and how it
was detected.

**`mine`** is fulfilled when **the owner produced the thing**: they sent the document, replied to the
original thread with the answer, moved or closed the ticket, created the deliverable, or the other party
acknowledged receipt. Look for this actively in the owner's sent messages and their own activity — an
entry that stays open after the work was done trains the owner to ignore the list, which is worse than
not having one.

Also close on `withdrawn` (the other party dropped it, or the owner was released from it) and
`superseded` (replaced by a newer ask). Record which, never silently delete.

**Capture the link at ingest time.** Slack search returns a permalink on every hit; email search on the
Sent folder returns a web link; **Teams chat search returns a null `webUrl` whenever a date filter is
set** — the date filter forces a per-chat scan path that omits the field, so run it with **no date
filter** and narrow with distinctive keywords from the message text instead.

Mirror the open list into `Wiki/{{PRIMARY_NS}}/Timeline.md` under **"Waiting on others"** (`theirs`) and
**"I owe"** (`mine`).

**Migration:** a wiki whose state file still has `pendingOutboundRequests` — carry those entries into
`commitments` with `direction: theirs`, `asked` from the original date, and `due` derived by the rule
above. Do it once, then use `commitments` only.

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
them, new ideas, threads opened and closed, signals — before anything else.

Then a **per-source line giving the window and how many records were actually retrieved.** This is what
makes a capped sweep visible: a source reporting exactly its page size, especially the same number week
after week, is a silent gap nobody would otherwise catch. Say explicitly where a source could not be
drained and which window is therefore incomplete.

Then: pages created and updated, notable decisions and action items, newly opened and newly closed
outbound asks, any source that was unavailable, backfill progress if a backfill is running, and the
window actually used if it was wider than 24h because of a missed run.
