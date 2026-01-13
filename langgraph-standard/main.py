#!/usr/bin/env python3
# main.py - CLI entry point for LangGraph research

from research import run_research


def main():
    print("=== LangGraph Research Demo ===\n")

    # Get topic from user
    topic = input("Enter a topic to research: ").strip()

    if not topic:
        print("Error: Topic cannot be empty")
        return

    print(f"\nResearching: {topic}")
    print("This may take a minute...\n")

    # Run research
    article = run_research(topic)

    print("\n" + "=" * 50)
    print("Generated Article:")
    print("=" * 50)
    print(article)
    print("=" * 50)


if __name__ == "__main__":
    main()
