# Universal SoundCheck / Church Audio Guard 12-Week Detailed Development Plan

Created: 2026-06-26

Reference document: `universal-soundcheck-plan.md`

Goal: Build a church broadcast / speech sound-check MVP within 12 weeks, then validate real user feedback and paid-conversion potential.

## Development Principles

- The initial MVP does not directly control consoles.
- Build audio-file analysis and real-time input analysis first.
- Narrow the target to church live streams, sermons, and host microphones.
- Results must be understandable to beginner volunteers.
- Provide numbers and graphs for engineers.
- Each week must end with a deliverable that can be shown.

## 12-Week Overall Goal

```text
Weeks 1-4: Complete file-analysis MVP and reports
Weeks 5-8: Complete real-time sound check and church workflow
Weeks 9-10: Run field tests and improve recommendation copy
Weeks 11-12: Validate demo, feedback, and sales potential
```

# Week 1 - Problem Definition and Sample Collection

Weekly goal: create criteria for distinguishing good and bad sound, and secure initial samples for analysis.

Key questions:

- What problems happen most often in church broadcasts?
- What problems do beginner volunteers need to know fastest?
- How should good samples and bad samples be separated?
- How many problem types should the MVP detect?

Tasks:

- Temporarily choose product name: Church Audio Guard or SoundCheck Box
- Confirm first target: church live-stream speech
- Collect five good samples
- Collect five bad samples
- Label problems by sample
- Limit problem types to six to eight
- Write the criteria table
- Draft the report sample layout

Draft problem types:

- Volume too low
- Volume too high
- Clipping
- Too much low end, causing muddiness
- Lack of 2-5kHz clarity
- Harsh 6-8kHz range
- High noise floor
- L/R balance mismatch

Deliverables:

- Sample audio folder
- Sample labeling table
- Problem-type definition document
- Report draft

Success criteria:

```text
There is a criteria table for good/bad sound,
and at least 10 samples have problem labels.
```

Notes:

- Do not cover full music mixes from the start.
- A small sample count is acceptable, but labeling criteria must be clear.
- Do not use copyrighted audio in external demos.

# Week 2 - Audio File Analysis MVP

Weekly goal: build an analyzer that calculates basic level, peak, clipping, and frequency-band information from WAV / MP3 files.

Tasks:

- Create Python project
- Create base folder structure
- Implement WAV loading
- Implement MP3 loading
- Decide mono/stereo handling
- Calculate average level
- Calculate RMS level
- Calculate peak level
- Detect clipping
- Implement simple FFT / spectrum analysis
- Calculate band energy
- Display results in CLI or Streamlit

Recommended file structure:

```text
soundcheck-guard/
├─ app.py
├─ file_analyzer.py
├─ metrics.py
├─ samples/
├─ reports/
└─ tests/
```

Basic metrics:

- duration
- sample rate
- channels
- peak dBFS
- RMS dBFS
- crest factor
- clipping count
- clipping ratio
- low band energy
- mid band energy
- high band energy

Deliverables:

- File upload / file path analysis feature
- Basic analysis result screen
- Analysis results for 10 samples

Success criteria:

```text
When a file is provided, basic judgments such as too quiet, too loud,
clipping present, or too much low end appear as text.
```

Test items:

- Normal WAV file analysis
- Normal MP3 file analysis
- Stereo file analysis
- Mono file analysis
- Very quiet file analysis
- Clipped file analysis
- Exception handling for too-short files

# Week 3 - Speech Clarity Analysis

Weekly goal: roughly detect muddiness, boxiness, lack of clarity, and harshness in sermon / host microphone audio.

Tasks:

- Create speech-specific analysis module
- Detect excessive 80-200Hz low end
- Detect 200-400Hz muddiness
- Detect 300-600Hz boxiness
- Detect 2-5kHz clarity
- Detect 6-8kHz harshness
- Calculate band scores
- Sort problem priority
- Summarize only the top three issues

Draft band criteria:

