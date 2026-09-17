---
name: wiki-setup
description: Set up, reconfigure or repair an LLM Wiki in this folder — builds the structure, schema and config, writes the folder's CLAUDE.md so questions and ingests route automatically afterwards, plans a resumable historical backfill, and creates the three scheduled jobs (daily ingest, daily brief, monthly lint). This is the entry point: it is invoked explicitly, as /wiki-setup, in a session opened on the folder the wiki should live in. Also use for "set up the wiki", "reconfigure the wiki", "add a source", "change my brief", "continue the backfill", or any request to change what gets ingested, when the jobs run, or where the brief goes.
---

# LLM Wiki — setup

Turns a folder into a self-maintaining knowledge base. Everything is plain markdown on disk, so it opens
in any editor, syncs with any drive, and is shared by sharing the folder. No CLI, no repository.

**Where this runs.** A session opened on the folder the wiki should live in — a real, writable local
folder, not a read-only project. If the folder is inside a synced drive (OneDrive, Dropbox, Google
Drive), the wiki is shareable by sync; see "Sharing" at the end.

## Phase 0 — Work out which mode you are in

This skill is invoked explicitly (`/wiki-setup`), so there is no ambiguity about whether to start.
Before saying anything, check the working folder:

- **No `llm-wiki.yml`** → fresh setup. Run the whole wizard.
- **`llm-wiki.yml` exists** → reconfigure. Read it, show the user what is currently configured, and ask
  what they want to change. Only re-ask the questions for the parts they are changing. Jump to Phase 9.
- **`llm-wiki.yml` exists but `Wiki/` does not**, or the hub pages are missing → repair. Rebuild the
  missing structure from the existing config without re-asking anything, then report what was rebuilt.
- **A backfill is in progress and the user asked to continue it** → skip straight to `references/backfill.md`
  and drain units. This is not a setup run.

**Check the folder is actually usable before asking a single question.** Write a temp file and delete
it. If the folder is read-only, this setup cannot proceed and nothing later will work — say so
immediately and ask them to open a session on a writable local folder instead. A read-only location
produces a wizard that runs happily for six questions and then fails at the point of writing, which is
the worst possible moment to discover it.

Also note whether the folder sits inside a synced drive (a path under OneDrive, Dropbox, Google Drive,
iCloud). Do not treat that as a problem — it is how this wiki gets shared — but it changes two later
answers (weight, and who runs the ingest), so establish it now.

On a fresh setup, open with one short line — greet them, say what this wiki is going to be, say it takes
a few minutes — then start asking. Do not lecture them about the architecture first.

## How to run the conversation

The people using this are not necessarily technical, and they should not have to be.

- **Use `AskUserQuestion` for every choice**, not free text. Give 2-4 concrete options with a real
  recommendation marked, and put the recommended one first. Free text only for things that genuinely have
  no options: a name, a path, an email address.
- **Ask in batches where the questions are related**, not one at a time across twenty turns. Four
  questions in one call is fine and is much less tiring than four separate turns.
- **Always have a default.** If someone says "just do whatever's normal", you must be able to finish the
  whole setup without asking anything else. Recommended defaults: Obsidian layout, whichever namespace
  preset fits their stated purpose, a 3-month backfill, ingest daily at 06:00, brief at 07:30 on weekdays, lint monthly on the
  1st, English, team audience.
- **No jargon in questions.** Ask "should the wiki keep notes on people's pay or performance?" — not
  "configure the privacy filter". Ask "how should the layout work — folders, or one flat list?" — not
  "logseq or obsidian". Explain the consequence, not the term.
- **Never ask for a credential, password, API key or token.** Connectors are authorized in Claude's own
  connector settings, never here. If a connector is missing, tell them where to go and record the source
  as pending — do not try to set it up yourself.
- Keep the whole thing to roughly **6-8 exchanges**. It should feel like a short conversation, not a form.

## Phase 1 — Work out who this is, then ask about the wiki

**This plugin ships with no idea who is using it**, and the scheduled jobs it creates need to know: they
address someone by name, judge whose sent messages count as outbound asks, and decide what "today" means.

