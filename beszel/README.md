# Beszel

Beszel is a lightweight, open-source server monitoring tool: a hub (web dashboard, built on PocketBase) plus a small agent on each machine.
In this guide you install the hub and a local agent with Docker Compose, connect your first system, explore the charts and per-container stats, set up an alert, watch it fire, and add a notification URL.

> Tested with Beszel 0.21.2 on 2026-11-16.
> Watch the video: https://youtu.be/OFU6p_-CXCc

## Requirements
- A Linux machine (small server, home lab box or virtual machine)
- Docker and Docker Compose, installed and running
- A web browser
- No account and nothing to pay (MIT licence)

## Step 1: Write the compose file and start Beszel
Make a folder, create `docker-compose.yml` and paste in the official file from the Beszel docs. It runs two containers: the hub on port 8090 and an agent for the same machine. The file in this folder is that official file with the image tags pinned to the tested version.

```bash
mkdir beszel
cd beszel
nano docker-compose.yml     # paste the file, save with Ctrl+O, Enter, exit with Ctrl+X
docker compose up -d
```
Expected output (abridged):
```
 Network beszel_default  Created
 Container beszel        Started
 Container beszel-agent  Started
```
Leave `TOKEN: <token>` and `KEY: "<key>"` as they are for now; you fill them in at Step 3.

## Step 2: Create the admin account
Open http://localhost:8090. On the first visit Beszel asks you to create an admin account. Enter your email address, a password of at least 8 characters, confirm it and click **Create account**. You land on the empty **All Systems** dashboard.

## Step 3: Connect your first system
1. Click **Add System** (top right) and stay on the **Docker** tab.
2. Name: `my-server`.
3. Host / IP: `/beszel_socket/beszel.sock` (the socket path from the docs, because hub and agent run on the same machine).
4. Copy the **Public Key** and the **Token** from the dialog and paste them into the compose file:
   ```bash
   nano docker-compose.yml
   ```
   Replace `"<key>"` with the key (keep the quotes) and `<token>` with the token. Save and exit.
5. Recreate the agent:
   ```bash
   docker compose up -d
   ```
6. Back in the browser, click **Add System** in the dialog. `my-server` appears in the list and its dot turns green as soon as the first numbers arrive (usually within a minute).

## Step 4: Feature one - the dashboard
**All Systems** shows one row per machine, updated in real time: CPU, memory, disk and network use, each with a bar that changes colour as it fills up.
- Type in the **Filter...** box to find a system.
- Use the column menu to choose which columns are shown.
- Click the system name to open its page.

## Step 5: Feature two - the system page and per-container charts
- Header: status, operating system, uptime and processor.
- Charts: CPU usage, memory, disk usage, disk I/O and bandwidth.
- **Docker CPU Usage** and **Docker Memory Usage**: every container is its own coloured band. Hover over a chart to see each container's value at that moment.
- The menu at the top right switches the time range (1 hour, 12 hours, a week, 30 days).

Tip: let the hub run for a while so the charts have some history.

## Step 6: Feature three - all containers in one list
Click the containers icon in the top bar to open **All Containers**. Each row shows a container, the system it runs on, its CPU, memory and network use, health and status. Click a column header such as **Memory** to sort.

## Step 7: Feature four - set up an alert
1. Back on the dashboard, click the bell icon on the `my-server` row. The **Alerts** panel opens.
2. Switch on **CPU Usage** and set it to "Average exceeds 20%" for 1 minute.
3. Switch on **Status**, so you hear about it if the machine goes down.
4. Changes save right away. Close the panel.

## Step 8: Watch the alert fire
Start a throwaway container that keeps the processor busy:
```bash
docker run -d --rm --name busy --cpus 10 alpine sh -c 'for i in $(seq $(nproc)); do (while :; do :; done) & done; wait'
```
Within a couple of minutes the CPU bar climbs and an **Active Alerts** banner appears ("Exceeds 20% in last 1 minute"). Click **View alerts** to see which rule fired. Then stop the load:
```bash
docker stop busy
```
Every alert is also recorded under **Settings > Alert History**.

Note: `--cpus 10` caps the container at 10 cores. On a machine with fewer cores Docker refuses a value above your core count; lower it (for example `--cpus 2`) or remove it.

## Step 9: Feature five - get notified
Open **Settings > Notifications**.
- **Email notifications**: type addresses here; this needs a mail server (SMTP) configured in the hub.
- **Webhook / Push notifications**: click **Add URL** and enter a notification URL for a service such as Discord, Telegram, Gotify or ntfy. For a self-hosted ntfy server the format is like `ntfy://ntfy.example.com/your-topic` (add `?scheme=http` if your server has no HTTPS). See the notification docs linked below for each service's URL format.
- Click **Test URL**; you should see "Test notification sent" and the message arrives in your service.
- Click **Save Settings**.

## Troubleshooting and tips
- Hub and agent on the same machine: use the Unix socket (`/beszel_socket/beszel.sock`), as in this guide. `localhost` does not work between the two containers.
- System stays red: check your firewall, and the logs in the hub's admin panel (PocketBase admin, at http://localhost:8090/_/).
- Empty container charts: run `docker stats`. If it shows zero memory, the Common issues page links a fix.
- Wrong disk shown: set the `FILESYSTEM` environment variable on the agent (see Common issues / agent docs).
- More: https://beszel.dev/guide/common-issues

## Limits and costs
- Free and open source (MIT).
- Pre-1.0 software (0.21 at the time of the video): expect changes between releases.
- Alerts do not reach you by themselves: you need a mail server or a push/webhook service.
- Mainly maintained by one developer.
- Not built for logs, traces, or deep analysis of a huge fleet.
- Only install agents on machines you own or manage.

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
```
Data lives in the `beszel_data`, `beszel_agent_data` and `beszel_socket` folders next to the compose file; delete them to remove everything.

## Official links
- Docs: https://beszel.dev/guide/getting-started
- Hub installation: https://beszel.dev/guide/hub-installation
- Notifications: https://beszel.dev/guide/notifications/
- Common issues: https://beszel.dev/guide/common-issues
- Source code: https://github.com/henrygd/beszel
- Licence: MIT (https://github.com/henrygd/beszel/blob/main/LICENSE)
- Releases: https://github.com/henrygd/beszel/releases
- Images: https://hub.docker.com/r/henrygd/beszel and https://hub.docker.com/r/henrygd/beszel-agent

---
Not affiliated with or endorsed by the Beszel authors. "Beszel" is used only to describe the software.
