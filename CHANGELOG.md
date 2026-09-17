# Changelog

Derived from [llm-wiki](https://github.com/MehmetGoekce/llm-wiki) by Mehmet Gökçe (MIT) — see
[LICENSE](LICENSE).

Versions your team can act on. Bumped on every repackage.

- **Patch** — wording, fixes, sharper instructions. Nothing to do.
- **Minor** — new behavior. Worth re-running `/wiki-setup` in reconfigure mode to pick it up.
- **Major** — changes how you start a wiki, or invalidates an existing setup. Read the entry.

On a shared wiki, reconfigure also re-copies the skills into the folder, so one person updating
propagates to everyone who syncs it.

## 1.13.1 — 2026-09-17

**Fixed — the commitment ledger was not scoped to the owner.**

The two directions were defined as "they owe the owner" and "the owner owes them", but nothing said that
third-party commitments are out of scope. Meetings and chats are full of them — *"Ana will send Dana the
deck"* — and an ingest reading a transcript would have captured those as readily as the owner's own. The
result is a list the owner can neither chase nor close, which is how a list stops being read.

- **Every entry has the owner on one side.** Commitments between other people are context, not tracked
  items; they surface in the log or a Focus Area if they matter.
- **Delegation does not remove a commitment.** Work the owner agreed to and handed on is still `mine` —
  what changed is who is doing it, not who answers for it.
- **A commitment to the owner's team that the owner will chase counts as `theirs`.** The test is who
  follows up or answers for it, not whose name is in the message.

## 1.13.0 — 2026-09-17

**Fixed — updates never reached deployed wikis' scheduled tasks.**

The 1.8.0 update mechanism covered only the folder's copy of the skills. Task prompts are generated once
at setup and live outside the folder, so **nothing had ever updated them.** Everything shipped since
1.8.0 — draining paged sources, two-directional commitments, item ids, async replies — was reaching new
wikis only. An existing wiki would have kept running its original instructions indefinitely, with no sign
anything was stale.

- **Every task now carries a stamped template version** in its first line, mirrored under that job in
  `llm-wiki.yml`. Without it there is no way to tell which template a running task came from.
- **New `references/task-self-update.md`**, embedded as Step 0 of every task: compare the stamp against
  the folder's `skills_version`, and if behind, regenerate the prompt from the current templates plus
  `llm-wiki.yml`.
- **The current run finishes on the prompt it started with**; the new one takes effect next run. This
  keeps 1.8.0's rule that a job must not rewrite the instructions it is midway through executing —
  otherwise nobody can say afterwards which version produced which output. One run's delay buys every run
  being attributable.
- **Regeneration is safe because configuration lives in `llm-wiki.yml`, never only in the prompt.**
  Accordingly, reply-learned format preferences (1.12.0) now go to a `preferences` block in the config
  rather than into the task text, where a rebuild would have destroyed them.
- **Failure is non-destructive**: if regeneration cannot complete, the existing prompt is kept, the run
  proceeds, and it is reported. A working old prompt beats a broken new one.
- **Regeneration is always reported** — version moved from and to, plus what changed. Nobody should
  discover their jobs changed behavior by noticing different output.
- **It never changes schedules, destinations or enabled sources.** It updates instructions, not choices.
- Setup gained a one-time migration for wikis predating stamping: offer to regenerate and stamp their
  tasks from current templates and existing config.

## 1.12.1 — 2026-09-17

**Fixed — Focus Area items had no id until a report rendered one.**

1.12.0 assigned ids at capture for commitments, but not for Focus Area items — while the report template
still showed `[52]` on open threads. The report would therefore have had to mint them, which defeats the
whole mechanism: an id generated while rendering is a position in that message, not an identity. It
shifts as items are added, closed or reordered, so *"close 52"* would land on a different item next week.

- Focus Area items now get their `[id]` **at ingest**, written onto the line in the wiki page, from the
  same wiki-wide `nextItemId` counter the commitments use. The schema's line format shows it.
- Stated explicitly in the protocol and both report templates: **a brief or report reads ids, it never
  invents them.** An item reaching a report without one is an ingest bug — assign it, write it back to
  the source, and say so.

## 1.12.0 — 2026-09-17

**Added — everything sent out is two-way, and every listed item is addressable.**

Reply handling existed only on the daily brief, was written around one chat connector, and Focus Area
reports had none at all. And nothing listed carried an identifier, so a reply had to quote text back —
which is why nobody would have bothered.

- **New `references/async-replies.md`**, embedded into every delivering task's prompt (the brief and each
  Focus Area report), filled in per channel — Slack thread, Teams chat or email reply. One copy to
  correct rather than a rule duplicated per template and left to drift.
