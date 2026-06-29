# AI Roadmap

Created: 2026-06-25

Status: Expansion plan after MVP

Related note: [[x32-ai-eq-mvp-plan]]

## Core Direction

Do not start by asking deep learning to judge every sound.

Start safely with rule-based analysis, collect field data, and add AI features step by step.

## Final Goal for AI Features

```text
Understand source type, problem frequency range, venue characteristics, and user intent,
then automatically create safe EQ recommendations.
```

## Phase Strategy

### Phase 0 - Start Without AI

Goal:

```text
Build the MVP with rule-based EQ recommendations.
```

Why this phase does not use AI:

- There is no data yet.
- Live sound has high risk when recommendations are wrong.
- Rule-based logic is explainable and easier to debug.
- Stability matters more than AI for a beginner-focused MVP.

Features to implement:

- [ ] HPF recommendation
- [ ] Muddy band detection
- [ ] Harsh band detection
- [ ] Clarity band detection
- [ ] Problem-band peak display
- [ ] Maximum change limits
- [ ] Revert function

Success criteria:

```text
The system can produce non-dangerous recommendations for vocal/speech channels.
```

## Phase 1 - Prepare AI Through Data Collection

Goal:

```text
Collect data that can later train AI.
```

Data to collect:

- [ ] Input audio spectrum
- [ ] EQ state before application
- [ ] Recommended EQ values
- [ ] Whether the user applied the recommendation
- [ ] Whether the user reverted the recommendation
- [ ] Before/after measurements
- [ ] Source type
- [ ] Room type
- [ ] Microphone type
- [ ] Speaker type
- [ ] User subjective rating

Example data:

```json
{
  "source_type": "speech",
  "room_type": "church",
  "channel": 1,
  "detected_problem": "muddy",
  "suggestion": {
    "freq": 315,
    "gain": -2.5,
    "q": 1.8
  },
  "user_applied": true,
  "user_reverted": false,
  "pre_peak_db": 6.8,
  "post_peak_db": 2.1,
  "rating": 4
}
```

Notes:

- [ ] Be careful about whether recording files are stored so personal information is not included.
- [ ] Review storing feature values instead of raw audio.
- [ ] Get consent for data use from field-test participants.

Success criteria:

```text
Secure at least 30 field-test records containing analysis, recommendations, and user reactions.
```

## Phase 2 - Source Classification AI

Goal:

```text
Classify whether the input sound is vocal, speech, guitar, keyboard, drums, or music playback.
```

Why it matters:

The same 300Hz range can be muddiness for a vocal and necessary body for an instrument.

Initial classes:

- [ ] Speech
- [ ] Vocal
- [ ] Music playback
- [ ] Guitar
- [ ] Keyboard
- [ ] Unknown

Input features:

- [ ] Average spectrum
- [ ] MFCC
- [ ] Spectral centroid
- [ ] Spectral rolloff
- [ ] RMS level
- [ ] Zero crossing rate

Model candidates:

- [ ] Random Forest
- [ ] XGBoost
- [ ] Small CNN
- [ ] Pretrained audio embedding model

Success criteria:

```text
Classify speech, vocal, and music playback with at least 85% accuracy.
```

## Phase 3 - Problem-Band Detection AI

Goal:

```text
Automatically detect problems such as muddiness, harshness, excessive low end, and lack of clarity.
```

Problems to classify:

- [ ] Muddy
- [ ] Boomy
- [ ] Harsh
- [ ] Boxy
- [ ] Nasal
- [ ] Dull
- [ ] Thin
- [ ] Feedback risk

Output:

```text
Problem type
Center frequency
Severity
Recommended direction
Confidence
```

Example:

```json
{
  "problem": "muddy",
  "frequency": 315,
  "severity": 0.72,
  "recommendation": "cut",
  "confidence": 0.81
}
```

Success criteria:

```text
The problem bands found by AI generally match problem bands marked by engineers.
```

## Phase 4 - EQ Recommendation AI

Goal:

```text
Recommend specific EQ values based on detected problems.
```

Output values:

- [ ] Frequency
- [ ] Gain
- [ ] Q
- [ ] HPF frequency
- [ ] Application priority
- [ ] Risk level

