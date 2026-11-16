# n8n

n8n is a workflow automation tool: you connect nodes (each does one job, like fetching data, checking a rule or asking an AI model) into workflows on a visual canvas.
In this guide you run it with Docker, build a first workflow (HTTP Request, If, Edit Fields), start a workflow from a webhook, and add an AI step with a free local model through Ollama.

> Tested with n8n 2.47.7 (image `docker.n8n.io/n8nio/n8n`) and Ollama (`ollama/ollama`) with `llama3.2` on 2026-11-16.
> Video: coming soon

## Requirements
- A computer with Docker installed (Linux, Mac or Windows).
- A few GB of free RAM for the small AI model (about 2 GB download).
- A web browser.
- No cloud sign-up and no API key: the owner account lives only in your own instance. Self-hosting is free under n8n's Sustainable Use License.

How it works: every workflow starts with a trigger (a click, a schedule or a web request). Data then flows from node to node as a list of items. You can run any single step and see exactly what goes in and what comes out.

## Step 1: Start n8n
Create a volume for your workflows and credentials, then run the official Docker command.
```bash
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```
Docker downloads the image and starts n8n. To stay on the version tested here, use `docker.n8n.io/n8nio/n8n:2.47.7`. Leave this terminal open.

Expected output (end of the log):
```
Version: 2.47.7
...
Editor is now accessible via:
http://localhost:5678
```

## Step 2: Set up the owner account
1. Open http://localhost:5678.
2. Enter an email, first name, last name and a password (at least 8 characters, one number and one capital letter). Click **Next**.
3. The short survey is optional: click **Get started**.
4. The offer of a free licence key for a few extra features can be skipped: click **Skip**.
5. You land on the n8n Assistant (an optional AI helper). Click **Overview** instead and close the banners at the top.

