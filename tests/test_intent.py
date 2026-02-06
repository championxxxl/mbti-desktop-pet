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
            "Schedule this to run daily",
            "Repeat this action",
            "Batch process these files",
            "自动执行",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.AUTOMATION_REQUEST, IntentType.TASK_EXECUTION, IntentType.CASUAL_CHAT]
            assert intent.confidence > 0.0
    
    def test_file_operation_intent(self, recognizer):
        """Test file operation recognition"""
        test_cases = [
            "Open the file 'test.py'",
            "Save this document",
            "Delete the folder",
            "Copy these files",
            "Move to directory",
            "保存文件",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.FILE_OPERATION, IntentType.TASK_EXECUTION, IntentType.CASUAL_CHAT]
            assert intent.confidence > 0.0
    
    def test_web_search_intent(self, recognizer):
        """Test web search recognition"""
        test_cases = [
            "Search for Python tutorials",
            "Google this for me",
            "Look up machine learning",
            "Find information online",
            "搜索这个",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [IntentType.WEB_SEARCH, IntentType.INFORMATION_QUERY, IntentType.CASUAL_CHAT]
            assert intent.confidence > 0.0
    
    def test_code_assistance_intent(self, recognizer):
        """Test code assistance recognition"""
        test_cases = [
            "Help me debug this function",
            "Review my code",
            "Fix this error",
            "Explain this class",
            "Write a function to...",
            "编程帮助",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [
                IntentType.CODE_ASSISTANCE, 
                IntentType.HELP_REQUEST, 
                IntentType.WRITING_ASSISTANCE,
                IntentType.CASUAL_CHAT
            ]
            assert intent.confidence > 0.0
    
    def test_writing_assistance_intent(self, recognizer):
        """Test writing assistance recognition"""
        test_cases = [
            "Help me write an email",
            "Draft a proposal",
            "Edit this paragraph",
            "Check my grammar",
            "Proofread this document",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [
                IntentType.WRITING_ASSISTANCE, 
                IntentType.HELP_REQUEST,
                IntentType.CASUAL_CHAT
            ]
            assert intent.confidence > 0.0
    
    def test_system_command_intent(self, recognizer):
        """Test system command recognition"""
        test_cases = [
            "Shutdown the computer",
            "Close the application",
            "Exit the program",
            "Minimize this window",
            "关闭程序",
        ]
        for test_input in test_cases:
            intent = recognizer.recognize_intent(test_input)
            assert intent.intent_type in [
                IntentType.SYSTEM_COMMAND, 
                IntentType.TASK_EXECUTION,
                IntentType.CASUAL_CHAT
            ]
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
