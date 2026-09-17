# Template: a Focus Area report task

**One task per Focus Area**, on the day and cadence the user picked. Schedule it after the ingest, so it
reports on data that has already landed.

---

<!-- llm-wiki task: {{TASK_KIND}} | template version: {{PLUGIN_VERSION}} | generated: {{DATE}} -->

## Step 0 — Adopt any pending update to this prompt

{{TASK_SELF_UPDATE}}

<!-- Setup fills this from references/task-self-update.md. Embed it in full — a scheduled run cannot
     read the reference file. -->

Produce this period's report for the Focus Area **{{FOCUS_AREA}}**, in the wiki at `{{WIKI_PATH}}`.

Read `llm-wiki.yml`, `Wiki/Schema.md` and `Wiki/{{FOCUS_AREA}}/_index.md` first.

## Step 0.5 — Read and act on replies to the last report

{{ASYNC_REPLY_PROTOCOL}}

<!-- Setup fills this from references/async-replies.md, with this task's channel and the state keys
     for this Focus Area's report. Embed it in full — a scheduled run cannot read the reference. -->

Do this **before** assembling the period, so this run's report already reflects whatever the owner said
about the last one.

## Step 1 — Assemble the period

The period runs from the last report's date (see `Wiki/{{FOCUS_AREA}}/Reports/`, newest page) to today.
If there is no previous report, the period starts at the Focus Area's earliest captured item, and say so.

Read, in this order: `Wiki/{{FOCUS_AREA}}/Log.md` (tail only — `grep -n "^## 20"` then read from the last
few date headers), `Decisions.md` in full — it is the live state, not a log — and `Goals.md`.

**Then sweep the rest of the wiki for anything this period that relates to the Focus Area and did not get
double-routed.** Ingest is supposed to route it both places; when it misses, the report is the backstop.
Anything you find, **write into the Focus Area's own pages before reporting it**, so the next run does not
have to find it again. Note in the report that it was picked up late — a recurring late-pickup pattern
means the ingest job's routing needs widening, which is worth knowing.

## Step 2 — Compute the metrics

Structural, counted from the pages, always:

| Metric | Definition |
|---|---|
| Items captured | Typed items added this period, and running total |
| Open threads | `follow-up` + `question` currently open, and the change vs last report |
| Decisions | `decision` items this period, and cumulative |
| Threads closed | Open threads resolved this period |
| Oldest open thread | Age in days of the longest-open one — the best early warning of a stall |
| Periods since last decision | Long gaps mean momentum has gone, whatever the activity count says |

Plus any user-defined metrics in `Goals.md`. **A metric with no feeding source reports as "not tracked",
never as zero** — zero is a finding, "not tracked" is a gap, and showing the second as the first is how a
report starts lying.

Every metric carries its **direction versus the previous report** (up / down / flat, with the delta). A
number without a direction is trivia — the whole value of a periodic report is the second derivative.

## Step 3 — Write the run page

`Wiki/{{FOCUS_AREA}}/Reports/YYYY-Www.md` — **this is the source of truth.** The HTML is generated from
these pages and is disposable; the pages are not.

### The standard this report is held to

**Aggregate first, narrate almost never.** This is a management read-out, not a diary. If something can
be a number, a delta or a table, it must not be a paragraph. The wiki already holds the full account —
the report's job is to say what the accumulated material *means*.

Hard budgets, and they are limits rather than targets:

| Part | Budget |
|---|---|
| Whole run page, excluding tables | **600 words** |
| Any single insight | **2 sentences** |
| Items listed in any one section | **5**, then "+N more" with a link |
| Paragraphs recounting what happened | **zero** |

**An insight is not an event.** This is the distinction the whole report turns on:

- ❌ *"On the 14th, Dana raised the pricing question again in the vertical sync, and Ana followed up by
  email on the 15th with the revised model, which Karim has not yet reviewed."* — three events, narrated.
  The reader learns what happened and nothing else.
- ✅ *"Pricing is the bottleneck: it's blocked three of the last four decisions and is now the oldest open
  thread at 23 days. Everything else in the area is moving."* — the same material, read.

If a period genuinely produced nothing to interpret, **say that in one line.** Padding a quiet week with
recounted detail is what made the first report unreadable.

### Sections, in this order

1. **Where it stands** — 3-4 sentences of synthesis. Not a summary of events; a judgement about the state
   of the area. What is moving, what is stuck, what changed about the *shape* of it.
2. **Objective progress**, where `Wiki/{{PRIMARY_NS}}/Objectives.md` has an objective mapped to this
   Focus Area. Current versus target, percentage attained, **pace** (percentage of the period elapsed
   against percentage attained — the number the owner cannot compute in their head), a projection where
   there are at least three data points, and a sparkline. This goes **above** the structural metrics: it
   is what the owner is actually measured on. Skip the section entirely if there are no objectives.
3. **KPIs** — the table from Step 2. Every metric with its value, its direction versus last period, and
   its trend across all runs. These stay because they are the early warning that an area is stalling,
   but they are no longer the headline when objective data exists.
