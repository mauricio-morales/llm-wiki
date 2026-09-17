# Task self-update — how a deployed wiki adopts a new plugin version

Setup embeds this block, filled in, as **Step 0 of every scheduled task**. One copy here to correct.

## The problem it solves

A scheduled task's prompt is generated once, at setup, and then runs unchanged forever. Improvements
shipped in later plugin versions — new rules about draining paged sources, tracking commitments, item ids
— live in the *templates*, and never reach a wiki that was set up before them. Without this step, a wiki
set up in March is still running March's instructions next year, with no sign that anything is stale.

## The propagation chain

```
plugin updated (marketplace)
  -> owner's next session notices, updates the folder's .claude/skills/   [see updates.md]
  -> next scheduled run sees its stamp is behind the folder's skills version
  -> regenerates its own prompt from the current templates + llm-wiki.yml
  -> new prompt takes effect on the FOLLOWING run
```

Two hops, both automatic. The only human action is approving the folder-skills update, which the owner is
prompted for at most weekly.

## Step 0, in every task

Each generated task prompt carries a stamp on its first line:

```
<!-- llm-wiki task: ingest | template version: 1.12.1 | generated: 2026-09-17 -->
```

At the start of a run:

1. Read `skills_version` from `llm-wiki.yml` and the stamp in this prompt.
2. **Equal, or the prompt is newer** — do nothing, silently. This is the normal case and must cost
   nothing.
3. **The prompt is behind** — regenerate it (below), then **continue this run under the instructions it
   started with.** The new prompt takes effect on the next run.

**Finishing the run on the old prompt is deliberate.** A job that rewrites the instructions it is
midway through executing is unreviewable when it misbehaves — nobody can say afterwards which version
produced which output. One run's delay is a small price for every run being attributable.

## Regenerating

The prompt is **template + configuration**. Rebuild it as:

- the current template from `.claude/skills/wiki-setup/references/task-<kind>.md` in the wiki folder,
- filled from `llm-wiki.yml` — sources and their verbatim notes, delivery, schedules, skip pattern,
  focus areas, **and the `preferences` block for this job**,
- stamped with the new version and today's date.

**Every setting lives in `llm-wiki.yml`, never only in the prompt.** That is what makes regeneration
safe. A preference that exists only inside a task prompt is destroyed the first time the task rebuilds —
which is why reply-learned preferences are written to `llm-wiki.yml`, not into the prompt text.

If regeneration cannot be completed — a template missing, config that will not fill cleanly — **keep the
existing prompt, run normally, and report it.** A working old prompt beats a broken new one. Never leave
a task with a half-written prompt.

## Report it

Whenever a task regenerates, say so in that run's report: the version moved from and to, and a one-line
summary of what changed, drawn from the CHANGELOG entries in between. The owner should never discover
that their jobs changed behavior by noticing different output.

## What this does not do

- **It does not update the plugin**, and it does not reach out to the network. It only closes the gap
  between the folder's skills and the tasks generated from them.
- **It does not run on a wiki whose folder skills are stale.** If the owner never approves the folder
  update, tasks stay where they are — correctly, since the templates they would rebuild from are the ones
  they already used.
- **It never changes schedules, delivery destinations or which sources are enabled.** Those are the
  owner's configuration. It updates *instructions*, not *choices*.
