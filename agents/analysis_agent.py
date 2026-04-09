import json
from typing import Optional
from anthropic import Anthropic
from config import get_client

SYSTEM_PROMPT = """\
You are a senior product strategist skilled in PM decision frameworks (RICE, MoSCoW,
opportunity sizing, jobs-to-be-done, etc.).

You receive a structured PM problem brief and produce a thorough decision analysis.
Generate exactly 3 distinct, meaningfully different strategic options. Be specific —
avoid generic placeholder language. Ground pros, cons, tradeoffs, and risks in the
actual context of the problem.

You MUST respond with ONLY valid JSON — no markdown, no code fences, no explanation.
Return exactly this structure:
{
  "options": [
    {
      "name": "<short option name>",
      "pros": ["<pro 1>", "<pro 2>", ...],
      "cons": ["<con 1>", "<con 2>", ...]
    },
    { ... },
    { ... }
  ],
  "recommendation": "<which option you recommend and a clear, specific justification>",
  "key_tradeoffs": ["<tradeoff 1>", "<tradeoff 2>", ...],
  "risks": ["<risk 1>", "<risk 2>", ...]
}"""


def _parse_json(text: str) -> dict:
    """Strip optional markdown code fences and parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if "```" in text:
            text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


class AnalysisAgent:
    """
    Analysis Agent — Stage 2 of the PM decision pipeline.

    Receives the structured problem brief from DiscoveryAgent (and optionally
    critique feedback from a prior iteration) and returns a full decision analysis
    with 3 options, a recommendation, key tradeoffs, and risks.

    Output contract:
        {
            "options": list[dict],          # each: {name, pros, cons}
            "recommendation": str,
            "key_tradeoffs": list[str],
            "risks": list[str],
        }
    """

    def __init__(self):
        self.client: Anthropic = get_client()
        self.model = "claude-sonnet-4-20250514"

    def run(self, problem_brief: dict, critique_feedback: Optional[str] = None) -> dict:
        """
        Analyse the problem brief and generate decision options.

        Args:
            problem_brief: Structured output from DiscoveryAgent.
            critique_feedback: Optional feedback string from a prior CritiqueAgent
                               run. When present, the agent must address these gaps.

        Returns:
            Analysis result dict.
        """
        brief_text = json.dumps(problem_brief, indent=2)

        if critique_feedback:
            user_message = (
                f"Problem brief:\n{brief_text}\n\n"
                f"A previous analysis was critiqued. Address ALL of the following "
                f"feedback in your revised analysis:\n{critique_feedback}"
            )
        else:
            user_message = f"Problem brief:\n{brief_text}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )
        return _parse_json(response.content[0].text)