4. **Insights** — 3-5 bullets, two sentences each, each one reading the numbers rather than restating
   them. Anchor each to a metric that moved — and **where objectives exist, frame them against the
   objective, not against activity.** "Decisions are up" is an observation about the wiki; "decisions are
   up but none moved the pipeline objective, which is now behind pace" is an observation about the
   owner's quarter. Prefer the uncomfortable observation: a stalling trend is
   worth more than a flattering one.
5. **Decisions** — one line each, who decided and on what authority. Cap at 5; link the rest.
6. **Needs the owner** — **only commitments the owner owes or is owed** (see the commitment ledger; other
   people's obligations are not tracked and are not listed here). Led by `[id]`, ranked by stake, capped
   at 5. Everything else stays in the wiki.
7. **Looking ahead** — what lands before the next report: dated commitments, scheduled decisions, known
   risks. Bullets, not prose.

**What does not go in:** a chronological account of the period, every open thread, every item captured,
restated context the owner already has, or any sentence beginning "As discussed". All of that is in
`Log.md` and one click away.

## Step 4 — Regenerate the HTML

`Reports/{{FOCUS_AREA}}-Report.html`, from `templates/report.html`. **Regenerate the whole file every
run** from all the run pages — do not append to the previous HTML. It is a rendered view; rebuilding it
is cheap, and it means a corrected run page corrects the report.

### The Overview pane is entirely aggregate

`{{OVERVIEW}}` is the standing view and **the most important part of the file** — it is what someone
opening it cold reads, and what the owner checks between reports. It is **not** a copy of the latest run
and contains **no** itemized lists.

It holds, in this order:

- **Objective tiles first**, where objectives map to this area: attained versus target, pace, and a
  sparkline. Then **KPI tiles** — current value, direction versus last period, sparkline across every run.
  Objectives outrank structural metrics for the top of the page; if there are none, the KPIs lead.
- **Where it stands** — 4-5 sentences, the state of the area as of now.
- **Trajectory** — 2-3 bullets on what the trends say over the whole history, not this period. Whether
  decision velocity is rising or falling, whether open threads are accumulating faster than they close,
  whether the oldest thread keeps getting older. These are only visible in aggregate and are the reason
  the cumulative view exists.
- **Counts, not lists** — "7 open threads, oldest 23 days" rather than seven lines. Link to the wiki.
- **Needs the owner** — the same owner-scoped commitments, top 3 by stake, with `[ids]`.

If the Overview cannot be read in under a minute, it is too long.

### Sparklines

Every KPI carries a trend. Inline SVG, no libraries, built from that metric's value on each run page:

```html
<span class="spark" role="img" aria-label="12 → 19 over 8 periods, rising">
  <svg viewBox="0 0 100 24" preserveAspectRatio="none">
    <polyline points="0,20 14,18 28,12 42,14 57,9 71,7 85,4 100,2"/>
  </svg>
</span>
```

Normalize each series to the 0-24 box independently — these show **shape**, not absolute comparison
between different metrics. Fewer than 3 runs: omit the sparkline rather than drawing a line through two
points, and say "trend from 3 periods". **Always give the `aria-label`** — a sparkline with no text
equivalent is invisible to a screen reader and to anyone reading the summary message.

### The rest

- `{{NAV_LINKS}}` — one `<a data-pane="run-YYYY-Www">` per run, **newest first**, each with its date.
- `{{PANES}}` — one `<section id="run-YYYY-Www" hidden>` per run, same ids as the nav.
- `{{FOCUS_STATEMENT}}` — the standing "what this is" line from the hub.

**No iframes and no external files.** One self-contained HTML file that switches panes in JavaScript.
The file lives in a synced folder and will be opened from disk and forwarded as an attachment. Browsers
restrict `file://` iframes and local `fetch`, relative paths break the moment someone moves or re-syncs
the file, and a multi-file report arrives at a colleague broken. One file always works, and the behavior
— click a run in the sidebar, it opens on the right — is identical.

If the file grows past ~2 MB, keep the newest 26 runs inline and link the older run pages from the
overview. The wiki still holds every run.

## Step 5 — Send the summary

{{DELIVERY_BLOCK}}

Short, and **written to be read on a phone**. Lead with one line confirming anything you actioned from
replies to the last report. Carry the `[IDs]` through, so every item named can be replied to.

**Then the two or three numbers that moved, with their direction** — not a description of the period.
Then the single most important insight, in one sentence. Then anything needing the owner. Then the path
to the HTML.

Six lines is plenty. If the message needs to be read twice to find the point, it is written wrong: what changed, the two or three numbers that moved and which
way, anything that needs a decision or is now overdue, and what lands before the next report. Then a
pointer to the HTML file by path.

**Lead with what needs the user, not with what happened.** A report summary whose first line is an
activity count gets skimmed; one whose first line is "the Q2 target decision is still unmade and it now
blocks two client conversations" gets acted on.

If nothing material happened, **say that in one line and send it anyway.** A quiet period is information,
and a report that silently skips quiet weeks is indistinguishable from a broken job.
