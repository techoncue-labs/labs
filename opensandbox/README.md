# OpenSandbox

OpenSandbox gives AI agents isolated, throwaway environments (sandboxes) where they can run commands and manage files, locally with Docker or later on Kubernetes.
In this guide you start the OpenSandbox server on your own machine, use the Python SDK to create a sandbox, run commands and code in it, write and read files, then use the `osb` command line tool and clean up.

> Tested with OpenSandbox 1.2.1 (opensandbox-server, opensandbox SDK and opensandbox-cli from PyPI) on 2026-11-16.
> Video: https://youtu.be/LoJh4OdPGn4

## Requirements
- Docker installed and running (required for local use). Docker CE is recommended over the snap package.
- Python 3.10 or newer, with `venv` and `pip`.
- `uv` (the official way to start the server uses `uvx`): https://docs.astral.sh/uv/
- Internet access the first time, to download the server and pull container images.
- No account and no API key.

Optional: pre-pull the sandbox image so the first sandbox starts quickly: `docker pull python:3.12-slim`.

## How it works
Your script (Python SDK) or the `osb` CLI talks to the sandbox server on port 8080. The server asks Docker to start a container from the image you pick. A small helper inside the container runs your commands and file operations and sends the results back.

## Step 1: Create the config
In a first terminal, write the example Docker configuration to `~/.sandbox.toml` and look inside.
```bash
uvx opensandbox-server init-config ~/.sandbox.toml --example docker
grep -A3 '^\[server\]' ~/.sandbox.toml
grep -A2 '^\[runtime\]' ~/.sandbox.toml
```
Expected output: the server section shows `host = "127.0.0.1"` and `port = 8080`; the runtime section shows `type = "docker"`.

## Step 2: Start the server
```bash
uvx opensandbox-server
```
Because no API key is set, the server asks you to confirm running without one. For a local test on your own machine, type `YES` (capitals) and press Enter. A few log lines later it reports that it is running on http://127.0.0.1:8080. Leave this terminal open.

(Non-interactive alternative from the docs: `OPENSANDBOX_INSECURE_SERVER=YES uvx opensandbox-server`.)

## Step 3: The built-in API page
Open http://localhost:8080/docs in your browser. It lists every endpoint (create, list, renew, pause, delete...). Open **List Sandboxes**, click **Try it out**, then **Execute**. The response comes back right away with an empty list: no sandboxes yet.

## Step 4: Install the Python SDK
In a second terminal, make a project folder and copy the three small scripts from this guide's `sample-data/` folder into it (`hello_sandbox.py`, `files_and_code.py`, `keep_alive.py`). Then create a virtual environment and install the official SDK.
```bash
mkdir -p ~/sandbox-demo
cp sample-data/*.py ~/sandbox-demo/    # run this from this guide's folder
cd ~/sandbox-demo && ls
python3 -m venv .venv
source .venv/bin/activate
pip install opensandbox
```
Expected output: pip ends with `Successfully installed ...`. The scripts need no settings: the SDK talks to localhost:8080 by default.

## Step 5: Your first script
```bash
cat hello_sandbox.py
```
It creates a sandbox from the `python:3.12-slim` image, runs three commands inside it (system name, Python version, current user), and destroys the sandbox in a `finally` block so nothing is left running even if something fails.

## Step 6: Create a sandbox and run commands
```bash
python hello_sandbox.py
```
Expected output (the ID and exact versions will differ):
```
Sandbox ready: <sandbox-id>
[sandbox] head -n 1 /etc/os-release -> PRETTY_NAME="Debian GNU/Linux ..."
[sandbox] python3 --version -> Python 3.12.x
[sandbox] whoami -> root
Sandbox destroyed
```
The system is Debian (the image, not your machine), and you are root only inside the sandbox. The server terminal logs each request.

## Step 7: Write a file, run code, read the result
`files_and_code.py` holds a few lines of made-up Python as a text block (seven temperatures and a summary file). The script writes that code into a file inside the sandbox, runs it there, and reads the summary back.
```bash
python files_and_code.py
```
Expected output:
```
[sandbox] summary written
Days: 7
Warmest: 24 C
Average: 21.0 C
```

## Step 8: Keep a sandbox running
`keep_alive.py` creates a sandbox with a 15-minute timeout, prints its ID and closes only the local connection. Keep the ID in a variable and look at Docker:
```bash
cat keep_alive.py
SB=$(python keep_alive.py); echo $SB
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}"
```
`docker ps` shows a real container running from the `python:3.12-slim` image. If you forget it, the timeout removes it (the default is 10 minutes).

## Step 9: The command line tool (osb)
```bash
pip install opensandbox-cli
osb config init
osb config set connection.domain localhost:8080
osb config set connection.protocol http
osb sandbox list
osb command run $SB -o raw -- python -c "print(6 * 7)"
osb file write $SB /tmp/note.txt -c "hello from the CLI" -o json
osb file cat $SB /tmp/note.txt -o raw
```
Expected: `osb sandbox list` shows your sandbox, the command prints `42`, and `file cat` prints `hello from the CLI`.

## Step 10: Clean up
```bash
osb sandbox kill $SB -o json
osb sandbox list
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}"
```
The list is empty and `docker ps` no longer shows the sandbox container. Finally, go back to the server terminal and press Ctrl+C to stop the server.

## Troubleshooting and tips
- Running without an API key is for local tests only. The docs say to always set `api_key` under `[server]` in production; clients then send it in the `OPEN-SANDBOX-API-KEY` header. Generate one with `openssl rand -hex 32` and put it in place of `CHANGE_ME_long_random_string`.
- Sandboxes expire after 10 minutes by default: pass a `timeout` when creating them, or renew them.
- On a cloud VM, if the sandbox health check times out, set `eip` under `[server]` in `~/.sandbox.toml` to the public IP or hostname clients use, then restart the server.
- If Docker came from a snap package and sandboxes fail to start, the troubleshooting guide suggests Docker CE instead.
- The first sandbox can be slow while Docker pulls images; pre-pull `python:3.12-slim`.
- To pin the tested versions: `uvx opensandbox-server@1.2.1`, `pip install opensandbox==1.2.1 opensandbox-cli==1.2.1`.
- Run only code you are allowed to run, on machines you control.

## Limits and costs
- Free and open source; no account needed.
- It is the box, not the brain: no AI agent is included, you bring your own.
- You run and secure the server yourself.
- By default sandboxes are normal Docker containers; stronger isolation (gVisor, Kata, Firecracker) needs extra setup.
- Young project with frequent releases; 1.2.1 was released in November 2026.

## Clean up
Covered in Step 10. To remove everything this guide created:
```bash
rm ~/.sandbox.toml
rm -rf ~/sandbox-demo
```

## Official links
- Docs and website: https://open-sandbox.ai
- Getting started: https://github.com/opensandbox-group/OpenSandbox#getting-started
- Server configuration: https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/getting-started/configuration.md
- Python SDK: https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/sandbox/python/README.md
- CLI guide: https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md
- Troubleshooting: https://github.com/opensandbox-group/OpenSandbox/blob/main/server/TROUBLESHOOTING.md
- Source code: https://github.com/opensandbox-group/OpenSandbox
- Licence: Apache-2.0 (https://github.com/opensandbox-group/OpenSandbox/blob/main/LICENSE)
- Releases: https://github.com/opensandbox-group/OpenSandbox/releases

---
Not affiliated with or endorsed by the OpenSandbox authors. "OpenSandbox" is used only to describe the software.
