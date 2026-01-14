#!/usr/bin/env python3
# main.py - CLI entry point for LangGraph research (5-node pipeline)

from research import run_research


def main():
    print("=== LangGraph Research Demo (5-Node Pipeline) ===\n")

    # Get topic from user
    topic = input("Enter a topic to research: ").strip()

    if not topic:
        print("Error: Topic cannot be empty")
        return

    print(f"\nResearching: {topic}")
    print("Pipeline: query_planner → researcher → fact_extractor → writer → fact_checker")
    print("This may take a minute...\n")

    # Run research
    result = run_research(topic)

    # Display article
    print("\n" + "=" * 50)
    print("GENERATED ARTICLE:")
    print("=" * 50)
    print(result["article"])

    # Display fact check results
    print("\n" + "=" * 50)
    print("FACT CHECK RESULTS:")
    print("=" * 50)
    print(result["fact_check_result"])
    print("=" * 50)


if __name__ == "__main__":
    main()
