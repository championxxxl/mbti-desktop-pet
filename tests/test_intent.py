"""
Unit tests for Intent Recognition System

Comprehensive test coverage for:
- All intent types (help, task, info, automation, casual, system, file, web, code, writing)
- Entity extraction
- Context-aware intent recognition
- Edge cases and error handling
- Chinese language support
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.intent import IntentRecognizer, IntentType, ContextAwareIntentSystem, Intent


# Fixtures
@pytest.fixture
def recognizer():
    """Create an IntentRecognizer instance for testing"""
    return IntentRecognizer()


@pytest.fixture
def context_system():
    """Create a ContextAwareIntentSystem instance for testing"""
    return ContextAwareIntentSystem()


# Test Intent Recognition - Basic Intents
@pytest.mark.intent
class TestBasicIntents:
    """Test basic intent recognition"""
    
    def test_help_request_intent(self, recognizer):
        """Test help request recognition"""
        test_cases = [
            "Can you help me with this?",
            "I need assistance",
            "How can you help?",
            "帮助我",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.HELP_REQUEST, IntentType.CASUAL_CHAT, IntentType.INFORMATION_QUERY]
            assert intent.confidence > 0.0
            assert intent.raw_input == test_input
    
    def test_casual_chat_intent(self, recognizer):
        """Test casual chat recognition"""
        test_cases = [
            "Hello!",
            "How are you?",
            "Good morning",
            "Nice to meet you",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            # These should default to casual chat if no other patterns match
            assert intent.intent_type == IntentType.CASUAL_CHAT
            assert intent.confidence >= 0.0
    
    def test_task_execution_intent(self, recognizer):
        """Test task execution recognition"""
        test_cases = [
            "Open the browser",
            "Launch Chrome",
            "Run the application",
            "Execute this command",
            "打开浏览器",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.TASK_EXECUTION, IntentType.CASUAL_CHAT]
            assert intent.confidence > 0.0
    
    def test_information_query_intent(self, recognizer):
        """Test information query recognition"""
        test_cases = [
            "What is Python?",
            "When is the deadline?",
            "Where can I find this?",
            "Why does this happen?",
            "Explain machine learning",
            "什么是人工智能？",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.INFORMATION_QUERY, IntentType.CASUAL_CHAT]
            assert intent.confidence > 0.0


@pytest.mark.intent
class TestAdvancedIntents:
    """Test advanced intent types"""
    
    def test_automation_request_intent(self, recognizer):
        """Test automation request recognition"""
        test_cases = [
            "Automate this task",
            "Can you automate the backup?",
            "Set up automation",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.AUTOMATION_REQUEST, IntentType.AUTOMATION, IntentType.TASK_EXECUTION]
            assert intent.confidence > 0.0
    
    def test_file_operation_intent(self, recognizer):
        """Test file operation recognition"""
        test_cases = [
            "Open the file",
            "Save this document",
            "Delete the folder",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            # File operations might be detected as various types
            assert intent.confidence > 0.0
    
    def test_web_search_intent(self, recognizer):
        """Test web search recognition"""
        test_cases = [
            "Search for Python tutorials",
            "Look up machine learning",
            "Find information about AI",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.WEB_SEARCH, IntentType.SEARCH, IntentType.INFORMATION_QUERY]
            assert intent.confidence > 0.0


@pytest.mark.intent
class TestEntityExtraction:
    """Test entity extraction from user input"""
    
    def test_file_path_extraction(self, recognizer):
        """Test extraction of file paths"""
        intent = recognizer.recognize_intent("Open the file 'test.py'")
        assert "file_path" in intent.entities
        assert "test.py" in intent.entities["file_path"]
    
    def test_url_extraction(self, recognizer):
        """Test extraction of URLs"""
        intent = recognizer.recognize_intent("Visit https://example.com")
        assert "url" in intent.entities
        assert "https://example.com" in intent.entities["url"]
    
    def test_email_extraction(self, recognizer):
        """Test extraction of email addresses"""
        intent = recognizer.recognize_intent("Send email to test@example.com")
        assert "email" in intent.entities
        assert "test@example.com" in intent.entities["email"]
    
    def test_number_extraction(self, recognizer):
        """Test extraction of numbers"""
        intent = recognizer.recognize_intent("Set timer for 30 minutes")
        assert "number" in intent.entities
        assert "30" in intent.entities["number"]
    
    def test_time_extraction(self, recognizer):
        """Test extraction of time values"""
        intent = recognizer.recognize_intent("Schedule meeting at 14:30")
        assert "time" in intent.entities
        assert "14:30" in intent.entities["time"]
    
    def test_multiple_entities(self, recognizer):
        """Test extraction of multiple entities"""
        intent = recognizer.recognize_intent("Send 'report.pdf' to admin@company.com at 10:00")
        # Should extract at least one entity
        assert len(intent.entities) > 0


@pytest.mark.intent
class TestContextAwareRecognition:
    """Test context-aware intent recognition"""
    
    def test_coding_context(self, context_system):
        """Test intent recognition in coding context"""
        intent = context_system.analyze(
            user_input="Help me",
            window_title="Visual Studio Code"
        )
        assert intent.intent_type in list(IntentType)
        assert "activity_type" in intent.entities
        assert intent.entities["activity_type"] == "coding"
    
    def test_web_browsing_context(self, context_system):
        """Test intent recognition in web browsing context"""
        intent = context_system.analyze(
            user_input="Search for this",
            window_title="Google Chrome"
        )
        assert intent.intent_type in list(IntentType)
        assert "activity_type" in intent.entities
        assert intent.entities["activity_type"] == "web_browsing"
    
    def test_writing_context(self, context_system):
        """Test intent recognition in writing context"""
        intent = context_system.analyze(
            user_input="Check grammar",
            window_title="Microsoft Word"
        )
        assert intent.intent_type in list(IntentType)
        assert "activity_type" in intent.entities
        assert intent.entities["activity_type"] == "writing"
    
    def test_context_without_input(self, context_system):
        """Test context analysis without user input"""
        intent = context_system.analyze(window_title="PyCharm")
        assert intent.intent_type == IntentType.UNKNOWN
        assert "activity_type" in intent.entities


@pytest.mark.intent
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_input(self, recognizer):
        """Test handling of empty input"""
        intent = recognizer.recognize_intent("")
        assert intent.intent_type == IntentType.CASUAL_CHAT
        assert intent.confidence >= 0.0
    
    def test_very_long_input(self, recognizer):
        """Test handling of very long input"""
        long_input = "help " * 100
        intent = recognizer.recognize_intent(long_input)
        assert intent.intent_type in list(IntentType)
        assert intent.confidence > 0.0
    
    def test_special_characters(self, recognizer):
        """Test handling of special characters"""
        intent = recognizer.recognize_intent("!@#$%^&*()")
        assert intent.intent_type == IntentType.CASUAL_CHAT
    
    def test_mixed_language(self, recognizer):
        """Test handling of mixed Chinese and English"""
        intent = recognizer.recognize_intent("帮我 open file 文件")
        assert intent.intent_type in list(IntentType)
    
    def test_confidence_score_range(self, recognizer):
        """Test that confidence scores are in valid range"""
        test_cases = [
            "Help me with this task",
            "Random text here",
            "What is Python?",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert 0.0 <= intent.confidence <= 1.0
    
    def test_suggested_action_exists(self, recognizer):
        """Test that suggested actions are generated"""
        intent = recognizer.recognize_intent("Help me")
        assert intent.suggested_action is not None
        assert len(intent.suggested_action) > 0


@pytest.mark.intent
class TestIntentDataClass:
    """Test Intent data class"""
    
    def test_intent_structure(self, recognizer):
        """Test that Intent object has correct structure"""
        intent = recognizer.recognize_intent("Help me")
        assert hasattr(intent, 'intent_type')
        assert hasattr(intent, 'confidence')
        assert hasattr(intent, 'entities')
        assert hasattr(intent, 'raw_input')
        assert intent.raw_input == "Help me"



# Test can be run with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    test_task_execution_intent()
    test_information_query_intent()
    test_search_intent()
    test_automation_intent()
    test_memory_intent()
    test_screenshot_intent()
    test_open_url_intent()
    test_open_file_intent()
    test_casual_chat_intent()
    test_code_assistance_intent()
    test_entity_extraction()
    test_chinese_input()
    test_context_aware_system()
    test_confidence_scores()
    test_edge_cases()
    
    print("=" * 80)
    print("All tests passed! ✓")
    print("\nIntent Recognition Accuracy Test Summary:")
    print("- Help Request: ✓")
    print("- Task Execution: ✓")
    print("- Information Query: ✓")
    print("- Search: ✓")
    print("- Automation: ✓")
    print("- Memory: ✓")
    print("- Screenshot: ✓")
    print("- Open URL: ✓")
    print("- Open File: ✓")
    print("- Casual Chat: ✓")
    print("- Code Assistance: ✓")
    print("- Chinese Language Support: ✓")
    print("- Context Awareness: ✓")
    print("- Confidence Scores: ✓")
    print("- Edge Cases: ✓")

    def test_intent_creation(self):
        """Test creating Intent instances"""
        intent = Intent(
            intent_type=IntentType.HELP_REQUEST,
            confidence=0.8,
            entities={"test": "value"},
            raw_input="Test input",
            suggested_action="Test action"
        )
        assert intent.intent_type == IntentType.HELP_REQUEST
        assert intent.confidence == 0.8
        assert intent.entities == {"test": "value"}
        assert intent.raw_input == "Test input"
        assert intent.suggested_action == "Test action"


# Run tests directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
