# Paperless-ngx

Paperless-ngx is a self-hosted document management system: it reads your scans and PDFs (OCR) and turns them into one searchable archive in your browser.
In this guide you install it with Docker Compose, add documents by upload and through the consume folder, search the text inside them, let matching rules sort them, and optionally ask them questions with a local AI model.

> Tested with Paperless-ngx 3.4.2 on 2026-11-16.
> Video: https://youtu.be/tLrnXSbYLm4

## Requirements
- A Linux machine (small server, home lab box or virtual machine) with Docker and Docker Compose.
- A web browser.
- No account and nothing to pay.
- Optional, for the AI part (Step 11): Ollama with a local model, ideally on a machine with a capable GPU.

How it works: you add documents by uploading them or by dropping them into a consume folder. Paperless runs OCR on scans, keeps the original file and makes an archive copy. Matching rules add the correspondent, document type and tags. Then you search the full text, or use saved views.

## Step 1: Download the official compose files
Make a folder, step into it, save the address of the project's compose folder in a variable `R`, and download three files: the Postgres compose file (saved as `docker-compose.yml`), `docker-compose.env` and `.env`.
```bash
mkdir paperless
cd paperless
R=https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docker/compose
curl -L -o docker-compose.yml $R/docker-compose.postgres.yml
curl -LO $R/docker-compose.env
curl -LO $R/.env
```

## Step 2: Set the secret key
```bash
nano docker-compose.env
```
Find `PAPERLESS_SECRET_KEY=change-me` and replace `change-me` with your own long random string:
```
PAPERLESS_SECRET_KEY=CHANGE_ME_long_random_string
```
Generate one with `openssl rand -hex 32`. Save and exit (in nano: Ctrl+O, Enter, Ctrl+X).

## Step 3: Start Paperless-ngx
```bash
docker compose pull
docker compose up -d
```
Three containers start: the database (Postgres), a broker (Valkey) and the web server. The official compose uses the `ghcr.io/paperless-ngx/paperless-ngx:latest` image; to stay on the version tested here, change that tag to `3.4.2` in `docker-compose.yml`.

## Step 4: Create the first user
Give it a minute on the first start, then open http://localhost:8000. The first visit asks you to create a user; this first account gets superuser rights. Enter a username, an optional email and a password (twice), then click **Sign up**. You land on the dashboard, with a welcome message and a button for a quick tour.

## Step 5: Add documents (feature 1)
Click **Upload** at the top, or drop files anywhere in the window. A panel shows each one being processed, and a few seconds later they are added. Click **Documents** in the sidebar to see them, each with a preview and the date Paperless read from the page.

Sample documents to follow along: see [Sample data](#sample-data). In the video: the October electricity invoice, the internet bill, the hardware receipt, the dentist letter and the insurance renewal.

## Step 6: The consume folder (feature 2)
The official compose bind-mounts `./consume` next to your compose file. Anything you copy there is picked up automatically, which is handy for a scanner. Copy an image-only scan into it:
```bash
cp ~/samples/oakridge-boiler-service-scan.pdf consume/
```
(Adjust the path to wherever your sample files are.) Paperless notices the file, runs OCR because the scan has no text layer, and the new document appears in the browser. Click **Open document**, then the **Content** tab to see the recognised text.

## Step 7: Search (feature 3)
Click the search bar at the top and type a word that only appears inside the scan, for example `burner`. Paperless finds it because it searches the recognised text. Click **Search** for the full results page (the document list filtered to the matches). Click **Reset filters** to show everything again.

## Step 8: Automatic sorting with matching rules (feature 4)
1. Open **Correspondents** in the sidebar and click **Create**. Name it `Brightwater Utilities`, set the matching algorithm to **Any**, type `Brightwater` as the match, and click **Save**.
2. Open **Document types**, click **Create**, name it `Invoice`, choose **Any**, type `invoice`, and click **Save**.

From now on, new documents containing those words get these labels automatically.

Test it by copying two new bills into the consume folder:
```bash
cp ~/samples/*-november.pdf consume/
```
Within seconds both appear already labelled `Invoice`, and the electricity bill is linked to Brightwater Utilities.

## Step 9: Saved views (feature 5)
In **Documents**, open the **Document type** filter and pick **Invoice**. Click **Views**, then **Save as...**. Name it `Invoices`, tick **Show on dashboard**, and click **Save**. Your Invoices list now appears on the **Dashboard**.

## Step 10 (optional): Turn on AI with a local model (feature 6)
AI is off by default. You need an Ollama server reachable from the Paperless container (the video used the `qwen3:14b` model on another machine on the network).
1. Open **Configuration**, then the **AI Settings** tab.
2. Switch AI on.
3. Set the embedding backend to **huggingface**, so the search index is built locally.
4. Set the LLM backend to **ollama**, type the model name (for example `qwen3:14b`) and the Ollama address (for example `http://<ollama-host>:11434`).
5. Click **Save**.

## Step 11 (optional): Ask your documents a question
Click the chat icon at the top and ask in plain words, for example:
```
When does my car insurance renew, and what's the yearly premium?
```
With the sample documents, the answer was 1 December 2026 and $660, with links to the documents it used.

## Sample data
`sample-data/` contains generators for the made-up documents used above (all names, companies and amounts are fictional):
```bash
cd sample-data
python3 make_samples.py   # 7 invoices/letters -> samples/*.pdf (needs Chromium or Chrome; otherwise print the HTML to PDF)
python3 make_scan.py      # image-only scan for OCR -> samples/oakridge-boiler-service-scan.pdf (needs: pip install pillow)
```

## Troubleshooting and tips
- Files stuck in the consume folder? Set `USERMAP_UID` and `USERMAP_GID` in `docker-compose.env` to match your own user (`id -u`, `id -g`).
- Scans saved on a network share often do not send file events; turn on polling (`PAPERLESS_CONSUMER_POLLING`, see the configuration docs).
- Documents not in English? Set the OCR language (`PAPERLESS_OCR_LANGUAGE`).
- For backups, use the built-in document exporter (see the administration docs), not just a copy of the containers.

## Limits and costs
- Free and open source (GPL-3.0).
- AI is optional and off by default; classic matching works without it.
- A remote AI model sends your document text to that provider. Prefer a local model, which needs a strong computer.
- The project is run by volunteers: check the docs and release notes before every upgrade.

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
```

## Official links
- Setup: https://docs.paperless-ngx.com/setup/
- Usage: https://docs.paperless-ngx.com/usage/
- AI features: https://docs.paperless-ngx.com/advanced_usage/#ai-features
- Configuration: https://docs.paperless-ngx.com/configuration/
- Administration (exporter, backups): https://docs.paperless-ngx.com/administration/
- Compose files: https://github.com/paperless-ngx/paperless-ngx/tree/main/docker/compose
- Source code: https://github.com/paperless-ngx/paperless-ngx
- Licence: GPL-3.0 (https://github.com/paperless-ngx/paperless-ngx/blob/main/LICENSE)
- Releases: https://github.com/paperless-ngx/paperless-ngx/releases

---
Not affiliated with or endorsed by the Paperless-ngx authors. "Paperless-ngx" is used only to describe the software.
