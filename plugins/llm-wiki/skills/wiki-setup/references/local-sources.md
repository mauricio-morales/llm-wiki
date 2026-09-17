# Local sources — filesystem paths and databases

**Consult this only when a user asks to ingest something that lives on their machine** — a folder, a
SQLite file, a local database, an application's own data store. It is not part of the setup conversation
and should never be raised unprompted.

## Why a local path is not automatically readable

A Cowork session runs sandboxed. It has the wiki folder, and it does **not** have arbitrary access to the
rest of the machine just because the session is "local". A path being on the same computer is not access.

This is the failure to expect: the user names a path, it looks completely reasonable, and the scheduled
job then fails to read it every night — which looks exactly like a quiet week. **Never record a local
source you have not actually read from within the session that will run it.**

The fix is to expose that specific resource through an **MCP server** configured in the desktop app.
Once configured, the ingest job reaches it through that server's tools rather than through the filesystem.

## Config file

`claude_desktop_config.json`:

- **macOS** — `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows** — `%APPDATA%\Claude\claude_desktop_config.json`

Entries go in the `mcpServers` object. **The app must be restarted** before a new server appears; a user
who says "I added it and it still doesn't work" has almost always not restarted yet.

## Match the server to the datastore

**Do not reach for these two examples regardless of what the user actually has.** They are a SQLite
server and a filesystem server. A MySQL or MariaDB database needs a MySQL/MariaDB server; Postgres needs a
Postgres one; a document store needs its own. Handing someone the SQLite config for a MySQL database
wastes their afternoon.

Establish what the source actually is first — ask if it is not obvious from the path or the application —
then find the matching server. **Search the MCP registry rather than reciting a package name from
memory**: names, maintainers and invocations change, and a stale package name fails in a confusing way.
Where a registry search tool is available in the session, use it; otherwise point the user at the
official MCP server list and name what to look for.

Prefer, in order: an official server for that datastore, a well-maintained community one, and only then a
generic workaround (for instance exporting to a file the filesystem server can reach).

### SQLite — verified working

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": [
        "--with", "mcp<2",
        "mcp-server-sqlite",
        "--db-path", "/absolute/path/to/your/local/database.db"
      ]
    }
  }
}
```

Useful when an application keeps its own SQLite store — local transcription apps, note apps, many desktop
tools. Point `--db-path` at the real file, not a directory.

### Filesystem — verified working

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents/your-project-folder",
        "/Users/username/Desktop/another-allowed-folder"
      ]
    }
  }
}
```

Each path after the package name is a directory the server is allowed to read. **Grant the narrowest set
that covers the source.** Every directory listed is reachable by anything using that server, forever —
`/Users/username` to reach one subfolder is a bad trade the user will not think about again.

### Credentials

A database server usually needs a user and password. **Those belong in `claude_desktop_config.json` and
nowhere else** — never in `llm-wiki.yml`, never in a task prompt, never in a wiki page. The wiki is plain
files in a folder that may well be synced to a whole team. Use a read-only database account wherever the
datastore supports one; the ingest never writes to a source.

## Capture the schema once, and put it in the task

**This is the part most worth getting right.** Once access works, inspect the source and write what you
found **into the ingest task prompt**. A scheduled job should never rediscover structure at 6am every
morning: it costs tokens on every run, it is slower, and a job that re-derives its own understanding
nightly will eventually derive it differently and change behavior with no code change.

**For a database**, record in the task prompt:

- Which tables matter, and what each holds in one line
- The columns actually used, with their types where it is non-obvious (epoch seconds versus ISO text is
  exactly the kind of thing that silently breaks a window calculation)
- **The stable identifier** for a record — the dedup key
- **The change-detection field** — a modified/updated timestamp. Where one exists, a record whose value
  advanced since last ingest must be **re-ingested and its wiki entry updated in place**, not skipped as
  already-seen. Edits after the fact are common: corrected transcripts, re-tagged speakers, renamed items.
- Any table that must be joined, and on what
- **Whether there is more than one list of things.** An application often keeps several related tables
  that all look like "the records" — capture every one that matters, because a job told about one will
  silently ignore the rest, and that gap is invisible.
- A worked example query for the window pull, so the run does not have to compose one from scratch

**For a folder**, record: the directory layout, which subfolders matter, file naming and what the parts
mean, which extensions to process and which to ignore, and how "new or changed" is determined (modified
time, a filename date, a sidecar index).

Write it as a compact block in the task prompt, not as a promise to go and look. The point is that a run
opens the prompt already knowing the shape of the data.

## Verify before recording

In order, and do not skip ahead:

1. The MCP server is configured and the app restarted.
2. **The session can actually reach it** — list the tables, or list the directory. Not "it should work".
3. Pull one real record for a known window and confirm the fields are what the schema block claims.
4. Only then record the source in `llm-wiki.yml` and write the schema block into the task.

If any step fails, record the source as `no_connector` with the reason rather than as enabled. A source
configured but unreachable is worse than one left out — it makes the job report quiet weeks.

## Schema drift

Applications update and change their stores. Treat a run where the recorded schema no longer matches —
a missing column, a renamed table, zero rows from a query that used to return some — as a **finding, not
an error to swallow**: report it, and re-capture the schema rather than quietly falling back to guessing.
The monthly lint is a reasonable place to re-verify that each local source still answers.
