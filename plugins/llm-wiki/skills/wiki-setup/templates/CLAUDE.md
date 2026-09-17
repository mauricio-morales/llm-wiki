# {{WIKI_NAME}}

{{PURPOSE}}

This project is an **LLM Wiki**. Its knowledge lives in `Wiki/` in this project's storage, and it is fed
automatically by scheduled jobs. The rules below are not optional and do not need to be invoked — they
are how this project works by default.

## Always use the wiki. Never wait to be asked.

The `wiki` skill is the default behavior of this project, not a command the user has to remember. The
user will never type `/wiki`. Route on intent:

**Any question → run the wiki `query` workflow first.**
Before answering anything from general knowledge, route through the wiki: read the namespace hub
`### Index` routing lines, pick the 3 most relevant pages, read only those, then answer with sources.
This includes questions that don't look like wiki questions — "what did we decide about X", "who owns
Y", "when is Z", "what's the status of...", "remind me...", "who is...", "why did we...". If the wiki
genuinely has nothing, say so plainly and then answer from general knowledge, labelled as such.

**Any of these verbs → run the wiki `ingest` workflow.**
`ingest` · `add` · `store` · `save` · `load` · `learn` · `capture` · `download` · `file` · `log` ·
`record` · `remember` · `note` · `keep` · `track this` · "put this in the wiki" — and the same
intent expressed without those words ("here's the transcript from the client call", a pasted document,
a dropped URL, "this is important for later").

**Maintenance verbs → the matching workflow.** "what's in the wiki / how big / how healthy" → `status`.
"check the wiki / clean up / fix links" → `lint` (use `--fix` only when they ask for fixes). "the wiki
is getting noisy / too much old stuff" → `prune`. "bring in my old notes" → `import`.

**Don't narrate the routing.** Don't say "running a wiki query" or "invoking the skill" — just answer,
and cite the pages you used. The user wants the knowledge base, not a play-by-play of the machinery.

## Focus Areas — first-class topics

{{FOCUS_BLOCK}}

Where this wiki has Focus Areas, they outrank normal routing. Anything that relates to one — however
loosely — is captured **in full** and written to **both** its normal home and the Focus Area's own pages.
An item that lives only in a chronological log has not been captured for the Focus Area.

Every Focus Area item is typed: `decision` (naming who decided and on what authority), `idea` (who raised
it), `follow-up` (owner, and date if stated), `question`, `signal`. A decision recorded without its
authority is worse than one recorded as provisional.

Match against the Focus Area's **statement** on its hub, not just its name — the statement is deliberately
broader, and it is the routing key.

## If you had to look it up, write it down

**When answering a question required going outside the wiki, file what you found.** Do not ask first.

The failure this prevents: a question arrives, the wiki doesn't have it, you go find it in a document,
you answer well — and the answer is lost. The next person asks the same thing and repeats the same hunt.

**File it silently when** the fact came from a source you actually opened (a document, contract, ticket,
email, page), it is a fact rather than a reading of one, and it fits an existing namespace. **Record
where it came from** — name the document and link it; "per the MSA at <link>, retrieved <date>" is worth
far more than the bare fact, because the next reader can check it. Say what you filed in one line. Don't
present it as a decision you're making.

**Ask once, after the answer, only when** the fact is inferred or uncertain (if you'd hedge writing it,
ask), it's sensitive (pay, performance, a flagged person, anything the privacy rules exclude), it
contradicts a page, it needs structural change (a new top-level namespace), or it's opinion rather than
fact — "the client is unhappy" is an interpretation, "the client raised three defects on the 09-08 call"
is a fact.

The costs are asymmetric: filing something redundant costs a few lines the next lint tidies. Not filing
it costs the same hunt, repeated by everyone who asks, forever.

Filing means filing **properly** — right page, routing line in the nearest enclosing hub, cross-links,
`updated` set, source recorded. A fact dumped somewhere unroutable hasn't been captured, it's been hidden.

## Where things are

- `llm-wiki.yml` — configuration. **Read it first, every session.** Never assume the paths or the schema.
- `Wiki/Schema.md` — page types, required properties, routing-line format, privacy rules. Read before
  writing anything.
- `Wiki/<Namespace>/_index.md` — the hub pages. Their `### Index` is the routing table.
- `Wiki/Reference/Access-Log.md` — append-only log of which pages were read and why.
- `Archives/` — text-only snapshots of ingested URLs.
- `wiki-ingest-state.json`, `wiki-brief-state.json` — job cursors at the folder root, outside `Wiki/` so
  they are never mistaken for wiki content. They hold cursors and tracking data, never credentials.
