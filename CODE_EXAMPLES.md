# Code Examples - Quick Action Buttons

## Using the Quick Action Buttons

This document provides code examples for understanding and extending the quick action button functionality.

## Basic Usage

### Launching the Application

```python
from mbti_pet.ui import DesktopPetApp

# Create and run the application
app = DesktopPetApp()
app.run()
```

The quick action buttons will be automatically available in the UI.

## Customizing Button Behavior

### Adding a Custom Screenshot Handler

```python
from mbti_pet.ui import PetWidget

class CustomPetWidget(PetWidget):
    def take_screenshot(self):
        """Override screenshot with custom behavior"""
        # Call parent method
        super().take_screenshot()
        
        # Add custom logic
        self.add_message("System", "Screenshot saved to custom location!")
```

### Extending the Memory Dialog

```python
from mbti_pet.ui import MemoryDialog
from PyQt5.QtWidgets import QLabel

class ExtendedMemoryDialog(MemoryDialog):
    def init_ui(self):
        """Add custom sections to memory dialog"""
        super().init_ui()
        
        # Add a custom statistics section
        stats_label = QLabel("Custom Statistics Here")
        self.layout().addWidget(stats_label)
```

### Adding Custom Automation Tasks

```python
from mbti_pet.automation import AutomationTask, AutomationStep, AutomationAction

# Create a custom task
custom_task = AutomationTask(
    name="Send Email",
    description="Open email client and compose new message",
    steps=[
        AutomationStep(
            action=AutomationAction.OPEN_APP,
            parameters={"app_name": "mail"},
            description="Open email client"
        ),
        AutomationStep(
            action=AutomationAction.WAIT,
            parameters={"duration": 2.0},
            description="Wait for app to load"
        ),
        AutomationStep(
            action=AutomationAction.PRESS_KEY,
            parameters={"key": "ctrl+n"},
            description="Create new email"
        )
    ]
)

# Add to automation assistant
from mbti_pet.automation import AutomationAssistant

automation = AutomationAssistant()
# Note: You would need to extend the library to add custom tasks
```

## Integrating with Other Systems

### Recording Button Clicks in Memory

```python
from mbti_pet.memory import MemoryManager

class TrackedPetWidget(PetWidget):
    def take_screenshot(self):
        """Track screenshot button usage"""
        # Record the button click
        self.memory.record_interaction(
            interaction_type="button_click",
            content="Screenshot button clicked",
            context={"button": "screenshot"},
            importance=3
        )
        
        # Call original method
        super().take_screenshot()
```

### Personality-Based Button Text

```python
class PersonalizedPetWidget(PetWidget):
    def init_ui(self):
        super().init_ui()
        
        # Customize button text based on personality
        if self.personality.mbti_type.value == "INTJ":
            self.screenshot_button.setText("📸 Capture")
            self.memory_button.setText("🧠 Analyze")
            self.automate_button.setText("⚡ Execute")
        elif self.personality.mbti_type.value == "ENFP":
            self.screenshot_button.setText("📸 Snap!")
            self.memory_button.setText("🧠 Remember!")
            self.automate_button.setText("⚡ Let's go!")
```

## Advanced Customization

### Custom Button Styling

```python
class StyledPetWidget(PetWidget):
    def init_ui(self):
        super().init_ui()
        
        # Apply custom styles
        self.screenshot_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A90E2, stop:1 #357ABD
                );
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
        """)
```

### Adding Keyboard Shortcuts

```python
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class KeyboardPetWidget(PetWidget):
    def init_ui(self):
        super().init_ui()
        
        # Add keyboard shortcuts
        screenshot_shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        screenshot_shortcut.activated.connect(self.take_screenshot)
        
        memory_shortcut = QShortcut(QKeySequence("Ctrl+Shift+M"), self)
        memory_shortcut.activated.connect(self.show_memory)
        
        automation_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        automation_shortcut.activated.connect(self.show_automation)
```

### Progress Indicators for Long Operations

```python
from PyQt5.QtWidgets import QProgressDialog

class ProgressPetWidget(PetWidget):
    def take_screenshot(self):
        """Add progress indicator"""
        # Show progress dialog
        progress = QProgressDialog("Taking screenshot...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        try:
            # Take screenshot
            super().take_screenshot()
        finally:
            progress.close()
```

## Testing Button Functionality

### Unit Test Example

