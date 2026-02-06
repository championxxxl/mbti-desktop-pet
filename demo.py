"""
Demo script to showcase MBTI Desktop Pet features
Run this to see the key functionality without launching the full GUI
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.personality import MBTIPersonality, MBTIType
from mbti_pet.intent import ContextAwareIntentSystem
from mbti_pet.memory import MemoryManager


def demo_personalities():
    """Demonstrate MBTI personality system"""
    print("\n" + "="*60)
    print("MBTI PERSONALITY SYSTEM DEMO")
    print("="*60)
    
    # Show a few personality types
    demo_types = [MBTIType.ENFP, MBTIType.INTJ, MBTIType.INFJ]
    
    for mbti_type in demo_types:
        personality = MBTIPersonality(mbti_type)
        print(f"\n{personality.get_personality_description()}")
        print(f"Greeting: {personality.get_greeting()}")
        print(f"Strengths: {', '.join(personality.traits.strengths)}")


def demo_intent_recognition():
    """Demonstrate intent recognition"""
    print("\n" + "="*60)
    print("INTENT RECOGNITION DEMO")
    print("="*60)
    
    intent_system = ContextAwareIntentSystem()
    
    test_inputs = [
        "Can you help me with Python programming?",
        "Open my browser",
        "What is machine learning?",
        "Automate this task for me",
        "帮我打开文件"  # Chinese: Help me open file
    ]
    
    for user_input in test_inputs:
        intent = intent_system.analyze(user_input=user_input)
        print(f"\nInput: '{user_input}'")
        print(f"Intent: {intent.intent_type.value}")
        print(f"Confidence: {intent.confidence:.2f}")
        print(f"Suggestion: {intent.suggested_action}")


def demo_memory_system():
    """Demonstrate memory system"""
    print("\n" + "="*60)
    print("MEMORY SYSTEM DEMO")
    print("="*60)
    
    memory = MemoryManager("./demo_memory.db")
    
    # Record some interactions
    interactions = [
        ("text_input", "Help with Python", 7),
        ("text_input", "Open browser", 5),
        ("response", "I can help you with Python!", 6),
        ("automation", "Screenshot taken", 4),
    ]
    
    print("\nRecording interactions...")
    for interaction_type, content, importance in interactions:
        memory.record_interaction(interaction_type, content, importance=importance)
        print(f"  - [{interaction_type}] {content}")
    
    # Show memory summary
    print("\n" + memory.get_summary())
    
    # Search memories
    print("\nSearching for 'Python'...")
    results = memory.db.search_memories("Python")
    for result in results:
        print(f"  - {result.content} (importance: {result.importance})")
    
    # Learn a pattern
    memory.learn_pattern("task", {"name": "coding", "frequency": "morning"})
    print("\nLearned pattern: Morning coding sessions")


def demo_automation():
    """Demonstrate automation system"""
    print("\n" + "="*60)
    print("AUTOMATION SYSTEM DEMO")
    print("="*60)
    
    print("\nAutomation features available:")
    print("  - Mouse and keyboard control")
    print("  - Screenshot capture")
    print("  - Application launching")
    print("  - Custom macro recording")
    print("  - Task automation (like Claude Desktop)")
    
    print("\nNote: Full automation demo requires PyAutoGUI installation")
    print("      Install with: pip install -r requirements.txt")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("MBTI DESKTOP PET - FEATURE DEMONSTRATION")
    print("="*60)
    print("This demo showcases the core features without launching the full GUI")
    
    demo_personalities()
    demo_intent_recognition()
    demo_memory_system()
    demo_automation()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("\nTo launch the full application:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run: python src/mbti_pet/main.py")
    print("\nOr if installed:")
    print("  pip install -e .")
    print("  mbti-pet")
    print()


if __name__ == "__main__":
    main()
