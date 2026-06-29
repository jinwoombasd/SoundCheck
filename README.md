# SoundCheck

SoundCheck is an early-stage audio quality assistant for churches, schools, small venues, and live-streaming teams.

The goal is to help non-expert operators quickly understand whether speech or broadcast audio is safe before a service, class, event, or stream begins.

## Product Direction

SoundCheck is not an automatic mixer and does not replace an audio engineer.

It is designed as an audio safety monitor that checks common problems, explains them in plain language, and gives cautious next-step guidance.

Initial focus:

- Church live-stream speech
- Sermon microphones
- Host and announcement microphones
- Pre-service sound checks
- Beginner-friendly reports

## MVP Scope

The first MVP focuses on audio analysis and reporting before any direct console control.

Planned checks include:

- Low or high speech level
- Clipping
- Excess low end
- Muddy low mids
- Weak speech clarity
- Harsh upper mids
- High noise floor
- Left/right balance mismatch

## Repository Contents

- `soundcheck/` - modular Python audio analyzer package
- `tests/` - regression tests using generated temporary WAV fixtures
- `docs/project/universal-soundcheck-plan.md` - product positioning and overall plan
- `docs/project/12-week-development-plan.md` - 12-week MVP development plan
- `docs/project/week-1-sound-criteria.md` - first-pass speech sample criteria
- `docs/project/week-1-report-template.md` - manual report template for early samples
- `docs/project/week-1-sample-inventory.md` - Week 1 sample tracking template
- `docs/project/week-2-analyzer-handoff.md` - Week 2 analyzer start conditions and scope
- `docs/roadmap/x32-ai-eq-mvp-plan.md` - X32-focused EQ assistant MVP concept
- `docs/roadmap/ai-roadmap.md` - later AI feature roadmap

## Analyzer Usage

Analyze a local WAV file:

```bash
python3 -m soundcheck.cli path/to/audio.wav
```

Print machine-readable output:

```bash
python3 -m soundcheck.cli path/to/audio.wav --json
```

WAV support works with the Python standard library. MP3 support is optional and requires either `soundfile` or `pydub` to be installed in the local environment.

## Current Status

This repository contains planning documents and the first file-based audio analyzer implementation. The analyzer currently reports duration, sample rate, channel count, level metrics, clipping, approximate speech-band energy, and cautious beginner-facing findings.

Raw audio samples should stay private until usage rights are confirmed.
