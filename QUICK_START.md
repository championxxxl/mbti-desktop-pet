# MBTI Desktop Pet - Quick Start Guide

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/championxxxl/mbti-desktop-pet.git
cd mbti-desktop-pet

# Install dependencies
pip install -r requirements.txt
```

### First Launch

```bash
python src/mbti_pet/main.py
```

**What happens:**
1. 🎭 MBTI Selection Dialog appears
2. Choose your personality type (16 options in 4 groups)
3. Click "确认选择 Confirm"
4. 🎨 Desktop pet appears on your screen!

### Using the Desktop Pet

#### 🖱️ Mouse Interactions

| Action | Result |
|--------|--------|
| **Left-click + Drag** | Move pet around screen |
| **Left-click** | Open chat window |
| **Right-click** | Show context menu |
| **Double-click** | Open chat window |

#### 📋 Context Menu Options

Right-click on the pet to access:

- 💬 **Chat** - Open chat window for conversation
- 🎭 **Change Personality** - Select a different MBTI type
- ⚙️ **Settings** - Configure preferences (coming soon)
- ❌ **Exit** - Close the application

### Features

#### ✨ Desktop Pet Window

- **Transparent Background** - Blends with your desktop
- **Always on Top** - Never hidden by other windows
- **Draggable** - Position anywhere you like
- **Animated** - Shows GIF animation (if available) or emoji
- **Persistent Position** - Remembers location when you close

#### 🎭 MBTI Personalities

Choose from 16 authentic MBTI types:

**🎯 Analysts (Purple)**
- INTJ 🎯 - The Architect
- INTP 🔬 - The Logician
- ENTJ 👑 - The Commander
- ENTP 💡 - The Debater

**🌟 Diplomats (Green)**
- INFJ 🌟 - The Advocate
- INFP 🌈 - The Mediator
- ENFJ ✨ - The Protagonist
- ENFP 🎨 - The Campaigner

**📋 Sentinels (Blue)**
- ISTJ 📋 - The Logistician
- ISFJ 🛡️ - The Defender
- ESTJ 📊 - The Executive
- ESFJ 🤝 - The Consul

**⚡ Explorers (Yellow)**
- ISTP 🔧 - The Virtuoso
- ISFP 🎭 - The Adventurer
- ESTP ⚡ - The Entrepreneur
- ESFP 🎉 - The Entertainer

#### 💬 Chat Interface

Click the pet to open the chat window:
- Have conversations with your AI companion
- Personality-driven responses based on MBTI type
- Memory system remembers your interactions
- Quick action buttons for automation

### Configuration

Config file location: `./data/config.json`

```json
{
  "mbti_type": "ENFP",
  "window_position": [100, 200],
  "window_size": [200, 200]
}
```

### Adding Custom Animations

Want to customize your pet's appearance?

1. Create a 200x200 pixel animated GIF
2. Save it as: `assets/pets/{YOUR_TYPE}/idle.gif`
3. Example: `assets/pets/ENFP/idle.gif`
4. Restart the application

**Animation Requirements:**
- Format: Animated GIF
- Size: 200x200 pixels (recommended)
- Background: Transparent
- Frame rate: 10-30 FPS
- File size: < 500KB

If no GIF is provided, the pet displays its emoji icon as a fallback.

### Testing

Run tests to verify everything works:

```bash
# All tests
python -m pytest tests/ -v

# Specific tests
python -m pytest tests/test_config.py -v
python -m pytest tests/test_ui_components.py -v
```

### Troubleshooting

#### Pet window not appearing?
- Ensure you're not in a headless environment
- Check Qt platform plugin: `echo $QT_QPA_PLATFORM`
- Try: `export QT_QPA_PLATFORM=xcb` (Linux)

#### Can't move the pet?
- Some tiling window managers restrict dragging
- Try using the chat window instead
- Check window manager settings

#### Configuration not saving?
- Ensure `./data/` directory is writable
- Check file permissions
- Delete `data/config.json` to reset

### Manual Testing

Use the provided test script:

```bash
python test_manual.py
```

This will guide you through testing all features.

### Screenshots

Generate UI screenshots:

```bash
python take_screenshots.py
```

Screenshots saved to your system's temp directory.

## 📖 Documentation

- **IMPLEMENTATION_GUIDE.md** - Technical implementation details
- **DESKTOP_PET_SUMMARY.md** - Executive summary
- **assets/README.md** - Animation guidelines
- **README.md** - Project overview

## 🎨 Customization Ideas

### Future Enhancements

1. **Multiple Animation States**
   - happy.gif, thinking.gif, working.gif, sleeping.gif
   
2. **Custom Sizes**
   - Small (100x100), Medium (200x200), Large (300x300)
   
3. **Sound Effects**
   - Greeting sounds, interaction sounds
   
4. **Notifications**
   - Desktop notifications from your pet
   
5. **Multiple Pets**
   - Run multiple personalities simultaneously

## 🤝 Contributing

Want to add features?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📝 License

See LICENSE file for details.

## 🆘 Support

Having issues?
- Check the troubleshooting section above
- Review the implementation guide
- Open an issue on GitHub

## 🎉 Enjoy Your Desktop Companion!

Your MBTI Desktop Pet is ready to keep you company while you work!

---

**Version:** 0.1.0  
**Status:** Production Ready  
**Last Updated:** 2026-02-06
