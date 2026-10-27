# Template: a one-off request task

Filled by the `wiki` skill (its "Something on a later date — one-off requests") when the owner asks for
something to happen **once**, at a later date. Passed as the `prompt` of a **one-time** scheduled task —
`fireAt`, never a cron expression.

The prompt is deliberately thin. **Everything about *what* to deliver lives on the request page in the
wiki**, so that deleting the task — which it does to itself once it has delivered — loses nothing. To run
the same thing again, a new task is made from the same page.

It carries no self-update step: it lives days or weeks, it reads its instructions from the page at run
time, and it uses the folder's current `wiki` skill to do the work.

---

<!-- llm-wiki task: once | request: {{REQUEST_PAGE}} | template version: {{PLUGIN_VERSION}} | generated: {{DATE}} -->

This is a one-off task for the wiki at `{{WIKI_PATH}}`. It runs once, delivers one thing to
{{OWNER_NAME}}, and then deletes itself. **What to deliver is not written here.** It is on the request
page, `{{REQUEST_PAGE}}` — read it; it is the whole brief.

## 1. Read

`llm-wiki.yml`, `Wiki/Schema.md`, then the request page.

- **The page is missing** → do not improvise from this task's title. Tell {{OWNER_NAME}}, where their brief
  goes, that the request page for task `{{TASK_ID}}` is gone, and stop. Leave the task in place.
- **`status` is `delivered` or `cancelled`** → do not deliver again. Go straight to step 5.

## 2. How current is it?

Read `lastSuccessfulRun` in `wiki-ingest-state.json`. The delivery time was chosen to land after the
ingest, so normally the wiki is current. If the ingest has not succeeded since the request last
collected, say so at the top of what you deliver — *"covers everything up to Mon 9 Nov, 06:00"* — rather
than presenting it as complete.

## 3. Build it

Follow the page's **Deliver** section literally — format, sections, length. Use its **Collected** section,
and query the wiki (per the `wiki` skill) for anything else the page asks for. Every collected item keeps
its `[id]` and its source link.

Save the result as an artifact — `Artifacts/YYYY-MM-DD-request-<slug>/`, with an `_about.md` — and link it
from the page's **Delivery log**.

## 4. Deliver

To {{OWNER_NAME}} only, where the page's `deliver_to` says. {{ONCE_DELIVERY_BLOCK}}

**Nothing goes to anyone else.** If the page says the result is meant for other people, deliver it to the
owner ready to forward — never send it on their behalf.

- **Delivered** → set `status: delivered` and `delivered_at`, and add a line to the Delivery log.
- **Delivery failed** → set `status: failed` with the error, and **do not delete this task**. Try the
  other channel the wiki uses for the brief, if there is one. The next ingest will see the failure.

## 5. Clean up — delete this task

Only when `status` is `delivered` or `cancelled`. Delete scheduled task **`{{TASK_ID}}`** with the
scheduler's delete tool — this task only, and only after checking that its id matches `task_id` on the
request page. Never delete any other task. Then set `task: deleted` on the page.

If the delete tool is not available in this run, set `task: pending-cleanup` on the page instead; the next
ingest removes it. A one-time task already stops itself after firing, so a missed cleanup costs a line in
the task list — never a second delivery, because the page's `status` is what decides that.
