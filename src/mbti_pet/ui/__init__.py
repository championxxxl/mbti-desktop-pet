"""
Desktop Pet UI
PyQt5-based interface for the desktop pet
"""

import sys
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox,
    QSystemTrayIcon, QMenu, QAction, QDialog, QListWidget,
    QDialogButtonBox, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap

from mbti_pet.personality import MBTIPersonality, MBTIType
from mbti_pet.intent import ContextAwareIntentSystem
from mbti_pet.memory import MemoryManager
from mbti_pet.automation import AutomationAssistant


class MemoryDialog(QDialog):
    """Dialog to display memory summary"""
    
    def __init__(self, memory_manager, parent=None):
        super().__init__(parent)
        self.memory = memory_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize the memory dialog UI"""
        self.setWindowTitle("Memory Summary 🧠")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Memory & Conversation History")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Memory content
        self.memory_display = QTextEdit()
        self.memory_display.setReadOnly(True)
        
        # Load and display memory data
        summary = self.memory.get_summary()
        recent_memories = self.memory.db.get_recent_memories(limit=10)
        
        content = f"<h3>Memory Summary</h3>"
        content += f"<p>{summary}</p>"
        content += f"<h3>Recent Interactions</h3>"
        
        for mem in recent_memories:
            content += f"<div style='margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 5px;'>"
            content += f"<b>{mem.interaction_type}</b> - <i>{mem.timestamp}</i><br>"
            content += f"{mem.content[:100]}..."
            content += f"</div>"
        
        # Get user patterns
        patterns = self.memory.get_user_preferences()
        if patterns.get('common_tasks') or patterns.get('frequent_apps'):
            content += f"<h3>Learned Patterns</h3>"
            if patterns.get('common_tasks'):
                content += f"<p><b>Common Tasks:</b> {len(patterns['common_tasks'])} patterns</p>"
            if patterns.get('frequent_apps'):
                content += f"<p><b>Frequent Apps:</b> {len(patterns['frequent_apps'])} apps</p>"
        
        self.memory_display.setHtml(content)
        layout.addWidget(self.memory_display)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)


class AutomationDialog(QDialog):
    """Dialog to display and execute automation tasks"""
    
    def __init__(self, automation_assistant, parent=None):
        super().__init__(parent)
        self.automation = automation_assistant
        self.parent_widget = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize the automation dialog UI"""
        self.setWindowTitle("Automation Tasks ⚡")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Available Automation Tasks")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instructions
        info_label = QLabel("Select a task and click 'Execute' to run it:")
        info_label.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(info_label)
        
        # Task list
        self.task_list = QListWidget()
        tasks = self.automation.get_available_tasks()
        
        for task_name in tasks:
            self.task_list.addItem(task_name)
        
        layout.addWidget(self.task_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.execute_button = QPushButton("Execute Task")
        self.execute_button.clicked.connect(self.execute_selected_task)
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin-top: 10px; padding: 5px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def execute_selected_task(self):
        """Execute the selected automation task"""
        current_item = self.task_list.currentItem()
        if not current_item:
            self.status_label.setText("⚠️ Please select a task first!")
            self.status_label.setStyleSheet("color: orange; margin-top: 10px; padding: 5px;")
            return
        
        task_name = current_item.text()
        self.status_label.setText(f"⏳ Executing '{task_name}'...")
        self.status_label.setStyleSheet("color: blue; margin-top: 10px; padding: 5px;")
        QApplication.processEvents()  # Update UI
        
        # Execute the task
        success = self.automation.execute_task_by_name(task_name)
        
        if success:
            self.status_label.setText(f"✅ '{task_name}' executed successfully!")
            self.status_label.setStyleSheet("color: green; margin-top: 10px; padding: 5px;")
            
            # Notify parent widget if available
            if self.parent_widget and hasattr(self.parent_widget, 'add_message'):
                self.parent_widget.add_message(
                    "Pet", 
                    f"✅ Automation task '{task_name}' completed successfully!"
                )
        else:
            self.status_label.setText(f"❌ Failed to execute '{task_name}'")
            self.status_label.setStyleSheet("color: red; margin-top: 10px; padding: 5px;")
            
            # Notify parent widget if available
            if self.parent_widget and hasattr(self.parent_widget, 'add_message'):
                self.parent_widget.add_message(
                    "Pet", 
                    f"❌ Failed to execute automation task '{task_name}'"
                )


class PetWidget(QWidget):
    """Main desktop pet window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.personality = MBTIPersonality.from_string("ENFP")
        self.intent_system = ContextAwareIntentSystem()
        self.memory = MemoryManager()
        self.automation = AutomationAssistant()
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        # Window settings
        self.setWindowTitle("MBTI Desktop Pet")
        self.setGeometry(100, 100, 600, 700)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        # Personality selector
        personality_label = QLabel("Personality:")
        self.personality_combo = QComboBox()
        for mbti_type in MBTIType:
            self.personality_combo.addItem(mbti_type.value)
        self.personality_combo.currentTextChanged.connect(self.change_personality)
        
        header_layout.addWidget(personality_label)
        header_layout.addWidget(self.personality_combo)
        header_layout.addStretch()
        
        # Pet display area
        self.pet_display = QLabel()
        self.pet_display.setFont(QFont("Arial", 48))
        self.pet_display.setAlignment(Qt.AlignCenter)
        self.pet_display.setStyleSheet("padding: 20px;")
        self.update_pet_display()
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(300)
        
        # Add greeting message
        greeting = self.personality.get_greeting()
        self.add_message("Pet", greeting)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.screenshot_button = QPushButton("📸 Screenshot")
        self.screenshot_button.setObjectName("screenshot_button")
        self.screenshot_button.setToolTip("Take a screenshot of the current screen")
        self.screenshot_button.clicked.connect(self.take_screenshot)
        
        self.memory_button = QPushButton("🧠 Memory")
        self.memory_button.setObjectName("memory_button")
        self.memory_button.setToolTip("View conversation history and learned patterns")
        self.memory_button.clicked.connect(self.show_memory)
        
        self.automate_button = QPushButton("⚡ Automate")
        self.automate_button.setObjectName("automate_button")
        self.automate_button.setToolTip("View and execute automation tasks")
        self.automate_button.clicked.connect(self.show_automation)
        
        action_layout.addWidget(self.screenshot_button)
        action_layout.addWidget(self.memory_button)
        action_layout.addWidget(self.automate_button)
        
        # Assemble layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.pet_display)
        main_layout.addWidget(self.chat_display)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(action_layout)
        
        self.setLayout(main_layout)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#screenshot_button {
                background-color: #2196F3;
            }
            QPushButton#screenshot_button:hover {
                background-color: #0b7dda;
            }
            QPushButton#memory_button {
                background-color: #9C27B0;
            }
            QPushButton#memory_button:hover {
                background-color: #7B1FA2;
            }
            QPushButton#automate_button {
                background-color: #FF9800;
            }
            QPushButton#automate_button:hover {
                background-color: #F57C00;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QToolTip {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        
    def update_pet_display(self):
        """Update pet emoji display"""
        emoji = self.personality.traits.default_emoji
        self.pet_display.setText(emoji)
        
    def change_personality(self, mbti_type_str: str):
        """Change pet personality"""
        self.personality = MBTIPersonality.from_string(mbti_type_str)
        self.update_pet_display()
        
        greeting = self.personality.get_greeting()
        self.add_message("Pet", f"Personality changed! {greeting}")
        
    def add_message(self, sender: str, message: str):
        """Add a message to chat display"""
        formatted_message = f"<b>{sender}:</b> {message}<br>"
        self.chat_display.append(formatted_message)
        
    def send_message(self):
        """Handle user message"""
        user_input = self.input_field.text().strip()
        
        if not user_input:
            return
        
        # Display user message
        self.add_message("You", user_input)
        self.input_field.clear()
        
        # Recognize intent
        intent = self.intent_system.analyze(user_input=user_input)
        
        # Record in memory
        self.memory.record_interaction(
            interaction_type="text_input",
            content=user_input,
            context={"intent": intent.intent_type.value},
            importance=7
        )
        
        # Generate response
        response = self.generate_response(intent)
        pet_response = self.personality.format_response(response)
        
        self.add_message("Pet", pet_response)
        
        # Record response in memory
        self.memory.record_interaction(
            interaction_type="response",
            content=response,
            importance=5
        )
        
    def generate_response(self, intent) -> str:
        """Generate response based on intent and personality"""
        # Use intent's suggested action as base
        base_response = intent.suggested_action or "I'm here to help!"
        
        # Add personality-specific touch
        traits = self.personality.traits
        
        if intent.intent_type.value == "help_request":
            return f"{base_response} I'm particularly good at {', '.join(traits.helpful_traits[:2])}."
        elif intent.intent_type.value == "automation_request":
            return f"{base_response} I can automate many tasks for you!"
        else:
            return base_response
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            success = self.automation.execute_task_by_name("Take Screenshot")
            
            if success:
                filepath = "screenshot.png"
                message = f"Screenshot taken successfully! 📸\nSaved to: {filepath}"
                
                # Show success message box with preview option
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Screenshot Success")
                msg_box.setText(message)
                msg_box.setIcon(QMessageBox.Information)
                
                # Try to show preview if file exists
                try:
                    import os
                    if os.path.exists(filepath):
                        pixmap = QPixmap(filepath)
                        if not pixmap.isNull():
                            # Scale down for preview
                            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            msg_box.setIconPixmap(scaled_pixmap)
                except Exception as e:
                    print(f"Could not load screenshot preview: {e}")
                
                msg_box.exec_()
                self.add_message("Pet", self.personality.format_response(message))
            else:
                message = "Failed to take screenshot. 😔\nPlease check if pyautogui is installed and you have necessary permissions."
                QMessageBox.warning(self, "Screenshot Failed", message)
                self.add_message("Pet", self.personality.format_response(message))
        except Exception as e:
            message = f"Error taking screenshot: {str(e)}"
            QMessageBox.critical(self, "Screenshot Error", message)
            self.add_message("Pet", self.personality.format_response(message))
        
    def show_memory(self):
        """Show memory summary in a dialog"""
        try:
            dialog = MemoryDialog(self.memory, self)
            dialog.exec_()
        except Exception as e:
            message = f"Error displaying memory: {str(e)}"
            QMessageBox.warning(self, "Memory Error", message)
            self.add_message("Pet", self.personality.format_response(message))
        
    def show_automation(self):
        """Show automation options in a dialog"""
        try:
            dialog = AutomationDialog(self.automation, self)
            dialog.exec_()
        except Exception as e:
            message = f"Error displaying automation tasks: {str(e)}"
            QMessageBox.warning(self, "Automation Error", message)
            self.add_message("Pet", self.personality.format_response(message))


class DesktopPetApp:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("MBTI Desktop Pet")
        
        # Main widget
        self.widget = PetWidget()
        
        # System tray icon (optional)
        self.create_tray_icon()
        
    def create_tray_icon(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self.app)
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self.app)
        show_action.triggered.connect(self.widget.show)
        
        hide_action = QAction("Hide", self.app)
        hide_action.triggered.connect(self.widget.hide)
        
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.app.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("MBTI Desktop Pet")
        
        # Note: Icon would need to be set with an actual icon file
        # self.tray_icon.setIcon(QIcon("icon.png"))
        
        self.tray_icon.show()
    
    def run(self):
        """Run the application"""
        self.widget.show()
        sys.exit(self.app.exec_())


def main():
    """Main entry point"""
    app = DesktopPetApp()
    app.run()


if __name__ == "__main__":
    main()