```python
import unittest
from unittest.mock import Mock, patch
from mbti_pet.ui import PetWidget

class TestQuickButtons(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = QApplication([])
        self.widget = PetWidget()
    
    def test_screenshot_button_exists(self):
        """Test that screenshot button is created"""
        self.assertIsNotNone(self.widget.screenshot_button)
        self.assertEqual(self.widget.screenshot_button.text(), "📸 Screenshot")
    
    def test_memory_button_tooltip(self):
        """Test memory button has tooltip"""
        tooltip = self.widget.memory_button.toolTip()
        self.assertIn("conversation history", tooltip.lower())
    
    @patch('mbti_pet.automation.AutomationAssistant.execute_task_by_name')
    def test_screenshot_execution(self, mock_execute):
        """Test screenshot button execution"""
        mock_execute.return_value = True
        self.widget.take_screenshot()
        mock_execute.assert_called_once_with("Take Screenshot")
    
    def tearDown(self):
        """Clean up"""
        self.app.quit()
```

### Integration Test Example

```python
def test_button_integration():
    """Test full button workflow"""
    from mbti_pet.ui import DesktopPetApp
    
    # Create app
    app = DesktopPetApp()
    widget = app.widget
    
    # Test initial state
    assert widget.screenshot_button.isEnabled()
    assert widget.memory_button.isEnabled()
    assert widget.automate_button.isEnabled()
    
    # Test button connections
    assert widget.screenshot_button.receivers(widget.screenshot_button.clicked) > 0
    assert widget.memory_button.receivers(widget.memory_button.clicked) > 0
    assert widget.automate_button.receivers(widget.automate_button.clicked) > 0
```

## Debugging Tips

### Logging Button Events

```python
import logging

class DebuggablePetWidget(PetWidget):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
    
    def take_screenshot(self):
        self.logger.info("Screenshot button clicked")
        try:
            super().take_screenshot()
            self.logger.info("Screenshot completed successfully")
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            raise
```

### Testing Dialog Display

```python
def test_memory_dialog():
    """Test memory dialog without Qt event loop"""
    from mbti_pet.memory import MemoryManager
    from mbti_pet.ui import MemoryDialog
    
    # Create memory manager
    memory = MemoryManager("./test.db")
    memory.record_interaction("test", "Test interaction", importance=5)
    
    # Create dialog (don't exec_, just show)
    dialog = MemoryDialog(memory)
    
    # Verify dialog properties
    assert dialog.windowTitle() == "Memory Summary 🧠"
    assert dialog.memory_display.toPlainText() != ""
```

## Performance Optimization

### Lazy Loading Dialog Content

```python
class OptimizedMemoryDialog(MemoryDialog):
    def init_ui(self):
        """Initialize dialog without loading content"""
        super().__init__(parent, load_content=False)
        
    def showEvent(self, event):
        """Load content only when dialog is shown"""
        self.load_memory_content()
        super().showEvent(event)
    
    def load_memory_content(self):
        """Load memory data on demand"""
        summary = self.memory.get_summary()
        self.memory_display.setHtml(self.format_memory(summary))
```

### Caching Automation Tasks

```python
class CachedAutomationDialog(AutomationDialog):
    _task_cache = None
    
    def init_ui(self):
        """Use cached tasks if available"""
        if not CachedAutomationDialog._task_cache:
            CachedAutomationDialog._task_cache = self.automation.get_available_tasks()
        
        self.tasks = CachedAutomationDialog._task_cache
        super().init_ui()
```

## Error Handling Best Practices

### Graceful Degradation

```python
class RobustPetWidget(PetWidget):
    def take_screenshot(self):
        """Robust screenshot with fallback"""
        try:
            super().take_screenshot()
        except ImportError:
            # pyautogui not installed
            QMessageBox.warning(
                self,
                "Feature Unavailable",
                "Screenshot feature requires pyautogui.\n"
                "Install with: pip install pyautogui"
            )
        except PermissionError:
            # Permission denied
            QMessageBox.critical(
                self,
                "Permission Error",
                "Unable to capture screen. Please grant screen recording permissions."
            )
        except Exception as e:
            # Generic error
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}"
            )
```

## Extension Points

### Custom Action Buttons

```python
class ExtendedPetWidget(PetWidget):
    def init_ui(self):
        super().init_ui()
        
        # Add a fourth button
        self.notes_button = QPushButton("📝 Notes")
        self.notes_button.setObjectName("notes_button")
        self.notes_button.setToolTip("Take quick notes")
        self.notes_button.clicked.connect(self.show_notes)
        
        # Add to action layout
        action_layout = self.findChild(QHBoxLayout)  # Find the action layout
        if action_layout:
            action_layout.addWidget(self.notes_button)
    
    def show_notes(self):
        """Show notes dialog"""
        # Implementation here
        pass
```

## Conclusion

These examples demonstrate how to:
1. Use the quick action buttons
2. Customize button behavior
3. Extend functionality
4. Test implementations
5. Handle errors gracefully
6. Optimize performance

For more information, see:
- `QUICK_ACTION_BUTTONS.md` - Feature documentation
- `UI_VISUAL_GUIDE.md` - Visual design guide
- `src/mbti_pet/ui/__init__.py` - Full implementation
