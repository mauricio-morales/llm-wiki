# Async-interactive delivery — replies are instructions

Every artifact this wiki sends out — the daily brief, every Focus Area report, anything added later — is
**a conversation, not a broadcast.** Whatever the owner replies to it is addressed to you, and must be
read, understood and **acted on before the next one is sent.**

Setup embeds this protocol into each delivering task's prompt, filled in for that task's channel. It
lives here so there is one copy to correct.

## Item IDs — what makes a reply actionable

**Every item listed in any sent artifact carries a short ID in square brackets**, at the start of the
line: `[41] Ana Ruiz — the Q4 rollout timeline...`

- **One counter per wiki**, `nextItemId` in `wiki-ingest-state.json`, monotonically increasing. IDs are
  unique across everything the wiki ever lists — commitments, report items, flagged findings — so
  "regarding 41" is never ambiguous, even with a brief and a report in flight the same morning.
- **Assigned at ingest, when the item is first written**, stored on the item in the wiki page or state
  file, and **never changed.** An ID that means one thing today and another tomorrow is worse than none:
  the owner will reply about yesterday's number.
- **Never minted at send time.** A brief or report *reads* ids; it never invents them. An id generated
  while rendering is a position in that message, not an identity — it shifts as items are added, closed
  or reordered, so a reply naming it silently resolves to the wrong item. If an item reaches a report
  without an id, that is an ingest bug: assign one, **write it back to the source**, and say so.
- **Never reused**, not even after an item closes. A recycled ID silently reassigns an old reply to a new
  item.
- Keep them short. `[41]` is typed one-handed on a phone; `[CMT-2026-0041]` is not, and the whole point
  is that replying costs nothing.

## Reading replies — before composing anything

1. Read the stored id of the artifact you last sent (`lastSentMessageId`, per artifact, in that task's
   state file), and fetch replies to it. Slack: the thread on that message. Teams: the chat thread.
   Email: replies to that message.
2. If there is no stored id — first run, or a state file predating this — skip the step **today only**,
   then store the new message's id after sending so the next run can check.
3. **Act on every reply before composing the new artifact**, so the new one already reflects it. Acting
   afterwards means the owner reads a report that contradicts what they just told you.

## What a reply can be, and what to do with it

**A state change** — *"close 41"*, *"[41] is done"*, *"drop 17, they went another way"*. Apply it to the
item: `fulfilled`, `withdrawn`, `superseded`. This is the most common reply and the one that must work
reliably, because it is how the owner keeps the list honest.

**A correction** — *"regarding 41, that's not true"*, *"he never agreed to that"*. **Fix it at the source** —
the wiki page or the state entry — not just in the next message. A correction applied only to the next
artifact reappears wrong the following day.

**A presentation or format preference** — *"stop showing the age"*, *"shorter"*, *"put what I owe last"*,
*"group these by client"*. **Update the task's own prompt** so it persists. A preference honored once and
forgotten is worse than ignoring it, because the owner stops bothering to ask.

**A request for information** — *"what happened with the Acme renewal?"*. Answer it in the next artifact,
or immediately if the channel supports a direct reply and it is time-sensitive.

**A scope change** — *"also track my Jira comments"*, *"stop reading that channel"*. That is a
reconfiguration: apply it to `llm-wiki.yml` and the ingest task, not just to this one.

**Something ambiguous.** Do not guess — especially not at a state change. **Closing the wrong item on a
misread is the one unrecoverable mistake here**, because the owner stops seeing it and assumes it was
handled. Say plainly in the next artifact what you could not interpret and ask.

## Confirm what you did

The next artifact opens with a short line confirming actions taken: *"Closed [41] and [17] per your
notes. Moved 'what you owe' to the top."* Two sentences at most.

This is not politeness. It is the only way the owner learns the channel works — and a reply they cannot
see landing is a reply they will stop sending.

## Rules

- **Never ignore a reply.** If it cannot be acted on, say why.
- **Never treat a reply as an aside.** "FYI Ana is out this week" is context that changes what to chase.
- **Act at the source, not in the presentation.** Corrections go to the wiki, state changes to the state
  file, preferences to the task prompt. Only answers go in the next message.
- **Do not re-read replies already acted on.** Record the last reply timestamp handled, per artifact.
- A reply arriving after a skipped send (an out-of-office day, say) still counts — process the backlog on
  the next run rather than only the most recent.
