# PM Decision Copilot

A multi-agent AI framework that helps product managers structure complex decisions through sequential reasoning, critique, and revision loops.

---

## Why I Built This

I'm a product manager with 10+ years building marketplace and search products. I found myself facing the same pattern repeatedly -- a vague question from a stakeholder, pressure to decide fast, and AI tools that gave me answers without helping me think.

I built this framework to fix that for myself first. I've used it on real decisions -- sponsored ranking strategy, feature prioritization, monetization tradeoffs -- and found that the critique loop in particular changed how I reason through hard problems. It forces explicit tradeoffs before you commit to a recommendation.

After using it internally, I walked a few PM peers through the workflow. Several of them have since adopted versions of it within their own teams. That response made me want to open-source it -- so any PM, at any company, can run structured multi-agent reasoning on their hardest decisions without needing an engineering team behind them.

This is not a polished product. It is a working framework that I use and believe in.

---

## The Problem

Product managers face decisions with incomplete information, competing stakeholder goals, and pressure for speed. Most AI tools generate answers quickly but skip explicit reasoning, undocumented tradeoffs, and shared clarity. This framework treats AI as a decision support layer -- not an answer machine.

---

## How It Works

Three specialized agents run sequentially:

- **Discovery Agent** -- reframes the raw problem, surfaces hidden assumptions, identifies real constraints
- **Analysis Agent** -- generates 3 distinct options with pros/cons, recommends a path with explicit tradeoffs and risks
- **Critique Agent** -- scores the reasoning quality 0-10 across three dimensions: tradeoff completeness, recommendation clarity, risk realism. If the overall score is below 7.0, sends specific feedback back to the Analysis Agent and triggers a revision. Max 2 revision cycles.

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

From [`examples/sponsored_ranking_decision.md`](examples/sponsored_ranking_decision.md) -- a real pipeline run on a sponsored search ranking decision:

**Recommendation**

> Graduated Prominence with Performance Gates is the optimal choice because it provides measurable revenue growth while protecting user experience through quantified guardrails. This approach allows for systematic testing of increased sponsored prominence (targeting 25-40% revenue uplift) while maintaining user satisfaction above 85% and search abandonment below 15%.

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

## Background

This framework was developed through applied experimentation with agentic AI workflows and refined through sessions with product teams at enterprise organizations. It is intentionally open-source so any PM team can clone and run it without requiring engineering support.

---

## Privacy

All examples are sanitized. No proprietary data, internal metrics, or confidential business context is included anywhere in this repository.

---

## License

MIT
