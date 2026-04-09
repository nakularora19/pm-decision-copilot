# Examples

This folder contains real outputs from running the PM Decision Copilot pipeline on actual product management decisions.

Each file documents one full pipeline run — from raw problem input through Discovery, Analysis, and Critique — and shows the structured recommendation the system produced.

## How to read these files

Every output follows the same structure:

| Section | Source agent | What it contains |
|---|---|---|
| **Problem Input** | User | The raw problem statement passed to the pipeline |
| **Discovery** | `DiscoveryAgent` | Reframed problem, desired outcome, surfaced assumptions, identified constraints |
| **Analysis** | `AnalysisAgent` | 3 evaluated options with pros/cons, recommendation, key tradeoffs, risks |
| **Critique** | `CritiqueAgent` | Scores across three dimensions, overall score, detailed feedback |
| **Run metadata** | `Orchestrator` | Iterations taken, log file location |

## Examples in this folder

| File | Decision | Critique score | Iterations |
|---|---|---|---|
| [sponsored_ranking_decision.md](sponsored_ranking_decision.md) | How prominent should sponsored search results be? | 7.0 / 10 | 2 |
| [uber_guaranteed_earnings.md](uber_guaranteed_earnings.md) | Should Uber introduce guaranteed earnings windows for suburban drivers? | — | Example input only |

## Running the pipeline yourself

```bash
source venv/bin/activate

# CLI
python main.py

# Streamlit UI
streamlit run app.py
```

Completed runs are automatically saved as JSON to `logs/run_<timestamp>.json`.
