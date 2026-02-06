# MBTI Desktop Pet Implementation Guide

## Overview

This document describes the implementation of the MBTI Desktop Pet core architecture, which transforms the application from a chat interface into a true desktop pet companion.

## Architecture Changes

### 1. Configuration Management Enhancement (`src/mbti_pet/config.py`)

**New Class: `ConfigManager`**
- Provides JSON-based persistent configuration storage
- Location: `./data/config.json`
- Features:
  - MBTI type selection persistence
  - Window position memory
  - Window size storage
  - Graceful error handling for corrupted files

**Key Methods:**
```python
ConfigManager()
  .load() -> Dict                    # Load entire config
  .save(config: Dict) -> bool        # Save entire config
  .get_mbti_type() -> str            # Get saved MBTI type
  .set_mbti_type(type: str) -> bool  # Save MBTI type
  .get_window_position() -> Tuple    # Get saved position
  .set_window_position(x, y) -> bool # Save position
```

### 2. MBTI Selection Interface (`src/mbti_pet/mbti_select.py`)

**Class: `MBTISelectDialog`**

A beautiful dialog that presents all 16 MBTI personality types organized into 4 color-coded groups:

- 🎯 **Analysts** (Purple): INTJ, INTP, ENTJ, ENTP
- 🌟 **Diplomats** (Green): INFJ, INFP, ENFJ, ENFP  
- 📋 **Sentinels** (Blue): ISTJ, ISFJ, ESTJ, ESFJ
- ⚡ **Explorers** (Yellow): ISTP, ISFP, ESTP, ESFP

**Features:**
- Each type shows emoji icon and personality name
- Click to select, confirm to save
- Saves selection to config.json automatically
- Beautiful color-coded group borders

**Usage:**
```python
from mbti_pet.mbti_select import MBTISelectDialog

dialog = MBTISelectDialog(config_manager)
result = dialog.exec_()
if result == QDialog.Accepted:
    selected = dialog.get_selected_type()
```

### 3. Desktop Pet Window (`src/mbti_pet/pet_window.py`)

**Class: `PetWindow`**

The main desktop pet window with the following characteristics:

**Window Properties:**
- Frameless (`Qt.FramelessWindowHint`)
- Always on top (`Qt.WindowStaysOnTopHint`)
- Transparent background (`Qt.WA_TranslucentBackground`)
- Tool window (no taskbar icon)
- Fixed size: 200x200 pixels

**Features:**

1. **Drag & Drop**
   - Left-click and drag to move pet anywhere on screen
   - Position automatically saved when released

2. **GIF Animation Support**
   - Loads `assets/pets/{MBTI_TYPE}/idle.gif` if available
   - Falls back to emoji if GIF not found
   - Smooth animation playback with QMovie

3. **Context Menu (Right-click)**
   - 💬 Chat - Opens chat window
   - 🎭 Change Personality - Shows MBTI selection dialog
   - ⚙️ Settings - Settings panel (coming soon)
   - ❌ Exit - Closes application

4. **Chat Window Integration**
   - Click pet to open chat window
   - Reuses existing `PetWidget` from `ui/__init__.py`
   - Positioned near the pet
   - Updates personality to match pet

**Usage:**
```python
from mbti_pet.pet_window import PetWindow

pet = PetWindow("ENFP", config_manager)
pet.show()
```

### 4. New Startup Flow (`src/mbti_pet/main.py`)

The refactored main entry point implements this flow:

```
Start Application
    ↓
Check config.json for MBTI type
    ↓
┌─────────────────┐        ┌──────────────────┐
│ No Config Found │   →    │ Show MBTI Selector│
└─────────────────┘        └──────────────────┘
                                    ↓
                           User selects type
                                    ↓
                           Save to config.json
                                    ↓
┌─────────────────┐                ↓
│ Config Exists   │   →   ┌────────────────────┐
└─────────────────┘       │ Create Pet Window  │
                          │ with saved type    │
                          └────────────────────┘
                                    ↓
                          Show pet at saved position
                                    ↓
                          Desktop Pet Running
```

### 5. Assets Directory Structure

```
assets/
└── pets/
    ├── README.md              # Documentation
    ├── INTJ/
    │   └── .gitkeep          # (idle.gif goes here)
    ├── INTP/
    │   └── .gitkeep
    └── ...                    # All 16 MBTI types
```

**Animation Requirements:**
- Format: Animated GIF
- Size: 200x200 pixels (recommended)
- Background: Transparent
- Frame rate: 10-30 FPS
- File size: < 500KB

**Fallback Behavior:**
If GIF not found, displays personality emoji:
- INTJ: 🎯, INTP: 🔬, ENTJ: 👑, ENTP: 💡
- INFJ: 🌟, INFP: 🌈, ENFJ: ✨, ENFP: 🎨
- ISTJ: 📋, ISFJ: 🛡️, ESTJ: 📊, ESFJ: 🤝
- ISTP: 🔧, ISFP: 🎭, ESTP: ⚡, ESFP: 🎉

