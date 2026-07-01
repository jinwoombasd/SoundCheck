# Week 3 Speech Clarity Handoff

Created: 2026-06-30

Related plan: `12-week-development-plan.md`
Related Week 2 handoff: `week-2-analyzer-handoff.md`

## Purpose

Move SoundCheck from general file analysis into first-pass speech clarity analysis for sermons, host microphones, and speech-focused church livestream checks.

This handoff does not add real-time input, console control, automatic EQ changes, Slack runtime changes, token changes, or public sample audio.

## Start Conditions

Week 3 can proceed now because the sample-free Week 2 analyzer path is implemented and covered with generated WAV fixtures.

The remaining Week 2 sample-dependent items are still open:

- Normal MP3 analysis with real speech audio after a private sample is available.
- Threshold behavior checked against five good and five bad labeled speech samples.

## Initial Week 3 Scope

The first Week 3 implementation should focus on cautious trend detection, not final audio judgment.

Speech-specific bands:

- 80-200Hz: proximity effect or excessive low end
- 200-400Hz: muddy or muffled tone
- 300-600Hz: boxy or closed-in tone
- 2-5kHz: speech clarity
- 6-8kHz: harshness

Minimum outputs:

- Problem-band scores
- Top-three speech clarity issues
- Cautious listener-facing summary text
- Engineer-facing band references

## Implementation Status

Started: 2026-06-30

Current behavior:

- `soundcheck/speech_analyzer.py` calculates Week 3 speech-band scores from loaded audio.
- `soundcheck/sample_comparison.py` can convert analysis reports into stable rows for the later private sample comparison table.
- Full analyzer JSON includes `speech_clarity_analysis` with band scores and at most three prioritized issues.
- Existing broad-band metrics and Week 1 report-field output remain available.
- Tests cover Week 3 band-score schema and generated muddy / harsh speech-band fixtures.

## Verification Checklist

- [x] Speech-specific analysis module exists.
- [x] 80-200Hz low-end band is calculated.
- [x] 200-400Hz muddy band is calculated.
- [x] 300-600Hz boxy band is calculated.
- [x] 2-5kHz clarity band is calculated.
- [x] 6-8kHz harshness band is calculated.
- [x] Top issues are limited to three items.
- [x] Sample-by-sample comparison table structure is available for labeled private samples.
- [ ] Thresholds are calibrated against five good and five bad private speech samples.
- [ ] Sample-by-sample comparison table is populated and reviewed after private sample labels are available.

## Deferred Work

Do not include these in Week 3 unless separately approved:

- Real-time microphone input
- X32 or other console control
- Automatic EQ changes
- Public sample audio commits without confirmed sharing rights
- Final accuracy claims before private sample validation

## Next Sample-Dependent Step

After five good and five bad private speech samples are available, populate the comparison table with expected labels, review the top issue order against listening notes, and adjust thresholds only when the same pattern appears across multiple samples.