Safety limits:

- [ ] Maximum boost +2dB
- [ ] Maximum cut -3dB
- [ ] Q from 1.0 to 3.0
- [ ] Maximum three recommendations
- [ ] Limit output-level changes
- [ ] No automatic application during live performance

Training data:

- [ ] EQ changes made by experts
- [ ] Recommendations applied by users
- [ ] Recommendations reverted by users
- [ ] Before/after measurements
- [ ] Blind-listening preferences

Success criteria:

```text
At least 70% of applied recommendations are not reverted by users.
```

## Phase 5 - Personalization and Room Adaptation

Goal:

```text
Make recommendations improve over time for each room, user preference, and microphone/speaker combination.
```

Personalization factors:

- [ ] Target curve by room
- [ ] Church sermon preset
- [ ] Band vocal preset
- [ ] Live-streaming preset
- [ ] Recommendation patterns users often revert
- [ ] Recommendation patterns users often apply

Example feature:

```text
This room tends to have too much 250Hz.
Future analyses will apply a stricter 250Hz reference.
```

Success criteria:

```text
Repeated use in the same venue reduces the number of needed corrections.
```

## Phase 6 - Natural-Language Sound Requests

Goal:

```text
Let users describe the sound they want in natural language instead of technical terms, then suggest EQ candidates.
```

Example inputs:

- [ ] The vocal is too muddy
- [ ] The sermon is hard to hear
- [ ] The sound is harsh
- [ ] Bring the vocal slightly forward
- [ ] There is too much low end
- [ ] It feels like feedback may happen

Example output:

```text
To reduce muddiness, cutting 315Hz by -2dB is recommended.
For clarity, 3.2kHz could be raised by +1dB, but it is safer to apply only the cut first.
```

Notes:

- Use natural-language features for explanation/recommendation before automatic application.
- If the user's wording is ambiguous, recommend only safe changes.
- Explain the reason for changes in a way humans can understand.

Success criteria:

```text
Beginners can request the adjustment they want without professional EQ terminology.
```

## Phase 7 - Multi-Console-Compatible AI

Goal:

```text
Keep one shared AI analysis engine and support multiple consoles by swapping only console-control adapters.
```

Structure:

```text
AI analysis engine
-> Common EQ command
-> Console-specific adapter
-> X32 / M32 / WING / SQ / QU / Yamaha, etc.
```

Common EQ command example:

```json
{
  "channel": 1,
  "band": 2,
  "freq": 315,
  "gain": -2.5,
  "q": 1.8
}
```

Console-specific adapters:

- [ ] X32/M32 OSC adapter
- [ ] Behringer WING adapter
- [ ] Allen & Heath SQ adapter
- [ ] Allen & Heath QU adapter
- [ ] Yamaha TF/DM3 adapter
- [ ] Soundcraft adapter

Success criteria:

```text
New consoles can be supported by adding adapters without changing AI recommendation logic.
```

## AI Development Priority

1. Rule-based recommendations
2. Data collection
3. Source classification
4. Problem-band detection
5. EQ recommendation model
6. Room/user personalization
7. Natural-language requests
8. Multi-console compatibility

## What AI Must Not Do

- [ ] Make large EQ changes during performance without user approval
- [ ] Automatically apply low-confidence recommendations
- [ ] Suddenly change output level significantly
- [ ] Over-change many bands at once
- [ ] Rely only on a slow model during feedback situations
- [ ] Make changes without explanations users can understand

## AI Safety Principles

```text
Recommend small changes
Explain clearly
Let the user apply
Always make revert possible
```

## First 100 Data Targets

- [ ] 30 church speech samples
- [ ] 30 vocal samples
- [ ] 20 music playback samples
- [ ] 20 rehearsal-room/small-venue samples

Each data item should include:

- [ ] Source type
- [ ] Room type
- [ ] Input spectrum
- [ ] Recommended EQ
- [ ] Applied or not
- [ ] Reverted or not
- [ ] Before/after measurements
- [ ] User rating

## Long-Term Vision

Ultimately, build a live-sound AI assistant that works regardless of console brand.

However, starting with a single X32 vocal/speech EQ recommendation flow is enough.
