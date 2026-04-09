from typing import Optional
from agents.discovery_agent import DiscoveryAgent
from agents.analysis_agent import AnalysisAgent
from agents.critique_agent import CritiqueAgent
from core.memory import Memory

MAX_RETRIES = 2  # max analysis→critique retry iterations after the first pass


class Orchestrator:
    """
    Orchestrator — coordinates the sequential agent pipeline.

    Pipeline:
        DiscoveryAgent → AnalysisAgent → CritiqueAgent
                              ↑_______________|  (loop if needs_revision, max MAX_RETRIES)

    On each retry, the critique feedback is injected into AnalysisAgent context
    so it can address specific gaps. After MAX_RETRIES the best result is returned.
    The final run is persisted to logs/ via Memory.
    """

    def __init__(self):
        self.discovery = DiscoveryAgent()
        self.analysis = AnalysisAgent()
        self.critique = CritiqueAgent()
        self.memory = Memory()

    def run(self, user_input: str) -> dict:
        """
        Execute the full pipeline for a given PM problem.

        Args:
            user_input: Raw problem statement from the user.

        Returns:
            dict with keys: problem_brief, analysis, critique, iterations.
        """
        # ── Stage 1: Discovery ──────────────────────────────────────────────
        print("\n[1/3] Discovery Agent — framing the problem...")
        problem_brief = self.discovery.run(user_input)
        self.memory.set("problem_brief", problem_brief)

        # ── Stage 2 + 3: Analysis → Critique loop ───────────────────────────
        critique_feedback: Optional[str] = None
        final_analysis = None
        final_critique = None

        for iteration in range(MAX_RETRIES + 1):
            pass_label = "pass 1" if iteration == 0 else f"revision {iteration}/{MAX_RETRIES}"
            print(f"\n[2/3] Analysis Agent — evaluating options ({pass_label})...")
            analysis = self.analysis.run(problem_brief, critique_feedback=critique_feedback)

            print(f"[3/3] Critique Agent — scoring the analysis ({pass_label})...")
            critique = self.critique.run(analysis)

            final_analysis = analysis
            final_critique = critique

            score = critique.get("overall_score", 0)
            needs_revision = critique.get("needs_revision", False)

            if not needs_revision or iteration == MAX_RETRIES:
                status = "PASS" if not needs_revision else "MAX RETRIES REACHED"
                print(f"\n  Critique score: {score}/10 — {status}")
                break

            print(f"\n  Critique score: {score}/10 — below threshold, revising...")
            critique_feedback = critique.get("feedback", "")

        result = {
            "problem_brief": problem_brief,
            "analysis": final_analysis,
            "critique": final_critique,
            "iterations": iteration + 1,
        }

        # ── Persist run ──────────────────────────────────────────────────────
        log_path = self.memory.save_run(result)
        self.memory.set("last_run", result)

        # ── Print summary ────────────────────────────────────────────────────
        _print_summary(result, log_path)

        return result


def _print_summary(result: dict, log_path: str) -> None:
    """Print a clean, human-readable summary of the pipeline output."""
    brief = result["problem_brief"]
    analysis = result["analysis"]
    critique = result["critique"]
    iterations = result["iterations"]

    divider = "─" * 60

    print(f"\n{'═' * 60}")
    print("  PM DECISION COPILOT — RESULTS")
    print(f"{'═' * 60}")

    print(f"\n{divider}")
    print("  PROBLEM")
    print(divider)
    print(f"  {brief.get('reframed_problem', '')}")
    print(f"\n  Desired outcome: {brief.get('desired_outcome', '')}")

    assumptions = brief.get("assumptions", [])
    if assumptions:
        print("\n  Assumptions surfaced:")
        for a in assumptions:
            print(f"    • {a}")

    constraints = brief.get("constraints_identified", [])
    if constraints:
        print("\n  Constraints identified:")
        for c in constraints:
            print(f"    • {c}")

    print(f"\n{divider}")
    print("  OPTIONS EVALUATED")
    print(divider)
    for i, opt in enumerate(analysis.get("options", []), 1):
        print(f"\n  Option {i}: {opt.get('name', '')}")
        for pro in opt.get("pros", []):
            print(f"    + {pro}")
        for con in opt.get("cons", []):
            print(f"    - {con}")

    print(f"\n{divider}")
    print("  RECOMMENDATION")
    print(divider)
    print(f"  {analysis.get('recommendation', '')}")

    tradeoffs = analysis.get("key_tradeoffs", [])
    if tradeoffs:
        print("\n  Key tradeoffs:")
        for t in tradeoffs:
            print(f"    • {t}")

    risks = analysis.get("risks", [])
    if risks:
        print("\n  Risks:")
        for r in risks:
            print(f"    ⚠ {r}")

    print(f"\n{divider}")
    print("  CRITIQUE")
    print(divider)
    scores = critique.get("scores", {})
    print(f"  Tradeoff completeness : {scores.get('tradeoff_completeness', '—')}/10")
    print(f"  Recommendation clarity: {scores.get('recommendation_clarity', '—')}/10")
    print(f"  Risk realism          : {scores.get('risk_realism', '—')}/10")
    print(f"  Overall score         : {critique.get('overall_score', '—')}/10")
    print(f"\n  {critique.get('feedback', '')}")

    print(f"\n{divider}")
    print(f"  Completed in {iterations} iteration(s).")
    print(f"  Run saved to: {log_path}")
    print(f"{'═' * 60}\n")
