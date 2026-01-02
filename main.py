# main.py - CLI interface for CrewAI research

from research import run_research


if __name__ == "__main__":
    # Ask user for topic
    topic = input("Enter the topic you'd like to research: ")

    print(f"\n🔍 Researching and writing about: {topic}")
    print("=" * 60)

    result = run_research(topic)

    # Format output as a blog post
    print("\n" + "=" * 60)
    print("📝 BLOG POST")
    print("=" * 60)
    print(f"\nTopic: {topic}")
    print("-" * 60)
    print(f"\n{result}\n")
    print("=" * 60)
