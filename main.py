"""
pm-decision-copilot — CLI entry point.

Usage:
    python main.py
"""

from core.orchestrator import Orchestrator


def main():
    print("PM Decision Copilot")
    print("=" * 40)
    problem = input("Describe the PM decision or problem you need help with:\n> ").strip()
    if not problem:
        print("No input provided. Exiting.")
        return

    orchestrator = Orchestrator()
    result = orchestrator.run(problem)
    print("\n--- Final Recommendation ---")
    print(result)


if __name__ == "__main__":
    main()
