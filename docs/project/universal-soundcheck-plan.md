# Universal SoundCheck / Church Audio Guard Plan

Created: 2026-06-25

Status: Idea refinement

Goal: Build a sound-check and broadcast-audio quality monitoring product that can sit beside any audio console.

## One-Line Goal

Build an app/device that helps churches, schools, small venues, and event teams check within 60 seconds whether the sound is ready before a service or event, and explain problems in a way beginners can understand.

## Product Positioning

This product is not an AI mixer that replaces an engineer.

It is an **Audio Safety Monitor** that reduces incidents when no engineer is present and helps maintain standards set by an engineer.

Bad positioning:

```text
AI mixes for you instead of an engineer.
```

Good positioning:

```text
It compares today's sound against last week's good baseline and tells you whether there is a problem.
```

## Core Customers

First-priority customers:

- Small and midsize churches
- School auditoriums
- Youth, Wednesday, and Friday church service teams
- Small venues
- Event rental teams
- Live-streaming teams

Actual users:

- Audio volunteers
- Part-time engineers
- Worship pastors
- Tech directors
- School AV managers
- Event staff

Buyers:

- Church pastors or ministry owners
- Worship directors
- Production directors
- School or institution administrators
- Installation vendors

## Problems Solved

- Users do not know whether today's sound is normal.
- Broadcast volume is too low.
- Voice sounds muddy.
- Clipping happens without anyone noticing.
- Settings seem different from last week.
- Beginner volunteers do not know where to look.
- Incidents happen when no engineer is present.
- Broadcast audio problems are discovered only after the service ends.

## MVP Direction

The first MVP **does not directly control consoles**. To work with every console, it only receives and analyzes an audio output.

```text
Console Main Out / Matrix Out / Stream Out / Monitor Out
-> Audio interface or USB input
-> App analysis
-> OK / Warning / Danger display
-> Report saved
```

## MVP Core Features

- Audio input device selection
- 30-second or 60-second sound check
- Input level meter
- Clipping detection
- Too-quiet and too-loud detection
- Excess low-end detection
- Speech clarity issue detection
- Harsh high-frequency detection
- Noise floor detection
- Stereo balance check
- Broadcast loudness estimate
- Comparison against a previous good baseline
- Beginner-friendly troubleshooting guide
- PDF / HTML report export

## First MVP Scope

Start with **church broadcast / speech sound check**.

Targets:

- Sermon microphone
- Host microphone
- Live-stream output
- Pre-service church sound check

Supported inputs:

- Laptop built-in input
- USB audio interface
- Console USB output
- OBS recording file upload

Analysis length:

- 30-second Quick Check
- 60-second Full Check

## Explicitly Not in the Initial Scope

- Direct control of every console
- Automatic EQ application
- Automatic mixing
- Direct Dante device control
- Dedicated hardware
- Deep-learning model training
- Replacement for complex professional RTA / Smaart workflows
- Automatic changes during live performance

The first goal must stay simple:

```text
A product that tells users whether the sound is okay.
```

## Product Name Candidates

- Church Audio Guard
- Sunday Sound Check
- SoundCheck Box
- LiveMix Guardian
- Stream Sound Doctor
- Venue Audio Check

Recommendation:

```text
B2B / church name: Church Audio Guard
General product name: SoundCheck Box
```

## System Structure

Stage 1 software MVP:

```text
Console / OBS / Audio File
-> Laptop App
-> Audio Analysis
-> Problem Detection
-> Recommendation
-> Report
```

Stage 2 hardware box:

```text
Console Output
-> SoundCheck Box
-> Web Dashboard
-> Report / Alert / History
```

Stage 3 console-specific control plugins:

```text
X32 / M32 Plugin
Allen & Heath Plugin
Yamaha Plugin
Soundcraft Plugin
PreSonus Plugin
```

## Analysis Items

Level check:

- Average loudness
- Peak level
- Too quiet
- Too loud
- Lack of headroom

Clipping check:

- Digital clipping
- Continuous clipping
- Excessive momentary peaks

Speech clarity check:

- 200-400Hz muddiness
- 300-600Hz boxy sound
- 2-5kHz clarity
- 6-8kHz harshness

Low-end check:

- 80-200Hz excessive low end
- Possible microphone proximity effect
- Whether HPF may be needed

Noise check:

- Noise floor during silence
- Possible hum
- Possible fan or room noise

Stereo check:

- L/R balance
- One-sided channel problem
- Mono compatibility warning

Baseline compare:

```text
Average loudness is 6dB lower than last week
Low end is 4dB higher than last week
High end is 3dB higher than last week
Noise floor increased
```

This feature has strong revenue potential because churches and event teams often say, "It was fine last week, but today something is wrong."

## App Screens

Main screen:

```text
[Input Device]
[Check Type: Speech / Music / Stream / Full Service]
[Start 60s Sound Check]

Status:
GOOD / WARNING / DANGER
```

Result screen:

```text
Overall Score: 78 / 100

Warnings:
- Speech level is slightly low
- Low frequency buildup detected around 250Hz
- Stream output may sound muddy
- No clipping detected
```

Beginner troubleshooting guide:

```text
Problem: Voice sounds muddy

Possible causes:
- Microphone is too close to the mouth
- HPF is off
- There is too much energy near 250Hz

Fix:
1. Try enabling HPF around 80-100Hz.
2. Try reducing 250Hz by 2-3dB.
3. Move the microphone slightly farther away.
```

