# Tech On Cue Labs

Free companion guides for the hands-on tutorials on the **Tech On Cue** YouTube channel.
Each folder follows one video step by step: requirements, the exact commands, what you should see, tips and troubleshooting, limits and costs, and links to the official docs.

## Tutorials

| Tool | What it is | Guide | Video | Tested version |
|------|------------|-------|-------|----------------|
| Beszel | Lightweight server and Docker monitoring | [beszel/](beszel/) | [Watch](https://youtu.be/OFU6p_-CXCc) | 0.21.2 |
| Chrome DevTools MCP | A real Chrome browser and DevTools for coding agents | [chromedevtoolsmcp/](chromedevtoolsmcp/) | [Watch](https://youtu.be/hOyVidyCSF0) | 1.13.0 |
| EdgeEver | Self-hosted notes and knowledge base | [edgeever/](edgeever/) | [Watch](https://youtu.be/ZFQvQUDJLJI) | v2.28.0 |
| goose | Open source AI agent for the terminal (with a local model) | [goose/](goose/) | [Watch](https://youtu.be/w1ZO6LMTu3E) | 1.59.0 |
| Immich | Self-hosted photo and video library | [immich/](immich/) | Coming soon | v3.4.1 |
| Jellyfin | Self-hosted media server for your own movies and shows | [jellyfin/](jellyfin/) | Coming soon | 12.4.0 |
| kage | Saves websites as static, JavaScript-free copies | [kage/](kage/) | [Watch](https://youtu.be/YPXyf7kizn8) | 0.3.12 |
| LobeHub | Self-hosted chat and agent workspace for AI models | [lobehub/](lobehub/) | [Watch](https://youtu.be/XsjdkBC9h3A) | 2.3.3 |
| n8n | Workflow automation with a visual editor | [n8n/](n8n/) | Coming soon | 2.47.7 |
| OpenSandbox | Isolated, throwaway sandboxes for AI agents | [opensandbox/](opensandbox/) | [Watch](https://youtu.be/LoJh4OdPGn4) | 1.2.1 |
| Paperless-ngx | Self-hosted document management with OCR | [paperless-ngx/](paperless-ngx/) | Coming soon | 3.4.2 |
| Sure | Self-hosted personal finance app | [surefinance/](surefinance/) | [Watch](https://youtu.be/F4c4jLpYKUE) | 0.7.6 |
| tau | Small coding agent for the terminal (with a local model) | [tau/](tau/) | [Watch](https://youtu.be/Dbpx1kRt6CY) | 0.4.11 |

All guides were last tested on 2026-11-16. The exact date and versions are at the top of each guide.

## How to use

1. Open the folder for the tool you want and read its `README.md` from top to bottom, ideally next to the video.
2. If a folder has a `compose.yaml` (or `docker-compose.yml`) or `.env.example`, copy it to your own working folder. Replace every `CHANGE_ME_...` value with your own, for example from `openssl rand -hex 32`. Never commit your real `.env`.
3. Some folders have a `sample-data/` folder with small scripts that create made-up data, so you can try the features without using your own files.
4. Tools change quickly. If a step no longer works, check the official docs linked in the guide, and please open an issue (see [CONTRIBUTING.md](CONTRIBUTING.md)).

Run these tools only on machines you own or manage, and keep anything you expose to the internet updated and behind proper authentication.

## Licence

Our own files (guides, compose and config files, sample-data scripts) are MIT licensed; see [LICENSE](LICENSE).
Each tool keeps its own licence, set by its authors; each guide names it and links to it. This repo does not contain or re-host any of the tools' code or images. Everything is pulled from the official sources.

## Not affiliated

Tech On Cue is not affiliated with, sponsored by, or endorsed by the authors of any tool covered here. Tool names are used only to describe the software. All sample data in this repo is made up.
