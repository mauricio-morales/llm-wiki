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

<!-- llm-wiki task: {{TASK_KIND}} | template version: {{PLUGIN_VERSION}} | generated: {{DATE}} -->

## Step 0 — Adopt any pending update to this prompt

{{TASK_SELF_UPDATE}}

<!-- Setup fills this from references/task-self-update.md. Embed it in full — a scheduled run cannot
     read the reference file. -->

Send {{OWNER}} a brief of what happened since the last brief and what is coming up — both today, and
what lands in the next 7 days that they own or need to prepare for.

The wiki is at `{{WIKI_PATH}}`. Read `llm-wiki.yml` first. Make the brief **assertive, short and
readable** — this is a morning message, not a report.

## Step 0.1: Should this brief be sent at all?

Do this **first**, before any wiki read.

**The invariant, regardless of what the derived pattern below says.**

An entry silences the brief when it is **all-day**, or when it **overlaps the daytime by 9 hours or
more**. Take daytime as roughly 07:00–19:00 local; it does not need to be exact, and it should not be
tuned to this person's precise hours — the test is how much of the day is consumed, not which clock
boundaries are hit.

**Measure the overlap with daytime, not the raw duration.** These are different numbers and the
difference is the whole rule:

| Entry | Duration | Daytime overlap | Verdict |
|---|---|---|---|
| All-day | 24h | full | **OOO** |
| 07:00–19:00 | 12h | 12h | **OOO** |
| 09:00–18:00 | 9h | 9h | **OOO** |
| 18:00–07:00 (evening protection block) | 13h | ~0h | working day |
| 12:00–13:00 (lunch) | 1h | 1h | working day |
| 09:00–12:00 (half morning) | 3h | 3h | working day |

A raw-duration test would call that fourth row an absence and go silent every single day — many calendars
carry a standing evening or overnight block precisely to stop out-of-hours bookings, and it is long.
Overlap handles it without special-casing anything: an overnight block consumes no daytime.

Where several entries cover the day between them, **add up their daytime overlap** — two four-hour
blocks with a gap are not absence, but 08:00–13:00 plus 13:00–18:00 is.

Anything below the threshold is a working day, whatever it is called and whether or not it is flagged
out-of-office. **When coverage is ambiguous, send the brief.** One that arrives on a quiet day costs
nothing; one that stays silent for a week because a lunch block read as absence is the failure that gets
this switched off.

The pattern observed on this calendar at setup:

{{SKIP_LOGIC}}

That is an observation, not a rule — calendars change. If what you see today contradicts it, trust the
calendar, say so in the run report, and update this task's prompt. **When you do skip a day, say which
entry caused it** in the run report, so a silent morning is always explainable.

If today is a skip day: stop. Send nothing, and do **not** touch `wiki-brief-state.json`. The gap
accumulates on purpose — the next brief picks up from the unchanged `lastBriefSentThroughDate` and covers
the whole stretch.

## Step 0.5: Read and act on replies to the last brief

{{ASYNC_REPLY_PROTOCOL}}

<!-- Setup fills this from references/async-replies.md, with this task's channel, the state keys
     (`lastSentMessageId`, `lastReplyHandledAt` in `wiki-brief-state.json`) and its fetch method
     filled in. Embed it in full — a scheduled run cannot go and read the reference. -->

**Do this before composing today's brief**, not after. A brief that contradicts what the owner told you
last night is worse than no brief: it proves the channel does not work, and they stop replying.

## The budget, and how to choose what fits

**The brief must be readable in five minutes. Ten is the failure point, not the target.**

Hard limits:

| | |
|---|---|
| Whole brief | **~450 words**, 700 absolute ceiling |
| Items in any one section | **5** |
| Extension beyond 5 | only for items that are **both high-impact and overdue-or-due-today**, hard ceiling **8** |
| Messages | **one** |

**Never split into parts, and never continue in a thread.** If it does not fit, that is not a formatting
problem to route around — it means too many items were selected, and the answer is to cut lower-ranked
ones. A brief delivered in two parts with a thread hanging off it has already failed: nobody reads to the
end of it, which means the top-ranked items get read and the rest may as well not have been sent.

### Triage: impact first, then urgency

Score every candidate item on both axes before selecting anything.

**Impact** — what it costs if it slips:

- **High** — a client or external commitment; revenue; anything about a person's pay, role or standing;
  a dated external deliverable; an objective at risk
- **Medium** — an internal deliverable with a date; a decision that is blocking someone else's work
- **Low** — a courtesy chase, an FYI, something nobody is waiting on

