# The update nudge — how a wiki asks to be upgraded

Setup embeds this, filled in, near the end of the **ingest** and **brief** tasks. One copy here to correct.

## Why a task has to do this

Updates reach a wiki in two hops: an interactive session refreshes the folder's skills, then each task
rebuilds its own prompt. **The first hop needs a human**, and if the owner never happens to open a session
on the folder, nothing moves — the jobs keep running old instructions indefinitely and never mention it.

The scheduled tasks are the only thing guaranteed to run. So they are the ones that must ask. **Nobody
should have to be told by a person that their wiki is behind; the wiki should say so itself.**

## Deciding whether to nudge

A scheduled run cannot always see the published plugin — it may not be installed in that context. Use
whichever of these is available, strongest first:

1. **The plugin's manifest is readable on this machine** (the marketplace copy, or an installed plugin
   directory). Compare its version to `skills_version` in `llm-wiki.yml`. This is a direct answer. Do not
   reach out to the network for it; if it is not on disk, fall through.
2. **This task's stamp is behind `skills_version`.** The folder moved ahead and this task has not rebuilt
   yet — the self-update step handles it, so only nudge if that step reported it could not.
3. **`lastUpdateCheck` in `llm-wiki.yml` is more than 14 days old.** Nobody has opened a session that
   checked. That is not proof an update exists, so **say exactly that** — "it has been three weeks since
   this wiki checked for updates", not "an update is available".

**Never claim an update exists on signal 3 alone.** Crying wolf about a version that may not exist is how
a nudge gets ignored permanently.

## Rate limit — this matters more than the nudge

Record `lastUpdateNudge` in the task's state file. **At most one nudge every 7 days**, across all tasks —
the brief and the ingest report must not both nudge in the same week.

**The brief is the place for it.** It is the artifact the owner actually reads. An ingest report nudge is
a fallback for wikis with no brief configured.

A line that appears every morning stops being read within three days, and it takes the rest of the brief's
credibility with it. If the owner ignores three nudges (roughly three weeks), **do not escalate frequency
— escalate specificity**: name what they are missing, concretely. Still once a week.

## What to say

One line. Bottom of the brief, never the top — it is housekeeping, not news.

**Say what they gain, not what version they are on.** A version number motivates nobody. Read the
CHANGELOG entries between the two versions and name the one or two changes that would actually affect
this wiki, in plain terms:

- ❌ *"llm-wiki 1.9.0 is available (you're on 1.7.0)."*
- ✅ *"Your wiki is a few versions behind — the newer one drains paged sources properly, which affects
  your email ingest. Open a session on this folder and say 'update the wiki' to pick it up."*

**Make it one action.** Tell them the exact words to say, and where. Not "run the setup wizard", not a
command they have to remember correctly — *"open a session on this folder and say 'update the wiki'"*.

If the reason is signal 3, say the honest version: *"this wiki hasn't checked for updates in three weeks
— open a session on the folder and say 'update the wiki' if you want it to look."*

## After they do it

Once `skills_version` moves, **clear `lastUpdateNudge`** and confirm it once in the next artifact: what
changed, in one line. Then stop mentioning it. The owner acted; the worst thing now is to keep talking
about it.
