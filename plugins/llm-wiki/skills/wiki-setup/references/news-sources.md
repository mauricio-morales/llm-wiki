# News topics — scanning the web, filtered by what the wiki already knows

A news feed nobody filters is noise, and it is the fastest way to make a wiki unreadable. What makes this
worth having is that **the wiki is the filter**: a story matters here because it touches a client, a
person, an employer, a competitor or an objective this wiki already tracks. Everything else is a headline
the owner could have got anywhere.

## Configuration

Up to **10 topics**, in `llm-wiki.yml`:

```yaml
news:
  enabled: true
  topics_per_run: 3          # round-robin; each topic comes round every 3-4 days
  max_captured_per_run: 5    # hard cap on what reaches the wiki
  cursor: 0                  # which topic the rotation is up to
  topics:
    - name: "Acme Corp"
      why: "our employer — funding, leadership, layoffs, product launches"
    - name: "Globex"
      why: "largest competitor in our vertical"
    - name: "EU AI Act enforcement"
      why: "we sell to European public sector; enforcement changes our compliance story"
```

**`why` is not decoration.** It is what separates a story that matters from one that merely mentions the
word — "Acme Corp" the employer versus a same-named bakery, "Mercury" the client versus the planet. Ask
for it, and keep it in the owner's words.

**Ten is a ceiling, not a target.** Three sharp topics produce a better wiki than ten vague ones, and
vague topics ("AI", "technology") return endless matches that clear no bar and waste every run.

## Round-robin

Scan `topics_per_run` topics each run, advancing `cursor` and wrapping. Each topic comes round every
three or four days — enough for anything that matters, and it keeps a daily job bounded.

Two exceptions to strict rotation:

- **A topic that produced a high-relevance capture last run is re-scanned next run**, once. Stories that
  touch this wiki tend to develop over days, and the follow-up is usually more useful than the first hit.
- **A topic never scanned** (newly added) goes first, regardless of cursor.

Record the scan in the run report **even when nothing was captured**: which topics were scanned, and that
they were quiet. Otherwise "no news items" and "we did not look" are indistinguishable, which is the same
failure as a truncated page-scan reported as a quiet week.

## Relevance — the part that matters

Before scanning, build the **known-entities set** from the wiki: client names (`Wiki/Clients`,
`Prospective-Clients`, `Former-Clients`), people (`Wiki/People`, `My-Team`, `Consultants`), the employer,
and every Focus Area statement and objective. This is cheap — hub `### Index` lines carry most of it.

Then grade every candidate story:

- **Direct** — it names a known entity. A client, a person the owner works with, the employer, a named
  competitor. **Capture it.**
- **Indirect** — it plainly bears on one without naming it: a regulator acting in a client's industry, an
  acquisition in a client's market, a competitor of a client, a policy change affecting a Focus Area.
  **Capture it, and say in one line what the connection is** — an indirect item with the connection
  unstated reads as a random headline and gets ignored.
- **Topical only** — it matches the topic but touches nothing this wiki knows. **Do not capture it.**
  This is most of what any search returns, and dropping it is the whole discipline. A story worth reading
  in general is not the same as a story worth keeping here.

**Never capture a story on a keyword match alone.** Company names collide, people share names, and a
wiki filling with same-name coincidences loses trust faster than one that misses a story.

**Cap at `max_captured_per_run`.** If more clear the bar than the cap allows, keep the ones touching the
most entities, or an objective, and say how many were dropped.

## Where captures go

Double-routed, like Focus Area material:

- `Wiki/{{PRIMARY_NS}}/News-Log.md` — the chronological record, one dated section per run.
- **The entity's own page** — a story about a client belongs on that client's page, under a "Market and
  news" section, not only in a log nobody reads backwards.
- A Focus Area's pages too, where it bears on one.

Each captured item records: the headline, the outlet, the date, **the connection to this wiki** (which
entity, direct or indirect), one or two sentences on what it says, and the link — with a text-only
snapshot in `Archives/` per the normal URL rule.

**Archive only what is captured**, never everything scanned. Ten topics a day of full snapshots would
bury the folder inside a month.

## Deduplication

The same story appears in many outlets and develops over days. Keep a `seenStories` set in the ingest
state keyed on a normalized headline plus the primary entity. A follow-up that adds something material
updates the existing entry in place rather than adding a new one; a re-run of the same story is skipped
silently.

## In the brief

News is **low-impact by default** under the brief's triage — it is context, not a commitment, and it must
never crowd out something the owner owes or is owed.

Surface it only when it is **direct and consequential**: a client acquired, an employer announcement, a
regulatory change hitting a Focus Area, a named competitor doing something material. **One line, at most
two items**, below the commitments. Everything else waits in the wiki for whenever the owner reads it.

A story that changes the stake on an existing commitment is different — say that **on the commitment**,
where it changes a priority, rather than as a separate news line.

## When the web is unavailable

Web access is not guaranteed in every environment a run happens in. If it is unavailable, **report it as
a source that could not be checked** — exactly as with any unauthorized connector — and leave the cursor
where it is so nothing is skipped. Do not silently produce a run with no news and no explanation.
