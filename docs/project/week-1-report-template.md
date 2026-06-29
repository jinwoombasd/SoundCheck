# Week 1 Report Template

Created: 2026-06-29

Related plan: `12-week-development-plan.md`
Related criteria: `week-1-sound-criteria.md`

## Purpose

Provide a first report format for church broadcast speech checks before the Week 2 analyzer is implemented.

This template is documentation-only. It does not define final thresholds and does not require live audio processing.

## Report Header

| Field | Value |
| --- | --- |
| Report title | Church Audio Guard Speech Check |
| Analysis date |  |
| Sample ID |  |
| File name or input source |  |
| Source type | Sermon / host / pre-service test |
| Reviewer |  |

## Overall Result

| Field | Value |
| --- | --- |
| Overall status | GOOD / WARNING / DANGER |
| Main finding |  |
| Confidence | Low / Medium / High |
| Usable for demo | Yes / No |

Status guidance:

- GOOD: The speech sample is understandable and has no obvious level, clipping, tonal-balance, noise, or stereo issue.
- WARNING: The sample is usable, but one or two issues should be reviewed before it becomes a reference sample.
- DANGER: The sample has a clear issue that would likely affect a live stream or recording.

## Top Issues

List up to three issues. Leave unused rows blank.

| Priority | Problem ID | Listener-facing explanation | Engineer note | Suggested next action |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

## Beginner Summary

Use one or two short sentences.

Example:

The voice is understandable, but it has too much low-frequency buildup. Online listeners may hear the speech as muddy or thick.

## Engineer Details

| Metric | Value | Note |
| --- | --- | --- |
| Duration |  |  |
| Channels | Mono / Stereo |  |
| Peak level |  |  |
| RMS or loudness estimate |  |  |
| Clipping evidence | None / Possible / Clear |  |
| Low-end balance | OK / Too much / Too little |  |
| Speech clarity | OK / Weak / Harsh |  |
| Noise floor | OK / High |  |
| L/R balance | OK / Mismatch |  |

## Recommendation Copy

Keep recommendations cautious until real thresholds are validated.

Recommended language:

- Check the speech microphone level before changing EQ.
- Compare this sample against a known good reference from the same room.
- If low-end buildup remains, review microphone placement and high-pass filter settings.
- If clipping is present, lower the source gain before raising downstream output level.

Avoid:

- Claims that the app can automatically fix the mix.
- Exact EQ instructions before measurements are validated.
- Advice that assumes a specific console model.

## Week 1 Use

Use this template for the first 10 labeled samples:

- Five good samples
- Five bad samples
- One primary problem label for each bad sample
- Notes explaining why each good sample is acceptable