## Testing

### Test Coverage

**New Tests Added:**
1. `tests/test_config.py` - Configuration management (12 tests)
2. `tests/test_ui_components.py` - UI components (6 tests)

**All Tests Passing:** 118 tests total ✅

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Configuration tests only
python -m pytest tests/test_config.py -v

# UI component tests only  
python -m pytest tests/test_ui_components.py -v

# Existing tests (personality, memory, intent)
python -m pytest tests/test_personality.py -v
```

### Manual Testing

```bash
# Test full application
python test_manual.py

# Or run directly
python src/mbti_pet/main.py
```

**Manual Test Checklist:**
- [ ] MBTI selection dialog appears on first run
- [ ] All 16 personality types are selectable
- [ ] Selection is saved to config.json
- [ ] Desktop pet appears as transparent window
- [ ] Pet can be dragged around screen
- [ ] Right-click shows context menu
- [ ] Clicking pet opens chat window
- [ ] Emoji displays when GIF not available
- [ ] Window position persists across restarts

## Usage Examples

### Basic Usage

```python
from mbti_pet.main import main

# Launch application
main()
```

### Programmatic Usage

```python
from PyQt5.QtWidgets import QApplication
from mbti_pet.config import ConfigManager
from mbti_pet.pet_window import PetWindow

# Create app
app = QApplication([])

# Create and show pet
config = ConfigManager()
pet = PetWindow("ENFP", config)
pet.show()

# Run
app.exec_()
```

### Configuration Management

```python
from mbti_pet.config import ConfigManager

config = ConfigManager()

# Save MBTI type
config.set_mbti_type("INTJ")

# Get MBTI type
mbti_type = config.get_mbti_type()  # Returns "INTJ"

# Save window position
config.set_window_position(100, 200)

# Get window position
x, y = config.get_window_position()  # Returns (100, 200)
```

## Key Features Implemented

✅ **Transparent Desktop Window**
- Frameless, always-on-top window
- Transparent background with no taskbar icon
- Perfect for desktop pet experience

✅ **MBTI Personality Selection**
- Beautiful 4-group layout with color coding
- All 16 types with emoji icons
- Persistent configuration

✅ **Drag & Drop Support**
- Smooth window dragging
- Position memory across sessions
- Visual cursor feedback

✅ **GIF Animation System**
- QMovie-based animation playback
- Automatic fallback to emoji
- 200x200 pixel support

✅ **Context Menu**
- Chat window access
- Personality switching
- Settings and exit options

✅ **Configuration Persistence**
- JSON-based storage
- MBTI type memory
- Window position memory
- Error-tolerant loading

## Backward Compatibility

All existing functionality is preserved:
- ✅ Chat interface (`PetWidget`) still works
- ✅ Memory system unchanged
- ✅ Intent recognition unchanged  
- ✅ Automation features unchanged
- ✅ All 118 existing tests pass

The chat interface is now accessed by clicking the desktop pet instead of launching directly.

## Future Enhancements

Potential additions:
1. Multiple animation states (happy, thinking, working, sleeping)
2. Settings panel implementation
3. Notification system
4. Window size customization
5. Multiple pet instances
6. Automatic personality detection
7. Voice interaction
8. System tray icon with quick actions

## Dependencies

No new dependencies added! Uses existing:
- PyQt5 (already required)
- Python standard library (json, pathlib)

## File Changes Summary

**New Files:**
- `src/mbti_pet/mbti_select.py` - MBTI selection dialog
- `src/mbti_pet/pet_window.py` - Desktop pet window
- `tests/test_config.py` - Configuration tests
- `tests/test_ui_components.py` - UI component tests
- `assets/README.md` - Assets documentation
- `assets/pets/*/. gitkeep` - Directory structure (16 files)

**Modified Files:**
- `src/mbti_pet/config.py` - Added ConfigManager class
- `src/mbti_pet/main.py` - New startup flow

**Total Changes:** 21 files created/modified

## Troubleshooting

**Issue: Pet window not appearing**
- Check if running in headless environment
- Verify Qt platform plugin is available
- Try setting `QT_QPA_PLATFORM=xcb` on Linux

**Issue: Config not saving**
- Ensure `./data/` directory is writable
- Check file permissions
- Verify no conflicting config files

**Issue: GIF not displaying**
- Verify GIF file exists at correct path
- Check GIF file is valid (use image viewer)
- Fallback emoji should display if GIF missing

**Issue: Drag not working**
- Verify window flags are set correctly
- Check if running on compatible window manager
- Some tiling window managers may restrict dragging

## Screenshots

### MBTI Selection Dialog
![MBTI Selection Dialog](https://github.com/user-attachments/assets/984dd99c-de15-4b68-b1c9-fd527583c1ba)

The selection dialog shows all 16 MBTI types organized in color-coded groups.

## Contributing

When adding new features:
1. Follow existing code style
2. Add tests for new functionality
3. Update this documentation
4. Ensure all tests pass
5. Test manually with `test_manual.py`

## License

Same as project license.
