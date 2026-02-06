"""
Desktop Pet UI
PyQt5-based interface for the desktop pet
"""

import sys
import logging
from typing import Optional
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox,
    QSystemTrayIcon, QMenu, QAction, QListWidget, QListWidgetItem,
    QScrollArea, QDialog, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QPixmap

from mbti_pet.personality import MBTIPersonality, MBTIType
from mbti_pet.intent import ContextAwareIntentSystem
from mbti_pet.memory import MemoryManager
from mbti_pet.automation import AutomationAssistant

# Configure logging
logger = logging.getLogger(__name__)


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


class MessageWidget(QWidget):
    """Custom widget for displaying a single chat message"""
    
    def __init__(self, sender: str, message: str, timestamp: str, is_user: bool = False):
        super().__init__()
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        self.is_user = is_user
        self.init_ui()
    
    def init_ui(self):
        """Initialize the message widget UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Create message container
        message_container = QWidget()
        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(12, 8, 12, 8)
        message_layout.setSpacing(4)
        
        # Sender and timestamp row
        header_layout = QHBoxLayout()
        sender_label = QLabel(self.sender)
        sender_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        time_label = QLabel(self.timestamp)
        time_label.setFont(QFont("Arial", 9))
        time_label.setStyleSheet("color: #666;")
        
        header_layout.addWidget(sender_label)
        header_layout.addWidget(time_label)
        header_layout.addStretch()
        
        # Message content
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Arial", 11))
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        message_layout.addLayout(header_layout)
        message_layout.addWidget(message_label)
        
        message_container.setLayout(message_layout)
        
        # Style based on sender
        if self.is_user:
            # User message - right aligned with green background
            message_container.setStyleSheet("""
                QWidget {
                    background-color: #DCF8C6;
                    border-radius: 10px;
                    max-width: 400px;
                }
            """)
            sender_label.setStyleSheet("color: #075E54;")
            layout.addStretch()
            layout.addWidget(message_container)
        else:
            # Pet message - left aligned with white background
            message_container.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    border-radius: 10px;
                    max-width: 400px;
                }
            """)
            sender_label.setStyleSheet("color: #128C7E;")
            layout.addWidget(message_container)
            layout.addStretch()
        
        self.setLayout(layout)


