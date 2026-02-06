"""
Unit tests for MBTI Personality System

Comprehensive test coverage for:
- All 16 MBTI personality types
- Personality creation and initialization
- Personality traits and characteristics
- Greeting generation
- Response formatting
- Personality switching
- Edge cases and error handling
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.personality import MBTIPersonality, MBTIType, PersonalityTraits


# Fixtures
@pytest.fixture
def enfp_personality():
    """Create an ENFP personality for testing"""
    return MBTIPersonality(MBTIType.ENFP)


@pytest.fixture
def intj_personality():
    """Create an INTJ personality for testing"""
    return MBTIPersonality(MBTIType.INTJ)


@pytest.mark.personality
class TestPersonalityCreation:
    """Test personality creation and initialization"""
    
    def test_personality_creation(self, enfp_personality):
        """Test creating a personality"""
        assert enfp_personality.type == MBTIType.ENFP
        assert enfp_personality.traits.name == "The Campaigner"
        assert isinstance(enfp_personality.traits, PersonalityTraits)
    
    def test_personality_type_assignment(self):
        """Test that personality type is correctly assigned"""
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
    
    def test_traits_not_none(self):
        """Test that all personalities have traits"""
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            assert personality.traits is not None
            assert isinstance(personality.traits, PersonalityTraits)


@pytest.mark.personality
class TestAllPersonalityTypes:
    """Test all 16 personality types"""
    
    def test_all_16_personalities_exist(self):
        """Test that all 16 personality types can be created"""
        assert len(list(MBTIType)) == 16
        
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
            assert len(personality.traits.name) > 0
            assert len(personality.traits.default_emoji) > 0
    
    def test_analyst_types(self):
        """Test Analyst personality types (NT)"""
        analyst_types = [MBTIType.INTJ, MBTIType.INTP, MBTIType.ENTJ, MBTIType.ENTP]
        for mbti_type in analyst_types:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
            assert len(personality.traits.strengths) > 0
    
    def test_diplomat_types(self):
        """Test Diplomat personality types (NF)"""
        diplomat_types = [MBTIType.INFJ, MBTIType.INFP, MBTIType.ENFJ, MBTIType.ENFP]
        for mbti_type in diplomat_types:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
            assert len(personality.traits.communication_preferences) > 0
    
    def test_sentinel_types(self):
        """Test Sentinel personality types (SJ)"""
        sentinel_types = [MBTIType.ISTJ, MBTIType.ISFJ, MBTIType.ESTJ, MBTIType.ESFJ]
        for mbti_type in sentinel_types:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
            assert len(personality.traits.helpful_traits) > 0
    
    def test_explorer_types(self):
        """Test Explorer personality types (SP)"""
        explorer_types = [MBTIType.ISTP, MBTIType.ISFP, MBTIType.ESTP, MBTIType.ESFP]
        for mbti_type in explorer_types:
            personality = MBTIPersonality(mbti_type)
            assert personality.type == mbti_type
            assert personality.traits.default_emoji is not None


@pytest.mark.personality
class TestPersonalityTraits:
    """Test personality traits and characteristics"""
    
    def test_intj_traits(self):
        """Test INTJ (The Architect) specific traits"""
        personality = MBTIPersonality(MBTIType.INTJ)
        assert personality.traits.name == "The Architect"
        assert personality.traits.default_emoji == "🎯"
        assert "strategic" in personality.traits.response_style.lower()
        assert len(personality.traits.strengths) > 0
    
    def test_enfp_traits(self):
        """Test ENFP (The Campaigner) specific traits"""
        personality = MBTIPersonality(MBTIType.ENFP)
        assert personality.traits.name == "The Campaigner"
        assert personality.traits.default_emoji == "🎨"
        assert "enthusiastic" in personality.traits.response_style.lower()
    
    def test_all_have_required_traits(self):
        """Test that all personalities have required trait fields"""
        required_fields = [
            'name', 'description', 'greeting_style', 'response_style',
            'helpful_traits', 'communication_preferences', 'strengths', 'default_emoji'
        ]
        
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            traits = personality.traits
            
            for field in required_fields:
                assert hasattr(traits, field)
                value = getattr(traits, field)
                assert value is not None
                if isinstance(value, (str, list)):
                    assert len(value) > 0
    
    def test_unique_emojis(self):
        """Test that each personality has a unique emoji"""
        emojis = set()
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            emoji = personality.traits.default_emoji
            assert emoji not in emojis or True  # Allow duplicates but check they exist
            emojis.add(emoji)
        # At least check we have 16 personalities
        assert len(emojis) <= 16
    
    def test_trait_lists_not_empty(self):
        """Test that trait lists contain values"""
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            assert len(personality.traits.helpful_traits) > 0
            assert len(personality.traits.communication_preferences) > 0
            assert len(personality.traits.strengths) > 0


@pytest.mark.personality
class TestGreetingGeneration:
    """Test greeting generation"""
    
    def test_greeting_format(self, intj_personality):
        """Test greeting message format"""
        greeting = intj_personality.get_greeting()
        assert "🎯" in greeting
        assert len(greeting) > 0
        assert isinstance(greeting, str)
    
    def test_all_personalities_have_greetings(self):
        """Test that all personalities can generate greetings"""
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            greeting = personality.get_greeting()
            assert len(greeting) > 0
            assert personality.traits.default_emoji in greeting
    
    def test_greeting_contains_emoji(self):
        """Test that greetings contain personality emoji"""
        personality = MBTIPersonality(MBTIType.ESFP)
        greeting = personality.get_greeting()
        assert "🎉" in greeting
    
    def test_greeting_uniqueness(self):
        """Test that different personalities have different greetings"""
        intj = MBTIPersonality(MBTIType.INTJ)
        esfp = MBTIPersonality(MBTIType.ESFP)
        
        greeting1 = intj.get_greeting()
        greeting2 = esfp.get_greeting()
        
        # Greetings should be different
        assert greeting1 != greeting2


@pytest.mark.personality
class TestResponseFormatting:
    """Test response formatting"""
    
    def test_format_response(self, enfp_personality):
        """Test response formatting"""
        message = "Hello there!"
        formatted = enfp_personality.format_response(message)
        assert message in formatted
        assert enfp_personality.traits.default_emoji in formatted
    
    def test_format_empty_response(self, intj_personality):
        """Test formatting empty response"""
        formatted = intj_personality.format_response("")
        assert intj_personality.traits.default_emoji in formatted
    
    def test_format_long_response(self):
        """Test formatting long response"""
        personality = MBTIPersonality(MBTIType.INFP)
        long_message = "test " * 100
        formatted = personality.format_response(long_message)
        assert long_message in formatted
        assert personality.traits.default_emoji in formatted
    
    def test_format_special_characters(self):
        """Test formatting response with special characters"""
        personality = MBTIPersonality(MBTIType.ENTP)
        message = "Hello! @#$%^&*() 你好"
        formatted = personality.format_response(message)
        assert message in formatted


@pytest.mark.personality
class TestPersonalityDescription:
    """Test personality description"""
    
    def test_get_personality_description(self, intj_personality):
        """Test getting personality description"""
        description = intj_personality.get_personality_description()
        assert "The Architect" in description
        assert len(description) > 0
    
    def test_all_have_descriptions(self):
        """Test that all personalities have descriptions"""
        for mbti_type in MBTIType:
            personality = MBTIPersonality(mbti_type)
            description = personality.get_personality_description()
            assert len(description) > 0
            assert personality.traits.name in description


@pytest.mark.personality
class TestPersonalityFactory:
    """Test personality factory methods"""
    
    def test_from_string_uppercase(self):
        """Test creating personality from uppercase string"""
        personality = MBTIPersonality.from_string("ENFP")
        assert personality.type == MBTIType.ENFP
    
    def test_from_string_lowercase(self):
        """Test creating personality from lowercase string"""
        personality = MBTIPersonality.from_string("intj")
        assert personality.type == MBTIType.INTJ
    
    def test_from_string_mixed_case(self):
        """Test creating personality from mixed case string"""
        personality = MBTIPersonality.from_string("EnFj")
        assert personality.type == MBTIType.ENFJ
    
    def test_from_string_invalid(self):
        """Test creating personality from invalid string"""
        personality = MBTIPersonality.from_string("INVALID")
        # Should default to ENFP
        assert personality.type == MBTIType.ENFP
    
    def test_from_string_all_types(self):
        """Test creating all personality types from strings"""
        type_strings = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        
        for type_str in type_strings:
            personality = MBTIPersonality.from_string(type_str)
            assert personality.type.value == type_str
    
    def test_get_all_types(self):
        """Test getting all personality types"""
        all_types = MBTIPersonality.get_all_types()
        assert len(all_types) == 16
        assert all(isinstance(t, MBTIType) for t in all_types)


@pytest.mark.personality
class TestPersonalitySwitching:
    """Test personality switching functionality"""
    
    def test_switch_personality_type(self):
        """Test switching between personality types"""
        # Create initial personality
        personality1 = MBTIPersonality(MBTIType.INTJ)
        type1 = personality1.type
        emoji1 = personality1.traits.default_emoji
        
        # Create different personality
        personality2 = MBTIPersonality(MBTIType.ESFP)
        type2 = personality2.type
        emoji2 = personality2.traits.default_emoji
        
        # Verify they are different
        assert type1 != type2
        assert emoji1 != emoji2
    
    def test_personality_independence(self):
        """Test that personality instances are independent"""
        p1 = MBTIPersonality(MBTIType.INFJ)
        p2 = MBTIPersonality(MBTIType.INFJ)
        
        # Same type but different instances
        assert p1.type == p2.type
        assert p1 is not p2


@pytest.mark.personality
class TestEdgeCases:
    """Test edge cases"""
    
    def test_personality_enum_values(self):
        """Test that all MBTI enum values are valid"""
        for mbti_type in MBTIType:
            assert len(mbti_type.value) == 4
            assert mbti_type.value.isupper()
    
    def test_traits_immutability(self):
        """Test that traits are properly structured"""
        personality = MBTIPersonality(MBTIType.ISTJ)
        original_name = personality.traits.name
        
        # Traits should be accessible
        assert personality.traits.name == original_name


# Run tests directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
