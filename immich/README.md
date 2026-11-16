# Immich

Immich is a self-hosted home for your photos and videos: a timeline, albums, a map and smart search, with phone apps for automatic backup.
In this guide you install it with Docker Compose, upload photos, search them by describing what is in them, and share an album with a link.

> Tested with Immich v3 (the release line set by the official `example.env`, `IMMICH_VERSION=v3`) on 2026-11-16.
> Video: coming soon

## Requirements
- A 64-bit Linux machine is recommended. Mac and Windows work through Docker Desktop, but the official docs discourage them.
- At least 6 GB of RAM and 2 CPU cores (8 GB and 4 cores recommended).
- Docker with the Compose plugin (`docker compose`, with a space).
- Disk space for your photos, plus about 10-20% extra for thumbnails and video copies.
- No account and nothing to pay.

Immich runs as four containers: `immich_server` (the web app on port 2283, stores your uploads), `immich_machine_learning` (local AI models for smart search and face recognition), `immich_postgres` (the database) and `immich_redis` (Valkey, the queue for background jobs such as thumbnails).

## Step 1: Download the official files
Make a folder, step into it, and download the compose file and the example environment file from the latest release.
```bash
mkdir immich-app
cd immich-app
wget -O docker-compose.yml https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
wget -O .env https://github.com/immich-app/immich/releases/latest/download/example.env
```

## Step 2: Set the database password
Open `.env` in an editor. It sets where your photos (`UPLOAD_LOCATION`) and the database (`DB_DATA_LOCATION`) are stored, and the database password.
```bash
nano .env
```
Change the `DB_PASSWORD` line to your own password, using only letters and numbers (`A-Za-z0-9`, no special characters or spaces):
```
DB_PASSWORD=CHANGE_ME_letters_and_numbers_only
```
One way to generate one: `openssl rand -hex 24`. Save and exit (in nano: Ctrl+O, Enter, Ctrl+X).

## Step 3: Start Immich
```bash
docker compose up -d
```
Docker pulls the images for the server, machine learning, Valkey and Postgres (a few minutes the first time), then creates and starts the containers. Check them:
```bash
docker compose ps --format "table {{.Name}}\t{{.Status}}"
```
Expected output (right after start; the health status turns to `healthy` after a short while):
```
NAME                      STATUS
immich_machine_learning   Up 2 seconds (health: starting)
immich_postgres           Up 2 seconds (health: starting)
immich_redis              Up 2 seconds (health: starting)
immich_server             Up Less than a second (health: starting)
```

## Step 4: Create the admin account
1. Open http://localhost:2283 and click **Getting Started**.
2. The first user becomes the admin. Enter an email, a password (twice) and your name, then click **Sign up**.
3. Log in with the same details.
4. A short setup wizard follows: theme, language, then privacy. The map uses an outside map tile service; you can switch that off here. Then storage template, backups and the mobile app. Click **Done**.

## Step 5: Upload photos (feature 1)
Click **Upload** (top right) and pick some photos. Immich reads the date inside each file and builds a timeline, newest first, grouped by day. Scroll through the days, or use the bar on the right to jump between months and years.

## Step 6: Photo details (feature 2)
Click a photo to open it, then click the **Info** button: date and time, file name and size, and the place (worked out from the photo's location) with a small map. Press the right arrow for the next photo, click the heart to add it to your favorites, and press Escape to go back.

## Step 7: Smart search (feature 3)
Click the search bar and describe what you want in plain words, for example `a red bicycle`, and press Enter. Matching photos come first even when no file name or tag contains the word. Try another, like `a dog on the beach`. This runs on your own server: after upload, the machine learning container analyses every photo with a CLIP model.

## Step 8: Map (feature 4)
Click **Map** in the sidebar. Every photo with a location appears, grouped into clusters with a count. Zoom in and the clusters split up by place. Click a cluster to open a side panel with the photos from that part of the map.

## Step 9: Places (feature 5)
Click **Explore**. Immich groups photos by the town or city where they were taken, using the GeoNames place database on your own server. Click **View All** to see every place, then click one to see only the photos from there.

## Step 10: Albums (feature 6)
Open **Albums** and click **Create album**. Type a title, click **Select photos**, pick the photos and click **Add assets**. The album shows the dates it covers and how many items it holds.

## Step 11: Share an album with a link (feature 7)
In the album, click the share icon, then **Create link**. You can set a custom URL, a password and an expiry (for example "in 7 days"). Click **Create link** to get the link and a QR code. Anyone with the link can view the album without an account.

## Step 12: Phone app (from the official quick start)
1. Install the Immich app from the App Store, Google Play or F-Droid.
2. Log in with your server's address: its IP and port 2283 (for example `http://192.168.1.10:2283`).
3. Tap the cloud icon at the top right, choose the albums to back up, and tap **Enable Backup**.

New photos then upload by themselves, though background backup depends on your phone's battery rules.

## Troubleshooting and tips
- Use `docker compose` (with a space). The old `docker-compose` command is no longer supported.
- Back up both your photo folder (`UPLOAD_LOCATION`) and the database. Immich makes a database backup every night, but it does not contain your photos.
- Plan disk space: thumbnails and video copies add about 10-20%.
- Only 4 GB of RAM? Run it with machine learning turned off.
- Use the compose file from the current release (the link above), not the one from the `main` branch, which may not match the release.

## Limits and costs
- Free and open source (AGPL-3.0). You can buy an optional licence to support the team; the project promises no paywalls.
- Immich is not a backup. The project says you still need a 3-2-1 backup of your photos.
- Almost everything stays on your server: map tiles and the version check use outside services, and both can be switched off.
- Reaching Immich from outside your home network is up to you to set up safely.

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
```
Your photos and database live in the folders set by `UPLOAD_LOCATION` and `DB_DATA_LOCATION` (by default `./library` and `./postgres`); delete those only if you want to remove everything.

## Official links
- Docs: https://docs.immich.app/overview/quick-start
- Docker Compose install: https://docs.immich.app/install/docker-compose
- Requirements: https://docs.immich.app/install/requirements
- Smart search: https://docs.immich.app/features/searching
- Sharing: https://docs.immich.app/features/sharing
- Backup and restore: https://docs.immich.app/administration/backup-and-restore
- FAQ: https://docs.immich.app/FAQ
- Supporting the project: https://docs.immich.app/overview/support-the-project
- Source code: https://github.com/immich-app/immich
- Licence: AGPL-3.0 (https://github.com/immich-app/immich/blob/main/LICENSE)
- Releases: https://github.com/immich-app/immich/releases

---
Not affiliated with or endorsed by the Immich authors. "Immich" is used only to describe the software.
