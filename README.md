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
- `docs/project/week-3-speech-clarity-handoff.md` - Week 3 speech clarity scope and verification status
- `docs/project/week-4-report-generation-handoff.md` - Week 4 report generation scope and verification status
- `docs/project/sample-week-4-report.html` - scrubbed synthetic demo HTML report
- `docs/project/sample-week-4-report.pdf` - scrubbed synthetic demo PDF report
- `docs/roadmap/x32-ai-eq-mvp-plan.md` - X32-focused EQ assistant MVP concept
- `docs/roadmap/ai-roadmap.md` - later AI feature roadmap

## Analyzer Usage

Analyze a local WAV or MP3 file:

```bash
python3 -m soundcheck.cli path/to/audio.wav
```

For a local MP3 sample:

```bash
python3 -m soundcheck.cli samples/week-1/good/sample-01.mp3
```

Print machine-readable output:

```bash
python3 -m soundcheck.cli path/to/audio.wav --json
```

Print fields mapped to the Week 1 report template, including report header placeholders, cautious overall result, top issues, engineer details, and band-energy data:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-1-json
```

Print the first Week 4 report-score structure, including the 100-point score breakdown for level, clipping, speech clarity, low-end balance, harshness, noise, and stereo balance:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-4-json
```

Write the first Week 4 HTML report:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-4-html reports/speech-check.html
```

Write a Week 4 PDF report:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-4-pdf reports/speech-check.pdf
```

Generated local reports should stay under `reports/`, which is ignored by Git.
Only commit scrubbed demo reports that contain no private audio, customer, venue, local path, token, or runtime-log details.

WAV support works with the Python standard library. MP3 support is optional and requires either `soundfile` or `pydub` to be installed in the local environment:

```bash
python3 -m pip install ".[mp3]"
```

PDF export is optional and requires `reportlab`:

```bash
python3 -m pip install ".[pdf]"
```

## Current Status

This repository contains planning documents and the first file-based audio analyzer implementation. The analyzer currently reports duration, sample rate, channel count, level metrics, clipping, approximate speech-band energy, Week 3 speech clarity band scores, top-three speech issues, cautious beginner-facing findings, an initial Week 4 report-score breakdown, and basic Week 4 HTML and PDF reports.

Week 3 comparison-table support is available for private labeled samples, but threshold calibration is still waiting on five good and five bad speech samples.

Raw audio samples should stay private until usage rights are confirmed.
