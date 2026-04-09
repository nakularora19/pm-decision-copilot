import json
from anthropic import Anthropic
from config import get_client

RETRY_THRESHOLD = 7  # overall_score below this triggers a retry

SYSTEM_PROMPT = """\
You are a rigorous PM advisor acting as devil's advocate. Your job is to
stress-test a product decision analysis — challenge assumptions, find blind spots,
and identify gaps in reasoning.

Score the analysis across three dimensions, each from 0 to 10:
  - tradeoff_completeness: Are all meaningful tradeoffs identified and fairly weighed?
    (penalise if important angles are missing or options are strawmanned)
  - recommendation_clarity: Is the recommendation specific, well-justified, and
    actionable? (penalise vague or hedge-everything recommendations)
  - risk_realism: Are risks concrete, plausible, and prioritised correctly?
    (penalise generic risks or missing high-impact failure modes)

Compute overall_score as the mean of the three scores, rounded to one decimal place.
Set needs_revision to true if overall_score < 7.

You MUST respond with ONLY valid JSON — no markdown, no code fences, no explanation.
Return exactly this structure:
{
  "scores": {
    "tradeoff_completeness": <int 0-10>,
    "recommendation_clarity": <int 0-10>,
    "risk_realism": <int 0-10>
  },
  "overall_score": <float, one decimal place>,
  "feedback": "<detailed critique: what was done well, what specific gaps exist, what must improve>",
  "needs_revision": <true|false>
}"""


def _parse_json(text: str) -> dict:
    """Strip optional markdown code fences and parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if "```" in text:
            text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


class CritiqueAgent:
    """
    Critique Agent — Stage 3 of the PM decision pipeline.

    Scores the AnalysisAgent output across three dimensions and decides whether
    the analysis needs revision. A score below RETRY_THRESHOLD triggers a retry
    in the orchestrator.

    Output contract:
        {
            "scores": {
                "tradeoff_completeness": int,
                "recommendation_clarity": int,
                "risk_realism": int,
            },
            "overall_score": float,
            "feedback": str,
            "needs_revision": bool,
        }
    """

    def __init__(self):
        self.client: Anthropic = get_client()
        self.model = "claude-sonnet-4-20250514"
        self.retry_threshold = RETRY_THRESHOLD

    def run(self, analysis_result: dict) -> dict:
        """
        Critique the analysis and return a scored evaluation.

        Args:
            analysis_result: Structured output from AnalysisAgent.

        Returns:
            Critique result dict. If needs_revision is True, the orchestrator
            should pass feedback back to AnalysisAgent and retry.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyse and critique this PM decision analysis:\n\n"
                               f"{json.dumps(analysis_result, indent=2)}",
                },
            ],
        )
        result = _parse_json(response.content[0].text)

        # Enforce needs_revision based on threshold in case the model drifts
        overall = result.get("overall_score", 0)
        result["needs_revision"] = overall < self.retry_threshold

        return result
