# LLM Wiki

A self-maintaining knowledge base that lives in a folder on your machine.

Ask it a question, it searches what it knows. Tell it something, it files it. Every morning it reads your
meetings, chats, email and tickets on its own, and sends you a brief on what happened and what's coming.

Plain markdown files, nothing to install beyond the plugin. You share it by sharing the folder.

---

## Quick start

**What you need first:** the **Claude desktop app**, and you'll be using it in **Cowork** — the mode
where Claude works on a folder on your computer and can create and edit files in it.

This won't work in Claude in a web browser, and it won't work in an ordinary chat or a Project. Your wiki
is a real folder of files, and something has to be able to write to it. If you're reading this in a
browser tab, install the desktop app first.

---

### 1. Add the plugin

**In the Claude app** — open **Settings → Plugins**, choose to add a marketplace (some versions call it
a plugin source or a repository), and paste in:

```
mauricio-morales/llm-wiki
```

Then install **llm-wiki** from the list that appears. That's it — and because it's connected to this
repository, you'll get updates as they're published.

**If you use Claude Code in a terminal**, the same thing in one line:

```
/plugin marketplace add mauricio-morales/llm-wiki
```

**If neither works**, download the `.zip` from
[Releases](https://github.com/mauricio-morales/llm-wiki/releases) and upload it in **Settings → Plugins**.
This works fine, but it's a one-time copy — it can't update itself, so you'd re-download each new version.

### 2. Make a folder for the wiki

A normal, empty folder on your computer — made in Finder or File Explorer, the same as any other folder.
Give it a real name: `Acme Wiki`, `My Work Brain`.

**If you want to share it with your team, create it inside a folder that already syncs** — your OneDrive,
Dropbox or Google Drive. That sync is how everyone else gets it later. If it's just for you, anywhere is
fine.

### 3. Start a **Cowork session** on that folder

This part matters, and it's the step people get wrong.

**It has to be a Cowork session** — the kind of Claude session that works on a folder on your computer
and can read and write the files in it. In the Claude app, start a new Cowork session and **choose the
folder you just made** when it asks which folder to work in.

An ordinary chat won't do. Neither will a Project. Both can *read* things you give them, but neither can
create and update files in a folder on your machine, and that is the entire job here — your wiki *is*
that folder.

You'll know you got it right because the session shows the folder it's working in.

**Star it while you're there.** In the folder picker there's a star next to each folder — clicking it
makes that folder the default for new sessions. Worth doing: everything below assumes you're in the wiki
folder when you ask it something, and starring it means every new session starts there instead of you
picking it each time. If you're setting up a wiki you'll use daily, this is the difference between asking
a question and remembering to set up a session first.

### 4. Type `/wiki-setup` and press enter

Type it into the message box like you'd type anything else — the leading `/` is part of it.

It then asks you a handful of multiple-choice questions: what to call the wiki, who can read it, which of
your connected tools it should read, when it should run, how far back to reach. A few minutes.

*"Just do whatever's normal"* is a complete answer to any of them.

**That one command is the only one you ever type.** After setup, the folder takes over — ask a question
and it searches the wiki, say "save this" and it files it, say "reconfigure the wiki" to change anything.

### Joining a wiki someone else set up

Do step 1, then skip to here.

1. **Make sure the shared folder has synced to your computer** — you should be able to open it in Finder
   or File Explorer and see a `Wiki` folder inside.
2. **Start a Cowork session on it** (same as step 3 above — a Cowork session, not an ordinary chat, and
   choose that folder). Star it in the picker to make it your default, so new sessions start here.
3. **Just start asking.**

It already knows what to do: the instructions live inside the folder, so they arrive with it. Nothing to
install, nothing to set up.

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

**It keeps itself current.** The folder gets its own copy of the skills, so it works for anyone who syncs
it — which means it can fall behind. Every so often (at most weekly, and only after it has finished what
you asked) a session checks whether a newer version is published and offers it in one line. Updates merge
rather than overwrite: anything you've customized is preserved, and a genuine conflict is shown to you
instead of guessed at. Scheduled jobs never update themselves.

Keep your own rules in `CLAUDE.md` and `Wiki/Schema.md` rather than in the skill files — those two are
yours, and no update touches them.

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

One person sets the wiki up in a folder on a synced drive. Everyone else syncs that folder and starts a
Cowork session on it. The instructions and a copy of the skills live inside the folder, so their session
knows what to do immediately — nothing to install.

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
hooks/                       SessionStart check that orients a session on a wiki folder
skills/wiki/                 the engine: query, ingest, prune, lint, status, import
skills/wiki-setup/           the setup wizard
  templates/                 Schema, Hub, Dashboard, Access-Log, CLAUDE.md, config, report shell
  references/                source catalog, backfill protocol, scheduled-task templates, updates
```

In the [repository](https://github.com/mauricio-morales/llm-wiki) this lives under `plugins/llm-wiki/`;
everything beside it there is development tooling and is not part of what you install.

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
