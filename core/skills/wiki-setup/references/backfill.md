# Historical backfill — the resumable protocol

Setup asks how far back to reach. Anything past a week or two is **not one task**; it is hundreds of
meetings, thousands of emails and months of chat. A single run will exhaust the user's token window long
before it finishes, and a backfill that dies halfway with no memory of where it got to is worse than no
backfill — it leaves a wiki that looks populated but has silent holes.

So a backfill is never executed as one pass. It is planned into small units, executed **one unit at a
time**, and checkpointed after every unit. Running out of tokens mid-backfill is an expected, ordinary
event, not a failure: the user comes back in their next window and it picks up exactly where it stopped.

## Depth options to offer

| Option | Depth | Rough size |
|---|---|---|
| None | Start fresh from today | 0 units |
| Light | 2 weeks | ~10-20 units |
| Standard | 3 months | ~60-100 units |
| Deep | 6 months | ~120-200 units |
| Full | 12 months | ~250-400 units |
| Custom | A date the user names | — |

Recommend **Standard (3 months)** by default: far enough back to cover the current quarter's decisions
and every live thread, shallow enough to finish in a few days of drain. Say the estimate out loud when
they pick, and say plainly that Full is measured in weeks of background drain, not hours.

Warn on two things before they choose:

- **Connector retention.** Most connectors don't hold a year. Chat search is often capped by the
  workspace plan, email is subject to retention policy, meeting transcripts are frequently 30-90 days.
  A 12-month request will return partial data for reasons that have nothing to do with this wiki. Set
  the expectation now rather than explaining the holes later.
- **Weight.** Deep backfills with attachment-following can put real bulk in `Archives/`, and on a synced
  folder every megabyte syncs to everyone who has it. For Deep and Full, default attachment-following to
  **off** during the backfill (it stays on for forward ingest) and say so.

## The plan file

`wiki-backfill-state.json`, at the storage root next to `llm-wiki.yml` — outside `Wiki/`, so it is never
mistaken for wiki content. Written by setup, updated after every unit.

```json
{
  "createdAt": "2026-09-11",
  "depth": "3 months",
  "windowStart": "2026-06-11",
  "windowEnd": "2026-09-11",
  "chunkSize": "week",
  "followAttachments": false,
  "status": "in_progress",
  "unitsTotal": 84,
  "unitsDone": 17,
  "unitsFailed": 1,
  "currentUnit": null,
  "units": [
    {
      "id": "email-2026-W24",
      "source": "email",
      "from": "2026-06-11",
      "to": "2026-06-17",
      "status": "done",
      "completedAt": "2026-09-11",
      "pagesTouched": 6,
      "itemsProcessed": 41,
      "note": ""
    },
    {
      "id": "meetings-2026-W24",
      "source": "meetings",
      "from": "2026-06-11",
      "to": "2026-06-17",
      "status": "failed",
      "attempts": 2,
      "note": "transcript fetch returned 502 twice; retry"
    }
  ]
}
```

`status` per unit: `pending` · `in_progress` · `done` · `failed` · `empty` · `truncated` · `skipped`.

`empty` is a real, successful outcome — that source had nothing in that week. Record it as `empty`, not
`done`, so a later reader can tell "we looked and there was nothing" from "we looked and found things".

**`truncated` is the one that protects the backfill's integrity.** A unit whose query hit a page cap and
could not be drained is **never** `done` and **never** `empty`. Mark it `truncated`, record how many
records came back and what the cap was, and split it (below). Marking a capped unit `done` is the single
worst thing this protocol can do: the checkpoint says that window is covered, nothing ever revisits it,
and the gap is permanent and silent. The whole value of checkpointing rests on `done` meaning done.

## Planning the units

1. One unit = **one source × one time chunk**. Never combine sources in a unit; their tool calls, failure
   modes and page destinations differ, and a mixed unit that half-fails cannot be cleanly retried.
2. Chunk size by expected volume: **week** for email, chat and meetings; **month** for tickets,
   documents, calendar and anything low-traffic. If a week's unit repeatedly overruns, split it to days
   and rewrite the remaining units for that source — record the change in the plan file.
   Backfill windows are wide and historical, which is exactly where page caps bite. Size chunks so a
   normal one returns **comfortably under** the source's page size, not near it.
3. Order units **oldest first**, and within a chunk, source by source in a fixed order. Chronological
   order matters: the log pages append, so out-of-order execution produces a log that reads backwards and
   a Timeline that resurrects dead deadlines.
4. Generate the full unit list at plan time. A plan you can count is a plan the user can see progress
   against; generating units lazily hides the finish line.

## Executing — the rules that make it survivable

**One unit per pass. Then checkpoint. Always.**

For each unit:

1. Mark it `in_progress` in the plan file **before** starting. If the run dies mid-unit, the next run
   sees `in_progress`, knows that unit is suspect, and re-runs it from the top rather than assuming it
   finished. Re-running a unit is safe; the ingest workflow appends and de-duplicates against what is
   already on the page.