```text
80-200Hz: proximity effect / excessive low end
200-400Hz: muddy / muffled
300-600Hz: boxy / closed-in
2-5kHz: speech clarity
6-8kHz: harshness
```

Deliverables:

- speech_analyzer.py
- Problem-band scores
- Top-three issue summary
- Sample-by-sample analysis comparison table

Success criteria:

```text
The main problems in sermon / speech audio can be summarized in three or fewer items.
```

Notes:

- Do not aim for perfect audio judgment at this stage.
- Consistent trend detection matters more than absolute truth.
- Recommendation copy should be cautious.

Example:

```text
There is a lot of energy near 250Hz. The voice may sound muddy.
```

# Week 4 - Report Generation

Weekly goal: save analysis results as HTML / PDF reports that can be sent to church staff or engineers.

Tasks:

- Calculate Overall Score
- Calculate Level score
- Calculate Clipping score
- Calculate Speech clarity score
- Calculate Low-end balance score
- Calculate Harshness score
- Calculate Noise score
- Calculate Stereo score
- Write beginner-friendly explanation copy
- Show engineer-facing metrics
- Generate HTML report
- Review PDF saving method

Draft scoring:

```text
Overall Score = 100 points

Level: 20 points
Clipping: 20 points
Speech clarity: 20 points
Low-end balance: 15 points
Harshness: 10 points
Noise floor: 10 points
Stereo balance: 5 points
```

Report structure:

- Title
- Analysis timestamp
- File name or input device
- Overall Score
- GOOD / WARNING / DANGER
- Top three issues
- Beginner troubleshooting guide
- Engineer details
- Frequency graph
- Whether to save this as a baseline for the next check

Deliverables:

- report_generator.py
- HTML report sample
- PDF report sample
- Three sample reports

Success criteria:

```text
Analysis results can be saved as a report suitable to send to church staff.
```

# Week 5 - Real-Time Input

Weekly goal: record 30 or 60 seconds from laptop built-in input, USB audio interface, or console USB output, then analyze automatically.

Tasks:

- Display audio input device list
- Select input device
- Select or auto-detect sample rate
- Implement real-time level meter
- Implement 30-second recording
- Implement 60-second recording
- Temporarily save recording files
- Connect recording to automatic analysis
- Warn when input is too quiet
- Guide users when there is no input

Draft screen:

```text
[Input Device]
[Check Length: 30s / 60s]
[Start Sound Check]

Input Level: -24 dBFS
Status: Listening...
```

Deliverables:

- realtime_recorder.py
- audio_input.py
- Input-device selection screen
- Record-then-analyze flow

Success criteria:

```text
Real-time sound checks can be run from a laptop or audio interface.
```

Test items:

- Built-in microphone input
- USB interface input
- No-input state
- Very quiet input state
- 30-second recording
- 60-second recording

# Week 6 - Quick Check Mode

Weekly goal: build a simple screen where volunteers can check within one minute whether today's sound is okay.

Tasks:

- 30-second Quick Check button
- 60-second Full Check button
- GOOD / WARNING / DANGER display
- Show only three issues
- Show beginner troubleshooting guide
- Report save button
- Recheck button
- Simplify result screen

Draft status criteria:

```text
GOOD: No major issue
WARNING: Check before service
DANGER: Fix recommended before broadcast
```

Beginner copy example:

```text
Problem: Voice may sound muddy.

Possible causes:
- Microphone is too close to the mouth
- HPF is off
- There is too much energy near 250Hz

Fix:
1. Try enabling HPF around 80-100Hz.
2. Try reducing near 250Hz by 2-3dB.
3. Move the microphone slightly farther away.
```

Deliverables:

- Quick Check screen
- Result summary screen
- Beginner recommendation copy

Success criteria:

```text
A beginner volunteer can check whether today's sound is okay within one minute.
```

# Week 7 - Baseline Compare

Weekly goal: save last week's good state and compare it with today's check result.

Tasks:

