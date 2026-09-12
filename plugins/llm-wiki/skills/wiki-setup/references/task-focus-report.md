# Template: a Focus Area report task

**One task per Focus Area**, on the day and cadence the user picked. Schedule it after the ingest, so it
reports on data that has already landed.

---

Produce this period's report for the Focus Area **{{FOCUS_AREA}}**, in the wiki at `{{WIKI_PATH}}`.

Read `llm-wiki.yml`, `Wiki/Schema.md` and `Wiki/{{FOCUS_AREA}}/_index.md` first.

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
these pages and is disposable; the pages are not. Sections, in this order:

1. **What changed** — the delta since the last report, in prose. Lead here. Not a list of everything that
   happened: what is *different*. If little changed, say so in one honest line rather than padding.
2. **Decisions** — each with who decided and on what authority. Superseded ones marked against what
   replaced them.
3. **Ideas & proposals** — raised, not yet decided, with who raised each.
4. **Open threads** — `follow-up` and `question`, with owner, age, and what is blocked while it sits.
   Ranked by what is at stake, not by age.
5. **Signals** — external facts that moved the picture.
6. **Looking ahead** — what lands before the next report: dated commitments, scheduled decisions, known
   risks. This section is why anyone reads a report on time rather than in arrears.
7. **Metrics** — the table, with directions.

## Step 4 — Regenerate the HTML

`Reports/{{FOCUS_AREA}}-Report.html`, from `templates/report.html`. **Regenerate the whole file every
run** from all the run pages — do not append to the previous HTML. It is a rendered view; rebuilding it
is cheap and it means a corrected run page corrects the report.

- `{{NAV_LINKS}}` — one `<a data-pane="run-YYYY-Www">` per run, **newest first**, each with its date.
- `{{PANES}}` — one `<section id="run-YYYY-Www" hidden>` per run, same ids as the nav.
- `{{OVERVIEW}}` — the standing view, not a copy of the latest run: where the Focus Area stands now,
  the metric trend across **all** runs, currently-open threads, and the live decision list. Someone
  opening this file cold should understand the state of the area from the overview alone.
- `{{FOCUS_STATEMENT}}` — the standing "what this is" line from the hub.

**No iframes and no external files.** One self-contained HTML file that switches panes in JavaScript.
This is deliberate: the file lives in a synced folder and will be opened from disk and forwarded as an
attachment. Browsers restrict `file://` iframes and local `fetch`, relative paths break the moment
someone moves or re-syncs the file, and a multi-file report arrives at a colleague broken. One file
always works, and the behavior — click a run in the sidebar, it opens on the right — is identical.

If the file grows past ~2 MB, keep the newest 26 runs inline and link the older run pages from the
overview. The wiki still holds every run.

## Step 5 — Send the summary

{{DELIVERY_BLOCK}}

Short, and **written to be read on a phone**: what changed, the two or three numbers that moved and which
way, anything that needs a decision or is now overdue, and what lands before the next report. Then a
pointer to the HTML file by path.

**Lead with what needs the user, not with what happened.** A report summary whose first line is an
activity count gets skimmed; one whose first line is "the Q2 target decision is still unmade and it now
blocks two client conversations" gets acted on.

If nothing material happened, **say that in one line and send it anyway.** A quiet period is information,
and a report that silently skips quiet weeks is indistinguishable from a broken job.