**Resolve that; do not interview them for it.** Every field below is already sitting in a connector, in
the session, or in the environment. Asking a user to go find their own Slack member ID is asking them to
do the connector's job, and it is exactly the kind of friction this setup exists to remove.

Work in this order, and stop as soon as a field is answered:

- **Name and email** — the signed-in identity, or the profile the connectors expose (most have a
  "current user" call; the mail and calendar connectors answer both fields on their own).
- **Timezone** — the environment's own clock and locale, corroborated by when their calendar events
  actually cluster. Never ask.
- **Chat user id**, only if the brief is going to a chat self-DM — **always** from the connector's
  current-user lookup. If it cannot be resolved at setup, leave it null and have the brief task resolve
  it at send time; the connector knows who it is authenticated as. This is never a question.
- **Working hours** — do not derive this at setup and do not ask. Leave it null. The brief only needs it
  for skip logic, and by then the calendar shows the real pattern far better than an answer given
  cold on day one.

Then **confirm once, in a single line, folded into the questions below** — not as a separate turn and not
as a form: *"I've got you as Ana Ruiz (ana@example.com), Europe/Warsaw — say if that's off."* Volunteered
as a statement they can correct, not a blank they must fill.

Only ask outright for a field that genuinely could not be resolved, and only if a job actually needs it.
A missing timezone is worth one question; a missing chat id never is — that one is a connector problem,
so say the connector isn't reachable rather than passing the work to the user.

The same principle applies to everything later in this setup: **if it can be extrapolated from a
connector, the environment, or what they have already said, extrapolate it.** Ask only what genuinely
cannot be known — their intent, their audience, their preferences. Those are theirs; the rest is yours
to find out.

Never ask for a password, token or API key. None of these fields is a credential.

Then, about the wiki itself — ask together:

1. **Name** — what to call it ("Acme Delivery Wiki", "My work brain"). Free text.
2. **Short name** — a one-word handle, lowercase, `^[a-z][a-z0-9-]*$`, e.g. `acme`, `personal`,
   `platform-team`. **This is not cosmetic and it is not optional.** One machine can host several wikis —
   a personal one and a shared team one is the common case — and they would otherwise collide: two
   scheduled tasks called `wiki-daily-ingest`, two indistinguishable rows in the task list, two briefs
   that look identical in the same inbox. The short name prefixes every task id and title
   (`acme-wiki-ingest`, "Acme · daily brief"), so the jobs stay tellable apart at a glance.
   Propose one derived from the wiki name or the folder and let them accept it; only ask if they reject
   it. If a task with that prefix already exists on this machine, the name is taken — say which wiki has
   it and ask for another.
3. **What it is for** — one sentence. Free text. This becomes the routing context on the Dashboard and
   genuinely shapes how later ingests decide what matters, so don't skip it.
4. **Audience** — *just me* or *shared with my team*. This is the most consequential answer in the whole
   setup: it decides whether the wiki may hold compensation, performance, and personal detail. If the
   folder is on a synced drive, lead with *shared* as the likely answer.
5. **Language** — the language every page gets written in, regardless of the language of the sources or
   of the conversation. Default to the user's own language.

If **team**, ask the follow-up plainly: *"Some of what your sources contain isn't for everyone who can
open this project — pay, performance cases, personal matters. Should the wiki keep that out?"* Default
**yes**. Record the exclusions in the Schema's "Privacy and exclusions" section in their words, not as a
generic boilerplate paragraph — a specific rule gets followed, a generic one gets interpreted away.

## Phase 2 — Structure

1. **Layout.** *"Folders per topic (opens nicely in Obsidian or any file browser)"* → `obsidian`, the
   default and the right answer for almost everyone. *"One flat list of files (Logseq style)"* → `logseq`.
   Ask it as a layout question; do not make them know either product.