Engineer report:

- Average level
- Peak level
- Dynamic range
- Noise floor
- Frequency balance
- Problem bands
- Before / after comparison
- Timestamp
- Input device

## Monetization Strategy

Stage 1: earn first through service.

```text
Church broadcast audio analysis report
- Receive recording file / YouTube link / OBS recording file
- Analyze loudness, clipping, clarity, and low-end issues
- Provide PDF report
```

Price examples:

```text
One-time analysis: $49-149
Four reports per month: $99-299/month
Church setup consulting included: $300-800
```

Stage 2 software subscription:

```text
Free:
- Analyze one file
- Basic score

Pro:
- $9-19/month
- Unlimited analysis
- Report saving
- Baseline compare

Church:
- $29-79/month
- Manage multiple services / teams
- PDF reports
- History
- Volunteer guide
```

Stage 3 hardware sales:

```text
SoundCheck Box Lite: $299-399
SoundCheck Box Pro: $599-799
Annual software: $99-299/year
```

Stage 4 installation vendor partnerships:

```text
Church installation vendors sell it as a maintenance tool after equipment installation
Include it in school/church packages
Generate regular inspection reports automatically
```

## Draft Technical Stack

MVP software:

```text
Language: Python
Audio analysis: numpy, scipy, librosa
Real-time input: sounddevice
UI: Streamlit
Graphs: plotly
Reports: HTML -> PDF
Storage: SQLite + JSON
```

Later productization:

```text
Frontend: React / Next.js
Local Agent: Python or Rust
Desktop App: Tauri or Electron
Hardware: Raspberry Pi / mini PC prototype
Cloud: optional report backup
```

Draft file structure:

```text
soundcheck-guard/
├─ app.py
├─ audio_input.py
├─ file_analyzer.py
├─ realtime_recorder.py
├─ metrics.py
├─ speech_analyzer.py
├─ recommender.py
├─ baseline.py
├─ report_generator.py
├─ samples/
├─ reports/
├─ tests/
└─ README.md
```

## Draft MVP Scoring

```text
Overall Score = 100 points

- Level: 20 points
- Clipping: 20 points
- Speech clarity: 20 points
- Low-end balance: 15 points
- Harshness: 10 points
- Noise floor: 10 points
- Stereo balance: 5 points
```

Example result:

```text
Overall Score: 72 / 100

Status: WARNING

Main Issues:
1. Speech level is too low
2. Muddy buildup around 250Hz
3. Stream output lacks clarity around 3kHz

No clipping detected.
Noise floor is acceptable.
```

## Product Roadmap

Phase 1: File analysis service.

```text
User uploads recording file
-> Analysis report provided
-> Sold together with manual consulting
```

Goal: fastest path to revenue.

Phase 2: Real-time SoundCheck app.

```text
Audio interface connection
-> 30-second / 60-second check
-> Report saved
```

Goal: software MVP that churches and schools can use directly.

Phase 3: Hardware box.

```text
Console output connection
-> Always-on monitoring
-> Web dashboard
-> Post-service report
```

Goal: equipment sales plus subscription model.

Phase 4: Console-specific control plugins.

Candidate consoles:

- X32 / M32
- Allen & Heath SQ / Qu
- Yamaha DM3 / TF
- Soundcraft Ui
- PreSonus StudioLive

Goal: expand from analysis-only into helping solve problems.

Phase 5: AI EQ Assistant.

```text
Analysis
-> EQ recommendation
-> User confirmation
-> Apply through console-specific plugin
-> Revert
```

AI EQ should be a **premium feature**, not the main product.

## Validation Metrics

Technical validation:

- File analysis success rate
- Real-time input stability
- Analysis time under 60 seconds
- Clipping detection accuracy
- Problem-band detection accuracy
- Report generation success rate

User validation:

- Time for beginners to understand results
- Whether users can fix a problem from the report
- Whether the report is useful to engineers
- Whether last-week comparison is useful
- Willingness to pay

Business validation:

- Would churches pay $29/month?
- Would schools pay $299/year?
- Would installation vendors use it as a maintenance tool?
- Is a $399 hardware box feasible?
- Can revenue start through report services?

## First Seven-Day Execution Plan

1. Temporarily choose product name, fix target to church live-stream speech, and write README.
2. Collect good and bad sermon audio samples and label problem types.
3. Create Python project, implement file-upload analysis, and calculate average, peak, and clipping.
4. Implement FFT analysis and calculate low/mid/high band averages.
5. Build problem-detection rules and scoring system.
6. Build Streamlit screen and display result cards.
7. Create a sample report and show it to two or three church staff or engineers for feedback.

## Key Direction

Do not start by saying:

```text
AI automatically mixes every console.
```

Say this instead:

```text
This is an Audio Guard that automatically checks sound status before a service or event
and explains problems so beginners can understand them.
```

Final product structure:

```text
SoundCheck app
-> Report service
-> Real-time monitoring
-> Hardware box
-> Console-specific control plugins
-> AI EQ Assistant
```

## Conclusion

This idea has stronger revenue potential than starting with X32 AI EQ because it solves broader and more painful problems:

- Users do not know whether today's sound is normal.
- Broadcast audio problems are discovered late.
- Beginner volunteers make mistakes.
- Users do not know how today differs from last week.

Therefore, the first product should start as a **SoundCheck / Audio Guard app**, not an **AI EQ app**.
