# goose

goose is a free, open source, general purpose AI agent that runs commands, edits files and tests the result on your own computer.
In this guide you install the goose command line tool, connect it to a free local model through Ollama, let it build and test a tiny project, use permission modes, run a recipe and add an extension.

> Tested with goose 1.59.0 and the qwen3:14b model in Ollama, on Linux, on 2026-11-16.
> Video: https://youtu.be/w1ZO6LMTu3E

## Requirements
- macOS, Linux or Windows. The commands below are for Linux and macOS; see the install docs for Windows.
- `curl`, `bzip2` and `tar` (used by the install script), and Python 3 for the example project.
- Ollama, the free local model runner: https://ollama.com/download
- A model that supports tool calling. This guide uses `qwen3:14b` (about 9.3 GB). A GPU helps a lot; the one used here had 20 GB of memory.
- No account and no API key.

## Step 1: Install the goose CLI
The install command from goose's docs. `CONFIGURE=false` skips the setup questions (you run them in Step 3).
```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash
goose --version
```
Expected output (shortened):
```
Detected OS: linux with ARCH x86_64
Downloading stable release: goose-x86_64-unknown-linux-gnu.tar.bz2...
Extracting goose-x86_64-unknown-linux-gnu.tar.bz2 to temporary directory...
Moving goose to /home/you/.local/bin/goose
Skipping 'goose configure', you may need to run this manually later
$ goose --version
 1.59.0
```
If `goose` is not found, add `~/.local/bin` to your `PATH` (for example `export PATH="$HOME/.local/bin:$PATH"` in `~/.bashrc`).

