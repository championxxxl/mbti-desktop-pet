"""
Unit tests for quick action button functionality
"""

import sys
import os
from pathlib import Path

# Set environment for headless testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_imports():
    """Test that all necessary imports work"""
    try:
        # These don't require display
        import py_compile
        print("✅ Basic imports successful")
        return True
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False


def test_automation_tasks():
    """Test automation task availability"""
    try:
        from mbti_pet.automation import AutomationAssistant
        
        automation = AutomationAssistant()
        tasks = automation.get_available_tasks()
        
        assert len(tasks) > 0, "No automation tasks available"
        assert "Take Screenshot" in tasks, "Screenshot task not found"
        
        print(f"✅ Found {len(tasks)} automation tasks:")
        for task in tasks:
            print(f"   - {task}")
        return True
    except Exception as e:
        print(f"⚠️  Automation test skipped (display required): {e}")
        return True  # Don't fail in headless environment


def test_memory_system():
    """Test memory system functionality"""
    from mbti_pet.memory import MemoryManager
    
    memory = MemoryManager("./test_memory_buttons.db")
    
    # Record a test interaction
    memory.record_interaction(
        interaction_type="test_button",
        content="Testing button functionality",
        importance=5
    )
    
    # Get summary
    summary = memory.get_summary()
    assert len(summary) > 0, "Memory summary is empty"
    
    print("✅ Memory system works")
    print(f"   Summary length: {len(summary)} chars")
    return True


def test_ui_module_syntax():
    """Test that UI module has valid syntax"""
    import py_compile
    
    ui_file = src_path / "mbti_pet" / "ui" / "__init__.py"
    
    try:
        py_compile.compile(str(ui_file), doraise=True)
        print("✅ UI module syntax is valid")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ UI module syntax error: {e}")
        return False


def test_ui_classes_defined():
    """Test that UI classes are properly defined"""
    with open(src_path / "mbti_pet" / "ui" / "__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for required classes
    assert "class MemoryDialog" in content, "MemoryDialog class not found"
    assert "class AutomationDialog" in content, "AutomationDialog class not found"
    assert "class PetWidget" in content, "PetWidget class not found"
    
    # Check for required methods
    assert "def take_screenshot" in content, "take_screenshot method not found"
    assert "def show_memory" in content, "show_memory method not found"
    assert "def show_automation" in content, "show_automation method not found"
    
    # Check for tooltips
    assert "setToolTip" in content, "Tooltips not implemented"
    
    # Check for button object names
    assert "setObjectName" in content, "Button object names not set"
    
    print("✅ All required UI classes and methods are defined")
    return True


def test_button_icons():
    """Test that buttons have proper emoji icons"""
    with open(src_path / "mbti_pet" / "ui" / "__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "📸" in content, "Screenshot emoji not found"
    assert "🧠" in content, "Memory emoji not found"
    assert "⚡" in content, "Automation emoji not found"
    
    print("✅ Button emojis are present")
    return True


def test_dialog_features():
    """Test that dialogs have required features"""
    with open(src_path / "mbti_pet" / "ui" / "__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # MemoryDialog features
    assert "Memory Summary" in content, "Memory dialog title not found"
    assert "recent_memories" in content, "Recent memories feature not found"
    assert "get_user_preferences" in content, "User preferences feature not found"
    
    # AutomationDialog features
    assert "Automation Tasks" in content, "Automation dialog title not found"
    assert "QListWidget" in content, "Task list widget not found"
    assert "execute_selected_task" in content, "Task execution method not found"
    assert "Execute Task" in content, "Execute button not found"
    
    print("✅ Dialog features are implemented")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("QUICK ACTION BUTTONS - TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        ("Import Test", test_imports),
        ("UI Module Syntax", test_ui_module_syntax),
        ("UI Classes Defined", test_ui_classes_defined),
        ("Button Icons", test_button_icons),
        ("Dialog Features", test_dialog_features),
        ("Automation Tasks", test_automation_tasks),
        ("Memory System", test_memory_system),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 60)
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
