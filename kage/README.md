# kage

kage renders each page of a website in headless Chrome, strips all JavaScript and saves the page plus its styles, images and fonts as an offline copy that runs no code.
In this guide you use the official Docker image to copy two small public sites, browse the copies, resume and scope a crawl, and pack a mirror into a single file.

> Tested with kage 0.3.12 on 2026-11-16.
> Video: https://youtu.be/YPXyf7kizn8

## Requirements
- Docker (the official image already bundles Chromium)
- Internet access to make a copy (not to read it)
- A web browser
- No account; free and open source (MIT)

Alternatives to Docker: Homebrew, Scoop, apt and dnf repositories, a .deb file, or `go install`. Those need Chrome or Chromium installed on the machine. See the installation docs.

## Step 1: Pull the official image
```bash
docker pull ghcr.io/tamnd/kage
docker run --rm ghcr.io/tamnd/kage --version
docker run --rm ghcr.io/tamnd/kage --help
```
Expected output:
```
kage version 0.3.12
```
`--help` lists the commands, including the four you will use most: `clone`, `serve`, `pack` and `open` (plus `parquet`, `completion`, `help`).

## Step 2: Your first copy
`example.com` is a domain reserved for examples, so it is safe to copy.
```bash
mkdir out
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage clone example.com
ls out/data/kage/example.com
```
Expected output:
```
kage cloning https://example.com/
kage: container detected, Chrome sandbox disabled
done /out/data/kage/example.com
  pages 1   assets 0
  open kage serve /out/data/kage/example.com
_kage  index.html
```
Inside the container the mirror lands in `/out/data/kage/<host>`, which is `./out/data/kage/<host>` on your machine. Trust the `done ...` line if the path differs. `_kage` holds assets and crawl state.

## Step 3: Open the copy
Serve the mirror. Publish port 8800 and tell kage to listen on every address inside the container so your browser can reach it:
```bash
docker run --rm -p 8800:8800 -v "$PWD/out:/out" ghcr.io/tamnd/kage serve /out/data/kage/example.com --addr 0.0.0.0:8800
```
Open http://localhost:8800 to see the Example Domain page, loaded from your disk. Press **Ctrl+C** in the terminal to stop.

## Step 4: Copy a docs site, with limits
Copy kage's own documentation site, starting with a small taste:
```bash
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage clone kage.tamnd.com --max-pages 8 --max-depth 2
```
kage reads the site's robots file, seeds itself from the sitemap and crawls breadth first. Expected output (end):
```
sitemap: seeded 7 URLs
...
done /out/data/kage/kage.tamnd.com
  pages 8   assets 5
  open kage serve /out/data/kage/kage.tamnd.com
```
Page and asset counts depend on the live site.

## Step 5: Browse the docs offline
```bash
docker run --rm -p 8800:8800 -v "$PWD/out:/out" ghcr.io/tamnd/kage serve /out/data/kage/kage.tamnd.com --addr 0.0.0.0:8800
```
Open http://localhost:8800. Same layout, fonts and colours as the live site. Click **Getting started > Installation**, then **Guides > Scoping a crawl**: links that were in scope open saved pages. Press **Ctrl+C** to stop.

## Step 6: Proof that the scripts are gone
```bash
curl -s https://kage.tamnd.com/ | grep -c "<script"
grep -c "<script" out/data/kage/kage.tamnd.com/index.html
```
Expected output (the live count can change):
```
3
0
```
`grep -c` exits with status 1 when it finds nothing; that is expected here.

## Step 7: Resume and refresh
Run the same clone without the page limit. kage reports what is already done and picks up the rest, without fetching pages twice:
```bash
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage clone kage.tamnd.com
```
Expected output (start):
```
resume: 8 pages already done
resume: picking up 7 pages
```
You can press **Ctrl+C** at any time; kage saves its place and the next run continues. Two related flags:
```bash
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage clone kage.tamnd.com --help | grep -E "refresh|force"
```
```
    -f --force     Delete any existing mirror for the host first
    --refresh      Re-Render every page in place to pull in changed content
```