- `.claude/skills/` — a copy of the wiki skills, so this folder works on its own for anyone who syncs it.
  **Do not personalize these files.** They are replaced by updates. Wiki-specific behavior belongs in this
  file; conventions belong in `Wiki/Schema.md`. Both survive every update untouched and take effect
  immediately, which a rule buried in a skill file does not.
- `.claude/skills/.baseline/` — a pristine copy of the skills as installed, so an update can tell a local
  edit from an upstream change. Never edit it, and never read it at runtime.

## Hard rules

1. **Append, never overwrite.** This wiki has no version control and no history — an overwrite is
   unrecoverable. Add new blocks; never rewrite existing ones. The one exception is `Timeline.md`,
   which is rebuilt by design.
2. **Never delete a page** unless the user explicitly asks for that page to be deleted. `prune` demotes
   pages out of routing; it never deletes them.
3. **Never run git.** This project is not a repository. There is nothing to commit.
4. **Never write credentials, passwords, API keys or tokens into a wiki page.** This storage is shared
   with everyone on the project and read by automated jobs. Credentials belong in Claude Memory (L1).
5. **Every page needs a routing line** in its namespace hub's `### Index`, or it is invisible to `query`.
6. **Every page needs at least one outgoing `[[link]]`.**
7. **Write pages in {{LANGUAGE}}**, regardless of the language of the source or of the conversation.
   Reply to the user in whatever language they used; write files in {{LANGUAGE}}.
8. **Never silently skip or truncate.** A source that was unavailable, a file too large to read in one
   pass, a link that couldn't be opened — say so. Silence reads as "there was nothing there", which is
   the one thing it must never mean.
9. **Drain paged sources to the last page.** Anything returning a list — mail, chat, tickets, files —
   pages its results. Follow the cursor (`nextLink`, `next_cursor`, `has_more`) until there are no more.
   **A result count at exactly the page size (100, 50, 25) is a cap, not an answer** — a real count is a
   ragged number. If it can't be drained, narrow the window and re-query rather than accepting a partial
   result, and if it still can't be, say which window is incomplete. A capped sweep and an empty one look
   identical once written down, and only one of them is true.

{{PRIVACY_BLOCK}}

## Figures from transcripts are low-confidence

Anything that came through speech-to-text is unreliable, and the "-teen"/"-ty" pairs are routinely
misheard: 15↔50, 16↔60, 13↔30, 14↔40, 17↔70, 18↔80, 19↔90. When a transcribed number is an order of
magnitude off from the other figures in the same conversation, **the transcriber got it wrong — that is
not the speaker misspeaking.**

- Reconcile against context before writing it down, and record the reconciled figure.
- Note the artifact: `$15M (transcript renders "$50 million"; read as $15M, -teen/-ty ASR confusion)`.
  Don't silently swap it, don't silently keep the wrong one.
- **Never put a transcription error in someone's mouth** ("he said 50") unless the audio was re-checked.
- Same caution for names, rates, percentages and dates. If context doesn't disambiguate, write that the
  figure is ambiguous rather than picking one.

## Follow shared links once

If a message shares a link or carries an attachment, open it once and record what it was about — one hop
only, no chasing links inside the linked document. The goal isn't to index everything; it's that weeks
later "that thing Ana sent" has an answer. *"Ana posted an attachment"* fails that. *"Ana posted the
recruitment request form; it asks for X, Y, Z"* passes.

Peek depth, not full ingest: what it is, who sent it, roughly what's in it, and any figure, date, name or
commitment on its face. A short paragraph. Escalate to a full ingest only if it independently clears the
bar (a contract, a client proposal, a live deliverable with a near-term date).

Record the pointer even when the content turns out to be thin — *"opened, it's the bare template with
nothing filled in"* is a useful finding; it stops someone later assuming that file held the decisions.
Do **not** follow credential-gated third-party links, unsubscribe/tracking URLs, or anything shaped like
a phishing probe — note that the link exists and was deliberately not opened, and why.

## The scheduled jobs

{{JOBS_BLOCK}}

{{SHARED_BLOCK}}

Their prompts are self-contained and live with the tasks, not here. To change what gets ingested, who
the brief goes to, or when they run, ask to **reconfigure the wiki** — that re-runs the setup wizard
against the existing config.
