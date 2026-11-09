# Changelog — LLM Wiki for ChatGPT

Released separately from the Claude plugin, under `chatgpt-v*` tags. Each version is built from a
version of the Claude plugin, named in its entry. For what the wiki itself does, see the Claude
[CHANGELOG](../../CHANGELOG.md): the behaviour is the same, and this file records only what is different
in ChatGPT.

Derived from [llm-wiki](https://github.com/MehmetGoekce/llm-wiki) by Mehmet Gökçe (MIT) — see
[LICENSE](../../LICENSE).

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
