# Optional features — and offering them on upgrade

Some features only exist if the owner switches them on. A wiki set up before a feature shipped has never
been asked about it, and **an upgrade is the moment to ask** — as a question that waits for an answer, not
as a sentence at the end of a summary. A recommendation buried in a closing paragraph is a recommendation
almost nobody reads, which makes the feature invisible to exactly the people who would use it.

## The registry

| Feature | Key | Since | Set up by | Already on when |
|---|---|---|---|---|
| Focus Areas — up to three topics the role is accountable for, with their own reports | `focus-areas` | 1.6.0 | Phase 2b | `focus_areas` is non-empty |
| Objectives — the owner's KPIs or OKRs, driving reports and the brief | `objectives` | 1.15.0 | Phase 2c | `Wiki/<primary>/Objectives.md` exists |
| News — topics to watch, scanned by its own job at a chosen cadence | `news` | 1.21.0 | Phase 3b | `news.enabled` is true |

**Maintainers: every new optional feature gets a row here, in the release that ships it.** Without one, an
upgrade has no way to know the feature exists, and every wiki that predates it never hears about it.

## Which ones to offer

On an upgrade, offer every registered feature that is:

- **not already on**, and
- **not recorded as `declined`** in `feature_offers` in `llm-wiki.yml`.

A feature recorded as `later` is offered again. One with no record at all is offered — including on wikis
that have been upgraded several times since the feature shipped, because **a version number says when a
wiki was last upgraded, not whether its owner was ever asked**. Upgrades before this rule existed rebuilt
jobs without offering anything, so "the wiki is already past that version" is not evidence of a question.

**Setup records answers too.** When the owner turns a feature down during setup (no Focus Areas, no
objectives, no news), write it to `feature_offers` as `declined`, so an upgrade never asks again what setup
already settled. Wikis set up before setup recorded this may be asked once more about something they
declined back then — one extra question, once, and then it is on record. That is the right trade against
the alternative, which is never asking at all.

## How to ask

**One `AskUserQuestion` call, one question per feature**, batched — up to four in a call. Each question
says what the feature does for *this* owner in a sentence, and offers three answers:

- **Set it up now** — run its setup phase straight after the question, in this same session.
- **Not now** — record `later`; offer it again on the next upgrade.
- **No thanks** — record `declined`; never offer it again. The owner can still switch it on any time by
  asking.

Ask **after** the mechanical part of the upgrade (skills refreshed, tasks rebuilt) and **before** the final
summary, so the summary can say what was actually set up rather than what could be.

**Never end an upgrade with a paragraph recommending a feature.** If it is worth mentioning, it is worth
asking.

Record each answer under `feature_offers` with the version it was offered in:

```yaml
feature_offers:
  news: { offered_in: "1.29.0", answer: later }
  objectives: { offered_in: "1.29.0", answer: declined }
  focus-areas: { offered_in: "setup", answer: declined }
```

A feature set up now needs no entry — being on is the record. A newly enabled source still gets the usual
backfill question, per `references/backfill.md`.
