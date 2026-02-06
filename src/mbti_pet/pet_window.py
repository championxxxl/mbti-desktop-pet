"""
Desktop Pet Window
Transparent, draggable desktop pet with MBTI personality
"""

import os
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QMenu, QAction, QApplication
)
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer
from PyQt5.QtGui import QFont, QMovie, QCursor

from mbti_pet.personality import MBTIPersonality
from mbti_pet.config import ConfigManager
from mbti_pet.mbti_select import MBTISelectDialog


class PetWindow(QWidget):
    """Transparent desktop pet window with drag support and animations"""
    
    DEFAULT_SIZE = 200  # Default window size (width and height)
    
    def __init__(self, mbti_type: str, config_manager: ConfigManager = None):
        """
        Initialize desktop pet window
        
        Args:
            mbti_type: MBTI personality type (e.g., "ENFP", "INTJ")
            config_manager: ConfigManager instance for saving position
        """
        super().__init__()
        
        self.mbti_type = mbti_type
        self.personality = MBTIPersonality.from_string(mbti_type)
        self.config_manager = config_manager or ConfigManager()
        
        # Drag state
        self.dragging = False
        self.drag_offset = QPoint()
        
        # Animation components
        self.movie = None
        self.pet_label = None
        
        # Chat window reference (created on demand)
        self.chat_window = None
        
        self.init_ui()
        self.load_animation()
        self.restore_position()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Window flags for transparent, frameless, always-on-top window
        self.setWindowFlags(
            Qt.FramelessWindowHint |      # No title bar or borders
            Qt.WindowStaysOnTopHint |     # Always on top
            Qt.Tool                       # Tool window (no taskbar icon)
        )
        
        # Transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set fixed size
        self.setFixedSize(self.DEFAULT_SIZE, self.DEFAULT_SIZE)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Pet display label
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("background-color: transparent;")
        
        layout.addWidget(self.pet_label)
        self.setLayout(layout)
        
        # Set cursor to indicate draggable
        self.setCursor(Qt.OpenHandCursor)
        
        # Set tooltip
        self.setToolTip(f"{self.personality.traits.default_emoji} {self.mbti_type} - {self.personality.traits.name}\nClick to chat, Right-click for menu")
    
    def load_animation(self):
        """Load and display pet animation (GIF) or emoji fallback"""
        # Try to load GIF animation
        gif_path = Path(f"assets/pets/{self.mbti_type}/idle.gif")
        
        if gif_path.exists():
            # Load GIF animation
            self.movie = QMovie(str(gif_path))
            self.movie.setScaledSize(QSize(self.DEFAULT_SIZE, self.DEFAULT_SIZE))
            self.pet_label.setMovie(self.movie)
            self.movie.start()
        else:
            # Fallback to emoji
            self.display_emoji_fallback()
    
    def display_emoji_fallback(self):
        """Display emoji as fallback when GIF is not available"""
        emoji = self.personality.traits.default_emoji
        self.pet_label.setFont(QFont("Arial", 80))
        self.pet_label.setText(emoji)
    
    def restore_position(self):
        """Restore window position from config or use default"""
        position = self.config_manager.get_window_position()
        
        if position:
            self.move(position[0], position[1])
        else:
            # Default to center-right of screen
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - self.DEFAULT_SIZE - 100
            y = screen.height() // 2 - self.DEFAULT_SIZE // 2
            self.move(x, y)
    
    def save_position(self):
        """Save current window position to config"""
        pos = self.pos()
        self.config_manager.set_window_position(pos.x(), pos.y())
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging and clicking"""
        if event.button() == Qt.LeftButton:
            # Start dragging
            self.dragging = True
            self.drag_offset = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.RightButton:
            # Show context menu
            self.show_context_menu(event.globalPos())
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging:
            # Move window
            self.move(self.mapToGlobal(event.pos() - self.drag_offset))
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release after dragging"""
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.dragging = False
                self.setCursor(Qt.OpenHandCursor)
                
                # Save position after dragging
                self.save_position()
            else:
                # Click without drag - show chat window
                self.show_chat_window()
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to show chat window"""
        if event.button() == Qt.LeftButton:
            self.show_chat_window()
    
    def show_context_menu(self, position: QPoint):
        """
        Show context menu with options
        
        Args:
            position: Global position for menu
        """
        menu = QMenu(self)
        
        # Menu styling
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
        
        # Chat action
        chat_action = QAction("💬 Chat", self)
        chat_action.triggered.connect(self.show_chat_window)
        menu.addAction(chat_action)
        
        # Change personality action
        change_personality_action = QAction("🎭 Change Personality", self)
        change_personality_action.triggered.connect(self.change_personality)
        menu.addAction(change_personality_action)
        
        menu.addSeparator()
        
        # Settings action (placeholder)
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # Exit action
        exit_action = QAction("❌ Exit", self)
        exit_action.triggered.connect(self.exit_application)
        menu.addAction(exit_action)
        
        menu.exec_(position)
    
    def show_chat_window(self):
        """Show or focus the chat window"""
        if self.chat_window is None or not self.chat_window.isVisible():
            # Import here to avoid circular dependency
            from mbti_pet.ui import PetWidget
            
            self.chat_window = PetWidget()
            
            # Update personality to match pet
            self.chat_window.personality = self.personality
            self.chat_window.update_pet_display()
            
            # Set combo box to current type
            index = self.chat_window.personality_combo.findText(self.mbti_type)
            if index >= 0:
                self.chat_window.personality_combo.setCurrentIndex(index)
            
            # Position chat window near pet
            pet_pos = self.pos()
            self.chat_window.move(pet_pos.x() - 300, pet_pos.y() - 100)
        
        self.chat_window.show()
        self.chat_window.raise_()
        self.chat_window.activateWindow()
    
    def change_personality(self):
        """Show MBTI selection dialog to change personality"""
        dialog = MBTISelectDialog(self.config_manager)
        result = dialog.exec_()
        
        if result == MBTISelectDialog.Accepted:
            new_type = dialog.get_selected_type()
            if new_type and new_type != self.mbti_type:
                # Update personality
                self.mbti_type = new_type
                self.personality = MBTIPersonality.from_string(new_type)
                
                # Reload animation
                if self.movie:
                    self.movie.stop()
                    self.movie = None
                self.load_animation()
                
                # Update tooltip
                self.setToolTip(f"{self.personality.traits.default_emoji} {self.mbti_type} - {self.personality.traits.name}\nClick to chat, Right-click for menu")
                
                # Update chat window if open
                if self.chat_window and self.chat_window.isVisible():
                    self.chat_window.personality = self.personality
                    self.chat_window.update_pet_display()
                    index = self.chat_window.personality_combo.findText(self.mbti_type)
                    if index >= 0:
                        self.chat_window.personality_combo.setCurrentIndex(index)
    
    def show_settings(self):
        """Show settings dialog (placeholder)"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Settings",
            "Settings panel coming soon!\n\nFor now, you can:\n- Right-click to access menu\n- Drag to move the pet\n- Click to open chat"
        )
    
    def exit_application(self):
        """Exit the application"""
        # Save position before exiting
        self.save_position()
        
        # Close chat window if open
        if self.chat_window:
            self.chat_window.close()
        
        # Close this window
        self.close()
        
        # Quit application
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save position when closing
        self.save_position()
        
        # Close chat window
        if self.chat_window:
            self.chat_window.close()
        
        event.accept()