class PetWidget(QWidget):
    """Main desktop pet window"""
    
    # Configuration constants
    MESSAGE_HISTORY_LIMIT = 20  # Maximum number of historical messages to load
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.personality = MBTIPersonality.from_string("ENFP")
        self.intent_system = ContextAwareIntentSystem()
        self.memory = MemoryManager()
        self.automation = AutomationAssistant()
        
        # Sending state management
        self.is_sending = False
        
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
        
        # Chat display - using QListWidget for better message management
        self.chat_display = QListWidget()
        self.chat_display.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.chat_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_display.setMinimumHeight(300)
        self.chat_display.setStyleSheet("""
            QListWidget {
                background-color: #F0F0F0;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QListWidget::item:selected {
                background-color: transparent;
            }
        """)
        
        # Load message history from memory
        self.load_message_history()
        
        # Add greeting message
        greeting = self.personality.get_greeting()
        self.add_message("Pet", greeting, is_user=False)
        
        # Input area
        input_layout = QHBoxLayout()
        
        # Input field with Enter key binding
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        # Connect Enter key to send message
        self.input_field.returnPressed.connect(self.send_message)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setToolTip("Click to send message (or press Enter)")
        
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
        """Update pet emoji display based on current personality"""
        emoji = self.personality.traits.default_emoji
        self.pet_display.setText(emoji)
        
    def change_personality(self, mbti_type_str: str):
        """
        Change pet personality type
        
        Args:
            mbti_type_str: MBTI type string (e.g., "ENFP", "INTJ")
        """
        self.personality = MBTIPersonality.from_string(mbti_type_str)
        self.update_pet_display()
        
        greeting = self.personality.get_greeting()
        self.add_message("Pet", f"Personality changed! {greeting}", is_user=False)
        
    def add_message(self, sender: str, message: str, is_user: bool = False, timestamp: Optional[str] = None):
        """Add a message to chat display with timestamp and proper styling"""
        # Generate timestamp if not provided
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        
        # Create message widget
        message_widget = MessageWidget(sender, message, timestamp, is_user)
        
        # Create list item
        item = QListWidgetItem(self.chat_display)
        item.setSizeHint(message_widget.sizeHint())
        
        # Add to list
        self.chat_display.addItem(item)
        self.chat_display.setItemWidget(item, message_widget)
        
        # Auto-scroll to bottom
        self.chat_display.scrollToBottom()
    
    def load_message_history(self):
        """Load recent message history from memory system"""
        try:
            # Get recent conversation history from memory
            recent_memories = self.memory.db.get_recent_memories(limit=self.MESSAGE_HISTORY_LIMIT)
            
            # Display historical messages
            for memory in reversed(recent_memories):  # Reverse to show oldest first
                if memory.interaction_type == "text_input":
                    # User message
                    timestamp = datetime.fromisoformat(memory.timestamp).strftime("%H:%M")
                    self.add_message("You", memory.content, is_user=True, timestamp=timestamp)
                elif memory.interaction_type == "response":
                    # Pet response
                    timestamp = datetime.fromisoformat(memory.timestamp).strftime("%H:%M")
                    formatted_response = self.personality.format_response(memory.content)
                    self.add_message("Pet", formatted_response, is_user=False, timestamp=timestamp)
        except Exception as e:
            # If loading history fails, just continue without history
            print(f"Could not load message history: {e}")
    def add_message(self, sender: str, message: str):
        """
        Add a message to the chat display
        
        Args:
            sender: The sender of the message (e.g., "You", "Pet")
            message: The message content
        """
        formatted_message = f"<b>{sender}:</b> {message}<br>"
        self.chat_display.append(formatted_message)
        
    def send_message(self):
        """
        Handle sending user message
        
        This method:
        1. Validates input
        2. Displays user message
        3. Disables send button to prevent duplicate sends
        4. Recognizes intent using the intent system
        5. Records interaction in memory
        6. Generates response using MBTI personality
        7. Displays response
        8. Re-enables send button
        9. Handles any errors gracefully
        """
        # Get user input
        user_input = self.input_field.text().strip()
        
        # Validate input - don't send empty messages
        if not user_input:
            return
        
        # Display user message
        self.add_message("You", user_input, is_user=True)
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
        
        self.add_message("Pet", pet_response, is_user=False)
        # Prevent duplicate sends while processing
        if self.is_sending:
            return
        
        try:
            # Set sending state
            self.is_sending = True
            self.send_button.setEnabled(False)
            self.send_button.setText("Sending...")
            self.input_field.setEnabled(False)
            
            # Display user message
            self.add_message("You", user_input)
            
            # Clear input field immediately after displaying
            self.input_field.clear()
            
            # Recognize intent using the context-aware intent system
            intent = self.intent_system.analyze(user_input=user_input)
            
            # Record user input in memory system
            self.memory.record_interaction(
                interaction_type="text_input",
                content=user_input,
                context={"intent": intent.intent_type.value},
                importance=7  # User input is important
            )
            
            # Generate response based on intent and personality
            response = self.generate_response(intent)
            pet_response = self.personality.format_response(response)
            
            # Display pet response
            self.add_message("Pet", pet_response)
            
            # Record response in memory system
            self.memory.record_interaction(
                interaction_type="response",
                content=response,
                importance=5
            )
            
        except Exception as e:
            # Log the full exception for debugging
            logger.error(f"Error in send_message: {e}", exc_info=True)
            
            # Show user-friendly error message
            error_message = "Sorry, something went wrong. Please try again."
            self.add_message("Pet", self.personality.format_response(error_message))
            
        finally:
            # Always restore UI state
            self.is_sending = False
            self.send_button.setEnabled(True)
            self.send_button.setText("Send")
            self.input_field.setEnabled(True)
            # Keep focus on input field for convenience
            self.input_field.setFocus()
        
    def generate_response(self, intent) -> str:
        """
        Generate response based on intent and personality
        
        Args:
            intent: The recognized Intent object containing user intent information
            
        Returns:
            str: Generated response string
        """
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
        success = self.automation.execute_task_by_name("Take Screenshot")
        
        if success:
            message = "Screenshot taken successfully! 📸"
        else:
            message = "Failed to take screenshot. 😔"
        
        self.add_message("Pet", self.personality.format_response(message), is_user=False)
        
    def show_memory(self):
        """Show memory summary"""
        summary = self.memory.get_summary()
        self.add_message("Pet", self.personality.format_response(f"Memory Summary:\n{summary}"), is_user=False)
        
    def show_automation(self):
        """Show automation options"""
        tasks = self.automation.get_available_tasks()
        task_list = "\n".join([f"- {task}" for task in tasks])
        
        message = f"Available automations:\n{task_list}"
        self.add_message("Pet", self.personality.format_response(message), is_user=False)
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
