# Artifacts — where derived output goes

## The rule

**Everything a run produces that is not a wiki page goes in `Artifacts/`, in a dated subfolder.** Nothing
is ever written to the wiki root.

An analysis, an export, a generated spreadsheet or deck, a scratch computation, a comparison table, a
one-off script — all of it is derived output. Left at the root it accumulates into a mess that nobody
dares delete because nobody remembers what produced it or whether anything depends on it.

## What may exist at the wiki root

An exhaustive list. Anything else is misplaced:

```
llm-wiki.yml          configuration
CLAUDE.md             how sessions behave here
Wiki/                 the knowledge base
Archives/             snapshots of ingested URLs — inputs we saved
Artifacts/            things this wiki produced — outputs
.claude/              the skills copy and its baseline
wiki-*-state.json     job cursors
```

`Archives/` and `Artifacts/` are easy to confuse and are opposites: **Archives holds copies of things
that came from elsewhere; Artifacts holds things made here.**

## Naming

```
Artifacts/YYYY-MM-DD-<scope>-<what>/
```

Dated first so the folder sorts chronologically, then enough words to say what it covers and what was
done — `2026-09-18-acme-renewal-rate-comparison`, not `2026-09-18-analysis` and certainly not `output`.
The name is what someone reads in six months deciding whether it can go.

**One folder per piece of work**, not per file. A run producing four files for one analysis makes one
folder holding four files.

## Every artifact folder carries `_about.md`

Short, and written at the time — not promised for later:

```markdown
# <what this is>

- **Produced:** 2026-09-18, by the <ingest | brief | a session | Focus report> run
- **Why:** the question or request that caused it
- **Derived from:** the wiki pages, sources or documents it was built from
- **Ingested:** yes (2026-09-18) | no | n/a — nothing here is a durable fact
- **Safe to delete after:** a date, or a condition, or "keep"
```

Without it, an artifact is an orphan file that nobody can evaluate, and the folder becomes write-only.

## Re-ingesting what an artifact learned

An artifact often contains facts worth keeping — an analysis that establishes a number, a comparison that
settles a question. **Those facts belong in the wiki, not only in the artifact**: a fact reachable only by
opening a spreadsheet in a dated folder is not in the knowledge base.

- Ingest the **conclusions**, not the working. The wiki wants what was established and what follows from
  it, not a copy of the calculation.
- **Link the artifact as the source** from the page that carries the fact, so the working is one hop away
  and the number can be checked.
- Mark `Ingested: yes` with the date in `_about.md`, so a later run does not ingest it a second time.
- If it holds nothing durable — a scratch calculation, an intermediate export — mark it `n/a`. That is a
  real answer, and it stops the question being reopened every time someone tidies up.

## Artifacts are the one thing here that is safe to delete

The wiki has no version history, so pages are never deleted outside an explicit instruction. **Artifacts
are different**: they are derived, their durable facts are already ingested, and most can be regenerated.
They are also what will grow the folder, and on a synced folder every megabyte reaches everyone.

So: the monthly lint reports `Artifacts/` size and lists folders past their stated delete-after date or
older than six months with `Ingested: yes`. **It proposes; it does not delete on its own** — an artifact
someone is mid-way through using looks identical to a stale one.

Never delete an artifact still linked from a live wiki page without saying so — the link becomes a dead
reference to evidence that used to exist, which is worse than a large folder.
