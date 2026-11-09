# Running in ChatGPT

These skills were written for Claude and translated for the **ChatGPT desktop app**. The build already
replaced file names (`CLAUDE.md` → `AGENTS.md`, `.claude/` → `.agents/`) and app names. What it could not
replace mechanically is below. **Where this page and the skill disagree, this page wins.**

If something here turns out to be wrong for the version of ChatGPT in front of you, do what achieves the
skill's intent, tell the owner plainly what you did differently, and never pretend a step happened.

## Where you are

A ChatGPT desktop session opened **on the wiki folder**, using Work mode (or Codex mode), with permission to
**write files in that folder**. That is what the skills mean by a "ChatGPT desktop session" (Claude:
"Cowork session"). A plain chat with no folder, or ChatGPT on the web, cannot keep a wiki. If you have no
folder, say so and stop before writing anything.

## Asking the owner a question

The skills say **`AskUserQuestion`**. ChatGPT has no multiple-choice tool, so ask in the chat:

- One message per batch the skill describes. Number the questions; give each 2-4 lettered options, the
  recommended one first and marked *(recommended)*, each with its one-line consequence.
- Say how to answer: *"Reply with the letters, like 1A 2C, or say it in your own words."*
- Then **stop and wait for the reply.** Never assume the recommended answer.

## Scheduled jobs

The skills name a scheduler tool: `create_scheduled_task`, `update_scheduled_task`,
`delete_scheduled_task`, `list_scheduled_tasks`, with a `cronExpression` (recurring) or a `fireAt` (one
time). In ChatGPT these are **scheduled tasks**, shown under **Scheduled** in the desktop app's sidebar.

- **Create them on the desktop, as local tasks on this folder**, running **in the project directory**,
  never in an isolated worktree. A worktree writes to a copy, so the wiki would never see the ingest.
- They need **permission to write files** in the folder. A read-only task fails at the first page it
  writes.
- `cronExpression` means the same recurring schedule, in local time. `fireAt` means a one-time task.
- **Task ids.** ChatGPT may not let you choose an id. Use the id the skill specifies as the task's
  **name**, and record what ChatGPT shows (name, and an id if there is one) in `llm-wiki.yml`. Anywhere a
  skill matches tasks by id, match by that name.
- **Tasks run only while the computer is on and the ChatGPT app is running.** Do not promise that a missed
  run catches up later; say a task due while the app was closed may not run until the next scheduled time.

**If you cannot create, change or delete a task yourself in this session**, do not report it as done:

1. Write the task's full prompt to `.agents/tasks/<task name>.md`.
2. Give the owner the exact steps: open **Scheduled** in the sidebar, create a task, set the name and the
   schedule (say both in words, e.g. *"every weekday at 07:30"*), choose this folder, choose to run it in
   the project directory, allow it to edit files, and paste the prompt from that file.
3. Record the job as `pending_manual: true` in `llm-wiki.yml` and check the task list again next session.

**One-off tasks that delete themselves** (`llm-wiki task: once`): if the task cannot delete itself, it
sets `task: pending-cleanup` on its request page as the skill already says, and the delivery tells the
owner, in one line, to delete it under **Scheduled**.

## Connectors

The sources a wiki reads (Outlook, Teams, Slack, Gmail, Google Drive, Jira…) are ChatGPT **apps /
connectors**, connected in ChatGPT's own settings. The skills name sources, not tool names. Use whichever
connected app provides the source.

- **Check them from a scheduled run, not only from this chat.** A connector that works here may not be
  available to a scheduled task. The first ingest report says which sources were reachable.
- Some company connectors (Outlook mail and calendar especially) need an admin to approve them. If one is
  missing, say that, and never ask the owner for a password or token instead.
- **Local sources** (a folder outside the wiki, a SQLite file): ChatGPT reaches them through a local MCP
  server. Where `references/local-sources.md` names `claude_desktop_config.json`, the ChatGPT equivalent is
  the MCP servers setting in the ChatGPT desktop app, or `~/.codex/config.toml` (`[mcp_servers.<name>]`)
  if the owner also uses Codex. If neither is clear in this version of the app, tell the owner what server
  is needed rather than editing config you cannot see.

## Delegating to a subagent

Where the setup skill says to **dispatch the `voice-profiler` agent**, spawn a subagent and tell it to
follow the `voice-profiler` skill, with the same inputs the skill lists. If subagents are not available,
follow the skill's own fallback (run it inline, in batches).

## Memory

"Claude Memory" or "ChatGPT Memory" (L1) means **ChatGPT's memory**, the facts it keeps about the owner
across chats. Credentials never go there, and never into the wiki.

## The folder's own files

- **`AGENTS.md`** is the folder's standing instructions. ChatGPT reads it in every session on the folder.
- **`.agents/skills/`** holds the folder's copy of the skills. ChatGPT discovers skills there by itself,
  which is why a teammate needs nothing installed. When a skill says to copy a skill into the folder,
  copy **its whole folder**, this `PLATFORM.md` included: the scheduled tasks read
  `.agents/skills/wiki/PLATFORM.md`.
- **A folder set up from Claude** has a `CLAUDE.md` and a `.claude/skills/` instead. Read `CLAUDE.md` as
  this folder's instructions when there is no `AGENTS.md`. Do not delete or rewrite either app's files.
  Only the `ingest_owner` runs the scheduled jobs, whichever app they use.

## Which version is running

`{{PLUGIN_VERSION}}` and "the running plugin's `plugin.json`" mean: `plugin.json` at the root of the
installed llm-wiki plugin, if it was installed as a plugin. Otherwise, use the `VERSION` file in the
`wiki-setup` skill's folder. It is the same number.

## Invoking setup

`@wiki-setup` (Claude: `/wiki-setup`). The owner can also just say *"set up the wiki"* or *"upgrade the
wiki"*.

## Upgrades

There may be no plugin to update: often the skills arrived **in the folder**, from the starter download.
The upgrade then works like this:

- **The owner puts the newest `llm-wiki-chatgpt-starter` zip inside the wiki folder** and asks to upgrade.
  Unpack it into `.agents/llm-wiki-update/`, treat `.agents/llm-wiki-update/LLM Wiki/.agents/skills/` as
  "the installed plugin" for the update procedure (baseline, three-way merge, never drop a local change),
  then delete `.agents/llm-wiki-update/`. Leave the zip itself for the owner to delete, and say so.
- **If llm-wiki was installed as a ChatGPT plugin**, the owner updates it under **Plugins** first, and the
  procedure runs as written.

What the brief's update nudge and every upgrade instruction should tell the owner:
*"download the newest llm-wiki zip from
https://github.com/mauricio-morales/llm-wiki/releases/download/chatgpt-latest/llm-wiki-chatgpt-starter.zip,
put it in your wiki folder, then start a new session there and ask it to upgrade the wiki."*

## No session-start hook

The Claude package runs a short check when a session opens. ChatGPT runs nothing. `AGENTS.md` carries
everything a session needs, so nothing is lost.
