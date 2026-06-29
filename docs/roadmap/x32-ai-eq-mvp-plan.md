# X32 AI EQ MVP Plan

Created: 2026-06-25

Status: Idea refinement

Related note: [[ai-roadmap]]

## One-Line Goal

Build a software MVP that analyzes one vocal/speech channel on a Behringer X32 for 10 seconds, shows EQ recommendations, and applies/reverts them with buttons.

## Product Positioning

This product is not an automatic mixing program that replaces professional engineers.

It is an EQ assistant that helps beginners and non-professional operators handle an X32 more safely.

## Core Users

- Church audio teams
- School auditoriums
- Small venues
- Event teams
- Band rehearsal rooms
- X32 Rack users
- Live-streaming spaces

## MVP Core Features

- [ ] LAN connection to X32
- [ ] Receive X32 USB audio input
- [ ] Select audio device
- [ ] Select one channel
- [ ] 10-second analysis
- [ ] Display RTA/spectrum
- [ ] Generate EQ recommendations
- [ ] Apply recommended EQ
- [ ] Save EQ before application
- [ ] Revert button
- [ ] Show before/after metrics
- [ ] Save analysis report

## First MVP Scope

Support only one channel at first.

Limit the target source to vocal or speech.

Generate at most three recommended EQ changes.

## Explicitly Not in the Initial Scope

- Supporting every console
- Analyzing all channels at once
- Fully automatic mixing
- Training deep-learning models
- Building a hardware box
- Overly flashy UI
- Unlimited automatic changes during performance

## System Structure

```text
X32 USB audio
-> Laptop app
-> Audio analysis
-> EQ recommendation
-> User confirmation
-> Apply X32 EQ over LAN/OSC
```

## Technical Stack

- Language: Python
- X32 control: python-osc
- Audio input: sounddevice or PyAudio
- Analysis: numpy, scipy
- UI: Streamlit first
- Graphs: plotly or matplotlib
- Storage: choose from JSON, CSV, or SQLite

## Draft File Structure

```text
x32-ai-eq/
├─ app.py
├─ x32_controller.py
├─ audio_input.py
├─ analyzer.py
├─ recommender.py
├─ presets.py
├─ reports/
└─ logs/
```

## 12-Week Development Plan

### Week 1 - Prepare X32 Connection

- [ ] Connect X32 and laptop to the same network
- [ ] Confirm X32 IP address
- [ ] Configure Python development environment
- [ ] Install python-osc
- [ ] Research X32 OSC address structure
- [ ] Test changing channel 1 EQ gain

Success criteria:

```text
When a command is sent from the computer, the X32 channel 1 EQ value actually changes.
```

### Week 2 - X32 EQ Control Module

- [ ] Channel-number selection
- [ ] EQ-band selection
- [ ] Frequency setting
- [ ] Gain setting
- [ ] Q setting
- [ ] EQ on/off setting
- [ ] Save current EQ values
- [ ] Revert function

Success criteria:

```text
The program can apply and revert EQ on the desired channel.
```

### Week 3 - USB Audio Input

- [ ] Connect X32 USB audio
- [ ] Display audio-device list
- [ ] Select X32 input device
- [ ] Select input channel
- [ ] Implement level meter
- [ ] Save input-level logs

Success criteria:

```text
When someone speaks into the microphone, the app level meter moves.
```

### Week 4 - RTA/Spectrum Display

- [ ] Implement FFT analysis
- [ ] Display 20Hz-20kHz graph
- [ ] Implement 1/3-octave or simple RTA
- [ ] Save 10-second average spectrum
- [ ] Add analysis button

Success criteria:

```text
The low, mid, and high frequency distribution of speech is visible on screen.
```

### Week 5 - First EQ Recommendation Logic

