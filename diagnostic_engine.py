You are a senior industrial automation engineer, instrumentation engineer, Python developer, AI engineer, and hackathon software architect.

I want you to build a COMPLETE, WORKING Stage-1 hackathon project called:

# AI INSTRUMENTATION ENGINE

### Intelligent Instrument Health Monitoring, Fault Diagnosis & Troubleshooting System

The project must be a REAL WORKING APPLICATION, not a conceptual prototype and not just an AI chatbot.

The objective is to demonstrate how an AI instrumentation engineer can monitor a virtual industrial process, detect instrumentation abnormalities, determine probable root causes, and provide an actionable troubleshooting procedure.

I have instrumentation/E&I engineering experience, so the engineering logic must be technically credible and understandable to an industrial instrumentation engineer.

---

# 1. TECHNOLOGY STACK

Use only simple technologies so the project can be completed quickly.

Required:

* Python 3.10+
* Streamlit
* Pandas
* NumPy
* Plotly
* Groq API
* LangGraph only if it genuinely simplifies the multi-agent workflow
* python-dotenv

Do NOT require:

* Next.js
* FastAPI
* Docker
* Kubernetes
* PostgreSQL
* Qdrant
* cloud infrastructure
* real PLC hardware
* real sensors
* OPC UA in Stage 1
* Modbus hardware

The application must run locally with:

```bash
streamlit run app.py
```

---

# 2. CORE ARCHITECTURE

Build the system around:

## 3 AI SPECIALIST AGENTS

### Agent 1 — Diagnostic Engineer

Purpose:

Determine WHAT is abnormal.

Inputs may include:

* process variables
* transmitter PV
* 4–20 mA signal
* engineering range
* instrument status
* trends
* redundant instrument values
* PLC values
* control valve command
* control valve feedback
* instrument air pressure

Output:

* abnormal instrument
* abnormal parameter
* severity
* evidence
* confidence
* initial diagnosis

---

### Agent 2 — Root Cause Engineer

Purpose:

Determine WHY the abnormality may be occurring.

It must consider multiple possible causes instead of immediately assuming the instrument is faulty.

For example:

Possible causes for abnormal pressure:

1. Genuine process pressure change
2. Transmitter calibration drift
3. Sensor failure
4. Impulse-line blockage
5. Wiring problem
6. Analog input problem
7. Power supply problem

The agent must rank the possible causes based on available evidence.

IMPORTANT:

Do not let the LLM invent sensor measurements.

All numerical measurements must come from the simulated plant or engineering calculation engine.

---

### Agent 3 — Troubleshooting Engineer

Purpose:

Determine WHAT THE TECHNICIAN SHOULD DO NEXT.

The output should contain:

1. Safety precautions
2. Required tools
3. Step-by-step troubleshooting procedure
4. Expected measurement
5. Actual measurement
6. Pass/fail decision
7. Next action
8. Escalation recommendation if required

The troubleshooting procedure should resemble a real industrial maintenance procedure.

---

# 3. IMPORTANT ENGINEERING RULE

DO NOT allow the LLM to perform fundamental engineering calculations when deterministic Python calculations can do them.

Create an Engineering Diagnostic Engine using Python.

For example:

For a 4–20 mA transmitter:

PV = LRV + ((mA - 4) / 16) × (URV - LRV)

Example:

LRV = 0 bar
URV = 16 bar
Current = 12 mA

Expected PV:

8 bar

The Python engine must perform these calculations.

The AI agents should receive the calculated evidence and reason about it.

Architecture:

Virtual Plant
↓
Engineering Calculation / Rule Engine
↓
Fault Detection
↓
Diagnostic Agent
↓
Root Cause Agent
↓
Troubleshooting Agent
↓
Final Engineering Report

---

# 4. VIRTUAL INDUSTRIAL PROCESS

Create a virtual tank/process system.

The system should include:

## Tank T-101

Variables:

* Tank level
* Tank pressure
* Tank temperature
* Flow
* inlet flow
* outlet flow

Create realistic changing values rather than completely random numbers.

For example:

Normal operating conditions:

Level: 50–70 %
Pressure: approximately 7–9 bar
Temperature: approximately 80–90 °C
Flow: approximately 150–200 m³/h

Use a simple dynamic simulation so values gradually change over time.

---

# 5. INSTRUMENTS

At minimum implement:

### PT-101

Pressure Transmitter

Range:

0–16 bar

Output:

4–20 mA

### PT-102

Redundant/reference Pressure Transmitter

Range:

0–16 bar

Output:

4–20 mA

### LT-101

Level Transmitter

Range:

0–100 %

Output:

4–20 mA

### TT-101

Temperature Transmitter

Range:

0–150 °C

Output:

4–20 mA

### FT-101

Flow Transmitter

Range:

0–300 m³/h

Output:

4–20 mA

### CV-101

Control Valve

Parameters:

* Command %
* Position feedback %
* Instrument air pressure
* valve status

---

# 6. FAULT INJECTION SYSTEM

This is one of the most important parts of the demo.

Create a Streamlit sidebar called:

# FAULT INJECTION

Allow the user to inject faults manually.

At minimum provide:

### Fault 1

PT-101 transmitter drift

Example:

Actual process pressure = 8 bar

PT-101 reports:

11.5 bar

---

### Fault 2

4–20 mA loop fault

Example:

Actual pressure = 8 bar

Expected signal ≈ 12 mA

Injected signal = 3.6 mA

---

### Fault 3

Stuck transmitter

PT-101 remains fixed at 8 bar while process pressure changes.

---

### Fault 4

Impulse line blockage

Make transmitter response slow or incorrect compared with actual process pressure.

---

### Fault 5

Control valve problem

Example:

Command = 80%

Feedback = 35%

---

### Fault 6

Low instrument air

Example:

Normal air pressure = 6 bar

Fault = 3.5 bar

---

### Fault 7

Sensor disagreement

PT-101 = 12.5 bar

PT-102 = 8.0 bar

while the actual process remains around 8 bar.

---

# 7. DETERMINISTIC FAULT DETECTION

Before calling the AI, create Python rules.

Examples:

IF:

abs(PT101 - PT102) > threshold

THEN:

flag sensor disagreement.

IF:

command - valve_feedback > threshold

THEN:

flag possible valve problem.

IF:

mA < 3.8 or mA > 20.5

THEN:

flag possible signal/loop fault.

IF:

transmitter value does not change while process changes

THEN:

flag possible stuck transmitter.

IF:

instrument air < minimum threshold

THEN:

flag pneumatic/control valve problem.

These rules should generate an "evidence package".

Example:

```python
{
    "instrument": "PT-101",
    "pv": 12.5,
    "reference_pv": 8.0,
    "loop_current": 19.6,
    "expected_current": 12.0,
    "deviation": 4.5,
    "sensor_disagreement": True,
    "process_stable": True
}
```

---

# 8. MULTI-AGENT WORKFLOW

Implement the three agents as a sequential workflow.

Preferred architecture:

```text
START
 ↓
Engineering Diagnostic Engine
 ↓
Diagnostic Agent
 ↓
Root Cause Agent
 ↓
Troubleshooting Agent
 ↓
Final Report
 ↓
END
```

If using LangGraph, create a proper StateGraph.

Use a shared state object containing:

* plant data
* instrument data
* detected abnormalities
* engineering calculations
* diagnostic findings
* root causes
* troubleshooting procedure

Do NOT create unnecessary agents.

Exactly three AI specialist agents should be used.

---

# 9. GROQ INTEGRATION

Use Groq API through an environment variable:

```text
GROQ_API_KEY=your_key_here
```

Create:

```text
.env
```

and:

```text
.env.example
```

Never hard-code the API key.

Use an appropriate currently available Groq model, but make the model name configurable through an environment variable.

