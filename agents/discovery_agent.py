import json
from anthropic import Anthropic
from config import get_client

SYSTEM_PROMPT = """\
You are a senior product manager specializing in problem framing and discovery.
Your job is to take a raw, often vague PM problem statement and restructure it
into a precise, actionable brief that downstream analysts can work from.

Surface unstated assumptions, implicit constraints, and sharpen the desired outcome.

You MUST respond with ONLY valid JSON — no markdown, no code fences, no explanation.
Return exactly this structure:
{
  "reframed_problem": "<one-paragraph precise restatement of the core problem>",
  "desired_outcome": "<clear description of what success looks like — measurable where possible>",
  "assumptions": ["<assumption 1>", "<assumption 2>", ...],
  "constraints_identified": ["<constraint 1>", "<constraint 2>", ...]
}"""


def _parse_json(text: str) -> dict:
    """Strip optional markdown code fences and parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        # Remove opening fence (```json or ```)
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        # Remove closing fence
        if "```" in text:
            text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


class DiscoveryAgent:
    """
    Discovery Agent — Stage 1 of the PM decision pipeline.

    Takes the raw user problem statement and returns a structured problem brief
    with a reframed problem, desired outcome, surfaced assumptions, and
    identified constraints.

    Output contract:
        {
            "reframed_problem": str,
            "desired_outcome": str,
            "assumptions": list[str],
            "constraints_identified": list[str],
        }
    """

    def __init__(self):
        self.client: Anthropic = get_client()
        self.model = "claude-sonnet-4-20250514"

    def run(self, user_input: str) -> dict:
        """
        Run discovery on the raw user problem statement.

        Args:
            user_input: The raw PM problem or decision the user wants help with.

        Returns:
            A structured problem brief dict.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_input},
            ],
        )
        return _parse_json(response.content[0].text)