**Urgency** — the clock: *overdue* · *due today or tomorrow* · *due this week* · *no date or far off*.

**Rank by impact first, urgency second.** A high-impact item due Thursday outranks a low-impact one that
has been overdue for a month. Age alone is the weakest signal there is — it measures how long something
has been ignorable, and things that stay ignorable usually deserve to be.

**Only high-impact *and* overdue-or-due-today items justify going past five.** Everything else waits for
tomorrow, when it will rank higher or turn out not to have mattered.

### What "cut" means

Cutting is **dropping whole low-ranked items, never thinning the ones shown.** A shown item keeps its
full detail — the ask, the stake, whose move, the link — because that detail is what makes it actionable
without opening anything. Five complete items beat fifteen truncated ones; the truncated fifteen force
the owner to go and look, which is the work the brief exists to remove.

Say what was cut, in one line at the end of the section: *"+9 more open, all lower-impact — in the wiki."*
A number is enough. The owner can ask, and can reply *"show me the rest"* — which the async-reply protocol
will honor as a standing preference.

## Step 1: Coverage window

The "what happened" section covers **from the day after `lastBriefSentThroughDate` through today**,
inclusive — not simply "yesterday". On a normal run that is one day. After a weekend or a stretch away it
is wider; synthesize it as one flowing recap rather than forcing a rigid per-day breakdown, but **don't
drop real items just because they are a few days old**.

**This section is a synthesis, not a log** — at most a short paragraph plus three or four bullets for
anything genuinely notable. The wiki holds the full account. If little happened, one honest sentence beats
a padded recap.

## Step 2: What to read

Read the hub `### Index` of `Wiki/{{PRIMARY_NS}}` first, then in practice these pages:

{{BRIEF_SOURCE_PAGES}}

These log pages are append-only and grow long — **do not read them start to finish.** Run
`grep -n "^## 20" <file>` to find the date headers, then Read with an `offset` at the last few, enough to
cover the window. Ingest only backfills through the prior day, so a gap for "today" is expected; state it
as-is rather than treating it as a fault.

Also worth a cheap glance each run — read the hub `### Index`, open a child page only if something is
actively in flight: {{WATCH_HUBS}}

## Step 3: Commitments — the section that has to be right

Read `commitments` from `wiki-ingest-state.json` and `Wiki/{{PRIMARY_NS}}/Timeline.md`'s "Waiting on
others" and "I owe" sections. **This is why the brief exists: nothing the owner is owed, and nothing the
owner owes, should ever be forgotten.**

### What surfaces today

An `open` commitment appears when **`due` is today or earlier**, and then **every day after that until it
is closed.** Not once — every day. An overdue item that stops being mentioned is an item that got dropped.

**Nothing surfaces before its due date. Nothing.**

This is the rule that keeps the section worth reading, and the temptation is always to break it "just for
this one". Do not:

- An ask sent yesterday with no stated deadline is **not** brief material. People need time to answer, and
  reminding the owner about it makes the section noise. The grace period (`commitment_grace_days`,
  default 14) exists precisely so silence has had time to become information.
- A commitment with a deadline next Thursday is not brief material until Thursday. The owner set that
  date, or accepted it; second-guessing it daily is not help.
- The same holds for things the owner owes. Being chased about your own untimed work three days in is how
  a list stops getting read.

Below `due`, commitments stay silently tracked. They are not gone; they are simply not today's problem.

### Two sections, never merged

**Five per heading**, ranked by impact then urgency, extending to eight only for items that are both
high-impact and overdue-or-due-today. Anything beyond that is a count and a pointer.

**"You're waiting on"** (`theirs`) and **"You owe"** (`mine`) are separate headings. They are opposite
instructions — one means chase someone, the other means do work — and a merged list makes the reader
sort them by hand every morning. Lead with **"You owe"**: it is the one where the owner's own day has to
change.

### How each line renders

Four things, in this order:

0. **The item's ID in square brackets**, first on the line: `[41]`. This is what lets the owner reply
   *"close 41"* or *"regarding 41, that's not true"* without quoting anything back. IDs are assigned at
   capture, never change, and are never reused — see the async-reply protocol above.
1. **The ask** — what was asked or agreed, specific enough to act on without opening the link.
2. **The stake** — what is blocked, at risk or undecided, with a date when there is one.
3. **Whose move and when** — name the other party, and say whether the date was their words or a default:
   *"due today (they said Friday)"* versus *"7 days since you asked, no date was given"*. **Do not present
   a defaulted nudge date as though it were a promised deadline** — the owner will quote it back to
   someone, and being wrong about that costs credibility.