For example:

```text
GROQ_MODEL=...
```

If the model name changes, I should only need to modify `.env`.

---

# 10. AI PROMPTS

Create separate system prompts for:

1. Diagnostic Engineer
2. Root Cause Engineer
3. Troubleshooting Engineer

The agents must behave like industrial instrumentation engineers.

They must:

* use the supplied evidence
* avoid inventing measurements
* clearly distinguish facts from hypotheses
* state uncertainty
* avoid claiming certainty when evidence is insufficient
* recommend verification measurements
* prioritize safety

The Root Cause Agent must NOT simply say:

"Transmitter is faulty."

It should say something like:

"PT-101 is reporting significantly higher pressure than PT-102 while the process trend remains stable. This makes transmitter measurement error a plausible cause. However, the actual process pressure should be verified using an independent calibrated gauge before replacing the transmitter."

---

# 11. STREAMLIT HMI

Create a professional-looking industrial dashboard.

Layout:

## Header

AI INSTRUMENTATION ENGINE

Subtitle:

Intelligent Instrument Health & Fault Diagnosis

---

## Section 1 — Plant Overview

Display:

* Tank level
* Pressure
* Temperature
* Flow
* Valve position
* Instrument air

Use gauges/cards where appropriate.

---

## Section 2 — Instrument Health

Create a table:

| Instrument |       PV |  Signal | Health | Status |
| ---------- | -------: | ------: | -----: | ------ |
| PT-101     |  8.1 bar | 12.1 mA |    98% | NORMAL |
| PT-102     |  8.0 bar | 12.0 mA |    97% | NORMAL |
| LT-101     |      62% | 13.9 mA |    96% | NORMAL |
| TT-101     |     86°C | 13.2 mA |    95% | NORMAL |
| FT-101     | 181 m³/h | 13.7 mA |    94% | NORMAL |
| CV-101     |      70% |  69% FB |    96% | NORMAL |

Health scores must be calculated from actual simulated conditions/rules, not randomly generated.

---

# 12. TREND GRAPHS

Add Plotly graphs for:

* pressure vs time
* level vs time
* temperature vs time
* flow vs time
* transmitter PV vs reference PV
* valve command vs feedback

The graphs must update as the simulation runs.

---

# 13. FAULT INJECTION UI

Sidebar:

```text
PROCESS CONTROL

[Start Simulation]

[Stop Simulation]

FAULT INJECTION

○ No Fault
○ PT-101 Drift
○ 4–20 mA Fault
○ Stuck Transmitter
○ Impulse Line Blockage
○ Control Valve Fault
○ Low Instrument Air
○ Sensor Disagreement

[Inject Fault]
```

Make the fault immediately visible on the HMI.

---

# 14. AI DIAGNOSIS BUTTON

Create a large button:

# 🔍 RUN AI DIAGNOSIS

When clicked:

1. Read current simulated plant data
2. Run engineering calculations
3. Run deterministic fault detection
4. Send evidence to Diagnostic Agent
5. Send diagnostic output to Root Cause Agent
6. Send results to Troubleshooting Agent
7. Display final engineering report

---

# 15. FINAL AI REPORT

Create a professional report:

## Instrument Under Investigation

PT-101

## Severity

HIGH

## Detected Condition

Pressure transmitter disagreement.

## Evidence

* PT-101 = 12.5 bar
* PT-102 = 8.0 bar
* Process pressure trend = approximately 8 bar
* Calculated expected current = approximately 12 mA
* Measured current = 19.6 mA

## Probable Causes

Show several possible causes with reasoning.

## Recommended Troubleshooting

Numbered procedure.

## Required Tools

For example:

* calibrated pressure gauge
* multimeter
* HART communicator if applicable
* test leads

## Technician Decision Tree

Example:

