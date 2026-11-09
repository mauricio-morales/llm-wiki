# LLM Wiki — setup in Claude

Using ChatGPT instead? See [setup in ChatGPT](setup-chatgpt.md). Everything else about the wiki, from what
setup asks to how sharing works, is in the [README](https://github.com/mauricio-morales/llm-wiki#readme).

## Set up

**What you need first:** the **Claude desktop app** (Mac or Windows), and you'll be using it in
**Cowork** — the mode where Claude works on a folder on your computer and can create and edit files in it.

The wiki won't run in Claude in a web browser, and it won't run in an ordinary chat or a Project. Your
wiki is a real folder of files, and something has to be able to write to it. If you're reading this in a
browser tab, install the desktop app first.

The steps are the same on both. Where a click differs, it says so.

---

### 1. Add the plugin

You only do this once.

**First, update the Claude app.** Older versions, on Windows especially, don't have the option this step
uses. Check for updates in the app's menu, or download the latest from
[claude.com/download](https://claude.com/download) and install it over the old one.

#### The normal way: add the marketplace

Open the **Cowork** tab, then **Customize** in the left sidebar → **Plugins** → **Add** → **Add
marketplace**. Paste this in and confirm:

```
mauricio-morales/llm-wiki
```

Then find **llm-wiki** in the list and click **Add**. Because it's connected to this repository, updates
arrive on their own.

#### Backup: upload the plugin as a file

Only if your app has no **Add marketplace** option, even after updating. This always works, but an
uploaded file doesn't update itself. When there's a new version your morning brief will say so, and you
repeat these steps with the new file.

1. **Download the file.** Open the [latest release](https://github.com/mauricio-morales/llm-wiki/releases/latest).
   Scroll down to **Assets** and click the file named **`llm-wiki-v….zip`**. Not the ones called
   "Source code", which won't work.
2. **If the browser asks, keep it.** Edge sometimes says the file "isn't commonly downloaded". Click the
   **…** next to it and choose **Keep**.
3. **Don't open or unzip it.** The app wants the `.zip` file exactly as it downloaded. It's in your
   **Downloads** folder. (On a Mac, Safari may unzip it on its own. If you find a folder instead of a
   `.zip`, download it again in Chrome or Edge.)
4. **Upload it.** In the Claude app, open the **Cowork** tab, then **Customize** in the left sidebar →
   **Plugins** → **Add**, choose the option to upload a plugin, and pick the `.zip` from **Downloads**.
5. **Check it's there.** **llm-wiki** now appears in your list of plugins.

If a later version of the app gains **Add marketplace**, switch to it: remove the uploaded llm-wiki,
then follow the normal way above. From then on, updates take one click.

*Already use Claude Code in a terminal? A plugin installed there stays in the terminal and doesn't reach
Cowork, so do the steps above anyway.*

### 2. Make a folder for the wiki

A normal, empty folder, made the same way as any other folder. Give it a real name: `Acme Wiki`,
`My Work Brain`.

- **On a Mac:** in Finder, go where you want it, then **File** → **New Folder**.
- **On Windows:** in File Explorer, go where you want it, right-click an empty spot → **New** →
  **Folder**.

**If you want to share it with your team, create it inside a folder that already syncs**: OneDrive,
Dropbox or Google Drive. That sync is how everyone else gets it later. (On Windows, your work OneDrive
is in File Explorer's left-hand column, usually as **OneDrive – *your company name***.) If it's just for
you, anywhere is fine.

### 3. Start a **Cowork session** on that folder

This part matters, and it's the step people get wrong.

**It has to be a Cowork session** — the kind of Claude session that works on a folder on your computer
and can read and write the files in it. In the Claude app, open the **Cowork** tab, start a new session,
and **choose the folder you just made** when it asks which folder to work in.

An ordinary chat won't do. Neither will a Project. Both can *read* things you give them, but neither can
create and update files in a folder on your machine, and that is the entire job here — your wiki *is*
that folder.

You'll know you got it right because the session shows the folder it's working in.

**Star it while you're there.** In the folder picker there's a star next to each folder. Clicking it
makes that folder the default, so every new session starts there instead of you picking it each time.
Worth doing: everything below assumes you're in the wiki folder when you ask it something, and a session
on the wrong folder can't see your wiki. (No star in your picker? Update the app. Until then, choose the
wiki folder each time you start a session.)

### 4. Type `/wiki-setup` and press enter

Type it into the message box like you'd type anything else — the leading `/` is part of it.

It then asks you a handful of multiple-choice questions: what to call the wiki, who can read it, which of
your connected tools it should read, when it should run, how far back to reach. A few minutes.

*"Just do whatever's normal"* is a complete answer to any of them.

**That one command is the only one you ever type.** After setup, the folder takes over — ask a question
and it searches the wiki, say "save this" and it files it, say "reconfigure the wiki" to change anything.

### Joining a wiki someone else set up

Do step 1, then skip to here.

1. **Make sure the shared folder has synced to your computer** — you should be able to open it in Finder
   or File Explorer and see a `Wiki` folder inside.
2. **Start a Cowork session on it** (same as step 3 above — a Cowork session, not an ordinary chat, and
   choose that folder). Star it in the picker so new sessions start there.
3. **Just start asking.**

It already knows what to do: the instructions live inside the folder, so they arrive with it. Nothing to
install, nothing to set up.

**Don't run `/wiki-setup` there.** Only one person runs the scheduled ingest. A second one means two jobs
appending to the same pages every morning, each pulling from a different person's email and chat — and
since the pages are append-only, nothing errors. It just quietly doubles, with someone's private inbox in
a shared wiki.

If you want your own morning brief, say **"set up a brief for me"** and it adds just that. A brief is
personal: it reads your pending asks and your calendar and goes to your Slack.

---

## Upgrading

New versions add features and fix problems, and your wiki keeps working on the old one until you upgrade.
You don't need to watch for releases: **your morning brief will tell you, about once a week, when your
wiki is behind.** You can also upgrade any time.

### 1. Update the plugin

- **Added as a marketplace** (the normal way): open **Cowork** → **Customize** → **Plugins**, find
  **llm-wiki**, and check for updates. If there is one, update it. If it doesn't show yet, quit Claude
  fully and reopen it.
- **Uploaded as a file** (the backup): an uploaded file can't update itself, so you upload the new one.
  Download the newest `llm-wiki-v….zip` from the
  [latest release](https://github.com/mauricio-morales/llm-wiki/releases/latest) and upload it the same
  way as in [step 1](#backup-upload-the-plugin-as-a-file). If the old version is still listed afterwards,
  remove **llm-wiki** from your plugins first, then upload the new file again. If your app now has **Add
  marketplace**, switch to it instead, and this step becomes one click from then on.

### 2. Upgrade your wiki

Start a **new** Cowork session on your wiki folder — a new one, so it picks up the plugin you just
updated — and **ask it to upgrade the wiki**, in your own words. *"Upgrade the wiki"* is enough.

It won't ask you the setup questions again. It:

- refreshes the copy of the plugin's instructions kept inside your wiki folder, **keeping anything you've
  customized**
- rebuilds your scheduled jobs (ingest, brief, lint, news) so they follow the new version from the next run
- adds any new job the version introduces, asking only what it genuinely needs from you — how often to
  check the news, say
- tells you in plain words what will work differently from tomorrow

If your wiki is already up to date, it says so in one line and stops.

**More than one wiki?** Do step 2 in each wiki's folder.

**Joined someone else's wiki?** You don't need to do anything. The person who set it up runs the upgrade,
and the updated instructions reach you through the shared folder. Please don't run it yourself on a shared
wiki: two people upgrading the same folder from different versions is how a synced folder ends up with
conflicting copies.
