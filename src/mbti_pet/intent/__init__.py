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
    # New intent types for improved recognition
    SEARCH = "search"              # 搜索请求
    AUTOMATION = "automation"      # 自动化任务
    MEMORY = "memory"              # 记忆相关
    SCREENSHOT = "screenshot"      # 截图请求
    OPEN_URL = "open_url"          # 打开网址
    OPEN_FILE = "open_file"        # 打开文件
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
    
    # Intent patterns with enhanced recognition rules
    # Each pattern has a weight: high specificity = higher weight
    # Note: \b (word boundary) doesn't work with Chinese characters, so Chinese patterns avoid it
    INTENT_PATTERNS = {
        IntentType.HELP_REQUEST: [
            (r'\b(help|assist|support|guide)\b', 0.5),
            (r'\b(show me|how to|can you help|could you help)\b', 0.6),
            (r'\b(need help|stuck|need assistance|need support)\b', 0.6),
            (r'(帮助|协助|支持|指导)', 0.5),
            (r'(需要帮助|困难|有困难)', 0.6),
            (r'(teach me|guide me)', 0.5),
            (r'(帮我|教我)', 0.5),
        ],
        IntentType.TASK_EXECUTION: [
            (r'\b(execute|perform|carry out)\b.*\b(task|action|job)\b', 0.7),
            (r'\b(do|run|start|launch)\b', 0.4),  # Removed 'open' to avoid conflict with line below
            (r'\b(open|close).*\b(browser|application|app|program|window)\b', 0.7),  # Specific pattern for opening/closing apps
            (r'(完成|执行|运行|启动|打开)', 0.5),
            (r'^(please |帮我 )?(do|execute|run)', 0.6),
            (r'^(完成|执行)', 0.6),
        ],
        IntentType.INFORMATION_QUERY: [
            (r'^(what|when|where|who|why|how|which)\b', 0.6),
            (r'\b(tell me|explain|describe|define)\b', 0.6),
            (r'^(什么|为什么|如何|哪里|为何|怎么)', 0.6),
            (r'(告诉我|解释|说明|定义)', 0.6),
            (r'(查询|询问|了解|知道)', 0.5),
        ],
        IntentType.AUTOMATION_REQUEST: [
            (r'\b(automate|automatic|automatically)\b', 0.7),
            (r'\b(schedule|repeat|batch|recurring)\b', 0.6),
            (r'\b(set up|setup).*\b(automation|automatic)\b', 0.8),  # "Set up automation"
            (r'(自动化|自动|定时|批量)', 0.7),
            (r'(重复|循环|定期)', 0.5),
            (r'(every|每|每天|每周|daily|weekly)', 0.6),
        ],
        IntentType.FILE_OPERATION: [
            (r'\b(file|folder|directory)\b.*\b(save|load|delete|move|copy|rename)\b', 0.7),
            (r'\b(create|make|new)\b.*\b(file|folder)\b', 0.7),
            (r'(文件|文件夹|目录)', 0.5),
            (r'(保存|删除|移动|复制|重命名|创建)', 0.5),
        ],
        IntentType.WEB_SEARCH: [
            (r'\b(google|bing|search engine)\b', 0.7),
            (r'\b(find online|look up online|search the web)\b', 0.7),
            (r'\b(look up|lookup)\b', 0.6),  # "Look up machine learning"
            (r'\b(browse|surf)\b', 0.4),
            (r'(在线搜索|网上查找|上网搜)', 0.7),
        ],
        IntentType.CODE_ASSISTANCE: [
            (r'\b(code|program|script)\b.*\b(debug|fix|error|bug)\b', 0.8),
            (r'\b(debug|fix)\b.*\b(code|program|script|function|error|bug)\b', 0.8),
            (r'^(debug|fix)\b', 0.6),  # Start with debug/fix
            (r'\b(function|class|variable|method|algorithm)\b', 0.6),
            (r'\b(compile|syntax|runtime)\b.*\b(error|issue)\b', 0.7),
            (r'(代码|程序|脚本)', 0.5),
            (r'(调试|修复|错误|函数|类|变量)', 0.6),
        ],
        IntentType.WRITING_ASSISTANCE: [
            (r'\b(write|draft|compose)\b.*\b(document|article|essay|email)\b', 0.7),
            (r'\b(edit|proofread|review|revise)\b', 0.6),
            (r'\b(grammar|spelling|punctuation)\b', 0.6),
            (r'(写作|撰写|编写)', 0.6),
            (r'(编辑|修改|校对|语法)', 0.6),
        ],
        IntentType.SYSTEM_COMMAND: [
            (r'\b(shutdown|restart|reboot)\b.*\b(computer|system|pc)\b', 0.8),
            (r'\b(close|quit|exit|kill)\b.*\b(application|app|program)\b', 0.7),
            (r'\b(minimize|maximize|restore)\b.*\b(window)\b', 0.7),
            (r'(关闭|退出|结束).*(程序|应用|窗口)', 0.7),
            (r'(重启|关机|最小化|最大化)', 0.6),
        ],
        # New intent types with comprehensive patterns
        IntentType.SEARCH: [
            (r'^(search|find|lookup|query)\b', 0.7),
            (r'\b(search for|find me|lookup)\b', 0.7),
            (r'^(搜索|查询|搜|找)', 0.8),
            (r'(搜索|查找|检索).*(教程|资料|信息|内容)', 0.8),
            (r'(search).{1,20}(tutorial|guide|info|how to)', 0.8),  # English only, limited range
            (r'(搜索|搜|查找).{1,20}(教程|指南|方法)', 0.8),  # Chinese only, limited range
        ],
        IntentType.AUTOMATION: [
            (r'^(automate|自动化)', 0.9),
            (r'(帮我自动|自动执行|自动完成)', 0.9),
            (r'\b(automate this|make it automatic)\b', 0.8),
            (r'(自动化.*任务|自动.*处理)', 0.8),
            (r'(批处理|批量处理|自动运行)', 0.7),
        ],
        IntentType.MEMORY: [
            (r'^(remember|记住|记录)', 0.9),
            (r'\b(save to memory|store this)\b', 0.8),
            (r'(记下来|记一下)', 0.8),
            (r'(记住|记录|保存|储存).*(这个|这件事|此事|信息)', 0.9),
            (r'\b(memorize|keep in mind)\b', 0.8),
            (r'(别忘了|不要忘记)', 0.8),
            (r'\b(recall|retrieve)\b', 0.7),
            (r'(想起|回忆)', 0.7),
            (r'\b(do you remember)\b', 0.8),
            (r'(你记得|还记得)', 0.8),
        ],
        IntentType.SCREENSHOT: [
            (r'^(screenshot|capture|截图|截屏)', 0.95),
            (r'\b(take a screenshot|capture screen)\b', 0.9),
            (r'(截图|截屏|抓图|屏幕截图)', 0.95),
            (r'\b(capture this|save screen)\b', 0.8),
            (r'(保存屏幕)', 0.8),
            (r'\b(screen capture|print screen)\b', 0.8),
        ],
        IntentType.OPEN_URL: [
            (r'https?://[^\s]+', 0.95),  # Direct URL
            (r'\b(open|go to|visit|navigate to)\b.*(http|www\.|\.com|\.org|\.net)', 0.9),
            (r'(打开|访问|进入|浏览).*(网址|网站|链接)', 0.8),
            (r'^(打开|open)\s*(www\.|http)', 0.9),
            (r'(\.com|\.org|\.net|\.cn|\.io)\b', 0.6),
        ],
        IntentType.OPEN_FILE: [
            (r'\b(open|edit|view)\b.*\b(file|document)\b', 0.8),
            (r'(打开|编辑|查看).*(文件|文档)', 0.8),
            (r'\b(open|edit|view)\b.*\.(py|txt|doc|pdf|jpg|png|xlsx|json|xml|cpp|java|js|html|css)', 0.9),
            (r'(打开).*\.(py|txt|doc|pdf|jpg|png|xlsx|json|xml|cpp|java|js|html|css)', 0.9),  # Chinese separately
            (r'"[^"]*\.(py|txt|doc|pdf|jpg|png|xlsx|json|xml|cpp|java|js|html|css)"', 0.9),
            (r"'[^']*\.(py|txt|doc|pdf|jpg|png|xlsx|json|xml|cpp|java|js|html|css)'", 0.9),
        ],
        # Enhanced casual chat patterns (should have low specificity)
        IntentType.CASUAL_CHAT: [
            (r'^(hi|hello|hey|哈喽)', 0.8),
            (r'^(你好|嗨)', 0.8),
            (r"^(how are you|how's it going|what's up)", 0.8),
            (r'^(你好吗|怎么样)', 0.8),
            (r'\b(nice|good|great|cool|awesome)\b.*\b(weather|day)\b', 0.7),
            (r'(不错|很好|棒|好).*天气', 0.7),
            (r'^(thanks|thank you)', 0.7),
            (r'^(谢谢|感谢)', 0.7),
            (r'^(bye|goodbye|see you)', 0.7),
            (r'^(再见|拜拜)', 0.7),
            (r'(好的|ok|okay|fine|sure|alright|行|可以)', 0.4),
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
        # Compile patterns with their weights
        self.compiled_patterns = {}
        for intent_type, pattern_list in self.INTENT_PATTERNS.items():
            compiled_list = []
            for pattern, weight in pattern_list:
                compiled_list.append((re.compile(pattern, re.IGNORECASE), weight))
            self.compiled_patterns[intent_type] = compiled_list
    
    def recognize_intent(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Intent:
        """
        Recognize intent from user input with improved confidence scoring
        
        Confidence Calculation:
        - Base score: Sum of matched pattern weights
        - Bonus for multiple matches: +0.1 per additional match (up to +0.3)
        - Length normalization: Longer specific matches get slight bonus
        - Threshold: 0.4 for non-casual intent types
        """
        user_input_lower = user_input.lower()
        user_input_len = len(user_input)
        
        # Calculate confidence scores for each intent
        intent_scores = {}
        intent_match_counts = {}
        
        for intent_type, pattern_weight_list in self.compiled_patterns.items():
            score = 0.0
            match_count = 0
            
            for pattern, weight in pattern_weight_list:
                match = pattern.search(user_input_lower)
                if match:
                    # Base weight from pattern
                    score += weight
                    match_count += 1
                    
                    # Small bonus for longer matches (indicates specificity)
                    match_len = len(match.group(0))
                    if match_len > 10:
                        score += 0.05
            
            # Bonus for multiple pattern matches (indicates strong intent)
            if match_count > 1:
                bonus = min((match_count - 1) * 0.1, 0.3)
                score += bonus
            
            # Cap score at 1.0
            intent_scores[intent_type] = min(score, 1.0)
            intent_match_counts[intent_type] = match_count
        
        # Determine best intent
        # Sort by score, then by match count as tiebreaker
        sorted_intents = sorted(
            intent_scores.items(),
            key=lambda x: (x[1], intent_match_counts.get(x[0], 0)),
            reverse=True
        )
        
        if sorted_intents:
            best_intent_type, best_score = sorted_intents[0]
            
            # Apply threshold logic
            # Casual chat has lower threshold (easier to match)
            # Other intents need higher confidence
            if best_intent_type == IntentType.CASUAL_CHAT:
                threshold = 0.3
            else:
                threshold = 0.4
            
            if best_score >= threshold:
                intent_type = best_intent_type
                confidence = best_score
            else:
                # If no intent meets threshold, default to casual chat
                intent_type = IntentType.CASUAL_CHAT
                confidence = 0.5
        else:
            # No patterns matched at all
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
            # New intent types
            IntentType.SEARCH: "I'll search for that information right away.",
            IntentType.AUTOMATION: "I can automate that task for you. Let me set it up.",
            IntentType.MEMORY: "I'll remember that for you.",
            IntentType.SCREENSHOT: "Taking a screenshot now...",
            IntentType.OPEN_URL: "Opening the URL for you...",
            IntentType.OPEN_FILE: "Opening the file...",
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