- **Replies are read and acted on *before* the next artifact is composed.** One that contradicts what the
  owner said last night proves the channel does not work, and they stop replying.
- **Act at the source, not in the presentation**: state changes to the state file, corrections to the wiki
  page, **format and presentation preferences into the task's own prompt** so they persist. A preference
  honored once and forgotten is worse than ignoring it outright.
- **Short `[41]`-style IDs** lead every listed item, so a reply can be *"close 41"* or *"regarding 41,
  that's not true"*. One monotonic counter per wiki (`nextItemId`), assigned at capture, **never changed
  and never reused** — a recycled id silently routes an old instruction to a new item. Kept short enough
  to type one-handed on a phone, which is the whole point.
- **Ambiguity is never guessed at, especially a close** — closing the wrong item is the unrecoverable
  case, because the owner stops seeing it and assumes it was handled. Say what could not be interpreted.
- **Each artifact opens by confirming what it actioned** ("Closed [41] and [17] per your notes"). Not
  politeness — a reply the owner cannot see landing is a reply they stop sending.
- Setup now tells the user the channel is two-way. One nobody knows about gets used as a broadcast.

## 1.11.0 — 2026-09-17

**Added — reference material for local filesystem and database sources.**

Found in the field: a request to index a local app's SQLite store failed because a Cowork session is
sandboxed and cannot read arbitrary paths. The docs actively said the opposite — *"the session already
runs on this machine, so there is no special access model"* — which would have led to recording a path
that the nightly job could never read, reporting quiet weeks forever.

- **Corrected that claim** in the source catalog and the setup wizard. A local path is not access.
- **New `references/local-sources.md`**: how to expose a local resource through an MCP server, the
  `claude_desktop_config.json` locations, the restart requirement, and verified SQLite and filesystem
  configs. **Not part of the setup conversation** — consulted only when a local source is requested.
- **Match the server to the datastore.** The two examples are SQLite and filesystem; MySQL, MariaDB,
  Postgres and document stores each need their own. Search the MCP registry rather than reciting a
  package name from memory, since a stale one fails confusingly.
- **Capture the schema once and write it into the ingest task.** Tables, the columns actually used and
  their types, the stable dedup key, and the change-detection timestamp — so a record edited after
  ingest is updated in place rather than skipped, and so a scheduled job never rediscovers structure at
  6am. Explicitly includes checking whether an app keeps *more than one* list of records, since a job
  told about one will silently ignore the rest.
- **Credentials go in `claude_desktop_config.json` only** — never `llm-wiki.yml`, a task prompt, or a
  wiki page. Read-only accounts where the datastore supports them; narrowest possible filesystem grants.
- Ad-hoc "index my X" requests now route to reconfigure rather than being done once by hand, which leaves
  the user believing a source is wired up when it is not.

## 1.10.0 — 2026-09-17

**Changed — commitment tracking now covers both directions and fires on deadlines.**

The previous version tracked only asks the owner **sent**, and aged them by time elapsed (7 days, then
14). Two things were therefore missed: anything the owner **agreed to produce** for someone else was
never tracked at all, and a stated deadline did nothing — a thing due Friday surfaced on day 7 regardless.

- **Two directions.** `theirs` (someone owes the owner) and `mine` (the owner owes someone). `mine` is
  captured **only when the owner accepted** the request — an unanswered ask from someone else is not a
  commitment, though it is flagged once so it does not vanish.
- **`due` is never empty, and drives everything.** A stated date wins, resolved to an absolute date
  against the *message's own* date at capture time ("by Friday" in a message sent Sept 2 is Sept 4). With
  no date stated, `due` = `asked` + 7 days, marked `dueIsExplicit: false`.
- **A defaulted nudge date is never presented as a promised deadline.** The brief says which it is,
  because the owner will quote it back to someone.