- Baseline saving feature
- Baseline name input
- Baseline date storage
- Compare today's result with baseline
- Show average loudness difference
- Show peak difference
- Show low-end difference
- Show clarity-band difference
- Show noise floor difference
- Generate comparison sentence

Comparison copy examples:

```text
Average loudness is 6dB lower than the previous good sample.
200-400Hz energy is 4dB higher than the previous good sample.
Noise floor increased compared with the previous good sample.
```

Deliverables:

- baseline.py
- Baseline save file or SQLite table
- Before / Today comparison screen
- Comparison report

Success criteria:

```text
The app can show how today's state differs from last week's good state.
```

Importance: this is the core differentiator. Users often say, "It was fine last week, but today something is wrong."

# Week 8 - Church Workflow

Weekly goal: let church users choose the check mode that matches their situation and start immediately.

Tasks:

- Sunday Service mode
- Sermon Mic mode
- Stream Output mode
- Draft Worship Band mode
- Pre-service checklist
- Adjust criteria by mode
- Adjust recommendation copy by mode
- Show mode in result report

Mode priorities:

Sermon Mic:

- speech level
- clarity
- low-end buildup
- harshness
- clipping

Stream Output:

- loudness
- clipping
- stereo balance
- noise floor
- overall tonal balance

Sunday Service:

- level
- clipping
- speech clarity
- baseline compare
- report saving

Worship Band:

- Keep this experimental at this stage.
- Do not write strong final-judgment copy.

Deliverables:

- Mode selection screen
- Mode-specific check settings
- Pre-service checklist
- Mode-specific report samples

Success criteria:

```text
Church users can see the menu and immediately start the check that matches their situation.
```

# Week 9 - First Field Test

Weekly goal: secure test data from real churches, auditoriums, or rehearsal spaces and verify whether the MVP detects real problems.

Tasks:

- Recruit at least two test locations
- Test audio interface connection
- Test console Stream Out / Matrix Out connection
- Record good state
- Intentionally create bad state
- Test low-volume state
- Test clipping state
- Test excessive low-end state
- Test microphone distance changes
- Collect user feedback
- Compare analysis results with actual listening judgment

Data to collect:

- Venue
- Equipment
- Input method
- Microphone type
- Console type
- Check mode
- App judgment
- Actual listening judgment
- User opinion

Deliverables:

- At least 10 real test data records
- Test result table
- Cases that worked well
- Cases that failed
- List of rules to improve

Success criteria:

```text
At least 10 real-location test data records are collected.
```

# Week 10 - Recommendation Copy and Detection Rule Improvements

Weekly goal: reduce false detections from field-test results and refine copy so both beginners and engineers can accept it.

Tasks:

- Remove overly technical wording
- Add beginner-friendly explanations
- Separate engineer details
- Remove risky EQ recommendations
- Fix ambiguous problem copy
- Adjust thresholds
- Reduce false positives
- Organize false negatives
- Adjust recommendation-copy priority

Copy principles:

- Do not state conclusions too absolutely.
- Guide users toward what they can verify directly.
- Do not recommend risky operations.
- Separate beginner and engineer screens.

Good copy example:

```text
The voice may sound slightly muddy.
If HPF is off, try enabling it around 80-100Hz.
```

Copy to avoid:

```text
You must reduce 250Hz by 6dB.
This setting is correct.
```

Deliverables:

- Recommendation copy library
- Updated detection thresholds
- False-positive case summary
- Improved report samples

Success criteria:

```text
Beginners can understand the results, and engineers can trust the metrics.
```

# Week 11 - Demo Completion

Weekly goal: build a demo that shows product value to a new viewer within three minutes.

Tasks:

- Clean up first screen
- Sample-file demo mode
- Quick Check demo scenario
- Baseline Compare demo scenario
- Before / after report example
- Three-minute demo script
- Landing-page draft
- Product intro copy

Three-minute demo flow:

