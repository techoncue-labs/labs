# LobeHub

LobeHub (formerly LobeChat) is a self-hostable chat and agent workspace for AI models, used from your browser.
In this guide you self-host it with the official Docker Compose setup script, connect free local models through Ollama, then try chat, switching models, agents and topics.

> Tested with LobeHub 2.3.3 (Docker image `lobehub/lobehub:latest` on 2026-11-16, Agent Gateway 0.5.0). To get exactly that version, use the image tag `lobehub/lobehub:2.3.3` instead of `latest`.
> Watch the video: https://youtu.be/XsjdkBC9h3A

## Requirements
- Linux or macOS, or Windows through WSL 2
- Docker and Docker Compose
- Minimum (light usage, from the docs): 2 CPU cores, 4 GB RAM, 20 GB disk
- Free ports: 3210, 9000, 9001, 8787, 8788 (plus 11434 for Ollama in this guide)
- For the local models: a graphics card helps (the Ollama command below uses an NVIDIA GPU via `--gpus=all`), and about 7 GB of disk for the two models
- No cloud account and no paid API key

## Step 1: Run the official setup script
Make a folder and run the official setup script with `-l en` for English. It downloads `docker-compose.yml`, `searxng-settings.yml`, `bucket.config.json` and `.env`.
```bash
mkdir lobehub && cd lobehub
bash <(curl -fsSL https://lobe.li/setup.sh) -l en
```
Answer the prompts:
- Deployment mode: press **Enter** (default, local mode)
- "Do you want to regenerate security secrets? (y/n) [y]": press **Enter**
- "Do you want to initialize the database? (y/n) [y]": press **Enter** (pulls the images, starts Postgres briefly, stops it)

Expected output (end):
```
Security secret generation results are as follows:
LobeHub:
  - URL: http://localhost:3210
```
The report also lists RustFS (port 9000) and the Agent Gateway (port 8787). The script writes freshly generated secrets into `.env`; keep that file private.

## Step 2: Start the stack
```bash
docker compose up -d
docker logs -f lobehub
```
Wait until the log shows the database migration and "Ready":
```
[Database] Start to migration...
✅ database migration pass.
...
- Local:        http://localhost:3210
✓ Ready in ...
```
Press **Ctrl+C** to stop following the logs (the app keeps running), then:
```bash
docker compose ps
```
Every service (lobehub, lobe-gateway, lobe-postgres, lobe-redis, lobe-rustfs, lobe-searxng) is listed as Up. `lobe-rustfs-init` exits after its one-time job, which is normal.

## Step 3: Create your local login
Open http://localhost:3210. This is your own instance, so the account lives only here.
1. Click **Sign up now**.
2. Enter an email address and a password (twice), click **Sign Up**, and agree to the terms.
3. A short welcome follows (usage data opt-out, language, your name, interests, suggested agents). Choose what you like or skip.
4. You land in the workspace with **Lobe AI** on the left. It has no model yet.

## Step 4: Start Ollama with two free models
Start Ollama with the Docker command from the LobeHub Ollama docs. It uses your GPU, keeps models in the `ollama` volume, opens port 11434 and allows cross-origin requests:
```bash
docker run -d --gpus=all -v ollama:/root/.ollama -e OLLAMA_ORIGINS="*" -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3.2
docker exec -it ollama ollama pull qwen3
```
Expected output (each pull ends with):
```
verifying sha256 digest
writing manifest
removing unused layers
success
```
llama3.2 is about 2 GB, qwen3 about 5.2 GB. No NVIDIA GPU? Drop `--gpus=all` (models then run on the CPU, slower).

So that the LobeHub container can reach Ollama by name (`http://ollama:11434`, used in the next step), attach Ollama to the stack's network. The network is `<folder>_lobe-network`, so with a folder called `lobehub`:
```bash
docker network connect lobehub_lobe-network ollama
```

## Step 5: Connect Ollama to LobeHub
1. Click your name, open **Settings**, then **Provider**, and pick **Ollama** (it is already switched on).
2. Set the address to `http://ollama:11434`.
3. Click **Fetch models**: llama3.2 and qwen3 appear. Switch both on.
4. Choose **llama3.2** next to the **Check** button and click **Check**: it passes. (The default check model is one you have not pulled, so pick llama3.2 first.)

## Step 6: Feature one - chat
On the home page, click the model name under the input box, open **Model**, and choose **llama3.2**. Type:
```
Explain what a Docker volume is, in two short sentences.
```
Press Enter. The answer streams in, generated on your machine, and the chat is saved as a topic. Hover over the answer to copy it, edit it, or ask again.

## Step 7: Feature two - switch models
Click the model name again and pick **qwen3**. Ask:
```
Write a three-line poem about a cup of tea.
```
Qwen3 thinks first; you can expand its reasoning, then it answers. You can switch models any time inside the same chat.

## Step 8: Feature three - agents
- Click **Community** in the sidebar and search (for example "Spanish"). Shared agents are sorted by category. Opening and adding community agents needs a LobeHub account sign-in.
- Build your own instead: click **Add Agent**, give it a name and create it. On its profile, pick its model (for example qwen3) and write its core instructions below.

## Step 9: Feature four - topics
Every conversation is saved as a topic of its agent.
- Open the three dots next to the chat title and choose **Add to Home Favorites**.
- Open the menu again, choose **Rename**, and call it `Docker notes`.
- Click the share button to export the chat as an image, Markdown, PDF or JSON.

Everything is stored in your own database.

## Troubleshooting and tips
- The setup script is for the first install only. After that, change settings in `.env` (see the "Custom deployment" part of the docs).
- Port already in use: change `LOBE_PORT` in `.env`.
- Database errors at the first start: the docs reset it like this (this deletes your chats and settings):
  ```bash
  docker compose down
  sudo rm -rf ./data
  docker compose up -d
  ```
- Ollama will not connect: check that Ollama was started with `OLLAMA_ORIGINS="*"`, that the address in the provider settings is right, and (for `http://ollama:11434`) that Ollama is attached to `lobehub_lobe-network`.
- To use a cloud model provider instead, enter its key in **Settings > Provider** (for example an OpenAI key from your provider's console). Never commit `.env` or keys to git.

## Limits and costs
- Licence: LobeHub Community License, based on Apache 2.0 with extra conditions. Commercial use without changing the code is allowed; developing and distributing a modified (derivative) version needs a commercial licence from LobeHub. Read it before reselling a fork.
- Small local models give simpler answers than large cloud models.
- Not everything works offline: the community market and web search need internet.
- Self-hosting is free; you handle updates and backups.

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
docker rm -f ollama        # add: docker volume rm ollama   to delete the models
```
Chats and files live in `./data` and `./s3_data` inside the `lobehub` folder.

## Official links
- Docs (Docker Compose): https://lobehub.com/docs/self-hosting/platform/docker-compose
- Ollama provider: https://lobehub.com/docs/usage/providers/ollama
- Agents: https://lobehub.com/docs/usage/getting-started/agent
- Topics: https://lobehub.com/docs/usage/agent/topic
- Source code: https://github.com/lobehub/lobehub
- Licence: LobeHub Community License, no SPDX identifier (https://github.com/lobehub/lobehub/blob/canary/LICENSE)
- Releases: https://github.com/lobehub/lobehub/releases
- Ollama image: https://hub.docker.com/r/ollama/ollama

---
Not affiliated with or endorsed by the LobeHub authors. "LobeHub" is used only to describe the software.
