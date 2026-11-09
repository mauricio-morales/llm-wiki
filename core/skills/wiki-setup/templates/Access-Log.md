---
access-log: true
type: reference
created: "{{DATE}}"
updated: "{{DATE}}"
---

## About

Append-only LRU signal. `query` adds one line per page it reads in full, recording **which** page loaded
and **why** it was picked. `prune` reads this to find cold pages; `status` reads it for the hot/cold
profile and routing transparency.

This page is exempt from orphan / stale / demote lint rules. Do not hand-edit; it is machine-appended.

Format: `- <ISO-date> -- [[Wiki/NS/Page]] -- <op> -- matched: "<why>"`

## Log (append-only, newest at bottom)

- {{DATE}} -- [[Wiki/Reference/Access-Log]] -- setup -- matched: "bootstrap"
