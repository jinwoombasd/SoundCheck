# Slack Codex Bridge

This is a local Socket Mode bridge that lets Slack act as the input surface for GPT, Cursor, and Admin Main agents.

## Run

From the bridge app root that contains `package.json`, open one terminal per agent and run:

```bash
npm run start:gpt
npm run start:cursor
npm run start:admin
```

Each agent uses tokens from `.env`.

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

CURSOR_AGENT_BOT_TOKEN=xoxb-...
CURSOR_AGENT_APP_TOKEN=xapp-...

ADMIN_MAIN_BOT_TOKEN=xoxb-...
ADMIN_MAIN_APP_TOKEN=xapp-...
```

## How to Call Agents from Slack

- GPT: `g:` or `codex:`
- Cursor: `c:` or `cursor:`
- Admin Main: `a:`, `admin:`, `m:`
- Admin Main DMs and app mentions are handled without a prefix.
- GPT and Cursor only handle channel messages with their own prefix.
- Messages with another agent's prefix are ignored.

Examples:

```text
g: Clean up the README
c: Find likely causes for the current bug
admin: Coordinate the work order for GPT and Cursor
```

## P0 Routing Verification Results

The current router has been stabilized around the following rules:

- `g:` / `codex:` is handled only by GPT.
- `c:` / `cursor:` is handled only by Cursor.
- `a:` / `admin:` / `m:` is handled only by Admin Main.
- Regular bot messages are ignored; only trusted agent bot messages are processed.
- If `ALLOWED_USER_IDS` is set, only registered users can issue commands.
- Admin Main can process messages from `CHANNEL_COMMAND_USER_IDS` without a prefix.

## How Main Runs GPT/Cursor

When a user sends a request without a prefix, Admin Main interprets the request and, when needed, invokes the GPT/Cursor runner internally.
The user receives Main's final summary in the Slack thread.

```text
User -> Slack -> Admin Main -> Internal run: GPT / Cursor -> Obsidian log -> Final Slack summary
```

If `g:` or `c:` is used directly in a channel, that agent handles the request directly.
When Admin Main splits work for GPT/Cursor, it uses the local runner instead of posting relay messages into the Slack channel.

If `ADMIN_MAIN_BOT_TOKEN` exists in `.env`, GPT/Cursor recognize the Admin Main bot as a trusted agent.
To give command permission to other bots, add their Slack bot user IDs to `TRUSTED_AGENT_USER_IDS` as a comma-separated list.

## Main Automatic Operation Mode

When Admin Main receives a user request, it automatically follows this flow:

1. Convert the request into a plan.
2. Decide whether approval is required.
3. Assign planning/implementation work to GPT through an internal run.
4. Assign risk/verification work to Cursor through an internal run.
5. Combine GPT/Cursor results and leave a final summary in the Slack thread.
6. If the change is risky or large, wait for user approval before proceeding.

When approval is required, reply in the same thread as follows:

```text
Approve
```

The current Main plan is stored in:

```text
docs/roadmap/current-plan.md
```

## Agent Role Documents

Each agent references the following role documents when running:

- Main: `docs/agents/main.md`
- GPT team: `docs/agents/gpt-team.md`
- Cursor team: `docs/agents/cursor-team.md`

Run, stop, and status-check criteria used during operations are summarized in `docs/operations-faq.md`.
Common local commands are listed in `docs/common-commands.md`.

## Logs

Conversation logs are saved as Markdown files that can be read in Obsidian.

```text
GPT:    obsidian-log/Agent Logs/GPT
Cursor: obsidian-log/Agent Logs/Cursor
Admin:  obsidian-log/Agent Logs/Main
```

## Admin Automatic Operation

Admin Main's automatic checks are always on. It periodically scans the project, assigns review work to GPT/Cursor through internal runs, and by default saves only Obsidian logs.

```text
AUTO_MAIN_INTERVAL_MS=1800000
AUTO_MAIN_STARTUP_DELAY_MS=60000
AUTO_MAIN_CHANNEL_ID=
AUTO_MAIN_POST_TO_SLACK=false
```

If Slack posting is needed, enable it with `AUTO_MAIN_POST_TO_SLACK=true`. If `AUTO_MAIN_CHANNEL_ID` is empty, the most recent conversation channel is used.

## Development Rules

- Ask the user before making broad or many-file changes.
- Do not put all code in one file; split it by feature.
- If a request is unclear, first confirm your understanding.
