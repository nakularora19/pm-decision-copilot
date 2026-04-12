# PM Decision Copilot

A multi-agent AI framework that helps product managers structure complex decisions through sequential reasoning, critique, and revision loops.

---

## Why I Built This

I'm a product manager with 10+ years of experience working on marketplace, search, and monetization problems. I kept running into the same pattern: a vague question from a stakeholder, pressure to decide fast, and AI tools that gave answers without helping me think.

I built this framework to solve that for myself first. I wanted a system that could take a messy product question, surface assumptions, force explicit tradeoffs, critique weak reasoning, and improve the recommendation before I acted on it.

I've used versions of this workflow on generalized decision types such as ranking tradeoffs, feature prioritization, and monetization vs user experience questions. The critique loop in particular changed how I reason through hard problems because it forces weaknesses to become visible before a recommendation feels complete.

After sharing the workflow with a few PM peers, I saw that the structure itself was useful beyond my own use cases. That made me want to open-source it so other PMs can run structured decision reasoning without needing a large engineering setup behind them.

This is not a polished product. It is a working system that I use, believe in, and want to keep improving.

All examples in this repository are generalized and sanitized. They do not reflect proprietary systems, confidential metrics, or company-specific implementation details.

---

## The Problem

Product managers face decisions with incomplete information, competing stakeholder goals, and pressure for speed. Most AI tools generate answers quickly but skip explicit reasoning, undocumented tradeoffs, and shared clarity. This framework treats AI as a decision support layer, not an answer machine.

---

## How It Works

Three specialized agents run sequentially:

- **Discovery Agent** : reframes the raw problem, surfaces hidden assumptions, identifies real constraints
- **Analysis Agent** : generates 3 distinct options with pros/cons, recommends a path with explicit tradeoffs and risks
- **Critique Agent** : scores the reasoning quality 0-10 across three dimensions: tradeoff completeness, recommendation clarity, risk realism. If the overall score is below 7.0, sends specific feedback back to the Analysis Agent and triggers a revision. Max 2 revision cycles.

---

## What Makes This Different

Most AI tools generate answers in a single pass. They may sound confident, but they often skip explicit reasoning, undocumented tradeoffs, and self-evaluation.

This system is different in three ways:

1. **Separation of reasoning stages**
   Discovery, analysis, and critique are handled independently instead of being collapsed into one prompt.

2. **Explicit evaluation of decision quality**
   The critique agent scores outputs across tradeoff completeness, recommendation clarity, and risk realism.

3. **Iterative improvement loop**
   If the reasoning is weak, the system sends targeted feedback back to the analysis stage and revises the output before finalizing it.

The goal is not to make AI sound smarter.

The goal is to make product reasoning more explicit, reviewable, and improvable.

---

## Architecture

```
User Input
    ↓
Discovery Agent  →  Problem Brief
    ↓
Analysis Agent   →  Options + Recommendation
    ↓
Critique Agent   →  Score + Feedback
    ↓ (if score < 7.0)
Analysis Agent   →  Revised Analysis
    ↓ (if score ≥ 7.0)
Final Output     →  Saved to logs/
```

---

## Example Output

From [`examples/sponsored_ranking_decision.md`](examples/sponsored_ranking_decision.md) -- pipeline run on a sponsored search ranking decision:

**Recommendation**

> Graduated Prominence with Performance Gates is the optimal choice because it provides measurable revenue growth while protecting user experience through quantified guardrails. This approach allows for systematic testing of increased sponsored prominence while maintaining clearly defined user experience guardrails and rollback criteria.

**Critique Scores**

| Dimension | Score |
|---|---|
| Tradeoff completeness | 8 / 10 |
| Recommendation clarity | 7 / 10 |
| Risk realism | 6 / 10 |
| **Overall** | **7.0 / 10** |

See the full output -- including all three options, tradeoffs, risks, and detailed critique feedback -- in [`examples/sponsored_ranking_decision.md`](examples/sponsored_ranking_decision.md).

---

## Quickstart

```bash
git clone https://github.com/nakularora19/pm-decision-copilot
cd pm-decision-copilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python3 main.py
```

For the Streamlit UI:

```bash
streamlit run app.py
```

---

## Project Structure

```
pm-decision-copilot/
├── agents/
│   ├── discovery_agent.py      # Stage 1: reframes problem, surfaces assumptions and constraints
│   ├── analysis_agent.py       # Stage 2: generates 3 options, recommends a path, lists risks
│   └── critique_agent.py       # Stage 3: scores reasoning quality, triggers revision if needed
├── core/
│   ├── orchestrator.py         # Runs the pipeline, manages the critique-revision loop
│   └── memory.py               # In-session state and JSON run persistence to logs/
├── examples/
│   ├── README.md               # Guide to reading pipeline outputs
│   ├── sponsored_ranking_decision.md   # Real output: sponsored search prominence decision
│   └── uber_guaranteed_earnings.md     # Example input ready to run
├── logs/                       # Auto-generated run logs (JSON, gitignored)
├── config.py                   # Loads ANTHROPIC_API_KEY from .env, returns Anthropic client
├── main.py                     # CLI entry point
├── app.py                      # Streamlit UI
├── AGENTS.md                   # Full agent specs: inputs, outputs, system prompts
├── requirements.txt            # anthropic, python-dotenv, streamlit
└── .env                        # Your API key (not committed)
```

---

## Design Decisions

This system intentionally prioritizes decision clarity over generative flexibility.

Four deliberate tradeoffs worth understanding before you extend this:

**Three separate agents vs one prompt**
Specialization improves output quality. Each agent has a focused system prompt and a single responsibility. The cost is latency and API spend -- three calls per pass instead of one.

**Critique loop with threshold vs single pass**
Self-correction catches reasoning gaps that a single-pass prompt misses. The tradeoff is added complexity: you need a scoring rubric, a retry mechanism, and a ceiling on iterations to avoid infinite loops.

**Structured JSON throughout**
Every agent outputs valid JSON with a defined schema. This makes outputs composable, loggable, and usable downstream. The constraint is that it limits freeform exploration -- the model must fit its reasoning into a fixed structure.

**Claude only, no LangChain**
No abstraction layers. The agent logic is plain Python and direct Anthropic SDK calls. This makes the code transparent, auditable, and easy to modify without understanding a framework's internals.

---

## When This Should Not Be Used

This system is not designed for:

- highly technical system architecture decisions
- legal, medical, or policy decisions requiring domain experts
- situations where live data analysis is required for accuracy
- fully autonomous decision-making without human review

It is most useful for early- to mid-stage product decisions where ambiguity is high and structured reasoning matters more than perfect certainty.

---

## Background

This framework was developed through applied experimentation with agentic AI workflows and refined through sessions with product teams at enterprise organizations. It is intentionally open-source so any PM team can clone and run it without requiring engineering support.

---

## Privacy

All examples are sanitized and intentionally generalized.

No personal information, proprietary data, internal metrics, confidential business context, or company-identifying implementation details are included anywhere in this repository.

---

## License

MIT
