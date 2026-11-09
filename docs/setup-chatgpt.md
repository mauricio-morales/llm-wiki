# LLM Wiki — setup in ChatGPT

Using Claude instead? See [setup in Claude](setup-claude.md). Everything else about the wiki, from what
setup asks to how sharing works, is in the [README](https://github.com/mauricio-morales/llm-wiki#readme).

> **Preview.** The ChatGPT version is built from the same instructions as the Claude one and does the
> same things, but it hasn't been run end to end in ChatGPT yet. If a step below doesn't match what you
> see, ChatGPT is told to say so and do the closest thing, never to pretend. Please
> [report it](https://github.com/mauricio-morales/llm-wiki/issues) with what you saw.

## Set up

**What you need first:** the **ChatGPT desktop app** (Mac or Windows), on a paid plan, signed in with
your work account if your company has one.

The wiki won't run in ChatGPT in a web browser. Your wiki is a real folder of files on your computer, and
only the desktop app can work inside a folder and keep its scheduled jobs running there. If you're reading
this in a browser tab, install the desktop app first.

The steps are the same on Mac and Windows. Where a click differs, it says so.

---

### 1. Download your wiki folder

There's nothing to install. You download a ready folder that already holds the instructions, in a hidden
folder called `.agents` that ChatGPT finds by itself.

1. **Download it:**
   [llm-wiki-chatgpt-starter.zip](https://github.com/mauricio-morales/llm-wiki/releases/download/chatgpt-latest/llm-wiki-chatgpt-starter.zip).
   This link always gets the newest version. If Edge says the file "isn't commonly downloaded", click the
   **…** next to it and choose **Keep**.
2. **Unzip it.** It's in your **Downloads** folder.
   - **On a Mac:** double-click it.
   - **On Windows:** right-click it → **Extract All…** → **Extract**.

   You get a folder called **LLM Wiki**. On Windows it may sit one level down, inside a folder named
   after the zip.
3. **Move the LLM Wiki folder where it should live, and rename it** if you like: `Acme Wiki`,
   `My Work Brain`. **To share it with your team later, put it inside a folder that already syncs**, such
   as your work OneDrive. (On Windows, that's in File Explorer's left-hand column, usually as
   **OneDrive – *your company name***.) If it's just for you, anywhere is fine.

Don't add or remove anything inside it. The **START HERE** file inside can be deleted once setup is done.

<details>
<summary>Prefer installing it as a ChatGPT plugin?</summary>

If your ChatGPT app lets you add plugins from a GitHub repository, add `mauricio-morales/llm-wiki`, then
install **llm-wiki** under **Plugins** and restart the app. Developers with the Codex CLI can run
`codex plugin marketplace add mauricio-morales/llm-wiki`. There's also a plugin zip,
[llm-wiki-chatgpt.zip](https://github.com/mauricio-morales/llm-wiki/releases/download/chatgpt-latest/llm-wiki-chatgpt.zip).

Then, instead of the starter folder, make a normal empty folder for the wiki and continue at step 2.
</details>

### 2. Connect the apps it should read

Setup asks which of your connected apps the wiki should read: email, calendar, chat, meeting notes,
tickets. Connect them in ChatGPT's settings, under **Apps** (some versions call them connectors), before
you start or when setup asks.

Some company apps, Outlook mail and calendar especially, need your IT admin to approve them. If one is
missing, setup carries on without it and tells you. **Never paste a password or token into the chat**: the
wiki never needs one.

### 3. Open a ChatGPT session on the wiki folder

This is the step people get wrong.

In the ChatGPT desktop app, switch to **Work** with the toggle above the message box, then **open a
folder** and choose your wiki folder. Allow ChatGPT to **edit files** in it when it asks. The wiki writes
its pages there, so a read-only session can't set it up.

An ordinary chat with no folder won't do. Your wiki *is* that folder, and the session has to be working
inside it. You'll know you got it right because the session shows the folder it's working in.

**Make it easy to come back to.** Everything below assumes you're in the wiki folder when you ask it
something. If your app lets you pin or favourite the folder, do it. Otherwise choose the wiki folder each
time you start a session.

### 4. Type `@wiki-setup` and press enter

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

1. **Make sure the shared folder has synced to your computer.** You should be able to open it in Finder
   or File Explorer and see a `Wiki` folder inside.
2. **Open a ChatGPT session on it**, same as step 3 above.
3. **Just start asking.**

There's nothing to download: the instructions live inside the folder. **This works when the wiki was set
up in ChatGPT.** A wiki set up in Claude keeps its instructions where Claude reads them, so for now use
Claude for that one.

**Don't run setup there.** Only one person runs the scheduled ingest. A second one means two jobs
appending to the same pages every morning, each pulling from a different person's email and chat, and
with someone's private inbox ending up in a shared wiki. If you want your own morning brief, say **"set
up a brief for me"** and it adds just that.

---

## Upgrading

Your morning brief tells you, about once a week, when your wiki is behind. You can also upgrade any time.

1. **Download the newest
   [llm-wiki-chatgpt-starter.zip](https://github.com/mauricio-morales/llm-wiki/releases/download/chatgpt-latest/llm-wiki-chatgpt-starter.zip).**
2. **Put the zip, as it is, into your wiki folder.** Don't unzip it.
3. **Start a new ChatGPT session on the wiki folder** and say *"upgrade the wiki"*.

It unpacks the new version itself and refreshes the instructions, **keeping anything you've customized**.
It rebuilds your scheduled tasks so they follow the new version, and tells you in plain words what changes.
When it's done, you can delete the zip.

*Installed it as a plugin instead?* Update **llm-wiki** under **Plugins** first, then do step 3.

**Joined someone else's wiki?** You don't need to do anything. The person who set it up runs the upgrade,
and it reaches you through the shared folder.

**Versions.** The ChatGPT package has its own version numbers and its own
[changelog](../platforms/chatgpt/CHANGELOG.md), released as `chatgpt-v…`. The Claude plugin's `v…`
releases are a different package; don't upload one into the other app.
