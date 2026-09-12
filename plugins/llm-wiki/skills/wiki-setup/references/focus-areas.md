# Focus Areas — the wiki's first-class topics

## The concept, and the name

A **Focus Area** is a part of the user's role they are accountable for and must stay on top of
continuously: a vertical they own, a transformation they are driving, a portfolio, a market they are
opening. Not a subject they find interesting — a **beat they cover**, file on, and report against.

Other names considered and rejected, so this does not get renamed on a whim: *Key Interests* (sounds
optional), *Priorities* (implies a ranking that will go stale), *Watchlist* (implies passive monitoring
when the user is actually driving it), *Mandates* / *Charters* (corporate, and nobody says them out loud).
**Focus Area** is what people already call this, and it needs no explanation.

**Up to three.** This is a hard cap and it is the point of the feature. Everything a Focus Area touches
gets double-handled, indexed and reported — worth it for three things, worthless for ten, because
"everything is first-class" means nothing is. If a user names five, say so plainly and ask which three
actually define their next two quarters. Fewer than three is fine. **Zero is fine and must be easy**: if
they have nothing that fits, create nothing — no namespaces, no pages, no report jobs, no mention of it
again.

## What being first-class actually means

Three things, and the first is the one that matters:

**1. Double routing.** Anything that relates to a Focus Area, however loosely, is written to **both** its
normal home (the day's log, the client page, the person's page) **and** the Focus Area's own pages. An
item that exists only in a chronological log has not been captured for the Focus Area — it is findable
only by someone who already knows when it happened, which is precisely the person who does not need to
look it up.

**2. Never light-touch.** Other material can be summarized in a line. A Focus Area item is captured in
full: what happened, who was involved, what was decided or proposed, and what it changes. The whole
reason it is first-class is that the weekly report has to be able to reconstruct the thread months later.

**3. Typed and attributed.** Every captured item carries a type and a source of authority — see below.
Untyped items are what turn a report into a list of things that happened, which is not a report.

## Item types

Every item captured for a Focus Area is one of these. The type is not decoration; it decides which
section of the report the item lands in.

| Type | What it is | Report section |
|---|---|---|
| `decision` | Something settled. **Must name who decided and on what authority** — theirs, delegated, or assumed | Decisions |
| `idea` | A proposal not yet decided. Names who raised it | Ideas & proposals |
| `follow-up` | An action someone owes. Names the owner and, where stated, the date | Open threads |
| `question` | Something open that needs an answer before anything can move | Open threads |
| `signal` | An external fact that moves the picture — a client change, a market move, a competitor, a number | What changed |

**Authority is not optional on a decision.** "We decided to target Q2" and "the GM decided to target Q2"
are different facts, and only the second survives being challenged three months later. Where authority is
unclear, record it as unclear rather than implying it — a decision recorded with borrowed authority is
worse than one recorded as provisional.

## Pages per Focus Area

Each Focus Area is **its own top-level namespace**, named for the area (`Tech-Vertical`,
`AI-Services`, `LATAM-Expansion`). Being a namespace rather than a page under something else is what
first-class means structurally.

```
Wiki/<Focus-Area>/_index.md              hub — routing + a standing "what this is" statement
Wiki/<Focus-Area>/Log.md                 chronological capture, append-only, typed items
Wiki/<Focus-Area>/Decisions.md           decisions + open threads, the live state (not a log)
Wiki/<Focus-Area>/Goals.md               what success looks like, with the metrics below
Wiki/<Focus-Area>/Reports/YYYY-Www.md    one page per report run — the source of truth for the report
```

Plus whatever the area itself grows: a client list, a membership draft, a deck ledger. Those emerge; do
not pre-create them.

**`Decisions.md` is a live state page, not a log.** Open threads move to closed in place; superseded
decisions are marked superseded next to what replaced them. The log records what happened; this page
records where things stand. Conflating the two is what produces a report that cannot say what changed.

## Goals and metrics

Ask at setup: **"What would tell you this is going well or badly?"** Two to four answers, in their words.
They go in `Goals.md` and become the trend lines in every report.

Every Focus Area also gets these **structural metrics** automatically, with no setup — they are counted
from the pages themselves, and they are what makes a trend visible even before anyone defines a KPI:

- Items captured this period, and the running total
- Open threads now, and the change since the last report
- Decisions made this period, and cumulative
- Threads closed this period
- Age of the oldest open thread — the single best early warning that a Focus Area is stalling
- Periods since the last decision — a long gap means momentum has gone, whatever the activity count says

State plainly that a user-defined metric only trends if something actually feeds it. If they name a
number no connected source reports, say so at setup and either find the source or record it as
manually-updated, rather than producing a report with a permanently empty chart.