```text
1. Start a pre-service sound check.
2. Test the sermon microphone for 30 seconds.
3. The app shows WARNING.
4. Show "average loudness is 6dB lower than last week."
5. Show "check HPF / microphone distance / gain" guidance.
6. Save the report.
```

Product description:

```text
Church Audio Guard checks sound status within 60 seconds before a service
and compares it with the previous good baseline so beginners can understand what changed.
```

Deliverables:

- Demo sample files
- Demo report
- Three-minute demo script
- Landing-page draft
- Feedback request message

Success criteria:

```text
A new viewer can understand the product value within three minutes.
```

# Week 12 - Sales Test

Weekly goal: show the MVP to real customer candidates and validate paid reports, subscriptions, and installed-product potential.

Tasks:

- Request feedback from five churches
- Request feedback from two schools / auditoriums
- Request opinions from two installation vendors
- Provide free analysis reports
- Ask about paid-conversion willingness
- Test prices
- Organize the customer segment with the strongest response
- Write the next 12-week plan

Questions:

- Can you understand the problem from this report?
- Could you use this as a pre-service check tool?
- Is the last-week comparison useful?
- Would you need an automatic weekly report?
- Would you pay $49-149 for one report?
- Is a $29-79/month subscription possible?
- Would a $299-399 hardware box interest you?

Draft price tests:

```text
One-time file analysis report: $49-149
Four reports per month: $99-299/month
Church app subscription: $29-79/month
Hardware Box Lite: $299-399
```

Deliverables:

- Feedback interview notes
- Price reaction summary
- Paid-interest customer list
- MVP improvement priorities
- Next-stage roadmap

Success criteria:

```text
At least one organization shows interest in a paid report, installation, or subscription.
```

# Weekly Deliverables Summary

| Week | Core Deliverable | Passing Criteria |
| --- | --- | --- |
| 1 | 10 samples, problem criteria table | Good/bad sound criteria exist |
| 2 | File-analysis MVP | Basic issues appear after file upload |
| 3 | Speech clarity analysis | Top three issues are summarized |
| 4 | HTML / PDF report | Report can be sent externally |
| 5 | Real-time input | 30s / 60s recording then analysis works |
| 6 | Quick Check | GOOD / WARNING / DANGER appears within one minute |
| 7 | Baseline Compare | Current state is compared with previous good state |
| 8 | Church modes | Situation-specific check modes can be selected |
| 9 | Field-test data | At least 10 real-location records are collected |
| 10 | Recommendation copy improvements | Beginners and engineers both understand results |
| 11 | Three-minute demo | Product value is clear to a new viewer |
| 12 | Sales test | At least one paid-interest customer exists |

# MVP Completion Criteria

After 12 weeks, the MVP should include:

- File upload analysis
- Real-time 30-second / 60-second checks
- Input level display
- Clipping detection
- Too-quiet / too-loud detection
- Excess low-end detection
- Speech clarity issue detection
- Harshness detection
- Noise floor detection
- Stereo balance check
- GOOD / WARNING / DANGER display
- Top-three issue summary
- Beginner troubleshooting guide
- Engineer detailed metrics
- HTML / PDF report saving
- Baseline saving
- Comparison with previous good state

# Decision After 12 Weeks

Continue if:

- Real churches, schools, or installation vendors show strong interest.
- At least one organization shows willingness to pay for reports or subscriptions.
- Baseline Compare receives a positive response.
- Users understand real problems from the report.

Pivot signals:

- Users do not understand the results.
- Recommendation copy is risky or confusing in real venues.
- Demand is stronger for consulting than analysis accuracy.
- Users only care about manual report services, not the app.

Next-stage candidates:

- Generate initial revenue through file-analysis report service
- Productize Streamlit MVP as a web or desktop app
- Run pilots with three to five churches
- Review SoundCheck Box hardware prototype
- Position as a maintenance report tool for installation vendors

# Most Important Sentence

```text
The first goal of this product is not automatic mixing;
it is building an Audio Guard that reduces sound incidents before services and events.
```
