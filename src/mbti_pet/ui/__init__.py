"""
Desktop Pet UI
PyQt5-based interface for the desktop pet
"""

import sys
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from mbti_pet.personality import MBTIPersonality, MBTIType
from mbti_pet.intent import ContextAwareIntentSystem
from mbti_pet.memory import MemoryManager
from mbti_pet.automation import AutomationAssistant


class PetWidget(QWidget):
    """Main desktop pet window"""
    
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
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(300)
        
        # Add greeting message
        greeting = self.personality.get_greeting()
        self.add_message("Pet", greeting)
        
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
        self.screenshot_button.clicked.connect(self.take_screenshot)
        
        self.memory_button = QPushButton("🧠 Memory")
        self.memory_button.clicked.connect(self.show_memory)
        
        self.automate_button = QPushButton("⚡ Automate")
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
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
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
        self.add_message("Pet", f"Personality changed! {greeting}")
        
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
            
            # Process the message using Qt's event processing
            QApplication.processEvents()
            
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
            # Handle any errors gracefully
            error_message = f"Sorry, I encountered an error: {str(e)}"
            self.add_message("Pet", self.personality.format_response(error_message))
            print(f"Error in send_message: {e}")
            
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
        
        self.add_message("Pet", self.personality.format_response(message))
        
    def show_memory(self):
        """Show memory summary"""
        summary = self.memory.get_summary()
        self.add_message("Pet", self.personality.format_response(f"Memory Summary:\n{summary}"))
        
    def show_automation(self):
        """Show automation options"""
        tasks = self.automation.get_available_tasks()
        task_list = "\n".join([f"- {task}" for task in tasks])
        
        message = f"Available automations:\n{task_list}"
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
