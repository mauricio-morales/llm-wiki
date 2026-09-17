# Source catalog

The sources the ingest job can check. Setup walks these **one at a time** and records an answer for each.

## How to ask

Before asking anything, **detect what is actually connected** — list the available tools and connectors
in the session. Then ask an informed question instead of a generic one:

- Connector detected → *"I can see a Slack connector. Ingest Slack? (yes / not this one / no)"*
- Not detected → *"Slack — no connector is connected here. Do you want it? I'll record it as pending and
  you can connect it later, or we skip it entirely."*

Three answers per source, always:

| Answer | Recorded as | Effect |
|---|---|---|
| Yes, and it's connected | `enabled` | In the ingest job now |
| Yes, but not connected yet | `no_connector` | Written into the job, skipped at runtime with a note until the connector appears |
| No | `declined` | Left out entirely |

`no_connector` matters: the source is in the job prompt from day one, so the day they authorize the
connector it starts working with no edit to anything. The job reports it as pending-not-broken each run.

**Ask about multiples.** Two Slack workspaces, a work and a personal mailbox, three Jira projects, two
SharePoint sites — these are common and each needs its own entry. After a `yes`, always ask *"just the
one, or more than one?"* and record each instance separately with its own identifier.

For each enabled source also capture **scope** — which channels, which folders, which projects, which
mailbox — and **noise filters**: the bot channels, automated digests and notification senders that
should be skipped. Getting the filters at setup saves the first weeks of runs from drowning in
notification traffic. Ask: *"anything that's pure noise — bot channels, automated digests, system
notifications?"*

## Cloud sources (connector-based — can run in the cloud)

**1. Meeting transcripts — video platform** (Zoom, Google Meet, Webex)
Meetings hosted or attended in the window; fetch the transcript, plus the summary and next-steps if
cheap. A meeting can legitimately have no transcript (recording off, still processing) — that is not an
error on its own; only flag it if no other source covers it either. → `Meetings-Log`

**2. Meeting transcripts — Teams / calendar**
Every calendar event in the window, as attendee or organizer. Check each for a transcript URL. WEBVTT
transcripts routinely exceed a single response — read them in chunks or delegate to a subagent, never
truncate. → `Meetings-Log`

**3. Chat — Teams**
Persistent chat threads and DMs, not just meeting chats. A message whose preview is
`<attachment id="...">` is **not empty** — it is a link to follow. → `Chats-Log`

**4. Chat — Slack**
DMs, group DMs and channels. **Prioritize conversation over announcement**: track per-channel
post/reaction counts in the state file over time and let that distinguish a channel where the team talks
from one a bot posts into. Ask which workspaces, and which channels matter. → `Slack-Log`

**5. Email**
Filtered, never dumped. Prioritize two-way threads, decisions, deadlines and anything from a frequent
contact; skip bulk mail, newsletters and system notifications. Maintain rolling `frequentContacts`
interaction scores in the state file so prioritization improves with use. Ask which mailboxes. Also scan
**Sent** — that is where outbound asks are found (see Outbound request tracking). → `Email-Log`

**6. Tickets — Jira / Linear / Asana**
A named project or board. Capture status changes, comments and decisions, not the full ticket body.
Digests are links, not summaries: a digest naming "48 work items" should be opened far enough to say what
kind of items they are, not just the count. Ask which projects. → `Tickets-Log`

**7. Calendar — forward-looking**
Not history — the next 30 days, rebuilt each run into `Timeline.md`. Recurring sub-day entries are
scheduling furniture, not events: collapse them out rather than listing them. Some calendars carry a
standing evening or early-morning block to stop out-of-hours bookings — that is not time off and must
never be read as absence. Judge by coverage, never by the entry's name. → `Timeline`

**8. Documents — SharePoint / Google Drive / Box / Dropbox**
A named site, drive or folder tree. New and modified documents in the window: what it is, who touched it,
what it says. Not a full-text index. Ask which sites/drives and which folders. → `Documents-Log`

**9. Wiki / docs — Confluence, Notion**
Pages created or edited in the window in a named space. → `Documents-Log`

**10. CRM — HubSpot, Salesforce**
Deals, companies and logged activity in the window. Useful for a team wiki with a commercial audience;
noise for a purely technical one. → routed by namespace, typically `Business` or `Clients`

**11. Code / PRs — GitHub, GitLab**
Merged PRs, releases and architecture-relevant discussion in named repos. Decisions and rationale, not
diffs. → `Tech`

**12. Anything else with a connector**
The catalog is not a closed list. If a connector is present that isn't listed here, offer it — same three
answers, same scope-and-noise questions, and route it to a namespace the user names.

## Local sources (force local execution)

**13. A folder on this machine**
A synced drive folder, a notes directory, a Downloads folder, an exports directory — anything on disk.

**14. A local application's database or export directory**
Local transcription apps (MacWhisper and similar), local note apps, anything that writes files locally.
Prefer reading the app's own database over its export files when it has one: exports are usually a subset
and are easy to forget to produce. Dedup on the app's own stable record ID mapped to a
last-modified timestamp — so a record that was edited after ingest (re-tagged speakers, a corrected
transcript) is **re-ingested and its existing wiki entry updated in place**, not skipped as already-seen.

**Both of these require local execution and a granted directory.** See below.

## Local sources (13 and 14)

**A local path is not automatically readable.** A Cowork session is sandboxed: it has the wiki folder, and
not the rest of the machine. Being on the same computer is not access — a perfectly reasonable-looking
path will simply fail to read, every night, and look exactly like a quiet week.

Reaching one means exposing it through an **MCP server** configured in the desktop app. **Do not walk the
user through that during setup** — it is a detour most people do not need. Record the source as pending
with the reason, finish the setup, and hand them `references/local-sources.md` afterwards.

**Never record a local source you have not actually read from** within the session that will run it.
Listing the directory or the tables, and pulling one real record, is the bar — not "it should work".

## Customization notes — ask for these on every enabled source

After the picks, offer a free-text note per source. This is the step that decides whether the job does
what the user meant or merely what the category implies.

*"Anything I should know about how you want each of these read? For example — 'only the sales
distribution list, not my own inbox', 'just #incidents and #releases', 'skip the recruiting bot', 'only
the Platform board', 'ignore internal-only documents'."*

Record it **verbatim** in the source's `notes` field and paste it **verbatim** into the task prompt.

Do not paraphrase it into a category. *"Only monitor the group distribution list, not my inbox"* and
*"ingest Outlook"* are different jobs, and the paraphrase in between ("monitor a mailbox") reverts to the
wrong one the first time a run reads it loosely. If a note contradicts something else the user said,
surface the conflict rather than picking a reading.

A note that narrows scope is also a **privacy boundary**, not just a filter — "not my inbox" on a shared
team wiki is the difference between a working system and one that quietly published someone's mail.
Treat it with that weight.

## Where the jobs run

**On this machine.** The wiki is a local folder and only a local run can write to it. Tasks execute while
the Claude app is open; one due while it was closed runs on next launch. Say that once at setup so a
quiet morning is never mistaken for a broken job.

Reading the wiki from elsewhere works through the folder, not through the jobs: if it sits on a synced
drive, the files reach every device that drive syncs to, and a session with that drive's connector can
read them there. That is real read access from a phone. It is not the ingest running in the cloud. State
it that precisely.