## Step 8: Copy just one section
Limit the crawl to a path prefix and write it to a separate output folder:
```bash
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage clone kage.tamnd.com --scope-prefix /guides -o /out/guides-only
ls out/guides-only/kage.tamnd.com out/guides-only/kage.tamnd.com/guides
```
Expected output:
```
out/guides-only/kage.tamnd.com:
_kage  guides  index.html

out/guides-only/kage.tamnd.com/guides:
index.html  packing-a-mirror  resuming-a-run  scoping-a-crawl  serving-a-mirror
```
kage still fetches the styles and images those pages need, plus the start page it began from. To skip parts instead, use `--exclude` (repeatable).

## Step 9: Pack it into one file
```bash
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage pack kage.tamnd.com
docker run --rm -v "$PWD/out:/out" ghcr.io/tamnd/kage pack kage.tamnd.com --format binary -o kage-docs
ls -lh out/*.zim out/kage-docs
```
Expected output (sizes vary):
```
packed kage.tamnd.com.zim
  size 1012.3 KiB
  open kage open kage.tamnd.com.zim
packed kage-docs
  size 24.6 MiB
  run ./kage-docs to view the site offline
```
The first command writes a ZIM file (the open offline format used by Kiwix). The second writes one self-contained program that is the site; it is larger because it carries a copy of kage.

## Step 10: Open the packed file
```bash
docker run --rm -p 8800:8800 -v "$PWD/out:/out" ghcr.io/tamnd/kage open kage.tamnd.com.zim --addr 0.0.0.0:8800 --open=false
```
Open http://localhost:8800: the same docs, served from the single ZIM file. `--open=false` turns off the automatic browser launch, which does not work inside a container. The same file also opens in Kiwix on desktop or phone. Press **Ctrl+C** to stop.

## More options worth knowing
- `--scroll`: scrolls each page so lazy-loaded images are saved too.
- `--subdomains`: also follows subdomains (for example a blog or docs subdomain).
- `--workers`: how many pages render at once (4 by default).
- `--crawl-delay`: spaces out page loads, to be gentle with the site.
- `clone --help` lists the rest.

## Troubleshooting and tips
- Images missing further down the page: the site loads them as you scroll; add `--scroll`.
- Links break when you open the files directly: some sites use root-relative links; use `kage serve` instead of opening the HTML files.
- Fewer pages than `--max-pages`: the limit counts queued addresses, and pages that fail or are blocked by robots rules still use a slot.
- Files in `out/` are created by the container and may be owned by root; use `sudo rm -rf out` to delete them if needed.

## Limits and costs
- Free (MIT); ZIM files also open in Kiwix, so you are not locked in.
- A copy is a snapshot: anything that needed JavaScript, such as a live search box, does not work.
- ZIM packs have title search but no full-text search index.
- Making a copy needs Chrome/Chromium or the Docker image.
- Early project (0.3 at the time of the video): expect changes.
- Copy only sites you are allowed to, follow their terms, and leave robots rules on.

## Clean up
```bash
rm -rf out                 # deletes all copies and packed files
docker rmi ghcr.io/tamnd/kage
```

## Official links
- Docs: https://kage.tamnd.com/getting-started/introduction/
- Installation: https://kage.tamnd.com/getting-started/installation/
- Guides: https://kage.tamnd.com/guides/scoping-a-crawl/ , https://kage.tamnd.com/guides/resuming-a-run/ , https://kage.tamnd.com/guides/packing-a-mirror/
- CLI reference: https://kage.tamnd.com/reference/cli/
- Source code: https://github.com/tamnd/kage
- Licence: MIT (https://github.com/tamnd/kage/blob/main/LICENSE)
- Releases: https://github.com/tamnd/kage/releases

---
Not affiliated with or endorsed by the kage authors. "kage" is used only to describe the software.
