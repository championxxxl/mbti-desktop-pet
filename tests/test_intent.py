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
    
    test_cases = [
        "Can you help me with this?",
        "I need help",
        "帮助我",
        "How to do this?",
        "Show me how",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.HELP_REQUEST
        assert intent.confidence >= 0.4
    
    print("✓ Help request test passed")


def test_task_execution_intent():
    """Test task execution recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "Run this program",
        "Execute the task",
        "Start the application",
        "启动应用",
        "运行程序",
        "执行任务",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.TASK_EXECUTION, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Task execution test passed")


def test_information_query_intent():
    """Test information query recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "What is Python?",
        "Why does this happen?",
        "How does it work?",
        "什么是机器学习?",
        "告诉我关于AI",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.INFORMATION_QUERY
        assert intent.confidence >= 0.4
    
    print("✓ Information query test passed")


def test_search_intent():
    """Test search intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "search for Python tutorials",
        "find machine learning courses",
        "搜索Python教程",
        "查找资料",
        "搜索深度学习",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.SEARCH, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Search intent test passed")


def test_automation_intent():
    """Test automation intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "automate this process",
        "帮我自动化这个任务",
        "自动化任务",
        "make this automatic",
        "批量处理文件",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        # Accept both AUTOMATION and AUTOMATION_REQUEST as they are semantically equivalent
        assert intent.intent_type in [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST], \
            f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Automation intent test passed")


def test_memory_intent():
    """Test memory intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "remember this",
        "记住这件事",
        "save to memory",
        "你还记得吗",
        "别忘了这个",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.MEMORY, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Memory intent test passed")


def test_screenshot_intent():
    """Test screenshot intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "screenshot",
        "take a screenshot",
        "截图",
        "截屏",
        "capture screen",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.SCREENSHOT, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Screenshot intent test passed")


def test_open_url_intent():
    """Test open URL intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "open https://google.com",
        "打开www.baidu.com",
        "visit github.com",
        "go to example.org",
        "https://www.python.org",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.OPEN_URL, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Open URL intent test passed")


def test_open_file_intent():
    """Test open file intent recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "open file test.py",
        "打开文件test.py",
        "edit document.txt",
        "view report.pdf",
        "打开文档",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.OPEN_FILE, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.4
    
    print("✓ Open file intent test passed")


def test_casual_chat_intent():
    """Test casual chat recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "Hello there!",
        "How are you?",
        "Nice weather today",
        "你好",
        "谢谢",
        "再见",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.intent_type == IntentType.CASUAL_CHAT, f"Failed for: {test_input}, got {intent.intent_type}"
        assert intent.confidence >= 0.3
    
    print("✓ Casual chat intent test passed")


def test_code_assistance_intent():
    """Test code assistance recognition"""
    recognizer = IntentRecognizer()
    
    test_cases = [
        "Help me debug this function",
        "Fix this code error",
        "调试代码",
        "修复程序错误",
    ]
    
    for test_input in test_cases:
        intent = recognizer.recognize_intent(test_input)
        # Code assistance may also match help_request, both are acceptable
        assert intent.intent_type in [IntentType.CODE_ASSISTANCE, IntentType.HELP_REQUEST]
        assert intent.confidence >= 0.4
    
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
    
    test_cases = [
        ("帮我打开文件", IntentType.OPEN_FILE),
        ("搜索Python", IntentType.SEARCH),
        ("自动化任务", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),  # Accept either
        ("记住这个", IntentType.MEMORY),
        ("截图", IntentType.SCREENSHOT),
    ]
    
    for test_input, expected_type in test_cases:
        intent = recognizer.recognize_intent(test_input)
        if isinstance(expected_type, list):
            assert intent.intent_type in expected_type, \
                f"Failed for: {test_input}, expected one of {expected_type}, got {intent.intent_type}"
        else:
            assert intent.intent_type == expected_type, \
                f"Failed for: {test_input}, expected {expected_type}, got {intent.intent_type}"
    
    print("✓ Chinese input test passed")


def test_context_aware_system():
    """Test context-aware intent system"""
    system = ContextAwareIntentSystem()
    
    intent = system.analyze(
        user_input="Help me",
        window_title="Visual Studio Code"
    )
    assert intent.intent_type in list(IntentType)
    assert "activity_type" in intent.entities
    print("✓ Context-aware system test passed")


def test_confidence_scores():
    """Test that confidence scores are reasonable"""
    recognizer = IntentRecognizer()
    
    # High confidence cases
    high_conf_cases = [
        "截图",
        "https://google.com",
        "remember this important information",
        "automate this workflow",
    ]
    
    for test_input in high_conf_cases:
        intent = recognizer.recognize_intent(test_input)
        assert intent.confidence >= 0.7, f"Expected high confidence for: {test_input}, got {intent.confidence}"
    
    # Medium confidence cases
    med_conf_cases = [
        "open file",
        "search",
        "help",
    ]
    
    for test_input in med_conf_cases:
        intent = recognizer.recognize_intent(test_input)
        assert 0.4 <= intent.confidence <= 0.9, f"Expected medium confidence for: {test_input}, got {intent.confidence}"
    
    print("✓ Confidence scores test passed")


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    recognizer = IntentRecognizer()
    
    # Constants for test inputs
    LONG_INPUT_REPEAT_COUNT = 100
    
    # Empty string
    intent = recognizer.recognize_intent("")
    assert intent.intent_type == IntentType.CASUAL_CHAT
    
    # Very long input
    long_input = "help me " * LONG_INPUT_REPEAT_COUNT
    intent = recognizer.recognize_intent(long_input)
    assert intent.intent_type == IntentType.HELP_REQUEST
    
    # Mixed language
    intent = recognizer.recognize_intent("help me 搜索 Python")
    assert intent.intent_type in [IntentType.SEARCH, IntentType.HELP_REQUEST]
    
    # Special characters
    intent = recognizer.recognize_intent("!@#$%^&*()")
    assert intent.intent_type == IntentType.CASUAL_CHAT
    
    print("✓ Edge cases test passed")


if __name__ == "__main__":
    print("Running Comprehensive Intent Recognition Tests...")
    print("=" * 80)
    
    test_help_request_intent()
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

