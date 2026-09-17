# Objectives — the owner's own KPIs and OKRs

If the owner is measured on something — quarterly OKRs, a personal scorecard, team targets — **that is
what the wiki should be reporting against.** Structural metrics (items captured, threads closed) say
whether the wiki is working. Objectives say whether the *owner* is.

Optional, like Focus Areas. Many people have none written down, and that is fine: ask once, accept no,
and never raise it again.

## Where they live

`Wiki/{{PRIMARY_NS}}/Objectives.md` — one page, the canonical copy. Focus Areas keep their own `Goals.md`
for area-specific measures; Objectives are the role-level ones, and a single objective may span several
areas or none.

Each objective records:

- **The statement**, in the owner's own words, not a paraphrase
- **Measure** — what number moves. If there is no number, say so; a qualitative objective is still worth
  tracking, it just reports as a judgement rather than a chart
- **Target** and **baseline** (where it started)
- **Period** — start and end dates. Quarterly is typical
- **Current value**, with the date it was last updated and **where it came from**
- **Source** — which connector, page or person supplies the number, or `manual`
- **Focus Areas** it maps to, if any

## Capturing them

**At setup**, right after Focus Areas: *"Are you measured on anything specific this quarter — OKRs, a
scorecard, team targets? If so I'll report against them."* Accept a rough answer; they can be tidied in
the page later.

**During ingest**, objectives turn up on their own — a planning deck, a quarterly review, a goals
document, a manager's message setting a target. When one appears and is not already on the page, **add
it and say so in the run report.** When a *number against an existing objective* appears, update the
current value and record where it came from. This is the main way the page stays alive; a goals page
nobody updates is worse than none, because it reports stale progress with confidence.

**Never infer a target.** If the owner said "grow the pipeline" with no number, record it as
qualitative rather than inventing 20%. A fabricated target produces fabricated progress.

## How they change the reports

**Focus Area reports lead with objective progress where an objective maps to that area**, above the
structural metrics. The structural ones stay — they are the early warning that the area is stalling —
but they are no longer the headline when something the owner is actually measured on is available.

For each mapped objective, report:

- **Current versus target**, and percentage attained
- **Pace** — percentage of the period elapsed against percentage attained. This is the single most useful
  number in the report and the one the owner cannot easily compute in their head: *"62% of the quarter
  gone, 34% attained"* says more than either figure alone.
- **Projection** — where the current rate lands by the period end, stated plainly: *"at this pace it
  finishes around 55% of target."* Only when there are at least three data points; below that say the
  trend is not yet readable rather than extrapolating from noise.
- **A sparkline** of the value across the period, with the target as context.

Insights are then framed against the objectives rather than against activity. *"Decisions are up"* is an
observation about the wiki. *"Decisions are up but none of them moved the pipeline objective, which is
now behind pace"* is an observation about the owner's quarter.

**An objective with no feeding source reports as "not tracked", never as zero** — and that gap is itself
worth reporting, because an objective nobody can measure is one that will be argued about at review time.

## How they change the daily brief

Lightly. **The brief is not an OKR dashboard** — a daily progress bar on a quarterly goal is noise, and it
will be skimmed past within a week.

What it does carry:

- **When something in the day's material moves an objective**, say which one and in which direction. That
  is a meaningful event, not a routine metric.
- **When a commitment the owner owes blocks an objective**, say so on that item. It changes the priority
  and it is exactly the connection that gets missed.
- **A short objective line when an objective is behind pace and the period is more than half gone** — at
  most one line, and only for the objectives actually at risk. Not every objective, not every day.

## Period rollover

When a period ends, **do not delete the objectives.** Close them out with their final attainment on the
page, keep them, and start the new period below. The history of what was targeted and what landed is the
most useful thing on that page at the next planning round, and it is the first thing anyone deletes.
