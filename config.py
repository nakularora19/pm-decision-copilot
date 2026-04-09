import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def get_client() -> Anthropic:
    """
    Return an authenticated Anthropic client.

    Reads ANTHROPIC_API_KEY from the environment (loaded via .env).
    Raises a clear error if the key is missing so misconfiguration is
    caught at startup rather than at the first API call.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Add it to your .env file: ANTHROPIC_API_KEY=sk-ant-..."
        )
    return Anthropic(api_key=api_key)
