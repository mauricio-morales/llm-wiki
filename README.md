# LLM Wiki

A self-maintaining knowledge base that lives in a folder on your machine.

Ask it a question, it searches what it knows. Tell it something, it files it. Every morning it reads your
meetings, chats, email and tickets on its own, and sends you a brief on what happened and what's coming.

Plain markdown files, nothing to install beyond the plugin. You share it by sharing the folder.

An implementation of **Andrej Karpathy's LLM wiki idea** — that instead of re-reading your documents on
every question, an LLM should incrementally build and maintain a wiki of what it has learned, and answer
from that. ([the original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f))

---

## Get started

The wiki runs in either app. Pick the one you use; the wiki it builds is the same.

- **[Set up in Claude](https://github.com/mauricio-morales/llm-wiki/blob/main/docs/setup-claude.md)**: the Claude desktop app, in Cowork.
  The original, and the most tested.
- **[Set up in ChatGPT](https://github.com/mauricio-morales/llm-wiki/blob/main/docs/setup-chatgpt.md)**: the ChatGPT desktop app. *Preview:
  built from the same instructions, not yet run end to end there.*

Each page takes you from installing to your first wiki in four steps, and covers joining a wiki someone
else set up and upgrading later.

> Built on the L1/L2 wiki architecture from **[llm-wiki](https://github.com/MehmetGoekce/llm-wiki)** by
> **Mehmet Gökçe** (MIT). See [Credits](#credits-and-license).

---

## What setup asks you

| | |
|---|---|
| **What this wiki is for** | One sentence. It shapes what later ingests decide is worth keeping |
| **Who can read it** | Just you, or your team. Decides whether pay, performance and personal matters stay out |
| **How it's laid out** | Folders per topic (recommended), or one flat list |
| **Which sections** | A client-services set (Clients, Prospective-Clients, Former-Clients, Consultants, People, Operations…), a general one, or your own |
| **Which sources** | Everything you have connected — meetings, chat, email, tickets, documents, calendar |
| **How to read each one** | Free text, in your words: *"only the sales distribution list, not my inbox"*, *"just #incidents and #releases"*. Copied into the job verbatim |
| **Focus Areas** | Up to three things your role is accountable for. Anything touching one gets captured in full and reported on a schedule. Zero is fine |
| **How far back** | Nothing, 2 weeks, 3 months (recommended), 6 months, a year |
| **Your brief** | Where it goes, when, and whether it skips days you're out |
| **Inbox responder** | Optional. Whether to draft replies to emails asking for information your wiki has, how often, and where to tell you drafts are waiting. Drafts only — nothing is ever sent. If yes, it learns your writing voice from your sent mail and checks samples with you, and offers to handle meeting reschedules — moving the meeting itself, or just drafting replies |

Anything you skip gets a sensible default. "Just do whatever's normal" is a complete answer.

**What it does not ask you.** Your name, your email, your timezone, your Slack or Teams user id — it
reads those from the connectors and your environment and confirms them in one line you can correct. You
should never have to go and look up your own member id. Working hours it doesn't even guess: the brief
learns them from your actual calendar.

## What it builds

```
llm-wiki.yml              the configuration — everything reads this first
CLAUDE.md                 the project's instructions (AGENTS.md in ChatGPT); this is what makes it automatic
Wiki/
  Schema.md               page types, conventions, your privacy rules
  Dashboard.md            what this wiki is and how it's fed
  <Namespace>/_index.md   a hub per section — its ### Index is the routing table
  Reference/Access-Log.md which pages get read, and why
Archives/                 text-only snapshots of any URL that got ingested
wiki-*-state.json         job cursors and the backfill plan
```

Plus the scheduled jobs:

- **Daily ingest** — reads your sources, files what matters, tracks what you're waiting on
- **Daily brief** — sends you what happened and what's coming, wherever you want it
- **Monthly lint** — checks the wiki's health, retires pages nobody reads, reports storage
- **News scan** — if you name topics or areas to watch: on the cadence you pick, it searches, reads the
  article, traces it to the primary source and follows developing stories up, keeping only what touches
  something your wiki knows — stories many outlets carry ranked above single-outlet ones
- **A report per Focus Area** — if you named any: a cumulative HTML report (sidebar of every run, overview
  with trends) plus a short summary message saying what changed and what needs you
- **One-off requests** — ask for something on a date (*"send me an agenda for my trip on the 9th, from
  everything we say we'll discuss there"*) and it gets a page in the wiki holding the whole request, plus a
  one-time task that delivers it and then **deletes itself**. Nothing is lost when the task goes: the page
  keeps the ask, everything collected, and when it went out — ask for it again and a new task is made from it
- **Inbox responder** — if you want it: once to three times a day, it finds emails asking you for something
  your wiki already knows — a date, a status, where something stands — **writes a reply draft**, and tells
  you drafts are waiting. **It never sends anything**, never marks mail read, and leaves anything asking you
  to decide, commit, approve or negotiate for you. It never puts internal or another client's information
  into a draft to an outside recipient. Drafts are written **in your voice**: during setup it reads your sent mail
  to learn how you write — and how that changes with how close you are to the reader — shows you a sample
  for each and asks if it sounds like you, then keeps learning from how you edit drafts before sending.
  Optionally it also handles **rescheduling**: when someone proposes a new time or declines because they
  can't make it, it checks your colleagues' calendars and **moves the meeting** — to the time proposed, or
  the earliest time everyone's free. Only when someone outside has to choose does it draft them a few
  times, and it moves the meeting once they pick — or picks from the times they offer. When a new meeting
  you accept collides with another, it reschedules the other one: moving it if it's yours, drafting a
  "can't make it — how about…" to its organiser if not. Only meetings you organise, only their time; every move
  is listed with an undo. Prefer to move meetings yourself? Choose drafts only

---

## For everyone using it afterwards

**You never type a command.** Not `/wiki`, not anything.

- **Ask a question** — "what did we decide about the Acme renewal?", "who owns the migration?", "what's
  the status of X?" — and it searches the wiki first, then answers with its sources.
- **Give it something to keep** — paste a document, drop a link, say "save this", "remember this",
  "add this", "log this" — and it files it in the right place and cross-links it.
- **Ask how it's doing** — "how's the wiki looking?" for health and metrics.
- **Change something** — "reconfigure the wiki" reopens the setup for adding a source, moving a schedule,
  or changing where the brief goes.

---

## Upgrading

New versions add features and fix problems, and your wiki keeps working on the old one until you upgrade.
You don't need to watch for releases: **your morning brief will tell you, about once a week, when your
wiki is behind**, and what to do. The steps are on your app's setup page:
[Claude](https://github.com/mauricio-morales/llm-wiki/blob/main/docs/setup-claude.md#upgrading) ·
[ChatGPT](https://github.com/mauricio-morales/llm-wiki/blob/main/docs/setup-chatgpt.md#upgrading).

The Claude plugin and the ChatGPT package are released separately, each with its own version number:
`v…` releases are Claude, `chatgpt-v…` releases are ChatGPT.

## How it works, briefly

**The idea.** Ordinary retrieval re-reads your sources on every question, so nothing accumulates — the
same synthesis gets done again and again, and it never gets better. Karpathy's proposal is to put a
compiled layer in between: the LLM reads new material once, writes what it learned into a wiki of linked
markdown pages, and answers from the wiki instead. Three operations keep it alive — **ingest** (read
sources, update pages and cross-references), **query** (answer from the compiled wiki), and **lint**
(find contradictions, stale claims and orphans). The human curates sources and asks questions; the LLM
does the bookkeeping.

This plugin implements that, and adds what it takes to run unattended: the ingest is scheduled and pulls
from your connectors rather than a folder of files, and it reports to you every morning.

The wiki is an **L1/L2 cache**. L1 is the assistant's own memory — the handful of things it must know every session.
L2 is this wiki — everything else, read on demand.

Two mechanisms keep L2 fast as it grows:

- **Hub-index routing.** Each section's hub carries one routing line per page: a link, a terse
  description, some tags. A question reads only those lines, picks the three best pages, and opens just
  those. It never greps the whole wiki.
- **LRU demote.** Every page read is logged with *why* it was picked. The monthly job retires pages
  nobody has opened in six months out of the routing index. The file stays, its links stay, it is still
  searchable — it just stops competing for attention. Nothing is ever deleted.

**Historical backfill is resumable by design.** A year of history is hundreds of source-weeks and will
not finish in one run. It is planned into small units, executed one at a time, and checkpointed after
each one — so running out of tokens halfway is an ordinary event you simply continue from. The daily
ingest also drains a few units every run, so a long backfill finishes on its own.

---

## Things worth knowing

**Weight.** Text pages stay small; archived web pages don't, so URLs are archived text-only (one real
case: 44.8 MB → 74.6 KB, every word and link intact). On a synced folder every megabyte is copied to
everyone who has it, so the monthly job reports the size and flags growth early.

**It keeps itself current.** The folder gets its own copy of the skills, so it works for anyone who syncs
it — which means it can fall behind. Every so often (at most weekly, and only after it has finished what
you asked) a session checks whether a newer version is published and offers it in one line. Updates merge
rather than overwrite: anything you've customized is preserved, and a genuine conflict is shown to you
instead of guessed at. Scheduled jobs never update themselves.

Keep your own rules in `CLAUDE.md` (`AGENTS.md` in ChatGPT) and `Wiki/Schema.md` rather than in the skill files — those two are
yours, and no update touches them.

**No version history.** The folder isn't a repository. So the rule everywhere is **append, never
overwrite**, and nothing is ever deleted except on your explicit instruction.

**Credentials never go in.** The wiki is shared storage read by automated jobs. Setup never asks for a
password or token, and the lint scans for leaked ones.

**The jobs run on your machine**, while the app (Claude or ChatGPT) is open. One due while it was closed runs on next
launch — a quiet morning is usually that, not a broken job.

**Reading it elsewhere** happens through the folder, not the jobs. On a synced drive the files reach
every device that drive syncs to, and a session with that drive's connector can read them from a phone.
That is real read access; it is not the ingest running in the cloud.

**Name your wiki something short.** One machine can host several — a personal one and a team one is
common — and the short name prefixes every scheduled task so they stay tellable apart.

**Numbers from transcripts get flagged, not trusted.** Speech-to-text routinely confuses 15 with 50 and
16 with 60. When a figure doesn't fit the rest of the conversation, the wiki records the discrepancy
rather than quietly picking one — and never attributes the error to whoever was speaking.

---

## Sharing it with your team

One person sets the wiki up in a folder on a synced drive. Everyone else syncs that folder and starts a
session on it in their app. The instructions and a copy of the skills live inside the folder, so their session
knows what to do immediately — nothing to install.

Two rules make the difference between that working and it quietly going wrong:

**One person runs the ingest.** Scheduled jobs are per-machine. If three people sync the folder and all
three have ingest jobs, three runs append to the same pages every morning — and since the pages are
append-only, nothing errors, it just silently triples. Worse, each run pulls from *that person's*
connectors, so a shared wiki ends up holding someone's private inbox. Whoever runs the setup is the
ingest owner; everyone else queries, files things manually, and runs their own brief.

**Briefs are personal.** A brief reads your pending asks and your calendar and goes to your Slack. Each
person who wants one sets up their own.

**Everyone uses the same app as whoever set it up, for now.** A wiki set up in Claude keeps its
instructions where Claude reads them, and one set up in ChatGPT where ChatGPT does. A teammate on the other
app can still open the files, but their sessions won't know the wiki's rules.

Sync isn't a merge — a simultaneous edit leaves a "conflicted copy" file rather than combining them. One
ingest owner makes that rare. If conflict copies do show up, the monthly job surfaces them and offers to
merge; it never deletes them.

---

## What's in the package

```
.claude-plugin/plugin.json   manifest
agents/voice-profiler.md     learns the owner's email voice from their sent mail, in its own context
hooks/                       SessionStart check that orients a session on a wiki folder
skills/wiki/                 the engine: query, ingest, prune, lint, status, import
skills/wiki-setup/           the setup wizard
  templates/                 Schema, Hub, Dashboard, Access-Log, CLAUDE.md, config, report shell
  references/                source catalog, backfill protocol, scheduled-task templates, updates
```

In the [repository](https://github.com/mauricio-morales/llm-wiki) this lives under `plugins/llm-wiki/`.
The ChatGPT package, `plugins/llm-wiki-chatgpt/`, is generated from it by `scripts/build_chatgpt.py`:
the same skills with ChatGPT's file names (`AGENTS.md`, `.agents/skills/`), a `PLATFORM.md` in each skill
for what doesn't translate word for word, and the voice profiler as a skill instead of an agent. Everything
else in the repository is development tooling and is not part of what you install.

## Credits and license

Three layers of other people's work sit under this:

**The idea** — [**Andrej Karpathy**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
who proposed the LLM wiki pattern: a persistent, LLM-maintained wiki compiled from your sources, with
ingest / query / lint as its core operations and the schema living in a `CLAUDE.md`. That shape is his,
and this plugin follows it closely.

**The implementation** — [**llm-wiki**](https://github.com/MehmetGoekce/llm-wiki) by **Mehmet Gökçe**,
MIT licensed. The L1/L2 cache architecture, hub-index routing, LRU-demote, and the schema, hub, dashboard
and access-log templates are derived from that project.

**The voice method** — the inbox responder's voice profiling compares the owner's real writing against the
model's own default output, after the "SICO comparative analysis" approach of the
[`voice-extract`](https://claudeskills.info/skills/athola/claude-night-market/voice-extract/) skill
(athola/claude-night-market), and tiers that voice by reader following Bell's
[audience design](https://en.wikipedia.org/wiki/Audience_design) and Giles' communication accommodation
theory. Ideas, not code — but the debt is real.

**This plugin** rebuilds it to set itself up conversationally instead of through a shell script, and adds
what running unattended needs: scheduled ingest, brief and lint jobs, connector sources rather than a
folder of files, resumable backfill, commitment tracking, and Focus Areas with their reports.

MIT licensed — the same license as the original, which MIT permits and which keeps the terms simple for
anyone building on this in turn. See [LICENSE](LICENSE), which reproduces the upstream notice in full.

This is an independent derivative work. It is not affiliated with, nor endorsed by, the original author.

## Contributing

Issues and pull requests welcome. Everything here is prompt content — Markdown skills, templates and a
single HTML report shell — so a change is a text edit, not a build. Two things to keep in mind:

- **No personal or organizational specifics.** This package is deliberately generic: the setup wizard
  learns who the user is from their connectors and environment. Examples use fictional names and
  `example.com`. A contribution that hardcodes one organization's calendar conventions, namespaces or
  naming habits makes the plugin worse for everyone else — that lesson is written into the skip-logic
  section for a reason.
- **Bump the version and add a CHANGELOG entry.** Patch for wording, minor for new behavior, major for
  anything changing how a wiki is set up or invalidating an existing one.
