# Agent Definitions

This document describes each agent in the `pm-decision-copilot` pipeline, its responsibilities, inputs, and outputs.

---

## Pipeline Overview

```
User Input
    │
    ▼
DiscoveryAgent          (Stage 1)
    │  problem_brief
    ▼
AnalysisAgent           (Stage 2)
    │  analysis_result
    ▼
CritiqueAgent           (Stage 3)
    │
    ├── score >= 7  →  Final Output
    │
    └── score < 7   →  loop back to AnalysisAgent (max 3 retries)
```

---

## DiscoveryAgent

**File:** `agents/discovery_agent.py`  
**Model:** `claude-opus-4-6`

### Purpose
Transforms a raw, often vague PM problem statement into a structured problem brief. Surfaces ambiguity, clarifies assumptions, and identifies key context needed for sound decision-making.

### Input
| Field | Type | Description |
|-------|------|-------------|
| `user_input` | `str` | Raw problem statement from the user |

### Output
```json
{
  "problem_statement": "Refined one-paragraph statement",
  "clarifications": ["assumption 1", "assumption 2"],
  "context": {
    "target_users": "...",
    "success_metrics": "...",
    "constraints": "...",
    "timeline": "...",
    "stakeholders": "..."
  }
}
```

---

## AnalysisAgent

**File:** `agents/analysis_agent.py`  
**Model:** `claude-opus-4-6`

### Purpose
Applies structured PM frameworks to evaluate decision options. Produces a ranked recommendation with supporting rationale and risk assessment.

### Input
| Field | Type | Description |
|-------|------|-------------|
| `problem_brief` | `dict` | Output from DiscoveryAgent |
| `critique_feedback` | `list[str]` | _(optional)_ Prior critique notes for retry iterations |

### Output
```json
{
  "options": [
    {"name": "Option A", "rationale": "...", "risks": ["..."], "score": 8},
    {"name": "Option B", "rationale": "...", "risks": ["..."], "score": 5}
  ],
  "recommendation": "Option A because ...",
  "frameworks_used": ["RICE", "MoSCoW"]
}
```

---

## CritiqueAgent

**File:** `agents/critique_agent.py`  
**Model:** `claude-opus-4-6`

### Purpose
Acts as a devil's advocate. Stress-tests the AnalysisAgent recommendation by challenging assumptions and surfacing blind spots. Assigns a confidence score that drives the retry loop.

### Retry Threshold
`RETRY_THRESHOLD = 7` — scores below this cause the orchestrator to loop back to AnalysisAgent.

### Input
| Field | Type | Description |
|-------|------|-------------|
| `analysis_result` | `dict` | Output from AnalysisAgent |

### Output
```json
{
  "score": 6,
  "critique": "The recommendation underweights retention risk...",
  "passes": false,
  "suggested_improvements": ["Consider churn data", "Add competitive analysis"]
}
```

---

## Orchestrator

**File:** `core/orchestrator.py`

Coordinates the pipeline, manages the critique-loop, and collects run data for memory persistence.

- **Max retries:** `MAX_RETRIES = 3`
- On each retry, CritiqueAgent feedback is injected into AnalysisAgent context.
- After `MAX_RETRIES`, the best-scored result is returned regardless of threshold.

---

## Memory

**File:** `core/memory.py`

Lightweight in-session state + JSON run logs written to `logs/`.

Log filename format: `logs/run_<ISO-timestamp>.json`
