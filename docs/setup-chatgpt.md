# LLM Wiki — setup in ChatGPT

Using Claude instead? See [setup in Claude](setup-claude.md). Everything else about the wiki, from what
setup asks to how sharing works, is in the [README](https://github.com/mauricio-morales/llm-wiki#readme).

> **Preview.** The ChatGPT version is built from the same wiki as the Claude one and does the same things,
> but it hasn't been run end to end in ChatGPT yet. If a step below doesn't match what you see, please
> [tell us](https://github.com/mauricio-morales/llm-wiki/issues) what you saw.

## Set up

**What you need first:** the **ChatGPT desktop app** (Mac or Windows), signed in with your **company's
ChatGPT workspace** account.

The wiki won't run in ChatGPT in a web browser. Your wiki is a real folder of files on your computer, and
only the desktop app can work inside a folder and run its scheduled jobs there. If you're reading this in
a browser tab, install the desktop app first.

The steps are the same on Mac and Windows. Where a click differs, it says so.

---

### 1. Make sure LLM Wiki is in your company's plugin directory

This happens **once for the whole company**, and only a ChatGPT workspace admin can do it. If LLM Wiki
already shows up under **Plugins** (step 2), someone has done it: skip ahead.

**For the admin:**

1. In ChatGPT, open **Admin** → **Plugins**, then **Add** → **Import marketplace**.
2. Enter the repository URL, exactly this, with no branch or folder:

   ```
   https://github.com/mauricio-morales/llm-wiki
   ```

3. Import it. A large import can take up to an hour.
4. Make **LLM Wiki** available to the people who should have it.

From then on, new versions arrive when the marketplace syncs (**Admin** → **Plugins** → **Marketplaces**
→ **Sync now** to pull one straight away).

### 2. Add the plugin

In the ChatGPT desktop app, switch to **Work** with the toggle above the message box, open **Plugins**,
find **LLM Wiki**, and click **+** to add it. If it doesn't appear, quit ChatGPT fully and reopen it.

### 3. Make a folder for the wiki

A normal, empty folder, made the same way as any other folder. Give it a real name: `Acme Wiki`,
`My Work Brain`.

- **On a Mac:** in Finder, go where you want it, then **File** → **New Folder**.
- **On Windows:** in File Explorer, go where you want it, right-click an empty spot → **New** →
  **Folder**.

**If you want to share it with your team, create it inside a folder that already syncs**, such as your
work OneDrive. (On Windows, that's in File Explorer's left-hand column, usually as **OneDrive – *your
company name***.) If it's just for you, anywhere is fine.

### 4. Connect the apps it should read

Setup asks which of your connected apps the wiki should read: email, calendar, chat, meeting notes,
tickets. Connect them in ChatGPT's settings, under **Apps** (some versions call them connectors), before
you start or when setup asks.

Some company apps, Outlook mail and calendar especially, need your admin to approve them. If one is
missing, setup carries on without it and tells you. **Never paste a password or token into the chat**:
the wiki never needs one.

### 5. Open a ChatGPT session on the wiki folder

This is the step people get wrong.

In **Work**, **open a folder** and choose the folder you just made. Allow ChatGPT to **edit files** in it
when it asks: the wiki writes its pages there, so a read-only session can't set it up.

An ordinary chat with no folder won't do. Your wiki *is* that folder, and the session has to be working
inside it. You'll know you got it right because the session shows the folder it's working in.

**Make it easy to come back to.** Everything below assumes you're in the wiki folder when you ask it
something. If your app lets you pin or favourite the folder, do it; otherwise choose it each time you
start a session.

### 6. Type `@wiki-setup` and press enter

Or just say *"set up the wiki"*.

It asks a handful of questions: what to call the wiki, who can read it, which of your connected apps it
should read, when it should run, how far back to reach. Each comes with numbered options. **Reply with the
letters**, like `1A 2C`, or answer in your own words. *"Just do whatever's normal"* is a complete answer
to any of them.

At the end it creates the wiki's **scheduled tasks**: the daily ingest, the morning brief, a monthly
check-up, and the news scan if you asked for one. They appear under **Scheduled** in the sidebar.

- **They run while your computer is on and the ChatGPT app is open.**
- **If ChatGPT can't create a task by itself**, setup gives you the exact steps: the task's name, its
  schedule in words, and a file holding the text to paste. Do those before you close the session.

**After setup, you never type a command again.** Ask a question and it searches the wiki; say "save this"
and it files it; say "reconfigure the wiki" to change anything.

### Joining a wiki someone else set up

1. **Add the plugin** (step 2), if you haven't.
2. **Make sure the shared folder has synced to your computer.** You should be able to open it in Finder
   or File Explorer and see a `Wiki` folder inside.
3. **Open a ChatGPT session on it**, same as step 5.
4. **Just start asking.**

**This works when the wiki was set up in ChatGPT.** A wiki set up in Claude keeps its instructions where
Claude reads them, so for now use Claude for that one.

**Don't run setup there.** Only one person runs the scheduled ingest. A second one means two jobs
appending to the same pages every morning, each pulling from a different person's email and chat, and
someone's private inbox ending up in a shared wiki. If you want your own morning brief, say **"set up a
brief for me"** and it adds just that.

---

## Upgrading

Your morning brief tells you, about once a week, when your wiki is behind. You can also upgrade any time.

1. **Update the plugin.** In **Work** → **Plugins**, find **LLM Wiki** and update it. If no update shows
   yet, your company's copy hasn't synced: ask your workspace admin to sync it (**Admin** → **Plugins** →
   **Marketplaces** → **Sync now**).
2. **Start a new ChatGPT session on your wiki folder**, a new one so it picks up the update, and say
   *"upgrade the wiki"*.

It refreshes the copy of the instructions kept inside your wiki folder, **keeping anything you've
customized**. It rebuilds your scheduled tasks so they follow the new version, and tells you in plain
words what changes. If your wiki is already up to date, it says so in one line and stops.

**Joined someone else's wiki?** You don't need to do anything. The person who set it up runs the upgrade,
and it reaches you through the shared folder.

**Versions.** The ChatGPT package has its own version numbers and its own
[changelog](../platforms/chatgpt/CHANGELOG.md), released as `chatgpt-v…`. The Claude plugin's `v…`
releases are a different package.

<details>
<summary>Developers: installing without a workspace admin</summary>

With the Codex CLI: `codex plugin marketplace add mauricio-morales/llm-wiki`, then add **LLM Wiki** from
**Plugins** in the desktop app and restart it. Each release also attaches the package as a zip, for
reference.
</details>
