# Chrome DevTools MCP

Chrome DevTools MCP (Chrome DevTools for agents) gives a coding agent a real Chrome browser plus DevTools: it can navigate, take screenshots, read console errors and network requests, and record performance traces.
In this guide you install it with npm, find two bugs and one slow image on a small made-up test page using its `chrome-devtools` command line tool, then connect it to your coding agent.

> Tested with chrome-devtools-mcp 1.13.0 (Node.js 22, Google Chrome 157) on 2026-11-16.
> Video: https://youtu.be/hOyVidyCSF0

## Requirements
- Node.js LTS, 20.19 or newer (it brings npm).
- Google Chrome, current stable version (Chrome for Testing also works).
- Later: a coding agent that supports MCP (for example Claude Code, Cursor, Copilot or Gemini CLI).
- No account and no API key.
- Optional, to follow along with the same test page: Python 3 with Pillow (see Step 3).

## Step 1: Check Node and Chrome
```bash
node --version
google-chrome --version
```
Expected output (your numbers may be higher):
```
v22.x.x
Google Chrome 157.x
```
On macOS or Windows, check the Chrome version under Chrome menu > Help > About Google Chrome instead.

## Step 2: Install it with one command
A global install from the official npm package. It also installs the `chrome-devtools` command line tool.
```bash
npm i chrome-devtools-mcp@latest -g
chrome-devtools --help
```
`--help` lists the commands (`start`, `status`, `stop`) and one command per tool your agent gets, such as `click`, `navigate_page`, `take_screenshot`, `list_console_messages`, `list_network_requests` and the `performance_*` tools.

## Step 3: A test page to debug
The video uses "Sunny Bakery", a made-up page served on `http://localhost:8080`. It looks fine, but clicking "Order now" does nothing and one menu picture is missing. To get the same page:
```bash
pip install pillow
python3 sample-data/make_site.py site     # creates ./site with index.html, hero.jpg, hero-small.jpg, croissant.png
(cd site && python3 -m http.server 8080)  # keep this running, use a second terminal for the next steps
```
Run the remaining commands from the folder that contains `site/`. You can also use any page you own instead.

## Step 4: Open the page
```bash
chrome-devtools navigate_page 1 --url http://localhost:8080
```
The first call starts the background server and a headless Chrome. It prints a warning that connected tools can see everything in this browser, then reports that it successfully navigated, with page 1 being Sunny Bakery.

## Step 5: Take a screenshot
```bash
chrome-devtools take_screenshot 1 --filePath site/shot.png
```
Open `http://localhost:8080/shot.png` in your browser: that image is exactly what an agent sees. Next to the croissant there is an empty frame where the cinnamon rolls should be.

## Step 6: Read the console
```bash
chrome-devtools list_console_messages 1
```
Expected: two errors.
- `Uncaught TypeError: Cannot read properties of null` - the script looks for a button id that does not exist, so "Order now" does nothing.
- A resource that failed to load with a 404.

## Step 7: Check the network
```bash
chrome-devtools list_network_requests 1
```
Every request the page made, with its status. `rolls.png` returns 404 (not found). A missing `favicon.ico` also shows up, which is harmless.

## Step 8: Test on a slow network
Emulate a slow connection, then record a performance trace that reloads the page. `grep` keeps only the key lines.
```bash
chrome-devtools emulate 1 --networkConditions "Slow 4G"
chrome-devtools performance_start_trace 1 --reload --autoStop --ignoreCache | grep -E "LCP:|insight name"
```
In the video the Largest Contentful Paint (LCP) was about 9 seconds, plus a list of insight names.

## Step 9: Ask why it is slow
```bash
chrome-devtools performance_analyze_insight 1 NAVIGATION_0 ImageDelivery
```
The insight explains that the hero image is 3200 pixels wide but shown at only 560, and that resizing it could save about 1.4 MB (the image made by `make_site.py` is a bit larger, so your figure will differ).

## Step 10: Fix it and measure again
Replace the hero with the smaller copy (about 1120 pixels wide) and run the same trace on the same slow network:
```bash
cp site/hero-small.jpg site/hero.jpg
chrome-devtools performance_start_trace 1 --reload --autoStop --ignoreCache | grep -E "LCP:|insight name"
```
In the video LCP dropped from about 9 seconds to about 1.5 seconds. Your numbers will differ, but the improvement should be clear.

## Step 11: Connect it to your agent
With an agent you do not type any of this. Add the official config to your agent's MCP settings:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```
Then ask in plain words, for example: "Check the performance of http://localhost:8080". The agent calls the same tools used above. When you are done with the command line tool, shut down its background browser:
```bash
chrome-devtools stop
```

## Troubleshooting and tips
- The agent can see and change everything in the browser it controls. Keep personal accounts out and use a separate, temporary profile: `--isolated` creates a temporary user data dir that is deleted when the browser closes.
- Usage statistics are sent to Google by default. Add `--no-usage-statistics` to the server args (for example `"args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]`), or set the environment variable `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`.
- Performance tools may send page URLs from traces to Google's CrUX API for real-user field data. Turn this off with `--no-performance-crux`.
- Running inside a Docker container: Chrome needed the `--no-sandbox` argument, passed with the `chromeArg` option (`--chromeArg=--no-sandbox`, or `"chromeArg": ["--no-sandbox"]` in the global config file `~/.config/cd4a/config.json` on macOS and Linux). Only do this inside a container.
- `chrome-devtools: command not found` after the install: the npm global bin folder is not on your `PATH`. Check it with `npm prefix -g` and add its `bin` folder to `PATH`.
- `chrome-devtools status` tells you whether the background server is running. The CLI runs Chrome headless by default.
- Options supported by the CLI: `chrome-devtools start --help`. All server options: see the configuration guide below.

## Limits and costs
- Free and open source (Apache 2.0); works with many agents: Claude Code, Cursor, Copilot, Gemini and more.
- Officially supports only Google Chrome and Chrome for Testing.
- It does not think by itself: the model, and any cost, comes from your agent.
- Young project: launched as a preview in September 2025 and changes every few weeks.
- Use it only on sites you own or are allowed to test, and keep personal data out of the browser it controls.

## Clean up
```bash
chrome-devtools stop                  # stop the background browser
npm uninstall -g chrome-devtools-mcp  # remove the package
rm -rf site                           # remove the test page
```
Stop the `python3 -m http.server` with Ctrl+C.

## Official links
- Docs: https://developer.chrome.com/docs/devtools/agents
- Launch post: https://developer.chrome.com/blog/chrome-devtools-mcp
- Source code: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Tool reference: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
- CLI guide: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md
- Configuration: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md
- npm package: https://www.npmjs.com/package/chrome-devtools-mcp
- Licence: Apache-2.0 (https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/LICENSE)
- Releases: https://github.com/ChromeDevTools/chrome-devtools-mcp/releases

---
Not affiliated with or endorsed by the Chrome DevTools MCP authors or Google. "Chrome DevTools MCP" is used only to describe the software.
