# AGENTS.md

This file documents the agent architecture for PM Decision Copilot. It is intended for two audiences -- PMs who want to understand how the system reasons, and developers who want to extend or customize it. It follows Claude Code agent documentation conventions.

---

## Philosophy

Three design principles drove every decision in this system:

1. **Separation of concerns** -- each agent has one job. Discovery does not analyze. Analysis does not critique. This makes each agent's output more focused and easier to evaluate.

2. **Explicit reasoning over fast answers** -- the system is deliberately slower than a single prompt. The extra steps exist to surface assumptions, document tradeoffs, and catch weak reasoning before it becomes a decision.

3. **Self-correction over perfection** -- rather than trying to write a perfect prompt, the Critique Agent catches gaps and triggers revision. This mirrors how good PMs actually work -- first draft, structured review, revision.

---

## Agent 1: Discovery Agent

**File:** `agents/discovery_agent.py`
**Role:** Problem framing and assumption surfacing

The Discovery Agent's job is to slow the user down before going fast. It takes a raw, often vague problem statement and transforms it into a structured problem brief. It does not generate options or recommendations -- that is the Analysis Agent's job.

**Input:**
```json
{
  "problem": "raw user input string",
  "context": "optional additional context",
  "constraints": "optional stated constraints"
}
```

**Output:**
```json
{
  "reframed_problem": "the real decision being made",
  "desired_outcome": "what success looks like with measurable signals",
  "assumptions": ["list of hidden assumptions surfaced"],
  "constraints_identified": ["list of real constraints including unstated ones"]
}
```

**System prompt philosophy:** The agent is instructed to act as a senior PM doing a problem alignment session. It should push back on vague framing, name hidden assumptions explicitly, and restate the problem in terms of a decision that can actually be made -- not a topic to explore.

**What good output looks like:** The reframed problem is more specific than the input. At least two assumptions are surfaced that the user did not explicitly state. Constraints include both stated and inferred ones.

---

## Agent 2: Analysis Agent

**File:** `agents/analysis_agent.py`
**Role:** Options generation, tradeoff mapping, and recommendation

The Analysis Agent receives the Discovery output -- not the original user input. This is intentional. It reasons against a structured problem brief, not a vague question. It generates exactly three options, evaluates each, and makes a recommendation with explicit tradeoffs and risks.

**Input:** the full output JSON from Discovery Agent

**Output:**
```json
{
  "options": [
    {
      "name": "option name",
      "pros": ["list"],
      "cons": ["list"]
    }
  ],
  "recommendation": "which option and why",
  "key_tradeoffs": ["list of explicit tradeoffs"],
  "risks": ["list of real risks with specificity"]
}
```

**System prompt philosophy:** The agent is instructed to generate meaningfully different options -- not variations of the same idea. The recommendation must be tied to the constraints identified by Discovery. Risks must be specific -- generic risks like "regulatory changes" or "market shifts" are not acceptable without concrete mitigation or impact detail.

**What good output looks like:** Three options that represent genuinely different strategic directions. A recommendation that references specific constraints from the Discovery output. Risks that name concrete failure modes, not categories.

**When revision is triggered:** If the Critique Agent scores this output below 7.0, the Analysis Agent receives the critique feedback as an additional input and produces a revised output. The revision must address the specific gaps named in the critique -- not just add more content.

---

## Agent 3: Critique Agent

**File:** `agents/critique_agent.py`
**Role:** Reasoning quality evaluation and revision triggering

The Critique Agent is the most important agent in the system. It does not generate new analysis -- it evaluates the quality of the Analysis Agent's reasoning and decides whether it is good enough to ship as a final output.

It scores across three dimensions:

- **Tradeoff completeness** -- did the analysis surface the real tradeoffs or only the obvious ones? Did it consider second-order effects?
- **Recommendation clarity** -- is the recommendation clearly tied to the problem constraints? Could someone act on it without asking follow-up questions?
- **Risk realism** -- are the risks specific and actionable? Or are they generic placeholders?

**Input:** the full output JSON from Analysis Agent

**Output:**
```json
{
  "scores": {
    "tradeoff_completeness": "0-10",
    "recommendation_clarity": "0-10",
    "risk_realism": "0-10"
  },
  "overall_score": "average of three scores",
  "feedback": "specific gaps and what the revision should address",
  "needs_revision": "true or false"
}
```

**Threshold:** overall score below 7.0 triggers revision. Maximum 2 revision cycles. If the score is still below 7.0 after 2 revisions, the system outputs the best available analysis with the critique feedback included so the user understands the gaps.

**System prompt philosophy:** The agent is instructed to be a tough but fair VP of Product reviewing a decision doc before a leadership presentation. It should name specific gaps, not offer general praise or criticism. Its feedback must be actionable -- specific enough that the Analysis Agent knows exactly what to fix.

---

## Orchestration

**File:** `core/orchestrator.py`

The orchestrator manages the full pipeline and the critique-revision loop. It does not make decisions -- it routes outputs between agents and enforces the retry logic.

**Pipeline flow:**

1. Receive user input
2. Run Discovery Agent -- produce problem brief
3. Run Analysis Agent -- produce options and recommendation
4. Run Critique Agent -- score the analysis
5. If `needs_revision` is true and retry count < 2:
   - pass critique feedback to Analysis Agent
   - increment retry counter
   - go to step 3
6. If `needs_revision` is false or retry count = 2:
   - compile final output
   - save to `logs/` via Memory
   - print formatted summary to terminal

The orchestrator passes the full output of each agent to the next -- not a summary. This preserves all context across the pipeline.

---

## Memory and Persistence

**File:** `core/memory.py`

Two responsibilities:

- **In-session state** -- stores agent outputs in a Python dict during the current run so the orchestrator can pass them between agents without re-running upstream stages.

- **Run persistence** -- saves the complete pipeline output as a JSON log file in `logs/` at the end of each run. File naming convention: `run_<ISO-timestamp>.json`. These logs are gitignored and never committed.

**Log structure:**
```json
{
  "timestamp": "ISO timestamp",
  "input": "original user input",
  "problem_brief": "Discovery Agent output",
  "analysis": "final Analysis Agent output",
  "critique": "final Critique Agent output",
  "iterations": "number of revision cycles"
}
```

---

## How to Extend This

*Written for PMs, not engineers.*

**Adding a new agent:** Create a new file in `agents/`. Give it one responsibility. Define its input and output as JSON schemas before writing any code. Add it to the orchestrator pipeline in `core/orchestrator.py`.

**Changing the critique threshold:** Open `agents/critique_agent.py` and change the `RETRY_THRESHOLD` constant. Default is `7.0`. Lower it for faster runs with less revision. Raise it for higher quality output at the cost of more API calls.

**Customizing for your domain:** The most valuable customization is editing the system prompts in each agent file. If you work in fintech, add fintech-specific risk categories to the Critique Agent prompt. If you work in consumer apps, add retention and engagement tradeoffs to the Analysis Agent prompt. The framework is domain-agnostic by default -- domain specificity makes it dramatically more useful.

**Adding memory across runs:** The current system has no memory between sessions. To add it, extend `core/memory.py` to read prior run logs on startup and inject relevant past decisions as context into the Discovery Agent prompt.

---

## Background

This agent architecture was developed through applied experimentation with agentic PM workflows and refined through hands-on sessions with product teams at enterprise organizations. The core insight -- that a Critique Agent loop produces better reasoning than any single-pass prompt -- emerged from real use on real product decisions.

For questions or contributions, open an issue or pull request.
