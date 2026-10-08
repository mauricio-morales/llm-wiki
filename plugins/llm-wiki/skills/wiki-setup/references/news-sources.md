# News — its own job, filtered by what the wiki already knows

A news feed nobody filters is noise, and it is the fastest way to make a wiki unreadable. What makes this
worth having is that **the wiki is the filter**: a story matters here because it touches a client, a
person, an employer, a competitor or an objective this wiki already tracks. Everything else is a headline
the owner could have got anywhere.

**News is a separate scheduled task, not a source of the ingest.** The ingest reads connectors — bounded,
paged, structured. News is open-ended: a search hit is a lead, the article has to be opened, the primary
source behind it found, a consequential claim corroborated, and a developing story checked again days
later. Inside the ingest that work fought the connectors for the same budget, and whichever lost was
silently thin. On its own it gets its own budget, its own cadence chosen by the owner, and its own
failures — a run that cannot reach the web never holds back the ingest's window. The run procedure lives
in `references/task-news.md`; this file is what setup needs to ask and configure.

## Asking — two questions

Ask in one `AskUserQuestion` call where possible, after the sources, never folded into the source picker.

### 1. What to watch

*"Want me to keep an eye on the news? Up to ten topics or areas — your employer, competitors, your
industry, a regulator, a market you sell into, a technology you are betting on. I only keep stories that
touch something this wiki knows about, so it stays useful rather than becoming a feed."*

**Zero is a real answer.** No topics → no news task, no `News-Log`, nothing to explain later.

