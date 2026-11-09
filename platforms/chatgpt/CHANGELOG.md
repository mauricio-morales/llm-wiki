# Changelog — LLM Wiki for ChatGPT

Released separately from the Claude plugin, under `chatgpt-v*` tags, with its own version numbers. Both
are built from the same wiki in `core/`. The Claude [changelog](../claude/CHANGELOG.md) has the full
history of what the wiki does; this one records each ChatGPT release and what is different in ChatGPT.

Derived from [llm-wiki](https://github.com/MehmetGoekce/llm-wiki) by Mehmet Gökçe (MIT) — see
[LICENSE](../../LICENSE).

## 0.2.0 — 2026-11-09

**Preview — rebuilt natively for ChatGPT, installed from your company's plugin directory.** Still not run
end to end in ChatGPT.

- **Written for ChatGPT, not translated from Claude.** The wiki is now written once, in `core/`, with no
  app in mind, and this package is built from it. ChatGPT's instructions say what ChatGPT does: questions
  as numbered options in the chat, scheduled tasks under **Scheduled** (run on the folder itself, allowed
  to edit files, with exact manual steps when a task can't be created automatically), apps for sources,
  the voice profiler as a subagent. The `PLATFORM.md` translation page is gone.
- **Installed like any ChatGPT plugin.** A workspace admin imports this repository once (Admin → Plugins
  → Import marketplace); everyone then adds LLM Wiki from **Plugins**, and updates come through the same
  way. The starter-folder download from 0.1.0 is retired.
- Built from the same wiki as Claude **1.38.3**.

## 0.1.0 — 2026-11-09

**Preview — first ChatGPT build. Not yet run end to end in ChatGPT.** Built from the Claude plugin
**1.38.3**, with every feature it has: guided setup, scheduled ingest, brief, lint and news, Focus
Areas, objectives, the inbox responder and email voice, rescheduling, and one-off requests.

What is different from Claude:

- **The folder's instructions are `AGENTS.md`**, and the folder's copy of the skills lives in
  `.agents/skills/`, where ChatGPT finds them without anything installed.
- **Two downloads.** The *starter* zip is a ready wiki folder: unzip it, open it in the ChatGPT desktop
  app, say "set up the wiki". The *plugin* zip is the same skills packaged as a ChatGPT plugin. The repo
  also has a ChatGPT marketplace (`.agents/plugins/marketplace.json`).
- **A translation page in every skill** (`PLATFORM.md`). It covers the parts that can't be swapped
  word for word:
  - questions are numbered options in the chat, not a question tool;
  - scheduled jobs are ChatGPT scheduled tasks, run on the folder itself, never in a worktree, with
    permission to edit files;
  - when a task can't be created automatically, the owner gets exact steps and the prompt in a file;
  - connectors are ChatGPT apps;
  - the voice profiler runs as a subagent following a skill.
- **Upgrades:** put the newest starter zip in the wiki folder and ask to upgrade. Local edits to the
  skills are merged, not overwritten.
- **No session-start hook.** `AGENTS.md` covers it.

Things to confirm on the first real run:
- that ChatGPT creates the scheduled tasks itself;
- which connectors a scheduled task can reach;
- that the skills in `.agents/skills/` are picked up in a folder that is not a git repository.