2. **Namespaces** — the top-level sections. Offer these as the choices, recommended one first:

   **A. Client services / delivery org** (recommended when the purpose mentions clients, delivery,
   accounts, consultants or staffing):
   `Clients` · `Prospective-Clients` · `Former-Clients` · `Consultants` · `My-Team` · `People` ·
   `Operations` · `Strategy` · `Tech` · `Reference` · `Personal`

   **B. General knowledge base** (recommended otherwise):
   `Business` · `Tech` · `Projects` · `My-Team` · `People` · `Learning` · `Reference` · `Content`

   **C. Name my own.**

   Whichever they pick, **propose additions from the purpose sentence they gave in Phase 1** — a wiki for
   one named initiative usually wants a namespace for it. Adding one later is cheap; it is a hub page and
   a config line.

   Three things worth knowing when shaping the list:

   - **`My-Team` is about the user's own team, and who that means depends on them.** For a manager it is
     their direct reports and the running of the team — 1:1s, performance, hiring, workload, team
     decisions. For an individual contributor it is the team they sit in — who does what, its rituals,
     its decisions, what is expected of them. Ask which, in one line, and write the answer into the hub's
     description so ingest routes to it correctly rather than guessing every run.

     Keep it distinct from `People`: `My-Team` is *my team's matters*, `People` is everyone else the user
     works with. A person can appear in both — their page lives under whichever relationship is primary,
     and the other namespace links to it rather than duplicating it. On a manager's wiki this namespace
     is usually the most sensitive one in the whole graph; make sure the privacy rules from Phase 1
     explicitly cover it.

   - **The client lifecycle is three namespaces, not one.** `Prospective-Clients` → `Clients` →
     `Former-Clients`. Keeping them separate is what lets "who are we pitching?" and "who do we bill?"
     be different questions, and it means a client that ends moves rather than disappears. Offer all
     three together or none.
   - **`Clients` holds one page or folder per client**, and those grow their own structure over time.
     Do not create per-client namespaces at the top level.
   - **Do not create a namespace you have no source for.** An empty hub is worse than a missing one: it
     shows up in routing, matches nothing, and costs a read on every query that touches its topic. If
     they want a section nothing currently feeds, say so and leave it out until a source exists.

   Namespaces must match `^[A-Za-z][A-Za-z0-9-]*$` — no spaces, no slashes. Fix an invalid name for them
   and say what you changed rather than making them retype it.

3. Note which namespace is the **primary** one — where the daily source logs land. `Personal` on a
   personal wiki; `Operations` (or a `Daily` namespace, offered if neither preset supplied one) on a team
   wiki, so the raw chronological material never clutters the curated sections. The primary namespace is
   a destination, not a topic: it is where the ingest writes by default when a fact has no better home.

## Phase 2b — Focus Areas

Read `references/focus-areas.md`. Ask once, plainly:

*"Is there anything your role is accountable for that you need this wiki to stay on top of continuously —
a vertical you own, a transformation you're driving, a market you're opening? Up to three. If nothing
fits, that's completely fine."*

**Zero is a real answer and must be frictionless.** If they say no, create nothing — no namespace, no
pages, no report job — and do not raise it again. Do not talk them into one.

For each Focus Area they name (cap at three; if they list more, say so and ask which three actually define
their next two quarters):

1. **A one-line statement of what it covers** — this becomes the hub's standing description and the
   routing key for everything else. Push for specificity: "the Tech vertical" routes badly; "the Tech
   vertical — its clients, their growth targets, and the AI-enabled services we sell into them" routes
   well, because ingest matches against it.
2. **What would tell you this is going well or badly?** Two to four, in their words. These become the
   trend lines. If they name a number no connected source reports, say so now and either find the source
   or mark it manually-updated — better than a permanently empty chart in every report.
3. **A report, or not?** Offer it; do not assume it. If yes: which day and cadence (weekly is the default;
   fortnightly and monthly are offered), and where the summary goes — same destinations as the brief.
   The HTML file is always written to the wiki either way; the summary message is what they are choosing.

Then tell them what changes, in one sentence, because it is the whole point: **anything that touches a
Focus Area now gets captured in full and written to its pages as well as wherever it normally lands, so
the report can reconstruct the thread later.**

## Phase 3 — Sources

Read `references/sources.md` and follow it. The short version:

