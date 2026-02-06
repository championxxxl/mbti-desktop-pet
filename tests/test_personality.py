"""
Unit tests for MBTI Personality System
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.personality import MBTIPersonality, MBTIType


def test_personality_creation():
    """Test creating a personality"""
    personality = MBTIPersonality(MBTIType.ENFP)
    assert personality.type == MBTIType.ENFP
    assert personality.traits.name == "The Campaigner"
    print("✓ Personality creation test passed")


def test_greeting():
    """Test personality greeting"""
    personality = MBTIPersonality(MBTIType.INTJ)
    greeting = personality.get_greeting()
    assert "🎯" in greeting
    assert len(greeting) > 0
    print("✓ Greeting test passed")


def test_all_personalities():
    """Test all 16 personality types"""
    for mbti_type in MBTIType:
        personality = MBTIPersonality(mbti_type)
        assert personality.type == mbti_type
        assert len(personality.traits.name) > 0
        assert len(personality.traits.default_emoji) > 0
    print("✓ All personalities test passed")


def test_from_string():
    """Test creating personality from string"""
    personality = MBTIPersonality.from_string("ENFP")
    assert personality.type == MBTIType.ENFP
    
    personality = MBTIPersonality.from_string("intj")
    assert personality.type == MBTIType.INTJ
    
    # Invalid type should default to ENFP
    personality = MBTIPersonality.from_string("INVALID")
    assert personality.type == MBTIType.ENFP
    print("✓ From string test passed")


def test_response_formatting():
    """Test response formatting"""
    personality = MBTIPersonality(MBTIType.ESFP)
    message = "Hello there!"
    formatted = personality.format_response(message)
    assert message in formatted
    assert personality.traits.default_emoji in formatted
    print("✓ Response formatting test passed")


if __name__ == "__main__":
    print("Running Personality System Tests...")
    print("=" * 50)
    
    test_personality_creation()
    test_greeting()
    test_all_personalities()
    test_from_string()
    test_response_formatting()
    
    print("=" * 50)
    print("All tests passed! ✓")
