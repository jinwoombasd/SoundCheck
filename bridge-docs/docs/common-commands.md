# Common Commands

This is a collection of local commands commonly used while operating Slack Codex Bridge.

Run these commands from the bridge app root that contains `package.json`.

## Run

```bash
npm run start:gpt
npm run start:cursor
npm run start:admin
```

To use all three roles, run each command in a separate terminal.

## Restart

```bash
npm run restart
npm run restart:gpt
npm run restart:cursor
npm run restart:admin
```

The restart command terminates the selected agent's existing `src/index.js` process and starts it again in the background. Logs are written to `dev/logs`.

## Health Check

```bash
npm run health
```

Checks token settings, status-file JSON, agent processes, and local tool detection in one run.

## Test

```bash
npm test
```

Validates routing, Main plan behavior, runner smoke checks, and health checks.

## Development Run

```bash
npm run dev
```

Runs `src/index.js` in watch mode with the default profile. For agent-specific Slack operation, use `start:gpt`, `start:cursor`, and `start:admin`.

## Stop

Terminate the process in the terminal where each agent is running. The default operation commands do not automatically kill existing processes.
