"""
pm-decision-copilot — CLI entry point.

Usage:
    python main.py
"""

from core.orchestrator import Orchestrator


def main():
    print("PM Decision Copilot")
    print("=" * 40)

    problem = input("Problem:\n> ").strip()
    if not problem:
        print("No problem provided. Exiting.")
        return

    context = input("\nContext (optional — press Enter to skip):\n> ").strip()
    constraints = input("\nConstraints (optional — press Enter to skip):\n> ").strip()

    user_input = f"Problem: {problem}"
    if context:
        user_input += f"\nContext: {context}"
    if constraints:
        user_input += f"\nConstraints: {constraints}"

    orchestrator = Orchestrator()
    orchestrator.run(user_input)


if __name__ == "__main__":
    main()