## Step 2: Get a local model
Start Ollama in the background with a larger context length (goose's docs say the default context is too small and goose then misses its tools), pull the model, and check it:
```bash
OLLAMA_CONTEXT_LENGTH=32768 nohup ollama serve > ollama.log 2>&1 &
ollama pull qwen3:14b
ollama list
```
Expected output:
```
pulling manifest
...
verifying sha256 digest
writing manifest
success
NAME         ID              SIZE      MODIFIED
qwen3:14b    bdbd181c33f2    9.3 GB    ...
```
If Ollama already runs as a system service (the default after installing it on many systems), skip the `ollama serve` line and set `OLLAMA_CONTEXT_LENGTH` for that service instead (see the Ollama docs).

## Step 3: Connect goose to Ollama
```bash
goose configure
```
Answer the questions:
1. "Share anonymous usage data to help improve goose?" - No (your choice).
2. "How would you like to set up your provider?" - Manual Configuration.
3. "Which model provider should we use?" - Search all providers..., type `oll`, choose Ollama (not Ollama Cloud).
4. "Provider Ollama requires OLLAMA_HOST" - keep `localhost`, press Enter.
5. "Would you like to configure advanced settings?" - No.
6. "Select a model:" - `qwen3:14b`.
7. "Which goose mode would you like to configure?" - Smart Approve Mode, so goose asks before it changes anything.

Expected end:
```
Configuration saved successfully to /home/you/.config/goose/config.yaml
Set to Smart Approve Mode - modifications require approval
```

## Step 4: Your first session
```bash
mkdir goose-demo
cd goose-demo
goose session
```
The header shows a new session with `ollama qwen3:14b` and the folder. Type a first question at the `>` prompt:
```
What can you do in this folder? Answer in three short bullet points. Reply in English.
```
After a few seconds the model answers (for example: list files, analyze code, run shell commands). Then type `/help` to see the in-session commands, such as `/mode`, `/model`, `/compact` and `/exit`.

## Step 5: Build and test a tiny project
A made-up task, still in the same session:
```
Create tip.py with split_bill(total, people, tip_percent): add the tip, divide by people, round to 2 decimals. Then create test_tip.py with three unittest test methods: test_even_split, test_with_tip, test_rounding. Run python3 -m unittest -v and tell me the result in one sentence. Reply in English.
```
Because of Smart Approve mode, goose asks before each write and each shell command: "Goose would like to call the above tool, do you allow?" Choose Allow. It writes both files and runs the tests:
```
Ran 3 tests in 0.000s
OK
```
The local model can take a minute or more to think.

## Step 6: Change it, then check it yourself
```
If a test failed, check whether the code or the test is wrong and fix it. Also make split_bill raise ValueError when people is less than 1, add a test for that, and run python3 -m unittest -v again. Reply in English.
```
Allow the tool calls. In the video the first edit accidentally emptied `tip.py`, the tests failed with an ImportError, and goose read the error, rewrote the file and ran the tests again until they passed. Now leave the session and check the result yourself:
```
/exit
```
```bash
ls
python3 -m unittest -v
```
Expected: `tip.py` and `test_tip.py` (plus `__pycache__`), and the tests pass. In the video goose replaced the rounding test with the new one instead of adding a fourth test (3 tests, not 4). Small models make mistakes like this, so always check what changed.

## Step 7: Sessions and permission modes
```bash
goose session list
goose session --resume
```
`session list` shows your sessions with id, name, date and folder; `--resume` reopens the latest one. In the session:
```
/mode approve
Delete test_tip.py. Reply in English.
```
In Approve mode goose asks before every tool. It shows the command it wants to run (`rm test_tip.py`); choose Deny. goose reports that the delete was blocked. Then:
```
/exit
```
```bash
ls
```
`test_tip.py` is still there. Note: after this step `goose info -v` showed `GOOSE_MODE: approve` in the config.

## Step 8: Save a task as a recipe
A recipe is a small YAML file with a version, title, description, instructions and prompt:
```bash
cat > recipe.yaml <<'EOF'
version: 1.0.0
title: Test check
description: Run the tests in this folder and summarise them
instructions: You are a careful helper. Only run tests, never change files. Reply in English.
prompt: Run the tests in this folder with python3 -m unittest and give a one-line summary of how many passed.
EOF
goose recipe validate recipe.yaml
goose run --recipe recipe.yaml --explain
GOOSE_MODE=auto goose run --recipe recipe.yaml
```
Expected:
```
✓ recipe file is valid
...
Ran 3 tests in 0.000s
OK
All 3 tests passed successfully.
```
`goose run` has no one to ask for approval, so the Approve modes stop with an error there. That is why the last command sets `GOOSE_MODE=auto` for this one run (this recipe only runs tests).

## Step 9: Add an extension
Extensions give goose new tools through the Model Context Protocol (MCP). The Developer extension is on by default.
```bash
goose configure
```
Choose Add Extension > Built-in Extension > Memory (lets goose remember your preferences), and set the timeout to `300` seconds. Expected:
```
Enabled memory extension
Configuration saved successfully to /home/you/.config/goose/config.yaml
```
Then show your version, config paths and every extension that is on:
```bash
goose info -v
```

## Troubleshooting and tips
- goose ignores its tools or your hints: the context length is probably too low. Raise `OLLAMA_CONTEXT_LENGTH` when you start Ollama.
- An error sending a request to localhost: Ollama is not running, or the model is not pulled yet.
- Stuck in a loop: press Ctrl+C and start a new session.
- In the CLI, avoid asking goose to start servers that never exit, such as a dev server.
- Keyring errors in containers or headless machines: goose's known-issues page says to set `GOOSE_DISABLE_KEYRING=1` there.
- `goose run -t "your task"` runs a single task and exits, handy in scripts.
- `/model` shows or switches the model in the middle of a session; `/compact` summarizes a long chat to save context.
- The desktop app shares the same settings as the CLI.

## Limits and costs
- goose is free (Apache 2.0). With a local model there is no bill, and your code stays on your machine.
- A small local model makes more mistakes than big cloud models; long, complex tasks may need a bigger model or a paid provider (with that provider's API key, for example `OPENAI_API_KEY=CHANGE_ME_your_api_key` from the provider's console; never commit it).
- goose runs real commands and edits real files. Use it on your own machine, in a project under version control, and keep an approval mode on until you trust it.

## Clean up
```bash
rm -rf goose-demo                 # the example project
ollama rm qwen3:14b               # frees about 9.3 GB
pkill -f "ollama serve"           # only if you started it with nohup in Step 2
```
goose itself is a single binary in `~/.local/bin/goose`; its config is in `~/.config/goose` and its sessions in `~/.local/share/goose`.

## Official links
- Docs: https://goose-docs.ai/docs/quickstart
- Install: https://goose-docs.ai/docs/getting-started/installation
- Local models (Ollama): https://goose-docs.ai/docs/getting-started/providers#local-llms
- CLI commands: https://goose-docs.ai/docs/guides/goose-cli-commands
- Permission modes: https://goose-docs.ai/docs/guides/managing-tools/goose-permissions
- Recipes: https://goose-docs.ai/docs/guides/recipes/session-recipes
- Extensions: https://goose-docs.ai/docs/getting-started/using-extensions
- Known issues: https://goose-docs.ai/docs/troubleshooting/known-issues
- Source code: https://github.com/aaif-goose/goose
- Licence: Apache-2.0 (https://github.com/aaif-goose/goose/blob/main/LICENSE)
- Releases: https://github.com/aaif-goose/goose/releases
- Ollama: https://ollama.com/download

---
Not affiliated with or endorsed by the goose authors. "goose" is used only to describe the software.
