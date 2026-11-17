# tau

tau is a small, readable coding agent from Hugging Face that lives in your terminal: it reads files, writes and edits code, and runs commands for you.
In this guide you install it with uv, connect it to a free local model in Ollama, let it build, edit and test a tiny project, and tour its main commands and saved sessions.

> Tested with tau 0.4.11 and the qwen3:14b model in Ollama, on Linux, on 2026-11-16.
> Video: https://youtu.be/Dbpx1kRt6CY

## Requirements
- macOS, Linux or Windows, and Python 3.12 or newer (uv can fetch Python for you).
- uv: https://docs.astral.sh/uv/getting-started/installation/
- Ollama, a free app that runs models locally: https://ollama.com/download
- A tool-capable model. This guide uses `qwen3:14b` (about 9 GB), which ran on one GPU with 20 GB of memory.
- No account and no paid key.

## Step 1: Install tau
```bash
uv --version
uv tool install tau-ai
tau --version
```
Expected: uv installs tau into its own environment and prints `Installed 1 executable: tau`; `tau --version` prints `0.4.11` (or newer). If uv warns that `~/.local/bin` is not on your `PATH`, run `export PATH="$HOME/.local/bin:$PATH"`.

## Step 2: Get a free local model
Ollama must be running with a longer context length than its default (see Troubleshooting). If you start it yourself:
```bash
OLLAMA_CONTEXT_LENGTH=32768 nohup ollama serve > ollama.log 2>&1 &
```
Then pull the model and check it:
```bash
ollama pull qwen3:14b
ollama list
```
The first pull downloads about 9 GB and ends with `success`; `ollama list` then shows `qwen3:14b`.

## Step 3: Connect tau to Ollama
Ollama speaks the OpenAI API on `http://localhost:11434/v1`. tau wants the name of an environment variable that holds an API key. Ollama ignores the key, so any word works; it only must not be empty.
```bash
export LOCAL_API_KEY=ollama
echo 'export LOCAL_API_KEY=ollama' >> ~/.bashrc
tau --provider local --base-url http://localhost:11434/v1 --api-key-env LOCAL_API_KEY --model qwen3:14b setup
tau providers | grep local
```
`setup` saves the provider; `tau providers` lists `local`, pointing at Ollama. (For a cloud provider you would put a real key in that variable instead, for example `CHANGE_ME_your_api_key` from the provider's console. Never commit it.)

## Step 4: First run
```bash
mkdir tip-calc
cd tip-calc
tau
```
The terminal turns into tau's interface: the conversation on top, the prompt box at the bottom, and below it the folder and the model (`local:qwen3:14b`). Type and press Enter:
```
hi, which tools can you use?
```
tau shows Thinking while the model works, then the answer streams in: read, write, edit and bash.

## Step 5: Build a tiny project
A made-up example:
```
Create a Python script called tip.py that takes a bill amount and a tip percent as command-line arguments and prints the tip and the total. Add a short README.md too.
```
tau calls the write tool; a green row reports the two files written (`tip.py` and `README.md`), then the model sums up what it made.

## Step 6: Read and edit a file
```
Read tip.py, then change it so an optional third number splits the total between that many people.
```
tau shows an edit row: it changes only the parts that need to change. (In the video the model chose a split option instead of a plain third number, which works too.) Press Ctrl+O to expand the tool calls and see the exact change, with new lines in green. Press Ctrl+O again to fold it back.

## Step 7: Run commands
```
Run tip.py with a bill of 80, a 20 percent tip and 4 people, then write a small unit test and run it.
```
Each bash call shows a short description instead of the raw command (Ctrl+O shows the exact commands and output). In the video the first run failed with an indentation mistake from the earlier edit; tau fixed it, wrote `test_tip.py`, and fixed code and test until the last run passed. Expected result: a tip of 16, a total of 96, and 24 per person. This took about three minutes on the local model.

## Step 8: Your own commands and files
- Start a line with `!` and the prompt turns into a `$`. `!ls` lists the folder, and the output is added to the conversation.
- Type `@` and part of a file name, then press Tab to pick the file, and add your question, for example: `@test_tip.py explain this in two sentences`.
- If an answer runs long, press Escape to stop it.

## Step 9: The main commands
- Ctrl+K opens the command palette; type to search it, for example `session`, and press Enter. The session view shows the model, the provider, the four tools and how much context is used. Escape closes it.
- `/tools` lists the four tools.
- `/model` opens the model picker.
- `/hotkeys` shows every keyboard shortcut.
- `/theme` switches the look, for example to `tau-light` and back to `tau-dark`.

## Step 10: Sessions and print mode
Press Ctrl+D to quit; tau prints how to resume. Back in the shell:
```bash
tau sessions
tau -p "list the files here and say what each one does"
tau
```
`tau sessions` lists saved sessions with their id, title and model. `tau -p` (print mode) prints the answer straight to the terminal, with no interface, which is handy in scripts. In the interface, type `/resume`, pick the earlier session, and you are back where you left off.

## Troubleshooting and tips
- "Missing provider API key": the variable is empty in this shell. Set it again (`export LOCAL_API_KEY=ollama`); Ollama does not check its value.
- The agent forgets what it just read: on GPUs under 24 GB, Ollama gives models only about 4,000 tokens of context by default, and its docs suggest at least 64,000 for coding tools. Start Ollama with a larger `OLLAMA_CONTEXT_LENGTH`, as far as your memory allows (32768 was used here).
- Tools never get called: in testing, Qwen 2.5 Coder printed its tool calls as plain text and nothing happened; Qwen3 called them properly. Use a tool-capable model, as tau's docs advise.

## Limits and costs
- tau is free (MIT). With a local model there is no bill per message, and your code stays on your machine.
- A 14B model is slower and makes more mistakes than big cloud models, so check its work. Answers here took from a few seconds to over a minute.
- tau runs real commands in your folder and its docs state it is not a sandbox: use it on your own projects, and a container or spare machine for anything risky.
- It is early (version 0.4) and changing fast.

## Clean up
```bash
rm -rf tip-calc              # the example project
uv tool uninstall tau-ai     # remove tau
ollama rm qwen3:14b          # frees about 9 GB
```
tau keeps its settings and sessions in `~/.tau`; delete that folder too if you want a completely fresh start. Remove the `LOCAL_API_KEY` line from `~/.bashrc` if you added it.

## Official links
- Docs: https://twotimespi.dev/quickstart/
- Providers and models: https://twotimespi.dev/guides/providers-and-models/
- Local inference: https://twotimespi.dev/guides/local-inference/
- TUI guide: https://twotimespi.dev/guides/tui/
- CLI reference: https://twotimespi.dev/reference/cli/
- Slash commands: https://twotimespi.dev/reference/slash-commands/
- Keybindings: https://twotimespi.dev/reference/keybindings/
- Source code: https://github.com/huggingface/tau
- PyPI package: https://pypi.org/project/tau-ai/
- Licence: MIT (https://github.com/huggingface/tau/blob/main/LICENSE)
- Releases: https://github.com/huggingface/tau/releases
- Ollama context length: https://docs.ollama.com/context-length

---
Not affiliated with or endorsed by the tau authors or Hugging Face. "tau" is used only to describe the software.
