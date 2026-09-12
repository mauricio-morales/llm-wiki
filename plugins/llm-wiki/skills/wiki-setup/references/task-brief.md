# Template: the daily brief task

Schedule it **after** the ingest job, with enough gap that ingest has finished (90 minutes is a safe
default). A brief that runs before its ingest reports yesterday's news as today's.

**Substitute the owner's real details from `llm-wiki.yml`'s `owner:` block when filling this template.**
The task prompt must name them explicitly — a scheduled run has no signed-in context to infer "me" from,
and an unqualified "me" in a task prompt resolves to nobody.

Fields in that block may be null by design. **A null is resolved at run time, never treated as a
failure**: a null `chat_user_id` is looked up with the chat connector's current-user call before sending;
null `working_hours` are inferred from the calendar's own pattern. Whatever a run resolves, it writes
back into `llm-wiki.yml` so the next run does not repeat the lookup. Never ask the user for one of these
at send time — a scheduled run has nobody to ask.

---

Send {{OWNER}} a brief of what happened since the last brief and what is coming up — both today, and
what lands in the next 7 days that they own or need to prepare for.

The wiki is at `{{WIKI_PATH}}`. Read `llm-wiki.yml` first. Make the brief **assertive, short and
readable** — this is a morning message, not a report.

## Step 0: Should this brief be sent at all?

Do this **first**, before any wiki read.

**The invariant, regardless of what the derived pattern below says:** an entry silences the brief only
if it covers the **whole working day** — all-day, or continuous start-to-finish coverage. A partial
block is a working day, whatever it is called and whether or not it is flagged out-of-office. Recurring
sub-day entries (evening or early-morning protection blocks, lunch, focus time) are **never** absence.
When coverage is ambiguous, send the brief. A brief that arrives on a quiet day costs nothing; one that
stays silent for a week because a lunch block was read as absence is the failure that gets this turned
off.

The pattern observed on this calendar at setup:

{{SKIP_LOGIC}}

That is an observation, not a rule — calendars change. If what you see today contradicts it, trust the
calendar, say so in the run report, and update this task's prompt. **When you do skip a day, say which
entry caused it** in the run report, so a silent morning is always explainable.

If today is a skip day: stop. Send nothing, and do **not** touch `wiki-brief-state.json`. The gap
accumulates on purpose — the next brief picks up from the unchanged `lastBriefSentThroughDate` and covers
the whole stretch.

## Step 0.5: Check for replies to the last brief

**Any reply left on a previous brief is a message to you** — a correction, a missing detail, a gap being
flagged — not an FYI aside. Treat it exactly as if it had been said in chat, and act on it **before**
compiling today's brief.

1. Read `lastBriefMessageId` from `wiki-brief-state.json`. If missing, skip this step today, but capture
   the id after today's send so tomorrow's run can check.
2. Fetch replies to that message ({{REPLY_FETCH}}).
3. For each reply, work out what it actually asks for, and **take the action it implies rather than just
   noting it**: a correction → fix it at the source, on the wiki page, not only in this task's state; a
   flagged ingest gap → run a targeted ingest for the missing period or source, then re-derive from the
   corrected wiki; a standing instruction about how the brief should work → update this task's prompt.
4. If a reply needs judgment rather than a mechanical fix, do your best and **say in today's brief what
   you did or could not resolve**, so it is visibly handled rather than silently dropped.
5. No replies → proceed silently. Don't announce "no replies".

## Step 1: Coverage window

The "what happened" section covers **from the day after `lastBriefSentThroughDate` through today**,
inclusive — not simply "yesterday". On a normal run that is one day. After a weekend or a stretch away it
is wider; synthesize it as one flowing recap rather than forcing a rigid per-day breakdown, but **don't
drop real items just because they are a few days old**.

## Step 2: What to read

Read the hub `### Index` of `Wiki/{{PRIMARY_NS}}` first, then in practice these pages:

{{BRIEF_SOURCE_PAGES}}

These log pages are append-only and grow long — **do not read them start to finish.** Run
`grep -n "^## 20" <file>` to find the date headers, then Read with an `offset` at the last few, enough to
cover the window. Ingest only backfills through the prior day, so a gap for "today" is expected; state it
as-is rather than treating it as a fault.

Also worth a cheap glance each run — read the hub `### Index`, open a child page only if something is
actively in flight: {{WATCH_HUBS}}

## Step 3: The waiting list — the section that has to be right

Pull the open asks from `wiki-ingest-state.json`'s `pendingOutboundRequests` and
`Wiki/{{PRIMARY_NS}}/Timeline.md`'s "Waiting on a reply".

**Every item renders four things, in this order:**

1. **The ask** — what was actually asked, specific enough to act on without opening the link.
2. **The stake** — what is blocked, at risk or undecided while it sits, with a date when there is one.
3. **Whose move it is** — say it explicitly. *"He owes you the estimate"* and *"you owe him an answer"*
   are opposite instructions and the brief must never blur them.
4. **The link** — a markdown link on the item, to the source message. Never a bare URL, and never a
   pointer to the wiki page instead of the message.

The age stays, but it is the least useful of the five. **Rank within a tier by stake, not by age** — an
11-day ask blocking a dated client call outranks a 21-day courtesy chase. Lead with `#waiting-overdue`.

The failure mode to avoid, concretely:

- ❌ `*Ana Ruiz* _(21d)_ — thread 1 · thread 2` — a name, a number and a URL. It says nothing about what
  was asked, who owes whom, or what breaks. Every link still has to be opened to triage.
- ✅ `*Ana Ruiz* _(12d)_ — you asked for a rollout timeline on the training programme. She owes you a
  date. It's now also blocking the Q4 proposal you promised Dana on Monday. — [Teams DM, Aug 27](<url>)`

All of this is already in the state file — `subject`, `stake`, `whoseMove`, `link`. **Read them and
render them. Do not re-derive them from the logs, and do not drop them for brevity** — this is the one
section where length buys action. If an older entry is missing `stake` or `link`, derive or resolve it
now, **write it back into the state file**, and render it. Capture once, not every morning.

**Open the linked message before quoting what it says.** Doing exactly this has caught real errors — a
log claiming an escalated ask "was never actually sent" when the linked message shows it was sent in full
and simply never answered. Trusting the log's summary would have had the owner re-send something they
had already sent.

Where an ask was partially addressed, say what is actually left rather than leaving it in the list as if
untouched.

If the list is empty, skip the section silently.

## Step 4: What's coming up

Today plus the next 7 calendar days, from `Timeline.md`: what they own, what needs preparation, what has
a hard date. Include commitments surfaced from conversations that aren't on the calendar — those are the
ones that get missed.

## Step 5: Deliver

{{DELIVERY_BLOCK}}

After a successful send, write to `wiki-brief-state.json`: `lastBriefSentThroughDate` (today, ISO) and
the sent message's id and channel, so tomorrow's Step 0.5 can pull replies on it.

**Transient tool failures are normal, not a misconfiguration.** Send tools can reject calls for several
minutes with capacity or classifier errors. Retry with backoff (20s, then 90s, then 180s) rather than
giving up after one failure. Do not burn retries in a tight loop with no wait between them. If it still
fails, report it and leave the state file untouched so tomorrow's brief covers both days.

## Filter the noise

Do not deep-read or report recurring automated traffic: system emails, ticket SLA digests, HR
notifications, meeting-recap bots, bot-only channels. {{NOISE_FILTERS}}
