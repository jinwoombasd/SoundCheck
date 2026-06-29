# Week 2 Analyzer Handoff

Created: 2026-06-29

Related plan: `12-week-development-plan.md`
Related criteria: `week-1-sound-criteria.md`
Related sample inventory: `week-1-sample-inventory.md`
Related report template: `week-1-report-template.md`

## Purpose

Prepare and track the Week 2 audio file analyzer work.

This handoff does not add sample audio, token changes, Slack process changes, or automatic operation changes.

## Start Conditions

Week 2 implementation should start when one of these is true:

- The first 10 Week 1 samples are listed in `week-1-sample-inventory.md`.
- Each bad sample has one primary problem label from `week-1-sound-criteria.md`.
- The user separately approves analyzer implementation before the full sample set is ready.

## Pre-Implementation Readiness Check

Before creating analyzer code, confirm these items:

- `week-1-sample-inventory.md` has five good samples and five bad samples.
- Every bad sample has one primary `P1-P9` label.
- Raw audio files are kept private unless sharing rights are confirmed.
- The first implementation target is still file-based WAV and MP3 analysis.
- No real-time input, X32 control, Slack runtime change, token change, or automatic EQ action is being added.

If any item is missing, continue with sample collection or labeling instead of starting implementation.

## Initial Analyzer Scope

The first analyzer should focus on file-based speech checks for WAV and MP3 files.

Minimum inputs:

- File path or upload source
- WAV file support
- MP3 file support
- Mono and stereo files
- Short speech clips from sermons, host microphones, or pre-service tests

Minimum outputs:

- Duration
- Sample rate
- Channel count
- Peak dBFS
- RMS dBFS
- Crest factor
- Clipping count
- Clipping ratio
- Low, mid, and high band energy
- Beginner-facing status text

## First Judgment Rules

The first version should only make cautious judgments:

- Too quiet
- Too loud
- Possible clipping
- Excess low end
- Weak speech clarity
- Harsh upper-mid range
- High background noise
- Left/right balance mismatch

Do not claim final accuracy until the sample labels and thresholds are validated.

## Implementation Status

Started: 2026-06-29

The first implementation is available as a modular Python package in `soundcheck/`.

Current behavior:

- WAV loading works through the Python standard library.
- MP3 loading is supported when either optional local dependency `soundfile` or `pydub` is installed.
- Tests use generated temporary WAV fixtures instead of committed sample audio.
- No real-time input, direct console control, automatic EQ action, Slack runtime change, token change, or public sample audio has been added.

## Suggested Module Boundaries

Keep the implementation modular from the first commit:

- `file_analyzer.py` for loading files and normalizing input data
- `metrics.py` for level, clipping, and channel metrics
- `speech_bands.py` for frequency-band calculations
- `judgments.py` for beginner-facing result text
- `reports.py` for report-ready output structures
- `tests/` for generated fixtures and regression tests

## Verification Checklist

Before Week 2 is considered complete, verify:

- Normal WAV analysis succeeds.
- Normal MP3 analysis succeeds.
- Mono and stereo files both work.
- Very quiet samples produce a quiet-level warning.
- Clipped samples produce a clipping warning.
- Too-short files fail with a clear error.
- Analysis output can fill the Week 1 report template.

## Deferred Work

Do not include these in the first Week 2 implementation unless separately approved:

- Real-time microphone input
- Direct console control
- Automatic EQ changes
- Slack runtime process changes
- Public sample audio commits without confirmed sharing rights