- **Surfaces on the due date and every day after until closed** — not once. An overdue item that stops
  being mentioned is an item that got dropped. Anything the owner owes with a real stated deadline also
  gets one heads-up the previous working day: being told on the morning it is due is often too late to
  produce a document.
- **Nothing surfaces before its due date.** A list of everything open every morning becomes wallpaper.
- **The brief renders two separate sections**, "You owe" first. They are opposite instructions — do work
  versus chase someone — and merging them makes the reader sort them by hand every day.
- **Closed only on evidence, never on age.** `theirs` closes when the answer or artifact arrives; `mine`
  closes when the owner produced it, actively looked for in their own sent messages and activity. An
  entry left open after the work was done trains the owner to ignore the list.
- Existing wikis: entries under `pendingOutboundRequests` are migrated into `commitments` with
  `direction: theirs` on the next run.

## 1.9.1 — 2026-09-17

**Fixed — the README never said the session has to be a Cowork session.**
- Step 3 said "open a session on that folder", which only makes sense to someone who already knows what
  kind of session that is. Earlier wording had said "Cowork" and it was removed as jargon — the wrong
  call: the fix for a term people don't know is to name it *and* explain it, not to replace it with
  something vaguer. It is now named, defined in one line ("the mode where Claude works on a folder on
  your computer and can create and edit files in it"), and stated in the prerequisites.
- Says plainly what will not work and why: an ordinary chat and a Project can both read what you give
  them, but neither can create and update files in a folder, which is the whole job — the wiki *is* the
  folder.
- Added a way to tell you got it right (the session shows the folder it's working in), and the same
  instruction in the "joining someone else's wiki" path, which had the same gap.
- Steps 2 and 4 spell out the parts assumed as obvious: make the folder in Finder or File Explorer, the
  leading `/` is part of the command.

## 1.9.0 — 2026-09-17

**Fixed — paged sources were being read one page deep and reported as quiet.**

Found in the field: an unscoped mail sweep returned its first 100 records, more existed, and the run
reported the window as quiet. Nothing errored. A capped sweep and an empty one are written to the wiki
identically, so the gap was invisible and would have stayed that way.

The existing "never silently truncate" rule only ever covered a **single item too large for one
response** — a long transcript. It said nothing about **paged result sets**, which fail in the opposite
direction: no error, a plausible-looking result, and a hole.

- **Drain to depletion.** Follow the cursor (`nextLink`, `next_cursor`, `has_more`, `offset`) until the
  source says there are no more pages. Added to the ingest job, the backfill protocol, the engine skill
  and the generated `CLAUDE.md`, so it applies whether or not a skill was explicitly invoked.
- **A result count at exactly the page size is a cap, not an answer.** 100, 50, 25, 200, 1000 — a real
  count is ragged. Treat an exact-page-size result as truncated until proven otherwise.
- **When it can't be drained, narrow and re-query** — split the window in half and recurse until each
  part returns under the cap — rather than accepting the partial.
- **New backfill unit status `truncated`.** A capped unit is never `done` and never `empty`; it is split
  into half-window units and the original marked `truncated`. Marking a capped unit `done` was the worst
  case available: the checkpoint would claim the window was covered, nothing would revisit it, and the
  gap would be permanent. A backfill is no longer "complete" while any unit is `truncated`.
- **Reports now carry per-source retrieved counts and windows**, which is the only place a cap shows.
- **`lastSuccessfulRun` is never advanced after a run with an undrained source** — leaving it widens the
  next window and retries the gap.
- **The monthly lint hunts for the signature**: per-source counts sitting at a round page size, and any
  backfill unit still marked `truncated`.

## 1.8.1 — 2026-09-12

**Changed — the plugin moved into `plugins/llm-wiki/` in the repository.**
- The repo root was the plugin root, so Spec Kit tooling added for developing the plugin (`.specify/`,
  `.claude/skills/speckit-*`) sat inside the plugin's boundary. The release zip was never affected — it
  copies an explicit file list — but a marketplace install clones the repo, and whether that tooling
  stayed dormant depended on skill-discovery rules rather than on structure. Nesting the plugin makes the
  separation structural: its root now contains only plugin files.
- The release workflow fails the build if anything matching dev tooling appears in the zip, so the
  guarantee is enforced rather than assumed.
- No change to the plugin's behavior, contents or install command. `/plugin marketplace add
  mauricio-morales/llm-wiki` is unchanged.

## 1.8.0 — 2026-09-12

**Added — the folder's copy of the skills keeps itself current.**
- Setup now also writes `.claude/skills/.baseline/`, a pristine copy of exactly what was installed. It is
  never edited or read at runtime; it exists so an update can tell a **local edit** (baseline → live) from
  an **upstream change** (baseline → new). Without it the two are indistinguishable and every update is
  either a clobber or a no-op.
- A session checks for a newer published version **at most weekly**, only when the plugin is present, and
  **only after finishing the user's request** — never before it, and never during a scheduled run, since a
  job that rewrites its own instructions mid-flight is unreviewable when it later misbehaves. Declining
  silences it for 7 days. No scheduled task was added for this.
- Applying an update: unmodified files are replaced outright (the common case, zero risk); modified files
  get a three-way merge. Conflicts are **shown, never guessed** — a silently mis-merged instruction is
  worse than no update, because it will be followed. A local change is never dropped to take an upstream
  one. Only the `ingest_owner` updates a shared wiki.
- Guidance, stated in the skills and the generated `CLAUDE.md`: **personalizations belong in `CLAUDE.md`
  and `Wiki/Schema.md`, not in skill files.** Those two are never overwritten, so a rule written there
  survives every update and takes effect immediately — the best merge conflict is the one never created.
- The monthly lint now reports baseline integrity and lists locally-modified skill files, and will
  re-stamp a missing baseline only when the live files are unmodified.

**Fixed**
- README quick start rewritten for people who don't use a terminal. The install step led with
  `/plugin marketplace add`, which only exists in Claude Code — someone in the desktop app had nothing to
  act on. The app's Settings → Plugins path now leads, with the slash command as the alternative and the
  zip as a last resort. Added the prerequisite nobody had stated: this needs the desktop app, not Claude
  in a browser. "Cowork session" replaced with plain language throughout.

## 1.7.0 — 2026-09-12

**Published as an open-source repository.**
- Repo doubles as its own marketplace: `.claude-plugin/marketplace.json` alongside `plugin.json`, with
  the plugin at `source: "./"`. Installable with `/plugin marketplace add mauricio-morales/llm-wiki`,
  which is also the path that delivers updates — an uploaded zip is machine-local and can never update.
- Added a release workflow: tagging `v*` builds the zip and attaches it to a GitHub Release. It refuses
  to publish if the tag, `plugin.json` and `marketplace.json` disagree on the version — the three drifting
  apart is the failure this project has already had once.
- The zip is **not committed**. It is generated from this repo, so a committed copy would duplicate the
  source and go stale on the next edit. `.gitignore` excludes it.
- README carries real install instructions.

## 1.6.3 — 2026-09-12

- Attribution to **Mehmet Gökçe** / [llm-wiki](https://github.com/MehmetGoekce/llm-wiki) extended beyond
  README and LICENSE to both skills, the CHANGELOG header, the share message, and the generated
  `Wiki/Schema.md` — the most directly derived artifact, so every wiki created carries the credit rather
  than only the package that made it.

## 1.6.2 — 2026-09-12

- Repository owner's GitHub handle substituted; `homepage` and `repository` set.
- README states explicitly that this is an independent derivative work, not affiliated with or endorsed
  by the original author.

## 1.6.1 — 2026-09-12

**Prepared for open-source publication.**
- Added `LICENSE` (MIT) — the manifest declared MIT but no license file existed. It reproduces the
  upstream **llm-wiki** MIT notice in full, as that license requires: the schema, hub, dashboard and
  access-log templates are derived from it, with substantial overlap remaining.
- README gained proper credits and a contributing note, including the standing rule that no personal or
  organizational specifics belong in this package.
- Removed the author's corporate email from the manifest; added `homepage` and an author `url`, both
  needing the repository owner's GitHub handle substituted before publishing.
- Example address changed to `example.com` (RFC 2606 reserved) rather than a real domain.

## 1.6.0 — 2026-09-12

**Added — Focus Areas: first-class topics with their own reporting.**
- Setup asks for **up to three** things the user's role is accountable for and must stay on top of. The
  cap is the feature: "everything is first-class" means nothing is. **Zero is frictionless** — name none
  and nothing is created or mentioned again.
- Each Focus Area gets its own namespace (`_index.md`, `Log.md`, `Decisions.md`, `Goals.md`, `Reports/`)
  and a one-line **statement** that becomes the routing key — matched against instead of the bare name,
  so ingest catches related material the title would miss.
- **Double routing**, enforced in the ingest job and the generated `CLAUDE.md`: anything touching a Focus
  Area is written to its normal home *and* the Focus Area's pages, captured in full rather than
  summarized. An item living only in a chronological log has not been captured.
- **Typed items** — `decision` / `idea` / `follow-up` / `question` / `signal` — with authority mandatory
  on decisions. The type decides which report section an item lands in; untyped items produce a list of
  events rather than a report.
- **One report task per Focus Area**, on the user's chosen day and cadence. Each run writes a run page
  (the source of truth), regenerates a cumulative HTML report, and sends a summary that leads with what
  needs the user rather than with an activity count.
- The HTML is a **single self-contained file**: sidebar of every run with an overview at the top, content
  on the right. No iframes and no external files — browsers restrict `file://` iframes and local fetch,
  and relative paths break when a synced file is moved or forwarded. Same behavior, but it survives being
  emailed. Regenerated whole each run from the run pages, so correcting a page corrects the report.
- Metrics are structural and automatic (items, open threads, decisions, threads closed, oldest open
  thread, periods since last decision) plus any the user names. Every metric carries its direction versus
  the previous run — a number without a direction is trivia. A metric with no feeding source reports as
  **"not tracked", never as zero**.

## 1.5.0 — 2026-09-11

**Changed — the wiki now captures what it learns instead of asking whether to.**
- Query write-back was "optional" and required confirmation before every write, so a session that went
  outside the wiki to answer something would *ask* whether to keep it. Asked often enough, that question
  stops being read. Now: **if answering required a source outside the wiki, the finding is filed** —
  silently, reported in one line.
- Added the capture rule, in both the engine skill and the generated `CLAUDE.md` so it applies in every
  session whether or not the skill is explicitly loaded:
  - **File without asking** when the fact came from a source actually opened, is a fact rather than a
    reading of one, and fits an existing namespace. Provenance is mandatory — name and link the document.
  - **Ask once, after the answer**, when the fact is inferred or hedged, sensitive, contradicts an
    existing page, needs structural change, or is opinion rather than fact.
  - Filing means filing properly: right page, routing line in the nearest enclosing hub, cross-links,
    `updated` set, source recorded. A fact dumped somewhere unroutable is hidden, not captured.

## 1.4.0 — 2026-09-11

**Fixed — routing could not reach nested pages.**
- `query` read only the top-level namespace hub and stopped. Any wiki that nests — a client folder with
  its own projects, say — had the sub-hub's `### Index` sitting there unreachable, so the pages that
  actually answered a question were invisible to routing and only findable by grep. Routing now
  **descends**: a routing line marked `#hub` is another index, not an answer, and it keeps matching down
  to 3 hops (namespace → entity → sub-namespace). Hub reads stay cheap, so this is still an index walk,
  not a scan.
- `ingest` now writes the routing line into the **nearest enclosing hub** rather than the top-level one,
  creates an `_index.md` whenever it creates a folder, and keeps a promoted page as its new folder's
  `_index.md` so inbound `[[links]]` still resolve.
- Schema documented sub-namespaces explicitly and raised max depth from 3 segments to 4
  (`Wiki/Clients/Acme/Projects/Page`). The old cap forbade structures that already exist and work.
- New lint rules: **missing sub-hub** (a folder with children and no `_index.md` — a routing dead end),
  **unmarked sub-hub** (a hub-pointing line without `#hub`, so routing never descends), and
  **over-deep nesting**.

**Added**
- **`My-Team`** namespace in both presets — the user's own team, with the meaning resolved at setup: a
  manager's direct reports and the running of the team, or the team an individual contributor sits in.
  Kept distinct from `People` (everyone else), and flagged as usually the most sensitive namespace on a
  manager's wiki, so the privacy rules must cover it explicitly.

## 1.3.0 — 2026-09-11

**Changed**
- Namespace defaults are now two presets instead of one generic list. **A. Client services / delivery
  org** — Clients, Prospective-Clients, Former-Clients, Consultants, People, Operations, Strategy, Tech,
  Reference, Personal — recommended when the stated purpose mentions clients, delivery, accounts or
  staffing. **B. General knowledge base** — the previous set — otherwise. The old default came from the
  upstream project and was missing the namespaces a client-facing org actually fills first.
- Setup also proposes namespaces from the purpose sentence, rather than only offering a fixed list.

**Added**
- Guidance that the client lifecycle is three namespaces (Prospective → Clients → Former), offered
  together or not at all, so an ending client moves rather than disappears.
- `Clients` holds one page or folder per client; no per-client top-level namespaces.
- Do not create a namespace with no source feeding it — an empty hub is worse than a missing one, since
  it joins routing, matches nothing, and costs a read on every query touching its topic.
- The primary namespace is described as a destination, not a topic: where ingest writes when a fact has
  no better home.

## 1.2.1 — 2026-09-11

**Fixed**
- Removed the `commands/` directory and the explicit `commands`/`skills` arrays from `plugin.json`.
  Both skills are already invocable as `/wiki` and `/wiki-setup`, so the command file was dead weight —
  the entry point people actually type never came from it. Declaring the arrays is also non-standard:
  no official plugin does it, and auto-discovery from the conventional directories is the current
  format. No change in how anything is invoked.

## 1.2.0 — 2026-09-11

**Added**
- Version stamping: `wiki_version` and `skills_version` in `llm-wiki.yml`, plus
  `.claude/skills/.llm-wiki-version` in the folder.
- The monthly lint reports version drift between the folder's copied skills and the running plugin —
  on a synced folder there was otherwise no signal that a teammate was running an old version.
  Reported as information, never as an error; a wiki a version behind works fine.

## 1.1.0 — 2026-09-11

**Changed — this is the version that works against a local folder.**
- Wikis now live in a **writable local folder** opened in a Cowork session, not a project. Setup
  verifies the folder is writable before asking anything.
- Entry point is **`/wiki-setup`**, invoked explicitly. The earlier "say hi and it starts" trigger is
  gone; the SessionStart hook is now only a pointer.
- Storage guidance is about folder weight and sync cost rather than a project quota. Same text-only
  archiving rule, better reason: on a synced folder every megabyte reaches everyone on every change.

**Added**
- **Short name**, required. Prefixes every scheduled task id and title (`acme-wiki-ingest`,
  "Acme · daily ingest") so several wikis on one machine stay tellable apart. Setup refuses a prefix
  already in use.
- **Per-source customization notes** — free text, in the user's words ("only the sales distribution
  list, not my inbox"), stored and pasted into the task prompt **verbatim**, never paraphrased. On a
  shared wiki a note that narrows scope is a privacy boundary, not a filter.
- **Sharing model**, documented and enforced: one designated ingest owner, personal briefs, and sync
  conflict copies surfaced by the lint rather than deleted. A teammate who runs `/wiki-setup` on an
  already-configured folder is now told what is running and who owns it.
- Setup copies the skills into the folder's `.claude/skills/`, so syncing the folder is enough — a
  teammate installs nothing.

**Fixed**
- **Identity is resolved, not requested.** Name, email, timezone and chat user id come from the
  connectors and the environment, confirmed in one correctable line. Nobody is asked to look up their
  own member id. Working hours are not asked or guessed; the brief infers them from the calendar.
- **Skip logic is structural.** A brief is silenced only by an entry covering the whole working day.
  Partial blocks — evening protection, lunch, focus time — are never absence, whatever they are called
  and whether or not they are flagged out-of-office. The previous wording generalized one person's
  calendar habits into a claimed norm and primed the model to hunt for them. Calendar naming is
  personal; coverage is not. The pattern observed at setup is now recorded as an observation the user
  can correct, and a skipped day must name the entry that caused it.

## 1.0.0 — 2026-09-11

First build. L1/L2 wiki with hub-index routing and LRU-demote, a guided setup, resumable historical
backfill, and three scheduled jobs: daily ingest, daily brief, monthly lint.