```text
Verify actual pressure
        │
        ├── Pressure actually high
        │       ↓
        │   Investigate process
        │
        └── Pressure normal
                ↓
        Check transmitter loop
                │
                ├── Loop abnormal
                │      ↓
                │   Check wiring/AI
                │
                └── Loop normal
                       ↓
                  Check calibration
```

---

# 16. SAFETY

Add a visible warning:

"AI recommendations are decision-support only. Follow plant procedures, permit-to-work requirements, isolation/LOTO procedures, and qualified-person verification before physical intervention."

The AI must never instruct a technician to bypass safety systems.

---

# 17. FILE STRUCTURE

Create a clean project:

```text
ai-instrumentation-engineer/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── agents/
│   ├── __init__.py
│   ├── diagnostic_agent.py
│   ├── root_cause_agent.py
│   └── troubleshooting_agent.py
│
├── simulation/
│   ├── __init__.py
│   └── virtual_plant.py
│
├── engineering/
│   ├── __init__.py
│   └── diagnostic_engine.py
│
├── ui/
│   ├── __init__.py
│   └── dashboard.py
│
└── utils/
    ├── __init__.py
    └── groq_client.py
```

Keep the architecture simple enough that I can understand and modify it.

---

# 18. REQUIREMENTS.TXT

Generate a complete requirements.txt containing only the packages actually required.

Avoid unnecessary dependencies.

---

# 19. README

The README must contain:

* Project overview
* Features
* Architecture
* Multi-agent explanation
* Installation
* API key setup
* Running instructions
* Fault injection instructions
* Example demo
* Future development
* Hackathon pitch

---

# 20. HACKATHON DEMO

Make sure the project supports this exact demonstration:

### Step 1

Start the virtual plant.

Everything is NORMAL.

### Step 2

Show:

PT-101 = approximately 8 bar

PT-102 = approximately 8 bar

### Step 3

Inject:

PT-101 transmitter drift.

PT-101 becomes:

12.5 bar

while PT-102 remains around:

8 bar.

### Step 4

Click:

RUN AI DIAGNOSIS

### Step 5

Show:

Diagnostic Agent:

"PT-101 measurement is inconsistent with the redundant transmitter and process behavior."

### Step 6

Root Cause Agent:

Provide probable causes and evidence.

### Step 7

Troubleshooting Agent:

Provide technician troubleshooting steps.

### Step 8

Repeat with:

Control valve fault.

Command = 80%

Feedback = 35%

The AI should diagnose possible valve/positioner/air/mechanical issues.

---

# 21. IMPORTANT CODING REQUIREMENTS

I want ACTUAL CODE.

Do not give me pseudocode.

Do not leave TODO placeholders.

Do not say "implement this later."

Every file must be complete and executable.

Handle:

* missing GROQ_API_KEY
* Groq API errors
* invalid responses
* simulation errors
* empty diagnostic results

The application must still run in DEMO MODE if no Groq API key is available.

In DEMO MODE, use deterministic engineering responses so I can demonstrate the application without an API key.

---

# 22. OUTPUT FORMAT

First give me the complete project architecture.

Then provide every file separately.

For each file use:

```text
FILE: app.py
```

followed by the complete code.

Then:

```text
FILE: agents/diagnostic_agent.py
```

and so on.

Do NOT omit any file.

After all files, provide:

1. Installation commands
2. .env setup
3. Run command
4. Exact hackathon demonstration procedure
5. Explanation of how the 3 agents communicate
6. Explanation of how the engineering rule engine works
7. Common errors and fixes

Before finishing, perform a consistency check mentally and make sure:

* all imports exist
* all functions called actually exist
* file paths are correct
* Streamlit can launch app.py
* Groq integration is consistent
* LangGraph state is consistent if used
* no undefined variables exist
* no API key is hard-coded
* the demo can run without Groq using DEMO MODE

The priority is:

1. WORKING SOFTWARE
2. ENGINEERING CREDIBILITY
3. IMPRESSIVE HACKATHON DEMO
4. CLEAN CODE
5. AI sophistication

Do not over-engineer Stage 1.
