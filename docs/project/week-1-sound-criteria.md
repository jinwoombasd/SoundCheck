# Week 1 Sound Criteria and Sample Labeling

Created: 2026-06-29

Related plan: `12-week-development-plan.md`

## Purpose

Define the first-pass criteria for separating good and bad church broadcast speech samples.

This document supports the Week 1 deliverables:

- Problem-type definition document
- Sample labeling table
- Report draft outline

## Target Audio

First target:

- Church live-stream speech
- Sermon microphone
- Host microphone
- Pre-service speech sound check

Out of scope for the first sample set:

- Full worship-band mixes
- Commercial copyrighted audio for external demos
- Console control or automatic EQ changes

## Initial Problem Types

| ID | Problem type | What the listener notices | First-pass detection hint | Beginner-facing explanation |
| --- | --- | --- | --- | --- |
| P1 | Volume too low | Speech is hard to hear compared with normal content | RMS and loudness estimate are below the reference range | The voice may be too quiet for online listeners. |
| P2 | Volume too high | Speech feels too loud or has little headroom | Peaks are close to 0 dBFS or average level is high | The voice may be too loud and could distort during louder moments. |
| P3 | Clipping | Harsh distortion on louder words | Repeated samples near full scale or clipped peak patterns | The audio is hitting the digital limit and may sound distorted. |
| P4 | Too much low end | Voice sounds boomy, thick, or muddy | Excess energy around 80-200Hz | The microphone may have too much low-frequency buildup. |
| P5 | Muddy low mids | Words feel unclear or covered | Excess energy around 200-400Hz | The voice may sound muddy and less easy to understand. |
| P6 | Lack of clarity | Consonants and speech detail are hard to understand | Weak 2-5kHz energy compared with low/mid bands | The voice may need more speech clarity. |
| P7 | Harsh upper mids | Speech feels sharp or tiring | Excess energy around 6-8kHz | The voice may sound harsh or uncomfortable. |
| P8 | High noise floor | Hiss, hum, room noise, or fan noise is noticeable | Noise remains high during pauses | Background noise may be too loud when nobody is speaking. |
| P9 | L/R balance mismatch | Audio leans left or right | Left and right channel levels differ significantly | The stream may sound stronger on one side than the other. |

## Sample Labeling Table

Use one row per audio file.

| Sample ID | File name | Source | Good/Bad | Primary problem | Secondary problems | Notes | Usable for demo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 |  | Sermon / host / test | Good / Bad | P1-P9 | P1-P9 |  | Yes / No |
| S02 |  | Sermon / host / test | Good / Bad | P1-P9 | P1-P9 |  | Yes / No |
| S03 |  | Sermon / host / test | Good / Bad | P1-P9 | P1-P9 |  | Yes / No |

Minimum Week 1 target:

- Five good samples
- Five bad samples
- At least one primary problem label per bad sample
- Notes explaining why each good sample is acceptable

## First Report Draft Layout

The first report should be readable by both volunteers and engineers.

Suggested sections:

1. Title and analysis timestamp
2. File name or input source
3. Overall status: GOOD, WARNING, or DANGER
4. Top three issues
5. Beginner explanation for each issue
6. Suggested next action
7. Engineer details
8. Frequency or band-energy graph placeholder

## Week 1 Completion Criteria

Week 1 is complete when:

- The problem-type list is accepted for the first MVP.
- At least 10 samples are labeled with good/bad status.
- Each bad sample has a primary problem label.
- The report outline is ready to use in Week 2 analysis output.
