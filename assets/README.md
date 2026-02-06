# Assets Directory

This directory contains visual assets for the MBTI Desktop Pet.

## Structure

```
assets/
└── pets/
    ├── INTJ/
    │   └── idle.gif    # Idle animation for INTJ personality
    ├── INTP/
    │   └── idle.gif
    ├── ENTJ/
    │   └── idle.gif
    └── ...             # One directory for each of the 16 MBTI types
```

## Pet Animations

Each MBTI personality type has its own directory under `assets/pets/`. Currently, each personality should have at least:

- `idle.gif` - The default idle animation shown when the pet is on the desktop

## Adding New Animations

To add animations for a personality type:

1. Create a GIF file (recommended size: 200x200 pixels)
2. Name it `idle.gif`
3. Place it in the corresponding MBTI type directory (e.g., `assets/pets/ENFP/idle.gif`)

## Fallback Behavior

If a GIF file is not found for a personality type, the desktop pet will display the corresponding emoji as a fallback:

- INTJ: 🎯
- INTP: 🔬
- ENTJ: 👑
- ENTP: 💡
- INFJ: 🌟
- INFP: 🌈
- ENFJ: ✨
- ENFP: 🎨
- ISTJ: 📋
- ISFJ: 🛡️
- ESTJ: 📊
- ESFJ: 🤝
- ISTP: 🔧
- ISFP: 🎭
- ESTP: ⚡
- ESFP: 🎉

## Animation Guidelines

- **Format**: GIF (animated)
- **Size**: 200x200 pixels (recommended)
- **Background**: Transparent
- **Frame rate**: 10-30 FPS
- **Duration**: 1-3 seconds loop
- **File size**: Keep under 500KB for smooth loading

## Future Animations

In future versions, we may add additional animation states:

- `happy.gif` - Happy/excited state
- `thinking.gif` - Thinking/processing state
- `working.gif` - Working/busy state
- `sleeping.gif` - Idle/sleeping state
