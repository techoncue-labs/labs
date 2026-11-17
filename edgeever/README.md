# EdgeEver

EdgeEver is an open source, self-hosted notes and knowledge base app with the classic three-pane layout (notebooks, note list, editor), plus web, desktop and phone apps.
In this guide you install it with Docker Compose, sign in, and use notebooks, notes, tags, search, a mind map and the ZIP export.

> Tested with EdgeEver v2.28.0 on 2026-11-16.
> Video: https://youtu.be/ZFQvQUDJLJI

## Requirements
- A Linux machine, 64-bit Intel/AMD or ARM, with kernel 5.6 or newer (a home server, NAS or small VM is fine).
- Docker Engine 24 or later with Docker Compose v2.
- A web browser.
- No account and nothing to pay. AI features are optional and not used here.

## How the Docker version works
One container runs the web workspace, the server and the sign-in. Notes live in a SQLite database and images/attachments in files, all inside one Docker volume (`edgeever-data`). You open it in the browser on port 8787.

## Step 1: Install with Docker Compose
Make a folder, step into it, and download the official compose file. Then set the version to run and a long admin password (generate one with `openssl rand -hex 32`), and start it.
```bash
mkdir edgeever && cd edgeever
curl -fsSL -o compose.yaml https://raw.githubusercontent.com/tianma-if/edgeever/main/compose.yaml
export EDGE_EVER_VERSION=v2.28.0
export EDGE_EVER_AUTH_PASSWORD='CHANGE_ME_long_random_string'
docker compose up -d
docker compose ps
```
Docker pulls the official image and starts it. Run `docker compose ps` again after 10 to 20 seconds until the status says `(healthy)`, with port `0.0.0.0:8787->8787/tcp`.

Alternative: this folder contains `compose.yaml` (the official file with v2.28.0 as the default tag) and `.env.example`. Copy both into your folder, `cp .env.example .env`, put your own password in `.env`, and run `docker compose up -d`. A `.env` file keeps the settings for later restarts, unlike `export`.

## Step 2: Sign in
Open http://localhost:8787. You see **Sign in to EdgeEver**. The username is `admin` by default; the password is the one you just set. Click **Open workspace**.

You land in the three-pane workspace: notebook tree on the left (with Inbox), note list in the middle, editor on the right. A new instance comes with a few sample notebooks and notes.

## Step 3: Feature one - notebooks
- In the left pane, next to **Notebooks**, click the plus button. Type `Home Projects` and click **Create**.
- Open the menu next to Home Projects and choose **New child notebook**. Name it `Garden` and click **Create**.

Garden appears inside Home Projects. Notebooks can nest as deep as you like.

## Step 4: Feature two - write a note
- With Garden selected, click **New note**. Click the title and type `Spring garden plan`.
- In the editor add a heading, a short paragraph, and a task list: `Buy tomato seeds`, `Fix the fence`, `Water the herbs`. Tick the first task.
- There is no save button: it saves by itself.
- Click the Markdown button to see the note as plain Markdown, then switch back to rich text.

## Step 5: Feature three - tags
- At the top of the note, click the tag button, type `garden,ideas` and press Enter. The tags appear on the note's card in the list.
- Click the tag icon at the top left: all your tags, with how many notes use each. Pick `ideas` to see every note with that tag, from any notebook.

## Step 6: Feature four - search
- Click **All notes**, then the **Search notes** box at the top of the list, and type `tomato`.
- The list narrows to the matching note right away. Search covers the full text of every note, not just titles.
- Click the result to open it in the editor. Press **Exit search** to get the full list back.

## Step 7: Feature five - a mind map (no AI)
- Next to **New note**, open **More** and choose **Mind map**. A new map opens with a starter template: a main topic and a few branches.
- Double-click the main topic and type `Weekend trip`.
- Click **Outline view**: the same map as a heading with a nested list. Add a new branch at the end, `Packing`, with child items such as `Tent` and `Snacks` (indent with Tab).
- Switch back to **Canvas view**: the new branch is on the map.

## Step 8: Feature six - export your notes
- Click **Profile** at the bottom left, then **Backup and Import**.
- Under **Import and export**, click **Export EdgeEver ZIP**; it downloads.

The ZIP holds plain Markdown files and your attachments, so you can read your notes without EdgeEver or import the same ZIP into another instance. EdgeEver can also import from Notion, Evernote, Obsidian and other apps.

## The web clipper (not set up here)
The EdgeEver Web Clipper is a browser extension for Chrome, Edge and Firefox that turns a web page into a clean note (text, images, source link) in your own instance. You connect it with an API token from your profile.

## Troubleshooting and tips
- Old kernel: if startup fails with `EISDIR reading .../node_modules/...`, upgrade the host OS or kernel first, before touching `/data` permissions or data.
- Reachable outside your home network? Put a reverse proxy with HTTPS (Caddy, Traefik, Nginx) in front of port 8787.
- Pin a version tag instead of `latest` for real use, and take a backup before every upgrade.
- Full backup of the volume: stop the container first (`docker compose stop edgeever`, wait for shutdown to complete), then copy the entire `edgeever-data` volume (SQLite file, `edgeever-secrets.json`, `resources`). Restore only while EdgeEver is stopped, into an empty volume.
- If you used `export`, set the variables again in a new terminal before running `docker compose` commands (or use a `.env` file).

## Limits and costs
- Free and open source.
- The AI assistant and AI diagrams need a model: bring your own key from an AI provider (get it from the provider's console), which may cost money. Not covered here.
- Very young project (first appeared June 2026) with new releases every few days, so expect changes.
- Keep your instance private, for your own notes.

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
```

## Official links
- Docs (Docker deployment): https://github.com/tianma-if/edgeever/blob/main/docs/deploy-docker.md
- README: https://github.com/tianma-if/edgeever/blob/main/README.md
- Source code: https://github.com/tianma-if/edgeever
- Licence: AGPL-3.0 (https://github.com/tianma-if/edgeever/blob/main/LICENSE)
- Releases: https://github.com/tianma-if/edgeever/releases
- Website: https://edgeever.org

---
Not affiliated with or endorsed by the EdgeEver authors. "EdgeEver" is used only to describe the software.
