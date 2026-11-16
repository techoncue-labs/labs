# Jellyfin

Jellyfin is a free media server: think of it as your own private streaming service. You point it at folders of video files, and it turns them into a library with posters, descriptions and progress tracking that you can stream to a browser, a phone or a TV.
In this guide you install it with Docker Compose, add Movies and Shows libraries, play a film with subtitles, browse a TV show, set up a family account with parental limits, and see where transcoding fits in.

> Tested with Jellyfin 12.4.0 on 2026-11-16.
> Video: coming soon

## Requirements
- A Linux machine (home server or virtual machine) with Docker and Docker Compose.
- Your own video files (movies, shows, home videos), or the made-up test media from [Sample data](#sample-data).
- A web browser.
- No account with anyone and nothing to pay.
- Optional: a graphics card. It only helps with transcoding.

How it works: your movies and shows sit in folders on the server. Jellyfin scans them, reads the names, and adds details and artwork, either from info files (NFO) next to the videos or from online databases. Then any app can play them. If a device can play the file as it is, Jellyfin streams it directly. If not, it converts it on the fly (transcoding).

## Step 1: Make a folder and add your videos
Make a folder called `jellyfin`, step into it, and copy your videos into a folder called `media`. The video uses a `Movies` and a `Shows` folder.
```bash
mkdir jellyfin && cd jellyfin
cp -r ~/my-videos media
ls media
```
(Adjust `~/my-videos` to wherever your videos are.) Expected output:
```
Movies  Shows
```

## Step 2: Write the compose file
```bash
nano docker-compose.yml
```
Paste the setup from the official docs, trimmed to the basics: the `jellyfin/jellyfin` image, port 8096, a config folder, a cache folder, and the media folder mounted read only. The same file is in this folder as [compose.yaml](compose.yaml).
```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin:12.4
    container_name: jellyfin
    ports:
      - 8096:8096/tcp
    volumes:
      - ./config:/config
      - ./cache:/cache
      - type: bind
        source: ./media
        target: /media
        read_only: true
    restart: unless-stopped
```
The video uses the plain `jellyfin/jellyfin` image (latest, which was 12.4.0 at the time). The `:12.4` tag above keeps you on the tested release; Docker Hub has no `12.4.0` tag. Save and exit (in nano: Ctrl+O, Enter, Ctrl+X).

## Step 3: Start Jellyfin
```bash
docker compose up -d
```
The first time, Docker also downloads the image (about 1.7 GB).

## Step 4: The setup wizard
1. Open http://localhost:8096 and the setup wizard starts.
2. Give your server a name (the video uses `Home Media`), keep English, and click **Next**.
3. Create your admin account: a username and a password, typed twice. Click **Next**.

## Step 5: Add your libraries
1. Click **Add Media Library** and choose the content type **Movies**.
2. Click the **+** next to **Folders**, open `/media`, pick `Movies`, and click **OK**.
3. Jellyfin normally fetches posters and details from online databases. Files that bring their own posters and NFO info files (like the sample media) use those. Click **OK**.
4. Do the same for Shows: **Add Media Library**, content type **Shows**, **+**, `/media`, `Shows`, **OK**, and **OK**.

Both libraries now appear in the list.

## Step 6: Finish and sign in
1. Click **Next**. Keep the metadata language (English) and click **Next**.
2. **Allow remote connections** means devices outside your home network. Leave it on, or switch it off if you only watch at home. Click **Next**, then **Finish**.
3. Sign in with the account you just made. You land on your home screen.

## Step 7: Browse your library (feature 1)
The home screen shows **My Media** at the top, and your recently added movies, each with its poster. Click a film (in the video: **The Lantern Keeper**). The details page shows the year, the length, the rating (PG), the video and audio format, an English subtitle file that Jellyfin found next to the video, and the plot from the info file.

## Step 8: Play, with subtitles (feature 2)
1. Click **Play**. The film starts in the browser, and the subtitles from the `.srt` file are already on.
2. Open the subtitles menu to switch them **Off**, or back on (**English**).
3. Open the settings and choose **Playback Info**. It says **Direct playing**: the browser can handle the file as it is, so nothing needs converting.

## Step 9: TV shows (feature 3)
Open **Shows** and click a show (in the video: **Garden Robots**). You get the show's rating, its description and a **Next Up** episode. Scroll down to the seasons and open **Season 1** to see every episode, each with its own picture and summary.

## Step 10: Family accounts (feature 4)
1. Open the user menu, then **Dashboard**, then **Users**, and click the **+** to add a user.
2. Call it `Kids`, give it a password, and tick the **Movies** and **Shows** libraries. Click **Save**.
3. Open the **Parental Control** tab and set the maximum allowed rating to **PG/TV-PG**. Click **Save**.

## Step 11: See the limits work
Sign out and sign in as `Kids`. With the sample media, only two films are left: **Captain Pebble** (G) and **The Lantern Keeper** (PG). The PG-13 and R films are hidden, and the **Garden Robots** show (TV-Y) is still there.

## Step 12: The dashboard and transcoding (feature 5)
Sign in as the admin again and open the **Dashboard**. It shows your server version, how many movies and episodes you have, connected devices, and recent activity.
Under **Playback**, open **Transcoding**. If your server has a graphics card, you can turn on hardware acceleration here (NVIDIA, Intel, AMD and others are on the list). It needs extra setup from the hardware acceleration docs, so the video leaves it at **None**; the sample films play directly anyway.

## Apps for every screen
The official apps cover Android and iPhone/iPad, Android TV and Fire TV, Roku, LG (webOS) and Samsung (Tizen) smart TVs, and Xbox, plus a Kodi add-on. Sign in with your server's address (for example `http://<server-ip>:8096`) and your user, and your libraries and watch progress come with you.

## Sample data
`sample-data/make_media.py` creates the made-up media used above: four short films (Captain Pebble G, The Lantern Keeper PG, Comet Relay PG-13, Midnight Circuit R) and the show Garden Robots (TV-Y, one season, three episodes), with our own posters, NFO info files and one English subtitle file. All titles and stories are fictional.
```bash
pip install pillow                      # also needs ffmpeg 6.1+ and the DejaVu fonts (Debian/Ubuntu: sudo apt install ffmpeg fonts-dejavu-core)
python3 sample-data/make_media.py ~/my-videos   # -> ~/my-videos/Movies, ~/my-videos/Shows (about 40 MB)
```
Then follow Step 1. The clips are VP9/Opus `.webm` files, so a normal browser plays them directly.

## Troubleshooting and tips
- Name your files the Jellyfin way: the movie title with the year in brackets (`The Lantern Keeper (2024)`), and episodes as `S01E01`. Then matching just works.
- Library looks empty? Check that the folder is mounted into the container (`/media`) and readable.
- Want to watch away from home? Put Jellyfin behind a reverse proxy with HTTPS, as the networking docs describe.
- Backups: use the **Backups** page in the dashboard, or keep a copy of the `config` folder, which holds your users, watch history and settings.

## Limits and costs
- Free and open source (GPL-2.0), with no paid tier.
- It only plays files you already have; it does not come with movies.
- Not every file plays on every device. When a device can't handle a format, the server has to transcode, and that needs a strong processor or a graphics card.
- The project is run by volunteers: read the release notes before you upgrade.

## Clean up
```bash
docker compose down
```
Your settings live in `./config` and `./cache`; delete those only if you want to start over. Your videos in `./media` are mounted read only and are not changed.

## Official links
- Container install: https://jellyfin.org/docs/general/installation/container/
- Movies (naming): https://jellyfin.org/docs/general/server/media/movies/
- Shows (naming): https://jellyfin.org/docs/general/server/media/shows/
- Users: https://jellyfin.org/docs/general/server/users/
- Hardware acceleration: https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/
- Networking (reverse proxy): https://jellyfin.org/docs/general/post-install/networking/
- Apps: https://jellyfin.org/downloads/clients/
- Source code: https://github.com/jellyfin/jellyfin
- Licence: GPL-2.0 (https://github.com/jellyfin/jellyfin/blob/master/LICENSE)
- Releases: https://github.com/jellyfin/jellyfin/releases

---
Not affiliated with or endorsed by the Jellyfin authors. "Jellyfin" is used only to describe the software.
