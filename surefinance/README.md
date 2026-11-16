# Sure

Sure is a free, self-hosted personal finance app (a community fork of Maybe Finance): accounts, transactions, budgets and net worth on one dashboard.
In this guide you install it with the official Docker Compose file, create a local account, add two accounts, import a CSV of transactions, set up categories and a monthly budget, and look at your net worth.

> Tested with Sure 0.7.6 (image tag `stable`, which pointed to `0.7.6-hotfix.1`) on 2026-11-16.
> Video: coming soon

## Requirements
- A computer or small server with Docker and Docker Compose v2 installed and running.
- About 512 MB of free memory is enough for everyday use (official docs).
- `curl` and `openssl` (installed on most Linux and macOS systems).
- No account with anyone, no bank login and no paid key. This guide skips the optional AI features and bank connections.

## Step 1: Get the official files
Make a folder, step into it, and download the sample compose file and the example environment file from the Sure repository.
```bash
mkdir -p ~/docker-apps/sure
cd ~/docker-apps/sure
curl --fail --location --silent --show-error --output compose.yml https://raw.githubusercontent.com/we-promise/sure/main/compose.example.yml
curl --fail --location --silent --show-error --output .env https://raw.githubusercontent.com/we-promise/sure/main/.env.example
ls -la
```
`curl` prints nothing on success; `ls -la` shows `compose.yml` and `.env`.

Optional: this folder also contains `compose.yaml`, the same official file with the image pinned to the version tested here. Use it instead of the downloaded `compose.yml` if you want exactly that version (keep only one compose file in the folder).

## Step 2: Secret key, database password, start
The app needs a secret key that only you know. The docs generate one with `openssl rand -hex 64`; this puts a fresh one straight into `.env`. Then set your own database password (replace the placeholder with a long random value, for example from `openssl rand -hex 32`) and check both lines.
```bash
sed -i "s/^SECRET_KEY_BASE=.*/SECRET_KEY_BASE=$(openssl rand -hex 64)/" .env
sed -i 's/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=CHANGE_ME_long_random_string/' .env
grep -E '^(SECRET_KEY_BASE|POSTGRES_PASSWORD)=' .env | cut -c1-60
```
On macOS, use `sed -i ''` instead of `sed -i`.

Start everything in the background and check it:
```bash
docker compose up -d
docker compose ls
```
Expected output: Docker creates the network and volumes, starts `db` and `redis`, waits until they are healthy, then starts `worker` and `web`. `docker compose ls` lists the project:
```
NAME      STATUS       CONFIG FILES
sure      running(4)   /home/you/docker-apps/sure/compose.yml
```
Give the web app 20 to 40 seconds to finish its first start.

## Step 3: Create your account
Open http://localhost:3000. A fresh install shows the Create account page. This account lives only on your own instance. Enter an email and a password with upper and lower case letters, a number and a symbol, then click **Create account**.

## Step 4: Set up your profile
- Type a first and last name, pick a country, click **Continue**.
- On Preferences, choose colour theme, language, currency and date format (the video keeps English and US dollars, sets the date format to YYYY-MM-DD and picks the dark theme). Click **Complete**.
- Tick a goal or two and click **Next**. You arrive at an empty dashboard that says "No accounts yet".

## Step 5: Feature one - accounts
- Click **Add account**, choose **Cash**, then **Enter account balance**.
- Name: `Everyday Checking`, balance `2500`, opening balance date the last day of the previous month, subtype **Checking**. Click **Create Account**.
- Click **New account**, choose **Credit Card**, **Enter account balance**: name `Demo Credit Card`, balance `300` (the amount owed), same date. Click **Create Account**.

Both accounts now show in the list on the left, under cash and credit cards.

## Step 6: Feature two - import a CSV
Make a small file of made-up transactions (12 rows, dated in the current month). From this guide's folder:
```bash
python3 sample-data/make_transactions_csv.py
```
It writes `transactions-YYYY-MM.csv` (use `--month 2026-11` for another month, `-o` for another file name).
Then in Sure:
- Go to **Transactions** and click **Import**. Under **Raw Data**, choose **Import transactions**.
- Pick `Everyday Checking` as the account, select the CSV file and click **Upload CSV**.
- Configure: Date = `Date` (format YYYY-MM-DD, taken from your preferences), Amount = `Amount`, amount type **Signed amount** with incomes positive (the default), then Name = `Name`, Category = `Category`, Notes = `Notes`. Click **Apply configuration**.
- Clean step: every row is shown in a table; red cells would be errors. Click **Next step**.
- Map step: Sure lists the categories it found in the file (Groceries, Utilities and so on) and will create them. Click **Next**, then **Next** again for tags, then **Publish import**.

The import runs in the background; a moment later the 12 transactions appear in your list, already categorised.

## Step 7: Feature three - categories
- Open **Settings**, then **Categories**. The nine categories from the import are listed.
- Click **New category**, type `Pets`, pick a colour and an icon, and create it.
- To change a transaction's category, open it from the Transactions page and pick another category from the menu. It saves right away.

## Step 8: Feature four - a monthly budget
- Click **Budgets** in the sidebar; it opens the current month. Click **New budget**.
- Budgeted spending `2200`, expected income `3200`, click **Continue**.
- Give each expense category a monthly limit, for example Groceries `350`, Entertainment `20`, Mortgage / Rent `1350`, and so on. Click **Confirm**.

The donut shows what is spent, and the list shows which categories are on track and which are over budget (with the sample data, Entertainment is over budget).

## Step 9: Feature five - net worth and privacy mode
- Click **Home** and scroll to **Net Worth**: what you own minus what you owe. With the sample data it is Everyday Checking minus the credit card, about $3,581.66.
- Cash flow fills in from the imported transactions; the menu at the top changes the time range.
- Click the eye icon at the top to hide every amount; click again to show them.

## Troubleshooting and tips
- Database connection error on the very first start: usually an old Postgres volume from an earlier attempt. The docs show how to reset it; this deletes that database:
  ```bash
  docker compose down
  docker volume rm sure_postgres-data
  docker compose up -d
  ```
- Import seems stuck: open **Settings > Background jobs**, which shows the queue and safe recovery actions. CSV imports need the `worker` container and Redis; check `docker compose logs worker`.
- Keep your `SECRET_KEY_BASE` safe and never replace it on an existing install, or encrypted data becomes unreadable. Back up your `.env`.
- Once your own account exists, you can close or restrict signups under **Settings > Self-Hosting > Onboarding**.
- Port 3000 already in use: set `PORT=` in `.env` to another port.

## Limits and costs
- Self-hosting is free and the code is open source.
- Still young: 0.7.6 was the latest stable release in November 2026, with new versions about every month.
- The AI assistant and bank sync are optional and need API keys or outside providers, some of which cost money. Not covered here.
- You are in charge of your own backups and updates (the official compose file includes an optional backup service; see the Docker guide).

## Clean up
```bash
docker compose down        # add -v only if you want to delete the data too
```

## Official links
- Docs (Docker self-hosting): https://github.com/we-promise/sure/blob/main/docs/hosting/docker.md
- Getting started guide: https://github.com/we-promise/sure/blob/main/docs/onboarding/guide.md
- Source code: https://github.com/we-promise/sure
- Licence: AGPL-3.0 (https://github.com/we-promise/sure/blob/main/LICENSE)
- Releases: https://github.com/we-promise/sure/releases
- Container images: https://github.com/we-promise/sure/pkgs/container/sure
- Website: https://sure.am

---
Not affiliated with or endorsed by the Sure authors. "Sure" is used only to describe the software.
