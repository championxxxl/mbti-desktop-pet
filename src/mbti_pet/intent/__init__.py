"""
Intent Recognition System
Analyzes user input and screen activity to determine user intent
"""

import re
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass


class IntentType(Enum):
    """Types of user intents"""
    HELP_REQUEST = "help_request"
    TASK_EXECUTION = "task_execution"
    INFORMATION_QUERY = "information_query"
    AUTOMATION_REQUEST = "automation_request"
    CASUAL_CHAT = "casual_chat"
    SYSTEM_COMMAND = "system_command"
    FILE_OPERATION = "file_operation"
    WEB_SEARCH = "web_search"
    CODE_ASSISTANCE = "code_assistance"
    WRITING_ASSISTANCE = "writing_assistance"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Detected user intent"""
    intent_type: IntentType
    confidence: float  # 0.0 - 1.0
    entities: Dict[str, Any]
    raw_input: str
    suggested_action: Optional[str] = None


class IntentRecognizer:
    """Recognizes user intent from text input and context"""
    
    # Intent patterns
    INTENT_PATTERNS = {
        IntentType.HELP_REQUEST: [
            r'\b(help|assist|support|guide|show me|how to|can you|could you)\b',
            r'\b(need help|stuck|困难|帮助|协助)\b',
        ],
        IntentType.TASK_EXECUTION: [
            r'\b(do|execute|run|perform|start|launch|open)\b',
            r'\b(完成|执行|运行|启动|打开)\b',
        ],
        IntentType.INFORMATION_QUERY: [
            r'\b(what|when|where|who|why|how|which)\b',
            r'\b(tell me|explain|describe|find|search)\b',
            r'\b(什么|为什么|如何|哪里|告诉我|解释)\b',
        ],
        IntentType.AUTOMATION_REQUEST: [
            r'\b(automate|automatic|schedule|repeat|batch)\b',
            r'\b(自动|定时|批量|重复)\b',
        ],
        IntentType.FILE_OPERATION: [
            r'\b(file|folder|directory|save|load|delete|move|copy)\b',
            r'\b(文件|文件夹|保存|删除|移动|复制)\b',
        ],
        IntentType.WEB_SEARCH: [
            r'\b(search|google|find online|look up|browse)\b',
            r'\b(搜索|查找|浏览)\b',
        ],
        IntentType.CODE_ASSISTANCE: [
            r'\b(code|program|debug|compile|function|class|variable)\b',
            r'\b(代码|编程|调试|函数|类)\b',
        ],
        IntentType.WRITING_ASSISTANCE: [
            r'\b(write|draft|compose|edit|proofread|grammar)\b',
            r'\b(写作|编辑|语法|校对)\b',
        ],
        IntentType.SYSTEM_COMMAND: [
            r'\b(shutdown|restart|close|quit|exit|minimize)\b',
            r'\b(关闭|退出|重启|最小化)\b',
        ],
    }
    
    # Entity extraction patterns
    ENTITY_PATTERNS = {
        "file_path": r'["\']([^"\']+\.[a-zA-Z0-9]+)["\']',
        "url": r'https?://[^\s]+',
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "number": r'\b\d+\b',
        "time": r'\b\d{1,2}:\d{2}\b',
    }
    
    def __init__(self):
        self.compiled_patterns = {
            intent_type: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for intent_type, patterns in self.INTENT_PATTERNS.items()
        }
    
    def recognize_intent(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Intent:
        """Recognize intent from user input"""
        user_input_lower = user_input.lower()
        
        # Calculate confidence scores for each intent
        intent_scores = {}
        for intent_type, patterns in self.compiled_patterns.items():
            score = 0.0
            for pattern in patterns:
                if pattern.search(user_input_lower):
                    score += 0.3
            intent_scores[intent_type] = min(score, 1.0)
        
        # Get best matching intent
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            if best_intent[1] > 0.3:
                intent_type = best_intent[0]
                confidence = best_intent[1]
            else:
                intent_type = IntentType.CASUAL_CHAT
                confidence = 0.5
        else:
            intent_type = IntentType.CASUAL_CHAT
            confidence = 0.5
        
        # Extract entities
        entities = self._extract_entities(user_input)
        
        # Add context information
        if context:
            entities.update(context)
        
        # Generate suggested action
        suggested_action = self._generate_suggested_action(intent_type, entities, user_input)
        
        return Intent(
            intent_type=intent_type,
            confidence=confidence,
            entities=entities,
            raw_input=user_input,
            suggested_action=suggested_action
        )
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        entities = {}
        
        for entity_type, pattern in self.ENTITY_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def _generate_suggested_action(
        self,
        intent_type: IntentType,
        entities: Dict[str, Any],
        user_input: str
    ) -> Optional[str]:
        """Generate a suggested action based on intent"""
        suggestions = {
            IntentType.HELP_REQUEST: "I can help you with that. What specifically do you need assistance with?",
            IntentType.TASK_EXECUTION: "I'll help you execute that task. Let me prepare the necessary steps.",
            IntentType.INFORMATION_QUERY: "Let me search for that information for you.",
            IntentType.AUTOMATION_REQUEST: "I can set up automation for that. Let me configure it.",
            IntentType.FILE_OPERATION: "I'll help you with that file operation.",
            IntentType.WEB_SEARCH: "I'll search for that online.",
            IntentType.CODE_ASSISTANCE: "I can help with your code. Let me analyze it.",
            IntentType.WRITING_ASSISTANCE: "I'll help you with your writing.",
            IntentType.SYSTEM_COMMAND: "I'll execute that system command.",
            IntentType.CASUAL_CHAT: "I'm here to chat! What's on your mind?",
        }
        
        return suggestions.get(intent_type, "How can I help you?")


class ScreenActivityAnalyzer:
    """Analyzes screen activity to determine user intent"""
    
    def __init__(self):
        self.activity_history: List[Dict[str, Any]] = []
    
    def analyze_window_title(self, window_title: str) -> Dict[str, Any]:
        """Analyze window title to determine activity"""
        analysis = {
            "activity_type": "unknown",
            "app_name": "",
            "context": {}
        }
        
        # Detect common applications
        if any(keyword in window_title.lower() for keyword in ["chrome", "firefox", "safari", "edge"]):
            analysis["activity_type"] = "web_browsing"
            analysis["app_name"] = "browser"
        elif any(keyword in window_title.lower() for keyword in ["code", "visual studio", "pycharm", "intellij"]):
            analysis["activity_type"] = "coding"
            analysis["app_name"] = "ide"
        elif any(keyword in window_title.lower() for keyword in ["word", "docs", "notepad"]):
            analysis["activity_type"] = "writing"
            analysis["app_name"] = "text_editor"
        elif any(keyword in window_title.lower() for keyword in ["excel", "sheets", "calc"]):
            analysis["activity_type"] = "spreadsheet"
            analysis["app_name"] = "spreadsheet_app"
        
        return analysis
    
    def detect_pattern(self) -> Optional[str]:
        """Detect patterns in user activity"""
        if len(self.activity_history) < 3:
            return None
        
        # Simple pattern detection
        recent_activities = self.activity_history[-5:]
        activity_types = [a.get("activity_type") for a in recent_activities]
        
        # Check for repeated activity
        if len(set(activity_types)) == 1:
            return f"User is focused on {activity_types[0]}"
        
        return None
    
    def add_activity(self, activity: Dict[str, Any]):
        """Add activity to history"""
        self.activity_history.append(activity)
        # Keep only recent history
        if len(self.activity_history) > 50:
            self.activity_history = self.activity_history[-50:]


class ContextAwareIntentSystem:
    """Combines text and screen analysis for intent recognition"""
    
    def __init__(self):
        self.text_recognizer = IntentRecognizer()
        self.screen_analyzer = ScreenActivityAnalyzer()
    
    def analyze(
        self,
        user_input: Optional[str] = None,
        window_title: Optional[str] = None
    ) -> Intent:
        """Analyze user intent from available inputs"""
        context = {}
        
        # Analyze screen activity if available
        if window_title:
            screen_context = self.screen_analyzer.analyze_window_title(window_title)
            context.update(screen_context)
            self.screen_analyzer.add_activity(screen_context)
        
        # Analyze text input if available
        if user_input:
            return self.text_recognizer.recognize_intent(user_input, context)
        
        # If only screen activity, create intent from that
        if context:
            return Intent(
                intent_type=IntentType.UNKNOWN,
                confidence=0.3,
                entities=context,
                raw_input="",
                suggested_action="I noticed you're working on something. Need any help?"
            )
        
        return Intent(
            intent_type=IntentType.UNKNOWN,
            confidence=0.0,
            entities={},
            raw_input="",
            suggested_action=None
        )
