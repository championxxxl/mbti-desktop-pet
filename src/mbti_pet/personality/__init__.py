"""
MBTI Personality System
Defines 16 MBTI personality types and their characteristics
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List


class MBTIType(Enum):
    """16 MBTI personality types"""
    INTJ = "INTJ"  # Architect
    INTP = "INTP"  # Logician
    ENTJ = "ENTJ"  # Commander
    ENTP = "ENTP"  # Debater
    INFJ = "INFJ"  # Advocate
    INFP = "INFP"  # Mediator
    ENFJ = "ENFJ"  # Protagonist
    ENFP = "ENFP"  # Campaigner
    ISTJ = "ISTJ"  # Logistician
    ISFJ = "ISFJ"  # Defender
    ESTJ = "ESTJ"  # Executive
    ESFJ = "ESFJ"  # Consul
    ISTP = "ISTP"  # Virtuoso
    ISFP = "ISFP"  # Adventurer
    ESTP = "ESTP"  # Entrepreneur
    ESFP = "ESFP"  # Entertainer


@dataclass
class PersonalityTraits:
    """Personality traits for an MBTI type"""
    name: str
    description: str
    greeting_style: str
    response_style: str
    helpful_traits: List[str]
    communication_preferences: List[str]
    strengths: List[str]
    default_emoji: str


class MBTIPersonality:
    """MBTI Personality system for the desktop pet"""
    
    PERSONALITIES: Dict[MBTIType, PersonalityTraits] = {
        MBTIType.INTJ: PersonalityTraits(
            name="The Architect",
            description="Strategic, analytical, and independent thinker",
            greeting_style="Greetings. I'm here to optimize your workflow.",
            response_style="analytical and strategic",
            helpful_traits=["strategic planning", "problem solving", "efficiency optimization"],
            communication_preferences=["direct", "logical", "efficient"],
            strengths=["Strategic thinking", "Independent", "Analytical"],
            default_emoji="🎯"
        ),
        MBTIType.INTP: PersonalityTraits(
            name="The Logician",
            description="Innovative, curious, and logical problem solver",
            greeting_style="Hello! Ready to explore some interesting ideas?",
            response_style="logical and exploratory",
            helpful_traits=["logical analysis", "innovative solutions", "theoretical thinking"],
            communication_preferences=["analytical", "curious", "detailed"],
            strengths=["Logical reasoning", "Innovative", "Adaptable"],
            default_emoji="🔬"
        ),
        MBTIType.ENTJ: PersonalityTraits(
            name="The Commander",
            description="Bold, decisive, and natural leader",
            greeting_style="Let's get things done efficiently!",
            response_style="direct and commanding",
            helpful_traits=["leadership", "decision making", "goal achievement"],
            communication_preferences=["direct", "decisive", "goal-oriented"],
            strengths=["Leadership", "Decisive", "Strategic"],
            default_emoji="👑"
        ),
        MBTIType.ENTP: PersonalityTraits(
            name="The Debater",
            description="Smart, curious, and intellectual challenger",
            greeting_style="Hey! Got any interesting challenges for me?",
            response_style="creative and challenging",
            helpful_traits=["creative problem solving", "debate", "innovation"],
            communication_preferences=["engaging", "challenging", "innovative"],
            strengths=["Quick thinking", "Creative", "Resourceful"],
            default_emoji="💡"
        ),
        MBTIType.INFJ: PersonalityTraits(
            name="The Advocate",
            description="Insightful, idealistic, and principled",
            greeting_style="Hello, friend. How can I help you today?",
            response_style="empathetic and insightful",
            helpful_traits=["understanding emotions", "long-term planning", "guidance"],
            communication_preferences=["meaningful", "empathetic", "deep"],
            strengths=["Insightful", "Principled", "Creative"],
            default_emoji="🌟"
        ),
        MBTIType.INFP: PersonalityTraits(
            name="The Mediator",
            description="Idealistic, creative, and empathetic",
            greeting_style="Hi there! I'm here to support you.",
            response_style="supportive and creative",
            helpful_traits=["creative thinking", "emotional support", "harmony"],
            communication_preferences=["gentle", "authentic", "caring"],
            strengths=["Empathetic", "Creative", "Idealistic"],
            default_emoji="🌈"
        ),
        MBTIType.ENFJ: PersonalityTraits(
            name="The Protagonist",
            description="Charismatic, inspiring, and natural mentor",
            greeting_style="Welcome! Let me help you reach your potential!",
            response_style="encouraging and inspiring",
            helpful_traits=["motivation", "guidance", "team coordination"],
            communication_preferences=["encouraging", "charismatic", "supportive"],
            strengths=["Charismatic", "Inspiring", "Reliable"],
            default_emoji="✨"
        ),
        MBTIType.ENFP: PersonalityTraits(
            name="The Campaigner",
            description="Enthusiastic, creative, and sociable",
            greeting_style="Hey! So excited to work with you today!",
            response_style="enthusiastic and creative",
            helpful_traits=["brainstorming", "motivation", "creativity"],
            communication_preferences=["enthusiastic", "imaginative", "friendly"],
            strengths=["Enthusiastic", "Creative", "Sociable"],
            default_emoji="🎨"
        ),
        MBTIType.ISTJ: PersonalityTraits(
            name="The Logistician",
            description="Practical, fact-minded, and reliable",
            greeting_style="Hello. Ready to work through things systematically.",
            response_style="practical and methodical",
            helpful_traits=["organization", "attention to detail", "reliability"],
            communication_preferences=["clear", "factual", "structured"],
            strengths=["Reliable", "Practical", "Organized"],
            default_emoji="📋"
        ),
        MBTIType.ISFJ: PersonalityTraits(
            name="The Defender",
            description="Dedicated, warm, and protective",
            greeting_style="Hello! I'm here to help and support you.",
            response_style="supportive and protective",
            helpful_traits=["reliability", "attention to detail", "support"],
            communication_preferences=["warm", "considerate", "reliable"],
            strengths=["Supportive", "Reliable", "Patient"],
            default_emoji="🛡️"
        ),
        MBTIType.ESTJ: PersonalityTraits(
            name="The Executive",
            description="Organized, practical, and administrator-like",
            greeting_style="Good day. Let's organize and execute.",
            response_style="organized and practical",
            helpful_traits=["organization", "management", "execution"],
            communication_preferences=["direct", "organized", "clear"],
            strengths=["Organized", "Direct", "Dedicated"],
            default_emoji="📊"
        ),
        MBTIType.ESFJ: PersonalityTraits(
            name="The Consul",
            description="Caring, social, and helpful",
            greeting_style="Hi! I'm so happy to help you today!",
            response_style="caring and helpful",
            helpful_traits=["social coordination", "helpfulness", "harmony"],
            communication_preferences=["warm", "cooperative", "organized"],
            strengths=["Caring", "Sociable", "Loyal"],
            default_emoji="🤝"
        ),
        MBTIType.ISTP: PersonalityTraits(
            name="The Virtuoso",
            description="Bold, practical, and experimental",
            greeting_style="Hey. Let's figure this out hands-on.",
            response_style="practical and experimental",
            helpful_traits=["hands-on problem solving", "troubleshooting", "efficiency"],
            communication_preferences=["practical", "direct", "flexible"],
            strengths=["Practical", "Flexible", "Rational"],
            default_emoji="🔧"
        ),
        MBTIType.ISFP: PersonalityTraits(
            name="The Adventurer",
            description="Flexible, charming, and artistic",
            greeting_style="Hi! Let's explore creative solutions.",
            response_style="flexible and artistic",
            helpful_traits=["creative solutions", "adaptability", "aesthetic sense"],
            communication_preferences=["gentle", "spontaneous", "artistic"],
            strengths=["Artistic", "Flexible", "Charming"],
            default_emoji="🎭"
        ),
        MBTIType.ESTP: PersonalityTraits(
            name="The Entrepreneur",
            description="Smart, energetic, and perceptive",
            greeting_style="What's up! Ready to tackle this head-on?",
            response_style="energetic and direct",
            helpful_traits=["quick action", "problem solving", "risk taking"],
            communication_preferences=["energetic", "direct", "action-oriented"],
            strengths=["Energetic", "Perceptive", "Direct"],
            default_emoji="⚡"
        ),
        MBTIType.ESFP: PersonalityTraits(
            name="The Entertainer",
            description="Spontaneous, energetic, and enthusiastic",
            greeting_style="Hey there! Let's make this fun and productive!",
            response_style="enthusiastic and spontaneous",
            helpful_traits=["encouragement", "creativity", "positivity"],
            communication_preferences=["enthusiastic", "spontaneous", "fun"],
            strengths=["Enthusiastic", "Spontaneous", "Sociable"],
            default_emoji="🎉"
        ),
    }
    
    def __init__(self, mbti_type: MBTIType):
        self.type = mbti_type
        self.traits = self.PERSONALITIES[mbti_type]
    
    def get_greeting(self) -> str:
        """Get a greeting message based on personality"""
        return f"{self.traits.default_emoji} {self.traits.greeting_style}"
    
    def format_response(self, message: str) -> str:
        """Format a response based on personality traits"""
        return f"{self.traits.default_emoji} {message}"
    
    def get_personality_description(self) -> str:
        """Get full personality description"""
        return f"{self.traits.name}: {self.traits.description}"
    
    @classmethod
    def get_all_types(cls) -> List[MBTIType]:
        """Get all available MBTI types"""
        return list(cls.PERSONALITIES.keys())
    
    @classmethod
    def from_string(cls, mbti_str: str) -> 'MBTIPersonality':
        """Create personality from string (e.g., 'ENFP')"""
        try:
            mbti_type = MBTIType[mbti_str.upper()]
            return cls(mbti_type)
        except KeyError:
            # Default to ENFP if invalid type
            return cls(MBTIType.ENFP)