4. **The link** — a markdown link to the source message. Never a bare URL, never a pointer to the wiki
   page instead of the message.

Rank by **stake, then by how overdue.** A commitment two days late that blocks a client call outranks one
three weeks late that nobody is chasing.

Worked examples:

- ❌ `*Ana Ruiz* _(21d)_ — thread 1 · thread 2` — a name, a number and a URL. Says nothing about what was
  asked, who owes whom, or what breaks. Every link still has to be opened to triage, and there is nothing
  to reply about.
- ✅ **You owe:** `**[41]** *Ana Ruiz* — the Q4 rollout timeline you agreed to on Aug 27. **Due today**,
  her words. She's presenting it Thursday, so slipping costs her the slot. — [Teams DM](<url>)`
- ✅ **You're waiting on:** `**[38]** *Dana Okafor* — the revised cost model you asked for. No date was
  given, so this is the 7-day nudge. It blocks the proposal you promised Karim by the 20th. — [email](<url>)`

**All of this is already in the state file** — `subject`, `stake`, `withWhom`, `due`, `dueIsExplicit`,
`link`. Read them and render them rather than re-deriving them from the logs.

**Never thin a shown item to save space** — an item without its stake and its link is one the owner has to
go and investigate, which is the work this is supposed to remove. Save space by **showing fewer items**,
per the budget above: full detail on the five that matter, a count for the rest. If an older entry is missing a field,
resolve it now, **write it back into the state file**, and render it. Capture once, not every morning.

**Open the linked message before quoting what it says.** Doing exactly this has caught real errors — a
log claiming an escalated ask "was never sent" when the linked message shows it was sent in full and
simply never answered. Trusting the summary would have had the owner re-send something they already sent.

Where a commitment was partially met, say what is actually left rather than listing it as untouched.

If both sections are empty, skip them silently.

## Step 3.5: Objectives — lightly

If `Wiki/{{PRIMARY_NS}}/Objectives.md` exists, read it. **The brief is not an OKR dashboard** — a daily
progress bar on a quarterly goal is noise and will be skimmed past within a week. Three things only:

- **Something in today's material moved an objective** — say which and in which direction. That is an
  event, not a routine metric.
- **A commitment the owner owes blocks an objective** — say so on that item. It changes the priority, and
  it is exactly the connection that otherwise gets missed.
- **An objective is behind pace and the period is more than half gone** — one line, only for the ones
  actually at risk. Not every objective, not every day.

If none of those apply, skip the section silently.

## Step 4: What's coming up

Today plus the next 7 calendar days, from `Timeline.md`: what they own, what needs preparation, what has
a hard date. Include commitments surfaced from conversations that aren't on the calendar — those are the
ones that get missed.

**Five items, ranked by impact then date.** A routine recurring meeting is not news and does not earn a
line; something needing preparation does. If the week is genuinely full, say so in a sentence rather than
listing it — the calendar already exists and the owner can open it.

## Step 5: Deliver

{{DELIVERY_BLOCK}}

**One message. Check it against the budget before sending** — if it is over, cut the lowest-ranked items
until it fits, rather than splitting it or moving detail into a thread.

After a successful send, write to `wiki-brief-state.json`: `lastBriefSentThroughDate` (today, ISO) and
the sent message's id and channel, so tomorrow's Step 0.5 can pull replies on it.

**Transient tool failures are normal, not a misconfiguration.** Send tools can reject calls for several
minutes with capacity or classifier errors. Retry with backoff (20s, then 90s, then 180s) rather than
giving up after one failure. Do not burn retries in a tight loop with no wait between them. If it still
fails, report it and leave the state file untouched so tomorrow's brief covers both days.

## Step 6: Is this wiki behind?

{{UPDATE_NUDGE}}

<!-- Setup fills this from references/update-nudge.md, with this task's state key for
     `lastUpdateNudge`. Embed it in full — a scheduled run cannot read the reference file. -->

One line, at the **bottom** of the brief, at most once a week. It is housekeeping, not news, and a line
that shows up every morning stops being read in three days — taking the rest of the brief's credibility
with it.

## Filter the noise

Do not deep-read or report recurring automated traffic: system emails, ticket SLA digests, HR
notifications, meeting-recap bots, bot-only channels. {{NOISE_FILTERS}}
