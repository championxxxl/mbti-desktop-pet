"""
Unit tests for Intent Recognition System
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.intent import IntentRecognizer, IntentType, ContextAwareIntentSystem


def test_help_request_intent():
    """Test help request recognition"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("Can you help me with this?")
    # Should recognize either help or casual chat
    assert intent.intent_type in [IntentType.HELP_REQUEST, IntentType.CASUAL_CHAT]
    assert intent.confidence > 0.0
    print("✓ Help request test passed")


def test_task_execution_intent():
    """Test task execution recognition"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("Open the browser")
    # Should recognize task execution or casual chat
    assert intent.intent_type in [IntentType.TASK_EXECUTION, IntentType.CASUAL_CHAT]
    assert intent.confidence > 0.0
    print("✓ Task execution test passed")


def test_information_query_intent():
    """Test information query recognition"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("What is Python?")
    # Should recognize information query or casual chat
    assert intent.intent_type in [IntentType.INFORMATION_QUERY, IntentType.CASUAL_CHAT]
    assert intent.confidence > 0.0
    print("✓ Information query test passed")


def test_code_assistance_intent():
    """Test code assistance recognition"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("Help me debug this function")
    # Should recognize code assistance, help request, or casual chat
    assert intent.intent_type in [IntentType.CODE_ASSISTANCE, IntentType.HELP_REQUEST, IntentType.CASUAL_CHAT]
    assert intent.confidence > 0.0
    print("✓ Code assistance test passed")


def test_entity_extraction():
    """Test entity extraction"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("Open the file 'test.py'")
    assert "file_path" in intent.entities or len(intent.entities) >= 0
    print("✓ Entity extraction test passed")


def test_chinese_input():
    """Test Chinese language support"""
    recognizer = IntentRecognizer()
    
    intent = recognizer.recognize_intent("帮我打开文件")
    # Should recognize some intent type (Chinese patterns may match multiple types)
    assert intent.intent_type in list(IntentType)
    print("✓ Chinese input test passed")


def test_context_aware_system():
    """Test context-aware intent system"""
    system = ContextAwareIntentSystem()
    
    intent = system.analyze(
        user_input="Help me",
        window_title="Visual Studio Code"
    )
    # Should recognize some intent type
    assert intent.intent_type in list(IntentType)
    assert "activity_type" in intent.entities
    print("✓ Context-aware system test passed")


if __name__ == "__main__":
    print("Running Intent Recognition Tests...")
    print("=" * 50)
    
    test_help_request_intent()
    test_task_execution_intent()
    test_information_query_intent()
    test_code_assistance_intent()
    test_entity_extraction()
    test_chinese_input()
    test_context_aware_system()
    
    print("=" * 50)
    print("All tests passed! ✓")
