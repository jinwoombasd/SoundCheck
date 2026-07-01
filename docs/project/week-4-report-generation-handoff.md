# Week 4 Report Generation Handoff

Created: 2026-07-01

Related plan: `12-week-development-plan.md`

## Purpose

Define the current Week 4 report-generation scope for SoundCheck and keep the next report work small, reviewable, and safe for a public product repository.

Week 4 focuses on turning the analyzer output into a report that can be sent to church staff or engineers. The first implementation should remain file-based and should not control audio consoles, upload private samples, or assume calibrated thresholds before the sample set is available.

## Current Implementation Status

Completed:

- Week 4 score breakdown is available through `soundcheck/report_scores.py`.
- Report fields are exposed through `AnalysisReport.to_week_4_report_fields()`.
- CLI JSON output is available with `--week-4-json`.
- HTML report writing is available with `--week-4-html OUTPUT_PATH`.
- PDF report writing is available with `--week-4-pdf OUTPUT_PATH` when the optional `pdf` dependency is installed.
- The HTML report includes a frequency-balance graph for low, low-mid, speech-mid, upper-mid, and high energy.
- Regression coverage includes score calculation, report-field mapping, CLI output, HTML rendering, HTML escaping, frequency-graph rendering, section order, and report file creation.

Not completed:

- Threshold calibration against five good and five bad private speech samples.

## Current CLI Usage

Generate the Week 4 score structure:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-4-json
```

Write the first HTML report:

```bash
python3 -m soundcheck.cli path/to/audio.wav --week-4-html reports/speech-check.html
```

Write the first PDF report:

```bash
python3 -m pip install ".[pdf]"
python3 -m soundcheck.cli path/to/audio.wav --week-4-pdf reports/speech-check.pdf
```

The `reports/` output path is an example only. Generated reports should not be committed unless they are scrubbed demo artifacts with no private audio, customer, church, or venue information.

Scrubbed demo artifacts are available as `docs/project/sample-week-4-report.html` and `docs/project/sample-week-4-report.pdf`. They were generated from synthetic demo values, not private audio.

## Acceptance Criteria

The current Week 4 report foundation is acceptable when:

- The score breakdown totals 100 points across level, clipping, speech clarity, low-end balance, harshness, noise, and stereo balance.
- The report shows an overall score and a GOOD, WARNING, or DANGER status.
- The report includes top issues, beginner-facing guidance, engineer-facing details, a frequency-balance graph, and baseline guidance.
- HTML output escapes user-controlled text such as file names and judgment messages.
- Generated local reports remain ignored under `reports/` unless a scrubbed demo artifact is separately approved.
- Existing analyzer JSON and Week 1 JSON output remain unchanged.
- `python3 -m pytest` passes.
- `git diff --check` passes.

## PDF Review Notes

PDF export was added after approval as an optional report path.

Current approach:

- Keep HTML as the canonical report format.
- Generate PDF locally with `reportlab`; no cloud service is used.
- Keep one smoke test that verifies PDF creation without private sample data.

## Sample Report Recommendation

Sample reports should wait until demo-safe audio or synthetic fixtures are selected.

Safe sample report rules:

- Do not commit private church, school, venue, customer, or livestream audio.
- Do not include real names, addresses, Slack IDs, tokens, local paths, or runtime logs.
- Use synthetic generated audio or explicitly cleared demo samples.
- Keep sample reports under a product documentation or demo-report folder only after approval.

## Next Small Work Candidate

The next no-approval task should be limited to verification or documentation, such as checking README consistency after report changes or rerunning focused HTML/PDF report tests.

The next approval-required task is checked-in sample report generation beyond the existing scrubbed synthetic demo artifacts.