2. Pull that source for that window only. Do not widen it because the window looked thin.
   **Drain every page.** Follow the cursor (`nextLink`, `next_cursor`, `has_more`, `offset`) until the
   source says there are no more. A result count at exactly the page size — 100, 50, 25 — is a cap, not
   an answer; assume more exists and prove otherwise.
   **If it cannot be drained, split the unit rather than accepting the partial.** Replace it in the plan
   with two half-window units (a week becomes two half-weeks, a day becomes two half-days), mark the
   original `truncated` with a note, and process the new units. Recurse until each returns under the cap.
   Record every split in the plan file so `unitsTotal` stays honest.
3. Ingest per the normal workflow — extract, route, cross-link, update hub `### Index` lines.
4. Write the unit's result to the plan file: `done` / `empty` / `failed`, with counts and any note.
5. **Stop and report progress if the context is getting heavy.** Do not try to squeeze in one more unit.
   A clean stop at unit 18 of 84 is a perfect outcome; a crash during unit 19 costs that unit's work.

Never hold more than one unit's raw source material in context. Once a unit is written to the wiki and
checkpointed, that material is done — do not carry it forward "for cross-referencing". Cross-references
come from the wiki pages, which is the entire point of writing them.

**Failures:** mark `failed` with the reason, and move on to the next unit. Do not abort the backfill for
one bad unit. Retry failed units at most twice, at the end of the run, after the pending queue is empty.
A unit that fails three times stays `failed` and gets reported — a permanent hole the user knows about
beats a backfill that refuses to finish.

## Resuming

Three ways, all reading the same plan file:

- **The user asks** — "continue the backfill", "keep ingesting history", or just "continue". Read the
  plan, report where it stands, and drain units until the context gets heavy.
- **The daily ingest job drains it automatically.** After its normal forward window, the ingest task
  checks for `status: in_progress` and processes **2-4 backfill units**, oldest pending first, then
  stops. This is the mechanism that actually finishes long backfills: they complete on their own over
  days of ordinary runs, without the user babysitting anything. Forward ingest always runs first — never
  let a backfill starve today's data.
- **A fresh session** — reading `llm-wiki.yml` and seeing an in-progress backfill is enough to mention
  it in one line, without derailing whatever the user actually asked for.

Always report backfill progress as `unitsDone / unitsTotal`, with the date the backfill has reached, and
the count of `failed`, `empty` and `truncated` units. **A non-zero `truncated` count is the most important
number in the report** — it is the only visible sign that part of the history was seen but not captured. "17 of 84 units, backfilled through 2026-06-24, 1 failed" tells
the user everything. "Backfill in progress" tells them nothing.

## Backfilling a source added later

**Every time a source is added — at setup, at reconfigure, or because someone asked mid-conversation for
something to be indexed — ask whether to backfill it, and how far back.** Never enable a source silently
from today forward; that leaves a hole nobody can see.

### Why it is not optional to ask

A source enabled without backfill answers questions as confidently as a fully-covered one. Ask "what did
we agree with Acme?" on a wiki with six months of email and three days of Slack, and the answer arrives
with no hint that half the record is missing. **Uneven history is worse than short history**, because
short history is obvious and uneven history is not.

### Default the depth to the wiki's existing coverage

Read `backfilled_through` on the other sources in `llm-wiki.yml` and **offer to match it**: *"Your other
sources go back to June. Match that for Slack, or pick a different depth?"* Matching is the right default
— it keeps coverage even, which is the thing that makes the wiki's answers trustworthy.

The usual options stand: none / 2 weeks / 3 months / 6 months / 12 months / a date. And the usual warning
— most connectors do not hold a year, so a deep request returns partial data for reasons that have
nothing to do with this wiki.

### Planning it

**Exactly the same protocol as the first run**, and for the same reason: one source × one time chunk per
unit, oldest first, checkpointed after each, drained a few units per ingest run. A source added later is
not a smaller problem — a year of one source is still hundreds of units, and running out of tokens
halfway through must stay an ordinary, resumable event.

**If a backfill is already in progress, append to it. Never start a second plan.**
`wiki-backfill-state.json` holds one plan. Add the new source's units to it, update `unitsTotal`, and let
the existing drain loop pick them up. Two competing plans mean two drains racing for the same budget,
and progress reporting that makes sense to nobody.

Where the new source's units interleave with existing pending ones, **order by date across the whole
queue** so the wiki fills chronologically rather than one source at a time. The logs append; a queue
processed source-by-source produces a log that reads in blocks.

### Record the coverage

When a source's units complete, write **`backfilled_through`** on that source in `llm-wiki.yml` — the
oldest date actually covered, not the date requested. They differ whenever a connector's retention cut
things short, and that difference is exactly what a later reader needs to know.

A source with `backfilled_through: null` has history only from the day it was enabled. Say so when it is
relevant to an answer.

## When it finishes

**A backfill is not complete while any unit is `truncated` or `in_progress`.** Those are unfinished work,
not results. Only `done`, `empty`, `failed` (after its retries) and `skipped` are terminal.

Set `status: complete`, report the totals — units done, empty, permanently failed; pages created; the
real date range actually covered versus the one requested (they differ whenever a connector's retention
cut it short, and that difference is the single most important line in the report). Then run `lint` once
over the result: a large backfill reliably produces orphans and missing routing lines, and fixing them
in one pass at the end is far cheaper than checking after every unit.
