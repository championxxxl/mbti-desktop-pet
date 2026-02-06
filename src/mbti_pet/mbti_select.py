"""
MBTI Selection Interface
Allows users to select their preferred MBTI personality type at startup
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QGroupBox, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from mbti_pet.personality import MBTIPersonality, MBTIType
from mbti_pet.config import ConfigManager


class MBTISelectDialog(QDialog):
    """Dialog for selecting MBTI personality type"""
    
    # MBTI groups with their types
    MBTI_GROUPS = {
        "分析家 Analysts": {
            "color": "#88619A",
            "types": ["INTJ", "INTP", "ENTJ", "ENTP"]
        },
        "外交家 Diplomats": {
            "color": "#33A474",
            "types": ["INFJ", "INFP", "ENFJ", "ENFP"]
        },
        "守卫者 Sentinels": {
            "color": "#4298B4",
            "types": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"]
        },
        "探险家 Explorers": {
            "color": "#E4AE3A",
            "types": ["ISTP", "ISFP", "ESTP", "ESFP"]
        }
    }
    
    def __init__(self, config_manager: ConfigManager = None):
        """
        Initialize MBTI selection dialog
        
        Args:
            config_manager: ConfigManager instance for saving selection
        """
        super().__init__()
        self.config_manager = config_manager or ConfigManager()
        self.selected_type = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("选择你的 MBTI 性格 - Choose Your MBTI Personality")
        self.setMinimumSize(700, 600)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("🎭 选择你的 MBTI 性格类型")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("选择一个与你最匹配的性格类型，你可以随时更改")
        subtitle_label.setFont(QFont("Arial", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        
        # Create groups
        for group_name, group_data in self.MBTI_GROUPS.items():
            group_widget = self.create_group(group_name, group_data["types"], group_data["color"])
            main_layout.addWidget(group_widget)
        
        # Confirm button (initially disabled)
        self.confirm_button = QPushButton("确认选择 Confirm")
        self.confirm_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.confirm_button.setMinimumHeight(50)
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #ccc;
                color: white;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:enabled {
                background-color: #4CAF50;
            }
            QPushButton:enabled:hover {
                background-color: #45a049;
            }
        """)
        
        main_layout.addWidget(self.confirm_button)
        
        self.setLayout(main_layout)
        
        # Apply overall style
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
        """)
    
    def create_group(self, group_name: str, mbti_types: list, color: str) -> QGroupBox:
        """
        Create a group box for a category of MBTI types
        
        Args:
            group_name: Name of the group (e.g., "Analysts")
            mbti_types: List of MBTI type strings
            color: Group color
            
        Returns:
            QGroupBox containing the group
        """
        group_box = QGroupBox(group_name)
        group_box.setFont(QFont("Arial", 11, QFont.Bold))
        group_box.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid {color};
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                background-color: white;
            }}
            QGroupBox::title {{
                color: {color};
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: white;
            }}
        """)
        
        # Grid layout for buttons (2x2)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        for i, mbti_type in enumerate(mbti_types):
            row = i // 2
            col = i % 2
            
            button = self.create_type_button(mbti_type, color)
            grid_layout.addWidget(button, row, col)
        
        group_box.setLayout(grid_layout)
        return group_box
    
    def create_type_button(self, mbti_type: str, color: str) -> QPushButton:
        """
        Create a button for an MBTI type
        
        Args:
            mbti_type: MBTI type string (e.g., "ENFP")
            color: Button color
            
        Returns:
            QPushButton for the type
        """
        # Get personality traits
        personality = MBTIPersonality.from_string(mbti_type)
        emoji = personality.traits.default_emoji
        name = personality.traits.name
        
        # Create button
        button = QPushButton(f"{emoji} {mbti_type}\n{name}")
        button.setFont(QFont("Arial", 10))
        button.setMinimumHeight(80)
        button.setCheckable(True)
        button.clicked.connect(lambda: self.select_type(mbti_type, button))
        
        # Store button reference for later access
        if not hasattr(self, 'type_buttons'):
            self.type_buttons = {}
        self.type_buttons[mbti_type] = button
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
                color: #333;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #f9f9f9;
                border: 3px solid {color};
            }}
            QPushButton:checked {{
                background-color: {color};
                color: white;
                border: 3px solid {color};
            }}
        """)
        
        return button
    
    def select_type(self, mbti_type: str, button: QPushButton):
        """
        Handle type selection
        
        Args:
            mbti_type: Selected MBTI type
            button: Button that was clicked
        """
        # Uncheck all other buttons
        for btn in self.type_buttons.values():
            if btn != button:
                btn.setChecked(False)
        
        # Set selected type
        self.selected_type = mbti_type
        
        # Enable confirm button
        self.confirm_button.setEnabled(True)
    
    def confirm_selection(self):
        """Confirm and save the selection"""
        if self.selected_type:
            # Save to config
            self.config_manager.set_mbti_type(self.selected_type)
            self.accept()
    
    def get_selected_type(self) -> str:
        """
        Get the selected MBTI type
        
        Returns:
            Selected MBTI type string or None if cancelled
        """
        return self.selected_type


def show_mbti_selector(config_manager: ConfigManager = None) -> str:
    """
    Show MBTI selection dialog and return selected type
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        Selected MBTI type string or None if cancelled
    """
    from PyQt5.QtWidgets import QApplication
    import sys
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    dialog = MBTISelectDialog(config_manager)
    result = dialog.exec_()
    
    if result == QDialog.Accepted:
        return dialog.get_selected_type()
    
    return None
