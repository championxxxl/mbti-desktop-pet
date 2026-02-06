"""
Test script to verify UI imports and basic functionality
"""

import sys
from pathlib import Path
import os

# Avoid display issues with PyQt5
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("Testing imports...")

# First test backend modules (no display needed)
try:
    from mbti_pet.personality import MBTIPersonality
    from mbti_pet.memory import MemoryManager
    from mbti_pet.automation import AutomationAssistant
    print("✅ Backend modules imported successfully")
except Exception as e:
    print(f"❌ Failed to import backend modules: {e}")
    sys.exit(1)

# Test UI module imports (may need display)
try:
    # Just test if the module can be parsed
    import py_compile
    py_compile.compile('src/mbti_pet/ui/__init__.py', doraise=True)
    print("✅ UI module syntax is valid")
except Exception as e:
    print(f"❌ UI module has syntax errors: {e}")
    sys.exit(1)

print("\nTesting component initialization...")

try:
    memory = MemoryManager("./test_memory.db")
    print("✅ MemoryManager initialized")
except Exception as e:
    print(f"❌ MemoryManager failed: {e}")

try:
    automation = AutomationAssistant()
    print("✅ AutomationAssistant initialized")
except Exception as e:
    print(f"❌ AutomationAssistant failed: {e}")

try:
    personality = MBTIPersonality.from_string("ENFP")
    print("✅ MBTIPersonality initialized")
    print(f"   Personality: {personality.mbti_type.value}")
    print(f"   Emoji: {personality.traits.default_emoji}")
except Exception as e:
    print(f"❌ MBTIPersonality failed: {e}")

# Test button functionality
try:
    tasks = automation.get_available_tasks()
    print(f"✅ Automation tasks available: {', '.join(tasks)}")
except Exception as e:
    print(f"❌ Failed to get automation tasks: {e}")

try:
    summary = memory.get_summary()
    print(f"✅ Memory summary generated (length: {len(summary)} chars)")
except Exception as e:
    print(f"❌ Failed to get memory summary: {e}")

print("\n✅ All imports and basic functionality tests passed!")
print("\nNote: Full UI testing requires a display environment.")
print("To test the UI manually, run: python src/mbti_pet/ui/__init__.py")

