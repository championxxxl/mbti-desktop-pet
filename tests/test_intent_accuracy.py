"""
Intent Recognition Accuracy Validation Test
Tests accuracy with a diverse set of realistic inputs
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.intent import IntentRecognizer, IntentType


# Comprehensive test dataset with expected intents
TEST_DATASET = [
    # Help Request
    ("Can you help me?", IntentType.HELP_REQUEST),
    ("I need assistance", IntentType.HELP_REQUEST),
    ("How do I do this?", [IntentType.HELP_REQUEST, IntentType.INFORMATION_QUERY]),  # Accept both
    ("帮我一下", IntentType.HELP_REQUEST),
    ("需要帮助", IntentType.HELP_REQUEST),
    
    # Task Execution
    ("Run the script", IntentType.TASK_EXECUTION),
    ("Execute this command", IntentType.TASK_EXECUTION),
    ("Start the server", IntentType.TASK_EXECUTION),
    ("运行程序", IntentType.TASK_EXECUTION),
    ("执行任务", IntentType.TASK_EXECUTION),
    
    # Information Query
    ("What is machine learning?", IntentType.INFORMATION_QUERY),
    ("Why does this happen?", IntentType.INFORMATION_QUERY),
    ("How does Python work?", IntentType.INFORMATION_QUERY),
    ("什么是人工智能?", IntentType.INFORMATION_QUERY),
    ("告诉我关于深度学习", IntentType.INFORMATION_QUERY),
    
    # Search
    ("search for Python tutorials", IntentType.SEARCH),
    ("find information about AI", IntentType.SEARCH),
    ("lookup machine learning", IntentType.SEARCH),
    ("搜索JavaScript教程", IntentType.SEARCH),
    ("查找React资料", IntentType.SEARCH),
    
    # Automation (accepts both AUTOMATION and AUTOMATION_REQUEST)
    ("automate this workflow", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),
    ("make this automatic", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),
    ("帮我自动化", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),
    ("自动执行任务", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),
    ("批量处理", [IntentType.AUTOMATION, IntentType.AUTOMATION_REQUEST]),
    
    # Memory
    ("remember this", IntentType.MEMORY),
    ("save to memory", IntentType.MEMORY),
    ("记住这件事", IntentType.MEMORY),
    ("别忘了", IntentType.MEMORY),
    ("你还记得吗", IntentType.MEMORY),
    
    # Screenshot
    ("screenshot", IntentType.SCREENSHOT),
    ("take a screenshot", IntentType.SCREENSHOT),
    ("capture screen", IntentType.SCREENSHOT),
    ("截图", IntentType.SCREENSHOT),
    ("截屏", IntentType.SCREENSHOT),
    
    # Open URL
    ("open https://google.com", IntentType.OPEN_URL),
    ("visit www.github.com", IntentType.OPEN_URL),
    ("https://python.org", IntentType.OPEN_URL),
    ("打开www.baidu.com", IntentType.OPEN_URL),
    ("go to example.com", IntentType.OPEN_URL),
    
    # Open File
    ("open file test.py", IntentType.OPEN_FILE),
    ("edit document.txt", IntentType.OPEN_FILE),
    ("view report.pdf", IntentType.OPEN_FILE),
    ("打开文件config.json", IntentType.OPEN_FILE),
    ("查看文档", IntentType.OPEN_FILE),
    
    # Casual Chat
    ("Hello!", IntentType.CASUAL_CHAT),
    ("How are you?", IntentType.CASUAL_CHAT),
    ("Nice weather", IntentType.CASUAL_CHAT),
    ("你好", IntentType.CASUAL_CHAT),
    ("谢谢", IntentType.CASUAL_CHAT),
    ("再见", IntentType.CASUAL_CHAT),
    
    # Code Assistance (may also match HELP_REQUEST)
    ("debug this code", [IntentType.CODE_ASSISTANCE, IntentType.HELP_REQUEST]),
    ("fix this error", [IntentType.CODE_ASSISTANCE, IntentType.HELP_REQUEST]),
    ("调试程序", [IntentType.CODE_ASSISTANCE, IntentType.HELP_REQUEST]),
    
    # Writing Assistance
    ("proofread this", IntentType.WRITING_ASSISTANCE),
    ("check grammar", IntentType.WRITING_ASSISTANCE),
    ("校对文章", IntentType.WRITING_ASSISTANCE),
    
    # Web Search (accept both WEB_SEARCH and SEARCH as they overlap)
    ("google this", IntentType.WEB_SEARCH),
    ("search online", [IntentType.WEB_SEARCH, IntentType.SEARCH]),
    ("在线搜索", IntentType.WEB_SEARCH),
]


def calculate_accuracy():
    """Calculate overall accuracy of intent recognition"""
    recognizer = IntentRecognizer()
    
    total = len(TEST_DATASET)
    correct = 0
    errors = []
    
    print("Testing Intent Recognition Accuracy...")
    print("=" * 90)
    
    for test_input, expected_intent in TEST_DATASET:
        result = recognizer.recognize_intent(test_input)
        
        # Handle cases where multiple intents are acceptable
        if isinstance(expected_intent, list):
            is_correct = result.intent_type in expected_intent
            expected_str = " or ".join([i.value for i in expected_intent])
        else:
            is_correct = result.intent_type == expected_intent
            expected_str = expected_intent.value
        
        status = "✓" if is_correct else "✗"
        
        if is_correct:
            correct += 1
        else:
            errors.append({
                'input': test_input,
                'expected': expected_str,
                'actual': result.intent_type.value,
                'confidence': result.confidence
            })
        
        # Print detailed results for failed cases
        if not is_correct:
            print(f"{status} Input: {test_input:40s}")
            print(f"  Expected: {expected_str:20s}")
            print(f"  Got:      {result.intent_type.value:20s} (confidence: {result.confidence:.2f})")
    
    accuracy = (correct / total) * 100
    
    print("=" * 90)
    print(f"\nAccuracy Results:")
    print(f"  Total Tests: {total}")
    print(f"  Correct: {correct}")
    print(f"  Incorrect: {total - correct}")
    print(f"  Accuracy: {accuracy:.1f}%")
    print()
    
    # Detailed error report
    if errors:
        print("Errors Breakdown:")
        print("-" * 90)
        for error in errors:
            print(f"Input: {error['input']}")
            print(f"  Expected: {error['expected']}")
            print(f"  Got: {error['actual']} (confidence: {error['confidence']:.2f})")
            print()
    
    return accuracy


def test_accuracy_threshold():
    """Test that accuracy meets the 80% threshold"""
    accuracy = calculate_accuracy()
    
    # Acceptance criteria: > 80% accuracy
    threshold = 80.0
    
    if accuracy >= threshold:
        print(f"✓ SUCCESS: Accuracy {accuracy:.1f}% meets the threshold of {threshold}%")
        return True
    else:
        print(f"✗ FAILED: Accuracy {accuracy:.1f}% below threshold of {threshold}%")
        return False


if __name__ == "__main__":
    print("Intent Recognition Accuracy Validation")
    print("=" * 90)
    print()
    
    success = test_accuracy_threshold()
    
    print()
    print("=" * 90)
    
    if success:
        print("Validation PASSED ✓")
        sys.exit(0)
    else:
        print("Validation FAILED ✗")
        sys.exit(1)