1. **Detect first.** Enumerate the connectors and tools actually available in this session before asking
   anything. An informed question ("I can see Slack, Outlook and Jira connected — which should I
   ingest?") is worth ten generic ones.
2. **Two questions, not fourteen.** First a multi-select over what is connected: *which of these should
   the wiki read?* Then a second multi-select over the rest of the catalog: *any of these you want but
   haven't connected yet?* — recorded as `no_connector`, written into the job now, activating by itself
   the day the connector appears.
3. **Ask about multiples** after the picks: two Slack workspaces, a second mailbox, several Jira projects.
   Each instance gets its own entry.
4. **Then offer a customization note on every source they picked**, in their own words, free text. This
   is the step that makes the difference between a job that works and one they turn off after a week.

   Ask it plainly and show what it is for: *"Anything I should know about how you want each of these
   read? For example — 'only the sales distribution list, not my own inbox', 'just the #incidents and
   #releases channels', 'skip anything from the recruiting bot', 'only the Platform board', 'ignore
   internal-only documents'."*

   **Record the note verbatim into the source's entry and paste it verbatim into the task prompt.** Do
   not paraphrase it into a category, and do not silently narrow it — *"only monitor the group
   distribution list, not my inbox"* is a completely different job from "ingest Outlook", and a
   paraphrase of it ("monitor a mailbox") reverts to the wrong behavior the first time a run interprets
   it loosely. If a note conflicts with something else they said, surface the conflict rather than
   picking a reading.

   Also capture the **noise list** here — the bot channels, automated digests and system senders worth
   skipping. Getting it now saves the first month of runs from drowning in notification traffic.
5. **Local folders** (a notes directory, an exports folder, a local transcription app's data): get the
   absolute path, and **verify by listing it before recording it**. An unverified path becomes a job that
   fails silently every night. If it cannot be read, record the source as pending with the reason — never
   drop it quietly.

## Phase 4 — Where the jobs run

**They run on this machine.** There is nothing to decide and nothing to ask: the wiki is a local folder,
the ingest writes to it, and only a local run can do that. Tasks execute while the Claude app is open,
and a task due while it was closed runs on next launch. Say that once, plainly, so a quiet morning is
never mistaken for a broken job.

Two consequences worth stating at setup, because both surprise people later:

- **Reading the wiki elsewhere.** The folder is on this machine. If it sits in a synced drive, the files
  reach every other device that drive syncs to — and a session with that drive's connector can read them
  there. That is genuine read access from elsewhere, including from a phone; it is not the full setup
  running in the cloud, and the ingest still only happens here. Say it that precisely rather than
  promising "query it anywhere".
- **On a shared wiki, exactly one person runs the ingest.** See Sharing at the end of this skill. Decide
  it now and record it — `ingest_owner` in the config — rather than discovering it when two people's jobs
  write the same log page in the same minute.

## Phase 5 — How far back

Read `references/backfill.md`. Offer: none / 2 weeks / **3 months (recommended)** / 6 months / 12 months
/ a date they name.

Say two things before they choose, both of which cause confusion later if unsaid:

- Most connectors do not hold a year. Transcripts are often 30-90 days, chat search is capped by the
  workspace plan, email follows a retention policy. A 12-month request returns partial data for reasons
  that have nothing to do with this wiki.
- A deep backfill is **days of background work, not one run**. It is planned into small units, executed
  one at a time, and checkpointed after every one, so running out of tokens partway through is an
  ordinary event they simply continue from — and the daily ingest job drains 2-4 units per run on its
  own, so it finishes without them doing anything.

Do not start the backfill during setup. Write the plan, then offer to run the first few units.

## Phase 6 — The daily brief

1. **Where does it go?** Slack DM to themselves, a Slack channel, email, a Teams chat, or nowhere (write
   it to a wiki page instead). Only offer destinations whose connector is actually available.
   **Resolve the identifier yourself** — the self-DM id from the connector's current-user lookup, the
   address from the profile you already have, a named channel from a channel search on the name they
   said. Ask for a name if you need one ("which channel?"); never ask for an id. Verify it resolves
   before recording it, and if it does not, say the connector could not resolve it rather than handing
   the lookup back to them.
2. **When?** Default 07:30 on weekdays. It must run **after** the ingest with a real gap — 90 minutes is
   safe. If they pick a brief time within 90 minutes of the ingest, move the ingest earlier and tell them
   why: a brief that runs before its ingest reports yesterday's news as today's.
3. **Which days?** Default weekdays. Put this in the cron, not in the prompt.
4. **Skip days.** *"Should it skip days you're out of office?"* Default yes — and that is the only
   question here.

   **The rule is structural, and it is the same for everyone: an entry silences the brief only if it
   covers the whole working day.** All-day, or continuous start-to-finish coverage. Anything less — a
   block in the middle, a recurring evening or early-morning entry, a couple of hours — is a normal
   working day, no matter what it is called and no matter that it is flagged out-of-office.

   Lead with that rule, because it needs no knowledge of anyone's habits. Calendar naming is personal:
   people mark absence in ways that make sense only to them, and a rule that depends on recognizing names
   fails on the first user who does it differently.

   **Then read the calendar to see how *this* person actually works.** Sample the last couple of months
   and look at what recurs and how much of a day it covers. You are not trying to recognize names — you
   are measuring coverage, which is the thing the rule actually turns on.

   Expect to find recurring sub-day entries that are flagged out-of-office but are not absence. Some
   people block evenings or early mornings to stop colleagues booking outside their hours; some block
   lunch; some block focus time. **Do not assume any of these exist, and do not go looking for a
   particular one.** Whatever the person's calendar shows, the structural rule already handles it —
   these are simply the cases where a name-based reading would have gone wrong.

   **Write the derived pattern into the config in plain language, as an observation rather than a
   verdict**, e.g. *"recurring 18:00-07:00 entries marked out-of-office appear on most weekdays; they do
   not cover a working day, so they are not absence."* Two reasons: the user can see whether you read
   them correctly and correct it in one sentence, and the brief can say which rule it applied when it
   decides to stay silent. A brief that goes quiet without being able to say why is indistinguishable
   from a broken one.

   Their timezone you already resolved in Phase 1; working hours the brief infers from the calendar's own
   pattern at run time. Both are better read from real data than from an answer given cold on day one.
5. **Tone.** Default: assertive, short, readable. Offer "more detailed" if they want it.

## Phase 7 — The monthly lint

Default: the 1st of the month at 09:00, with auto-fix on for safe fixes, and `prune --months 6`.

Ask one thing: *"Should it tidy the wiki automatically, or just report what it finds?"* If they pick
report-only, record it — the task will run `lint` without `--fix` and list demote candidates without
demoting them. Either way, it **never deletes a page**; say that, because "prune" sounds like it does.

## Phase 8 — Confirm once

Show the whole plan in one compact summary: name, audience, language, layout, namespaces, every source
with its status and scope, where the jobs run, the three schedules, where the brief goes, the backfill
depth with its unit estimate. Then ask for a single yes.

This is the one place to be thorough. It is much cheaper to fix a wrong answer here than after three
weeks of ingest has been routed into the wrong namespace under the wrong privacy rule.

## Phase 9 — Write the files

All paths relative to the wiki folder.

1. `llm-wiki.yml` — from `templates/llm-wiki.yml`, every placeholder filled, including the
   `owner:` block from Phase 1. The jobs read the owner from here; never hardcode a name into a task.
2. `Wiki/Schema.md` — from `templates/Schema.md`. Fill `{{PRIVACY_RULES}}` with the user's actual rules
   from Phase 1, `{{FORMAT_RULES}}` and `{{LAYOUT_NOTE}}` per the chosen layout.
3. `Wiki/Dashboard.md` — from `templates/Dashboard.md`, including the jobs table.
4. A hub page per namespace — from `templates/Hub.md`. Obsidian: `Wiki/<NS>/_index.md`.
   Logseq: `pages/Wiki___<NS>.md`. Give each a one-line description of what belongs in it; a hub whose
   purpose is written down gets routed to correctly.
5. `Wiki/Reference/Access-Log.md` — from `templates/Access-Log.md`.
5b. For each Focus Area: its namespace hub (with the statement from Phase 2b as the hub description),
    `Log.md`, `Decisions.md`, `Goals.md` (carrying the metrics they named), and an empty `Reports/`
    folder. Skip entirely if there are none.
6. `Archives/` — create the folder (with a `.keep` file so it survives sync).
7. `wiki-ingest-state.json` — `{"lastSuccessfulRun": null, "commitments": [], "frequentContacts": {}, "channelActivity": {}}`.
8. `wiki-brief-state.json` — `{"lastBriefSentThroughDate": null}`, only if the brief is enabled.
9. `wiki-backfill-state.json` — the full unit plan, only if a backfill was chosen.
10. `CLAUDE.md` — from `templates/CLAUDE.md`. **This is the piece that makes the wiki automatic**: it is
    what routes every future question to `query` and every "save this" to `ingest` without anyone typing
    a command. Fill `{{PRIVACY_BLOCK}}` and `{{JOBS_BLOCK}}` with this project's real configuration.
    If a `CLAUDE.md` already exists, **append a clearly-marked LLM Wiki section — never overwrite it.**
11. `.claude/skills/wiki/SKILL.md` — **copy the `wiki` engine skill into the folder itself.** This is
    what makes the folder self-contained: anyone who syncs it and opens a session on it gets the engine
    and the `CLAUDE.md` together, with no plugin to install. Copy `wiki-setup` alongside it if the wiki
    is shared, so a teammate can reconfigure without chasing the plugin. If the folder is not shared,
    this copy is still worth making — it keeps the wiki working if the plugin is ever uninstalled.
12. `.claude/skills/.baseline/` — a **second, pristine copy** of every skill file just written. Never
    edited, never read at runtime. It is what lets a later update tell a local edit apart from an upstream
    change; without it the two are indistinguishable and no safe merge exists. Refresh it whenever the
    live copies are refreshed — the two must always describe the same version. See `references/updates.md`.
13. `.claude/skills/.llm-wiki-version` — a single line holding the plugin version these copies came
    from. Also write it to `wiki_version` and `skills_version` in `llm-wiki.yml`. **Re-copy the skills
    and re-stamp this on every reconfigure**, so a plugin update actually reaches the folder — on a
    shared wiki the folder is the distribution channel, and a copy nobody refreshes is a team quietly
    running an old version. If you cannot read the running plugin's version, write `unknown` rather
    than guessing; the lint reports that honestly instead of comparing against a fiction.

Never write a credential into any of these. Never create a git repository.

## Phase 10 — Create the three scheduled tasks

Use the scheduled-task tool. Fill the templates in `references/`: `task-ingest.md`, `task-brief.md`,
`task-lint.md`.

Each prompt must be **fully self-contained** — every run starts with no memory of this conversation.
Spell out the absolute folder path, connector names, channel ids, scope, **the verbatim customization
note for every source**, noise filters and destinations. Never write "as discussed" or "the sources we
chose" into a task prompt.

**Name them with the wiki's short name**, every time, with no exception:

| | id | title |
|---|---|---|
| Ingest | `<slug>-wiki-ingest` | `<Wiki name> · daily ingest` |
| Brief | `<slug>-wiki-brief` | `<Wiki name> · daily brief` |
| Lint | `<slug>-wiki-lint` | `<Wiki name> · monthly lint` |
| Focus report | `<slug>-focus-<area>` | `<Wiki name> · <Area> report` |

One report task **per Focus Area** that asked for one, from `references/task-focus-report.md`, scheduled
after the ingest. None, if there are no Focus Areas.

Unprefixed ids collide the moment this user sets up a second wiki, and a collision here is not a tidy
error — it is a second wiki silently overwriting the first one's job.

Defaults: ingest `0 6 * * *`, brief `30 7 * * 1-5`, lint `0 9 1 * *`. Cron is evaluated in local time.

After creating them, **verify all three appear in the task list** with the right prefix, and record their
real ids in `llm-wiki.yml`. Tell the user the tasks run while the Claude app is open, and that a task due
while it was closed runs on next launch.

## Phase 11 — First run

Offer, in this order:

1. **Run the ingest once now**, so they see something in the wiki within minutes rather than tomorrow
   morning. Strongly recommended — an empty wiki on day one is what makes people abandon this.
2. **Start the backfill**, if they chose one: run the first 2-3 units, then stop and show progress. Do
   not attempt the whole thing.
3. **Send a test brief**, so they can confirm it arrives where they expect and looks right.

## Phase 12 — Hand over

Tell them, in a few lines, in plain language:

- **They never need a slash command again.** Ask a question and it searches the wiki. Say "save this" or
  "remember this" or paste something in and it files it. That is the whole interface.
- What the three jobs will do and when, and that they run on this machine while the app is open.
- Where the wiki lives — the actual folder path — and that it is plain markdown they can open in any
  editor. If it is on a synced drive, that it reaches their other devices that way.
- That saying **"reconfigure the wiki"** re-opens this wizard — to add a source, change the brief, or
  move the schedule.
- If a backfill is running: how far along, and that it finishes on its own.

## Before you finish: the placeholder check

Every template in `templates/` and `references/` is written with `{{PLACEHOLDER}}` markers. A file
written out with one still in it is a silent, permanent bug — a task prompt containing `{{SKIP_LOGIC}}`
does not error, it just behaves strangely every night forever.

**After writing the files and creating the tasks, grep every written file and every task prompt for
`{{`. If anything matches, you missed a substitution — fix it before reporting success.**

The ones most often missed, because they need composing rather than copying:

| Placeholder | What it holds |
|---|---|
| `{{SOURCE_BLOCKS}} {{LOG_PAGE_MAP}}` | One block per enabled source: connector, scope, filters, destination page |
| `{{SKIP_LOGIC}} {{SKIP_PATTERN}}` | What this calendar actually looks like, as an observation. Never a naming rule — the whole-working-day coverage test is the rule, and it is already in the template. If nothing notable recurs, say that; do not invent a pattern to fill the space |
| `{{DELIVERY_BLOCK}} {{REPLY_FETCH}}` | The exact send tool, channel id, and how replies get read back |
| `{{BRIEF_SOURCE_PAGES}} {{WATCH_HUBS}}` | The specific pages the brief reads, by path |
| `{{PRIVACY_RULES}} {{PRIVACY_BLOCK}} {{PRIVACY_LINE}} {{PRIVACY_LINT}}` | The user's own exclusions, in their words. `personal` audience: say plainly that no cross-user filter applies |
| `{{ATTACHMENT_POLICY}}` | Whether to follow attachments during backfill (default off for deep backfills) |
| `{{PRUNE_CONFIRM}}` | Whether the monthly job demotes automatically or only lists candidates |
| `{{NOISE_FILTERS}}` | Their actual bot channels, digests and system senders |
| `{{TASK_TABLE}} {{JOBS_BLOCK}} {{SOURCE_SUMMARY}}` | Composed from the final configuration, after the tasks exist |
| `{{WIKI_SLUG}}` | The short name. Every task id and title carries it |
| `{{PLUGIN_VERSION}}` | The running plugin's version, from its `plugin.json`. `unknown` if it cannot be read — never a guess |
| `{{INGEST_OWNER}} {{SHARED_FOLDER}} {{SHARED_BLOCK}}` | Who owns the scheduled ingest, and the shared-folder rules in `CLAUDE.md`. On a solo wiki, `SHARED_BLOCK` says plainly that this wiki is not shared — do not leave it empty |
| `{{FOCUS_AREA}} {{FOCUS_STATEMENT}}` | Per Focus Area. The statement is the routing key — specific, not a label |
| source `notes` | The user's verbatim customization for each source, pasted into the task prompt as written — never paraphrased |

Where a placeholder has no applicable content — no noise filters, no skip rule — write the explicit
"none" sentence rather than deleting the section. A job that says *"no channels are filtered"* is
unambiguous; a job with a gap where the filter section should be invites a future run to invent one.

## Sharing a wiki with a team

The model is: **one person sets the wiki up in a folder on a synced drive; everyone else syncs that
folder and opens a session on it.** The `CLAUDE.md` and the copied skills travel with the folder, so a
teammate's session knows how to behave the moment it opens. Nothing else is installed.

Set this up correctly and it is genuinely that simple. Two things will break it if they are not decided
at setup, and both are invisible until they have already caused damage:

**1. Exactly one person runs the ingest.**

The scheduled jobs are per-machine. If three people sync the folder and all three have ingest jobs, three
runs write the same log pages at the same hour every morning — and because the pages are append-only,
nothing errors. It just quietly triples. Worse, each run pulls from *that person's* connectors, so a
shared wiki ends up holding a teammate's private inbox, filed under a heading that implies it is the
team's.

So: **the person who runs `/wiki-setup` is the ingest owner.** Record them as `ingest_owner` in
`llm-wiki.yml`. Everyone else syncs the folder and gets query, manual ingest, and the brief if they want
their own — but **not** the scheduled ingest. Write that into the shared `CLAUDE.md` explicitly, because
a teammate who runs `/wiki-setup` on a folder that already has a config is one "yes" away from creating a
duplicate job, and the wizard should tell them so instead of obliging.

When a teammate opens a session on an already-configured folder and asks to set it up, say what is
already running and who owns it, and offer only the safe options: their own brief, a one-off manual
ingest, or taking over as ingest owner deliberately — which means the current owner disables theirs first.

**2. Sync is not a merge.**

OneDrive, Dropbox and Drive resolve a simultaneous edit by keeping both and renaming one
(`Meetings-Log (Ana's conflicted copy).md`). Append-only writing makes this rare, not impossible. Two
habits keep it that way: one ingest owner (above), and letting sync settle before a big write rather than
editing a page that is mid-download. If conflicted copies do appear, **do not delete them** — surface
them, and offer to merge the divergent sections into the canonical page.

**What the team gets without any setup of their own:** ask a question, get an answer from the wiki with
sources; paste something in, have it filed. That is the whole interface, and it works from the folder
alone.

**What each teammate needs their own copy of:** the brief, if they want one. It is personal — it reads
*their* pending asks and *their* calendar and goes to *their* Slack. A shared brief addressed to one
person is noise for everyone else. Set theirs up with the same short name plus their own suffix
(`acme-wiki-brief-ana`) so the task list stays readable.

## Reconfigure mode

Read the existing `llm-wiki.yml`, show what is configured, and change only what they ask for. Common
requests and what each touches:

| Request | Update |
|---|---|
| Add or remove a source | `llm-wiki.yml` sources, the ingest task prompt, possibly the execution location |
| Connected a connector that was pending | Flip `no_connector` → `enabled` in config and task prompt |
| Change brief destination or time | `llm-wiki.yml` jobs.brief, the brief task prompt and cron |
| Change the schedules | The task crons, and the ingest/brief ordering gap |
| Add a namespace | `llm-wiki.yml`, a new hub page, the Schema's namespace list, the Dashboard |
| Change the privacy rules | The Schema's exclusions section and `CLAUDE.md`'s privacy block |
| Backfill further back | Extend `wiki-backfill-state.json` with new units and re-plan |
| Stop a job | Disable the task; keep the config so it can be turned back on |

Two rules that hold in every reconfigure:

- **Adding a local-folder source flips ingest to local execution.** Say so before doing it.
- **Never rewrite existing wiki content** to match a new convention. A schema change applies going
  forward; retrofitting it silently rewrites history that cannot be recovered. If they want existing
  pages migrated, do it as an explicit, confirmed, page-by-page pass.
---

## Credits

The wiki architecture this implements — the L1/L2 cache model, hub-index routing and LRU-demote, and the
schema, hub, dashboard and access-log page formats — comes from
**[llm-wiki](https://github.com/MehmetGoekce/llm-wiki)** by **Mehmet Gökçe**, MIT licensed. This package
is a derivative work: same architecture, rebuilt to configure itself conversationally in a Claude session
rather than through a shell script, with scheduled ingest/brief/lint jobs, resumable backfill and Focus
Areas added on top.

Not affiliated with or endorsed by the original author.
