# LLM Wiki

A self-maintaining knowledge base that lives in a folder on your machine.

Ask it a question, it searches what it knows. Tell it something, it files it. Every morning it reads your
meetings, chats, email and tickets on its own, and sends you a brief on what happened and what's coming.

Plain markdown, no database, no CLI. You share it by sharing the folder.

---

## Quick start

**1. Add the plugin.**

```
/plugin marketplace add mauricio-morales/llm-wiki
```

Or download the zip from [Releases](https://github.com/mauricio-morales/llm-wiki/releases) and upload it
in Claude's plugin settings — though the marketplace is what delivers updates, and an uploaded zip can't.

**2. Make a folder for the wiki.** To share it with a team, put it somewhere synced — a OneDrive,
Dropbox or Google Drive folder your team already has.

**3. Open a Cowork session on that folder.** Point it at the folder itself, not a project — the wiki
needs to write files.

**4. Run `/wiki-setup`.**

It asks a handful of multiple-choice questions: what to call it, who can read it, which of your connected
tools it should read, when it should run, how far back to reach. A few minutes. *"Just do whatever's
normal"* is a complete answer to any of them.

**That one command is the only one you ever type.** After setup the folder's `CLAUDE.md` takes over — ask
a question and it searches the wiki, say "save this" and it files it, say "reconfigure the wiki" to change
anything.

### Joining a wiki someone else set up

Skip steps 2-4. **Sync the folder, open a Cowork session on it, and start asking** — it already knows what
to do, because the instructions and the skills live in the folder. There's nothing else to install.

**Don't run `/wiki-setup` there.** Only one person runs the scheduled ingest. A second one means two jobs
appending to the same pages every morning, each pulling from a different person's email and chat — and
since the pages are append-only, nothing errors. It just quietly doubles, with someone's private inbox in
a shared wiki.

If you want your own morning brief, say **"set up a brief for me"** and it adds just that. A brief is
personal: it reads your pending asks and your calendar and goes to your Slack.

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

Anything you skip gets a sensible default. "Just do whatever's normal" is a complete answer.

**What it does not ask you.** Your name, your email, your timezone, your Slack or Teams user id — it
reads those from the connectors and your environment and confirms them in one line you can correct. You
should never have to go and look up your own member id. Working hours it doesn't even guess: the brief
learns them from your actual calendar.

## What it builds

```
llm-wiki.yml              the configuration — everything reads this first
CLAUDE.md                 the project's instructions (this is what makes it automatic)
Wiki/
  Schema.md               page types, conventions, your privacy rules
  Dashboard.md            what this wiki is and how it's fed
  <Namespace>/_index.md   a hub per section — its ### Index is the routing table
  Reference/Access-Log.md which pages get read, and why
Archives/                 text-only snapshots of any URL that got ingested
wiki-*-state.json         job cursors and the backfill plan
```

Plus three scheduled jobs:

- **Daily ingest** — reads your sources, files what matters, tracks what you're waiting on
- **Daily brief** — sends you what happened and what's coming, wherever you want it
- **Monthly lint** — checks the wiki's health, retires pages nobody reads, reports storage
- **A report per Focus Area** — if you named any: a cumulative HTML report (sidebar of every run, overview
  with trends) plus a short summary message saying what changed and what needs you

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

## How it works, briefly

The wiki is an **L1/L2 cache**. L1 is Claude's memory — the handful of things it must know every session.
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

**No version history.** The folder isn't a repository. So the rule everywhere is **append, never
overwrite**, and nothing is ever deleted except on your explicit instruction.

**Credentials never go in.** The wiki is shared storage read by automated jobs. Setup never asks for a
password or token, and the lint scans for leaked ones.

**The jobs run on your machine**, while the Claude app is open. One due while it was closed runs on next
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

One person sets the wiki up in a folder on a synced drive. Everyone else syncs that folder and opens a
Cowork session on it. The `CLAUDE.md` and a copy of the skills live in the folder, so their session knows
what to do immediately — nothing to install.

Two rules make the difference between that working and it quietly going wrong:

**One person runs the ingest.** Scheduled jobs are per-machine. If three people sync the folder and all
three have ingest jobs, three runs append to the same pages every morning — and since the pages are
append-only, nothing errors, it just silently triples. Worse, each run pulls from *that person's*
connectors, so a shared wiki ends up holding someone's private inbox. Whoever runs `/wiki-setup` is the
ingest owner; everyone else queries, files things manually, and runs their own brief.

**Briefs are personal.** A brief reads your pending asks and your calendar and goes to your Slack. Each
person who wants one sets up their own.

Sync isn't a merge — a simultaneous edit leaves a "conflicted copy" file rather than combining them. One
ingest owner makes that rare. If conflict copies do show up, the monthly job surfaces them and offers to
merge; it never deletes them.

---

## What's in the package

```
.claude-plugin/plugin.json   manifest
CHANGELOG.md                 what changed, and whether you need to do anything about it
hooks/                       SessionStart check: prompts setup when a project is empty
skills/wiki/                 the engine: query, ingest, prune, lint, status, import
skills/wiki-setup/           the wizard
  templates/                 Schema, Hub, Dashboard, Access-Log, CLAUDE.md, llm-wiki.yml
  references/                source catalog, backfill protocol, the three task templates
```

## Credits and license

Built on the L1/L2 wiki architecture from **[llm-wiki](https://github.com/MehmetGoekce/llm-wiki)** by
Mehmet Gökçe — the hub-index routing and LRU-demote model, and the schema, hub, dashboard and access-log
templates, are derived from that project and used under the MIT License. This plugin rebuilds it to set
itself up conversationally in a Claude session instead of through a shell script, and adds the scheduled
ingest/brief/lint jobs, resumable backfill, Focus Areas and their reports.

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