## Step 3: Your first workflow (feature 1)
The video uses a small made-up bakery orders API. To follow along, run the one in `sample-data/` (see [Sample data](#sample-data)).
1. Click **Build a workflow**.
2. Click **Add first step**, type `manual` and pick **Trigger manually**.
3. Click the **+** next to it, type `HTTP Request` and press Enter.
4. Paste the URL of the orders API, for example `http://host.docker.internal:8000/orders`.
5. Click **Execute step**. Six orders come back, shown as a table.

## Step 4: Make a decision with an If node (feature 2)
1. Close the panel, click the **+** again and add an **If** node.
2. From the input on the left, drag the `total` column into the first value. n8n writes the expression for you.
3. Open the operator menu, choose **Number**, then **is greater than**, and type `20`.
4. Click **Execute step**. Three big orders go to the **true** branch and three small ones to the **false** branch.

## Step 5: Shape the data with Edit Fields (feature 3)
1. Click the **+** on the true branch and add **Edit Fields**.
2. Drag in `customer`, then `total`.
3. Click **Add Field**, name it `next_step`, and set the value to `Call to confirm the order`.
4. Execute the step: every big order now carries that note.
5. Close the panel and click **Execute workflow**. The counts on each connection show the items flowing: 6, then 3 and 3.
6. Rename the workflow to `Big orders`.

## Step 6: Start a workflow from outside with a webhook (feature 4)
1. Click the **+** at the top left and choose **New workflow**.
2. Add a first step, type `webhook` and press Enter.
3. Set **HTTP Method** to `POST`, **Path** to `feedback`, and **Respond** to **When Last Node Finishes**, so the caller gets the result.
4. Click **Listen for test event**.
5. In a second terminal, send a test message:
```bash
curl -X POST http://localhost:5678/webhook-test/feedback -H 'Content-Type: application/json' -d '{"message": "The sourdough was amazing, but delivery was two hours late."}'
```
n8n answers, and the editor shows the message that just arrived.

## Step 7: Run Ollama next to n8n
As the n8n docs suggest, put both containers on one Docker network, then start Ollama on it and pull a small model (`llama3.2`, about 2 GB).
```bash
docker network create n8n-net
docker network connect n8n-net n8n
docker run -d --name ollama --network n8n-net -v ollama:/root/.ollama ollama/ollama
docker exec ollama ollama pull llama3.2
```
No API key is needed, and your messages stay on your machine.

## Step 8: The AI step (feature 5)
1. Back in n8n, close the webhook panel and add a **Basic LLM Chain** after the Webhook.
2. Set **Source for Prompt** to **Define below** and type the question, for example: `Is this customer message positive or negative? Answer in one short sentence. Message: `
3. Drag `message` (under `body`) from the webhook input to the end of the prompt.
4. Under **Model**, click the **+** and choose **Ollama Chat Model**.
5. Create the credential: set the Base URL to `http://ollama:11434` (the container name, not localhost) and click **Save**. The model `llama3.2` is picked.
6. Close the panel, click **Execute workflow**, and send another message from the second terminal:
```bash
curl -X POST http://localhost:5678/webhook-test/feedback -H 'Content-Type: application/json' -d '{"message": "The croissants were stale and my order arrived an hour late."}'
```
A few seconds later the local model's answer comes back, for example "The customer message is negative."

## Step 9: Publish and use the production URL (feature 6)
Click **Publish** and confirm. The production URL now works without the editor open. Call it without `-test` in the path:
```bash
curl -X POST http://localhost:5678/webhook/feedback -H 'Content-Type: application/json' -d '{"message": "The birthday cake was perfect, everyone loved it!"}'
```
Expected output (the model's wording can vary):
```
{"text":"The message is positive."}
```
Open the **Executions** tab to see every run with its status and time.

## Sample data
`sample-data/` contains a made-up bakery orders API (Python 3, no dependencies) for Step 3:
```bash
python3 sample-data/bakery_api.py    # serves http://<your machine>:8000/orders
```
From inside the n8n container, `localhost` is the container itself. Use `http://host.docker.internal:8000/orders`; on Linux, add `--add-host=host.docker.internal:host-gateway` to the `docker run` in Step 1 (Docker Desktop on Mac and Windows provides it automatically). Alternatively use your machine's LAN IP.

## Troubleshooting and tips
- Keep the `n8n_data` volume: your workflows and credentials live there.
- n8n cannot reach Ollama? Put both containers on the same network and use the container name (`http://ollama:11434`), not `localhost`.
- Webhook silent? The test URL (`/webhook-test/...`) only works while the editor is listening. Publish the workflow to use the production URL (`/webhook/...`).
- To update, pull the new image (`docker pull docker.n8n.io/n8nio/n8n`) and start the container again.

## Limits and costs
- n8n is fair-code, not open source: under the Sustainable Use License it is free for your own and your company's internal use, but you cannot resell it as a service.
- Some features need a free licence key, and enterprise features need a paid plan.
- A small local model is slower and simpler than large cloud models.
- When you self-host, updates and backups are your job.

## Clean up
Stop n8n with Ctrl+C in its terminal (the `--rm` flag removes the container; your data stays in the volume). Then:
```bash
docker rm -f ollama
docker network rm n8n-net
docker volume rm n8n_data ollama   # only if you want to delete your workflows and the model too
```

## Official links
- Docker install: https://docs.n8n.io/hosting/installation/docker/
- Ollama credentials: https://docs.n8n.io/integrations/builtin/credentials/ollama/
- Sustainable Use License: https://docs.n8n.io/sustainable-use-license/
- Source code: https://github.com/n8n-io/n8n
- Licence: Sustainable Use License (not an SPDX-listed licence; source-available "fair-code") (https://github.com/n8n-io/n8n/blob/master/LICENSE.md)
- Releases: https://github.com/n8n-io/n8n/releases
- Ollama: https://github.com/ollama/ollama

---
Not affiliated with or endorsed by the n8n authors. "n8n" is used only to describe the software.
