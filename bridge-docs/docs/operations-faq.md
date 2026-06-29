# Operations FAQ

These are the items commonly checked when operating Slack Codex Bridge directly.

## Run

From the bridge app root that contains `package.json`, run each agent in a separate terminal.

```bash
npm run start:gpt
npm run start:cursor
npm run start:admin
```

If only Admin Main is running, direct GPT/Cursor replies will not work. To use all three roles, run all three processes together.
The full list of common local commands is documented in `docs/common-commands.md`.

## Restart

```bash
npm run restart
npm run restart:gpt
npm run restart:cursor
npm run restart:admin
```

The restart command terminates the selected agent's existing `src/index.js` process and starts it again in the background. Run logs are saved in `dev/logs`.

## Health Check

```bash
npm run health
```

The health result checks token settings, status-file JSON, agent processes, and local tool detection in one run.
Warnings are not immediate failures; they are items to review before operation.

## Slack Call Rules

```text
g:      Call GPT directly
codex:  Call GPT directly
c:      Call Cursor directly
cursor: Call Cursor directly
m:      Call Admin Main directly
a:      Call Admin Main directly
admin:  Call Admin Main directly
```

Requests without a prefix are judged by Admin Main. When needed, Admin Main runs GPT/Cursor through the internal runner and leaves only the final summary in Slack.

## Stop

Terminate the process in the terminal where each agent is running. By default, this project does not automatically kill existing processes.

## Automatic Operation

Automatic operation is always on.

```text
AUTO_MAIN_INTERVAL_MS=1800000
AUTO_MAIN_POST_TO_SLACK=false
```

Even with automatic checks enabled, the operating rule is not to perform large code changes, token changes, env changes, or enable Slack auto-posting by default without user approval.

## Logs and Status Files

The current request board is:

```text
docs/roadmap/current-plan.md
```

The long-term operating reference is:

```text
docs/roadmap/project-roadmap.md
```

Obsidian logs are saved in folders by agent.

```text
GPT:    obsidian-log/Agent Logs/GPT
Cursor: obsidian-log/Agent Logs/Cursor
Admin:  obsidian-log/Agent Logs/Main
```
