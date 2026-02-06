# MBTI Desktop Pet - Architecture Documentation

## System Architecture

### Overview
The MBTI Desktop Pet is built with a modular architecture, separating concerns into distinct components that work together to provide an intelligent, personality-driven desktop assistant.

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface (UI)                     │
│                        PyQt5 GUI                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────────┐
│                   Core Components                            │
├──────────────────┬──────────────┬──────────────┬────────────┤
│  Personality     │   Intent     │   Memory     │ Automation │
│    System        │ Recognition  │   System     │   Engine   │
└──────────────────┴──────────────┴──────────────┴────────────┘
                  │
┌─────────────────┴───────────────────────────────────────────┐
│                   Data Layer                                 │
│                 SQLite Database                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Personality System (`personality/`)

**Purpose**: Implements MBTI personality types and traits

**Key Classes**:
- `MBTIType` (Enum): 16 personality types
- `PersonalityTraits` (Dataclass): Characteristics of each type
- `MBTIPersonality`: Main personality handler

**Features**:
- 16 distinct MBTI personality types
- Unique communication styles per type
- Personality-specific responses
- Dynamic personality switching

**Example**:
```python
from mbti_pet.personality import MBTIPersonality, MBTIType

# Create personality
personality = MBTIPersonality(MBTIType.ENFP)

# Get greeting
greeting = personality.get_greeting()
# Output: "🎨 Hey! So excited to work with you today!"
```

### 2. Intent Recognition (`intent/`)

**Purpose**: Analyzes user input and context to determine intent

**Key Classes**:
- `IntentType` (Enum): Types of user intents
- `Intent` (Dataclass): Detected intent with confidence
- `IntentRecognizer`: Text-based intent recognition
- `ScreenActivityAnalyzer`: Screen activity analysis
- `ContextAwareIntentSystem`: Combined analysis

**Features**:
- Pattern-based text analysis
- Entity extraction (URLs, files, numbers, etc.)
- Screen activity monitoring
- Context-aware suggestions
- Multi-language support (English + Chinese)

**Intent Types**:
- Help Request
- Task Execution
- Information Query
- Automation Request
- File Operation
- Web Search
- Code Assistance
- Writing Assistance
- System Command
- Casual Chat

**Example**:
```python
from mbti_pet.intent import ContextAwareIntentSystem

intent_system = ContextAwareIntentSystem()

# Analyze user input
intent = intent_system.analyze(
    user_input="Help me with code formatting"
)

print(intent.intent_type)  # IntentType.CODE_ASSISTANCE
print(intent.confidence)   # 0.6
print(intent.suggested_action)  # "I can help with your code..."
```

### 3. Memory System (`memory/`)

**Purpose**: Stores and retrieves user interactions for learning

**Key Classes**:
- `MemoryEntry` (Dataclass): Single memory record
- `MemoryDatabase`: SQLite storage layer
- `MemoryManager`: High-level memory operations

**Features**:
- Persistent storage in SQLite
- Interaction history tracking
- Pattern learning and recognition
- Context retrieval for responses
- User preference analysis
- Importance-based ranking

**Database Schema**:
```sql
-- Memories table
CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    interaction_type TEXT,
    content TEXT,
    context TEXT,
    importance INTEGER,
    tags TEXT,
    created_at DATETIME
);

-- Patterns table
CREATE TABLE user_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT,
    pattern_data TEXT,
    frequency INTEGER,
    last_seen DATETIME
);
```

**Example**:
```python
from mbti_pet.memory import MemoryManager

memory = MemoryManager()

# Record interaction
memory.record_interaction(
    interaction_type="text_input",
    content="Help with Python",
    importance=7,
    tags=["python", "help"]
)

# Get context for response
context = memory.get_context_for_response("Python")
```

### 4. Automation System (`automation/`)

**Purpose**: Executes automated tasks like Claude Desktop

**Key Classes**:
- `AutomationAction` (Enum): Types of actions
- `AutomationStep` (Dataclass): Single automation step
- `AutomationTask` (Dataclass): Complete task definition
- `AutomationEngine`: Task executor
- `TaskLibrary`: Pre-defined tasks
- `AutomationAssistant`: High-level interface