**Propose before asking.** By this point setup knows the employer (from the owner's email domain), the
purpose sentence, the Focus Areas and objectives, and often the clients and competitors the purpose names.
Offer the obvious candidates as a multi-select — *"your employer, Example Corp; the Tech vertical Focus
Area; the EU AI Act, which your purpose mentions"* — and let them add their own. Extrapolate what can be
extrapolated; ask only for intent.

For each topic, get:

- **`name`** — the company, person, regulator, market or area.
- **`why`** — why it matters, **in their words, verbatim**. Required. It is what separates "Acme Corp" the
  employer from a same-named bakery and "Mercury" the client from the planet, and for an *area of
  interest* it is the test itself: a story that bears on what the `why` says is relevant even when it
  names nothing in the wiki. Without it an area is just a keyword.
- **`queries`** — optional, and worth offering for areas rather than entities. "Nearshore software
  services" surfaces under "nearshoring", "IT outsourcing Latin America", "delivery centre opens"; one
  phrase misses most of it. Propose two or three; let them correct.
- **`outlets`** — optional. A trade publication, a regulator's press page, a company's newsroom. Checked
  directly each time the topic comes round, because the best source for a niche area is rarely what a
  general search ranks first.

**Push back gently on vague topics.** "AI" or "technology" match everything and clear no bar; ask what
about it they care about, and turn the answer into the `why` and `queries`. **Ten is a ceiling, not a
target** — three sharp topics produce a better wiki than ten vague ones.

### 2. How often

*"How often should I check?"* Options, recommended first:

| Choice | Cron (default time) | Rotation |
|---|---|---|
| **Every weekday morning (recommended)** | `0 5 * * 1-5` | every topic at least weekly |
| Every day | `0 5 * * *` | every topic at least weekly |
| Twice a week | `0 5 * * 1,4` | every topic, every run |
| Once a week | `0 5 * * 1` | every topic, every run |

"Other" covers more than once a day for a fast-moving situation — it is expensive and rarely changes what
the brief says, so do not offer it unprompted.

**Time of day is derived, not asked:** the run must **finish before the brief** and **never overlap the
ingest**, since both write entity pages and the shared id counter. Default to one hour before the ingest.
If the ingest is moved later, the news job moves with it. Say the time once in the confirmation summary.

## Sizing the rotation

`topics_per_run` is computed, not asked: **the smallest number that brings every topic round at least
once a week** at the chosen cadence — `ceil(topics / runs_per_week)`, minimum 1, and every topic on a
weekly or twice-weekly cadence. Recompute it whenever topics or cadence change. A weekday job with six
topics scans two a day; a weekly one scans all six.

The task's window per topic is "since that topic was last scanned", so a less frequent cadence costs
nothing in coverage — only in how quickly the owner hears.

## Multiple reports rank higher

**A story carried by several independent outlets outranks one carried by a single outlet.** Breadth of
coverage is the cheapest honest signal of weight available to a run: it means editors in more than one
newsroom judged it worth reporting, and it means the facts have been checked more than once. A single
trade-blog item and a story the wires, the business press and the regulator all carry are not the same
size, and a wiki that grades them the same buries the second under the first.

- **Count independent reports, not copies.** Syndicated wire copy, a press release reprinted verbatim
  and aggregator rewrites of one article are **one** report. Independent means separate reporting.
- **The count decides ordering**, everywhere ordering happens: which candidates are opened first when the
  fetch budget is tight, which captures survive `max_captured_per_run`, and which items the brief shows.
- **It never replaces the relevance bar.** A widely covered story that touches nothing in this wiki is
  still not captured, and a single-outlet story that names a client still is. Coverage ranks among
  stories that already cleared the bar; it does not let one in.
- **Record it on the item** — `reports: 4 (Reuters, FT, Bloomberg, regulator notice)` — and update it in
  place when a later run finds the story spreading. A story going from one outlet to five is itself
  news, and a reason to re-rank it.

## Configuration

In `llm-wiki.yml`:

```yaml
news:
  enabled: true
  topics_per_run: 2          # computed: every topic comes round at least weekly
  max_captured_per_run: 5    # hard cap on what reaches the wiki per run
  max_fetches_per_run: 25    # page opens per run, follow-ups and primary-source hops included
  topics:
    - name: "Example Corp"
      why: "our employer — funding, leadership, layoffs, product launches"
    - name: "Globex"
      why: "largest competitor in our vertical"
    - name: "EU AI Act enforcement"
      why: "we sell to European public sector; enforcement changes our compliance story"
      queries: ["AI Act enforcement", "AI Office fines", "high-risk AI obligations"]
      outlets: ["https://digital-strategy.ec.europa.eu/en/news"]

jobs:
  news:
    enabled: true
    template_version: "X.Y.Z"
    preferences: []
    task_id: "<slug>-wiki-news"
    schedule: "0 5 * * 1-5"
    state_file: "wiki-news-state.json"
```

Run state — per-topic last-scanned dates, rotation cursor, seen stories, open threads, pending candidates —
lives in `wiki-news-state.json`, never in the config. Config is the owner's; state is the job's.

## Where captures go

**Never onto an entity's main page.** Main pages hold internal facts; outside reporting is a different
kind of fact and would dilute them. Captures go to:

- `Wiki/<namespace>/News/<Entity>.md` — one `News` sub-namespace per namespace that has news (clients,
  people, a Focus Area), created on first capture. News about a client that is a folder still goes to
  `Wiki/Clients/News/<Client>.md`, never inside the client's folder.
- `Wiki/<primary>/News/<Topic>.md` for a topic with no entity in the wiki — an industry, a regulator.
- `Wiki/<primary>/News-Log.md`, one dated section per run, for the brief.

Never a Focus Area's `Log.md`, its `Decisions.md`, or `Objectives.md` either. **News is pulled in at read
time** — a question about an entity, a Focus Area report, the brief — rather than written into internal
pages. The owner saying "add that to Acme's page" is the one exception.

Each item carries an `[id]` from the wiki-wide counter, the connection to this wiki, its report count, and
a text-only archive of the page. **Archive only what is captured**, never everything opened.

## In the brief

News is **low-impact by default** under the brief's triage — context, not a commitment, and it must never
crowd out something the owner owes or is owed. The brief reads every `News-Log` section dated since the
last brief (a twice-weekly job writes on Monday and Thursday; Tuesday's brief still needs Monday's), and
surfaces only what is **direct and consequential**, ranked by independent reports, **one line, at most two
items**, below the commitments. A story that changes the stake on an existing commitment is said **on the
commitment**.

## Changing it later

"Add a news topic", "stop watching Globex", "check the news weekly instead" are reconfigure requests:
update `news.topics` or `jobs.news.schedule`, recompute `topics_per_run`, regenerate the news task's
prompt. A reply to a brief like *"drop Globex"* or *"more on 63"* goes the same way through the brief's
reply handling — topics are configuration, so they go to `llm-wiki.yml`, never only into a prompt.

Removing the last topic disables the task (keep the config and state so it can be turned back on). Adding
the first topic to a wiki with none creates it.