- [ ] Write HPF recommendation rules
- [ ] Detect 200-400Hz muddiness
- [ ] Detect 2-5kHz clarity
- [ ] Detect 6-8kHz harshness
- [ ] Limit recommendations to at most three EQ changes
- [ ] Limit maximum boost to +2dB
- [ ] Limit maximum cut to -3dB

Success criteria:

```text
After 10 seconds of analysis, the app returns two or three EQ recommendations.
```

### Week 6 - Apply/Revert Flow

- [ ] Preview recommendation results
- [ ] Implement apply button
- [ ] Automatically save current EQ before application
- [ ] Implement revert button
- [ ] Save apply logs
- [ ] Show errors on failure

Success criteria:

```text
Applying a recommendation changes X32 EQ, and reverting returns to the previous state.
```

### Week 7 - App UI Cleanup

- [ ] X32 IP input
- [ ] Connection status display
- [ ] Audio-device selection
- [ ] Channel selection
- [ ] Analysis button
- [ ] Recommendation results display
- [ ] Apply/revert buttons
- [ ] Graph area layout

Success criteria:

```text
The full flow can be controlled on screen instead of from the terminal.
```

### Week 8 - Before/After Metrics

- [ ] Calculate problem-band peak reduction
- [ ] Calculate frequency-balance error
- [ ] Calculate low-end excess index
- [ ] Calculate clarity-band ratio
- [ ] Calculate average-level difference before/after
- [ ] Save report

Success criteria:

```text
The app can show before/after differences numerically.
```

### Week 9 - First Field Test

- [ ] Recruit three test locations
- [ ] Test with the same microphone and placement
- [ ] Record before sample
- [ ] Apply recommendations
- [ ] Record after sample
- [ ] Record metrics
- [ ] Run blind-listening comparison with three to five people

Success criteria:

```text
At least three real-use data sets are collected.
```

### Week 10 - Recommendation Algorithm Improvement

- [ ] Fix excessive low-end cuts
- [ ] Fix excessive high-frequency boosts
- [ ] Stop analysis when input level is too low
- [ ] Review speech/music distinction rules
- [ ] Prevent repeated changes to the same band
- [ ] Show warnings for large changes

Success criteria:

```text
Field tests show fewer risky or awkward recommendations.
```

### Week 11 - Demo Quality

- [ ] Choose project name
- [ ] Clean up first screen
- [ ] Add demo mode
- [ ] Clean up before/after graphs
- [ ] Create report example
- [ ] Write a three-minute demo scenario

Success criteria:

```text
A new viewer can understand the product value within three minutes.
```

### Week 12 - MVP Packaging

- [ ] Document installation
- [ ] Document required equipment
- [ ] Document X32 routing
- [ ] Clean up error messages
- [ ] Write test checklist
- [ ] Record demo video

Success criteria:

```text
Another person can run the app by following the guide.
```

## Validation Metrics

### Technical Validation

- [ ] X32 EQ control success rate
- [ ] Revert success rate
- [ ] Audio input stability
- [ ] Analysis time
- [ ] App error count

### Audio Validation

- [ ] Feedback margin improvement in dB
- [ ] Problem-band peak reduction
- [ ] Frequency-balance error reduction
- [ ] Clarity-band ratio change
- [ ] Average-level difference before/after

### User Validation

- [ ] Time for beginners to understand the app
- [ ] Trust in recommendations
- [ ] Confidence provided by revert function
- [ ] Blind-test preference
- [ ] Actual willingness to pay

## Business Validation Questions

- [ ] Would church audio teams pay a monthly subscription?
- [ ] Does this app actually make beginners less anxious?
- [ ] Is the biggest pain for X32 users EQ, feedback, or routing?
- [ ] Can software alone be sold, or is a hardware box required?
- [ ] Which console should be supported second?

## Next Steps

- [ ] Start with X32 OSC control testing
- [ ] Verify X32 USB audio input
- [ ] Build the channel 1 vocal analysis screen
- [ ] Implement rule-based EQ recommendations
- [ ] Run the first test in a real space