**Features**:
- Mouse and keyboard automation
- Screenshot capture
- Application launching
- Custom macro recording
- Safety features (failsafe)
- Cross-platform support

**Supported Actions**:
- Click (mouse)
- Type (keyboard)
- Press Key
- Move Mouse
- Scroll
- Screenshot
- Wait/Delay
- Open/Close App

**Example**:
```python
from mbti_pet.automation import AutomationAssistant

automation = AutomationAssistant()

# Execute pre-defined task
automation.execute_task_by_name("Take Screenshot")

# Get available tasks
tasks = automation.get_available_tasks()
```

### 5. User Interface (`ui/`)

**Purpose**: PyQt5-based graphical interface

**Key Classes**:
- `PetWidget`: Main application window
- `DesktopPetApp`: Application manager

**Features**:
- Chat interface
- Personality selector
- Real-time emoji display
- Action buttons
- System tray integration
- Modern, clean design

**UI Components**:
- Header: Personality selector
- Pet Display: Large emoji showing current personality
- Chat Display: Conversation history
- Input Field: User message input
- Action Buttons: Quick access to features

## Data Flow

### User Message Flow

```
User Input
    ↓
Intent Recognition
    ↓
Memory Storage (Record)
    ↓
Response Generation (with Personality)
    ↓
Memory Storage (Record Response)
    ↓
Display to User
```

### Automation Flow

```
User Request
    ↓
Intent Recognition (Automation Request)
    ↓
Task Selection/Creation
    ↓
Automation Engine Execution
    ↓
Result Feedback
    ↓
Memory Storage
```

### Memory Learning Flow

```
User Interaction
    ↓
Extract Patterns
    ↓
Store in Database
    ↓
Update Frequency
    ↓
Influence Future Responses
```

## Configuration System

The application uses a hierarchical configuration system:

1. **Environment Variables** (`.env`)
2. **Default Values** (in code)
3. **Runtime Configuration** (user preferences)

Key configuration areas:
- API keys for AI services
- Default personality type
- Memory settings
- Monitoring intervals
- Automation preferences

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed to git
2. **Automation Safety**: PyAutoGUI failsafe enabled
3. **Data Privacy**: Local SQLite database, no cloud sync
4. **Permission Management**: Requires appropriate system permissions

## Performance Optimization

1. **Database Indexing**: Indexes on timestamp and interaction_type
2. **Memory Limits**: Configurable maximum memory size
3. **Batch Operations**: Efficient bulk memory retrieval
4. **Lazy Loading**: Components initialized on demand

## Extension Points

The architecture supports extensions in several areas:

1. **New Personality Types**: Add to MBTIType enum
2. **Custom Intent Patterns**: Add to INTENT_PATTERNS
3. **Automation Tasks**: Create new AutomationTask instances
4. **Memory Analyzers**: Implement pattern detection algorithms
5. **UI Themes**: Modify stylesheet

## Future Enhancements

1. **AI Integration**: OpenAI/Anthropic for enhanced responses
2. **Voice Interface**: Speech recognition and synthesis
3. **Plugin System**: Third-party extensions
4. **Cloud Sync**: Optional cloud backup
5. **Mobile App**: Companion mobile application
6. **Multi-language**: Full internationalization

## Testing Strategy

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **UI Tests**: PyQt test framework
4. **Manual Testing**: User acceptance testing

## Deployment

1. **Development**: Run from source with Python
2. **Distribution**: PyInstaller for standalone executables
3. **Platforms**: Windows, macOS, Linux

## Dependencies

Core dependencies:
- Python 3.8+
- PyQt5: GUI framework
- PyAutoGUI: Automation
- SQLite3: Database (built-in)
- python-dotenv: Configuration
- pynput: Input monitoring

## Troubleshooting

Common issues and solutions:

1. **PyAutoGUI not working**: Check system permissions
2. **Database locked**: Close other instances
3. **Import errors**: Check PYTHONPATH
4. **UI not showing**: Check display settings

---

For more information, see the main README.md or contact the maintainers.
