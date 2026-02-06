"""
Memory System for Desktop Pet
Stores and retrieves user interactions and context
Similar to Memu - remembers user patterns and preferences
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3


@dataclass
class MemoryEntry:
    """Single memory entry"""
    timestamp: str
    interaction_type: str  # "text_input", "screen_activity", "automation", "response"
    content: str
    context: Dict[str, Any]
    importance: int  # 1-10 scale
    tags: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MemoryDatabase:
    """SQLite-based memory storage"""
    
    def __init__(self, db_path: str = "./data/memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                content TEXT NOT NULL,
                context TEXT,
                importance INTEGER,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_interaction_type ON memories(interaction_type)
        """)
        
        conn.commit()
        conn.close()
    
    def add_memory(self, memory: MemoryEntry):
        """Add a new memory entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO memories (timestamp, interaction_type, content, context, importance, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            memory.timestamp,
            memory.interaction_type,
            memory.content,
            json.dumps(memory.context),
            memory.importance,
            json.dumps(memory.tags)
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_memories(self, limit: int = 10, interaction_type: Optional[str] = None) -> List[MemoryEntry]:
        """Get recent memories, optionally filtered by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if interaction_type:
            cursor.execute("""
                SELECT timestamp, interaction_type, content, context, importance, tags
                FROM memories
                WHERE interaction_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (interaction_type, limit))
        else:
            cursor.execute("""
                SELECT timestamp, interaction_type, content, context, importance, tags
                FROM memories
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in results:
            memories.append(MemoryEntry(
                timestamp=row[0],
                interaction_type=row[1],
                content=row[2],
                context=json.loads(row[3]) if row[3] else {},
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else []
            ))
        
        return memories
    
    def search_memories(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Search memories by content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, interaction_type, content, context, importance, tags
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (f"%{query}%", limit))
        
        results = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in results:
            memories.append(MemoryEntry(
                timestamp=row[0],
                interaction_type=row[1],
                content=row[2],
                context=json.loads(row[3]) if row[3] else {},
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else []
            ))
        
        return memories
    
    def get_memory_count(self) -> int:
        """Get total number of memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def update_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Update or create a user pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if pattern exists
        cursor.execute("""
            SELECT id, frequency FROM user_patterns
            WHERE pattern_type = ? AND pattern_data = ?
        """, (pattern_type, json.dumps(pattern_data)))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing pattern
            cursor.execute("""
                UPDATE user_patterns
                SET frequency = frequency + 1, last_seen = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (result[0],))
        else:
            # Create new pattern
            cursor.execute("""
                INSERT INTO user_patterns (pattern_type, pattern_data, frequency)
                VALUES (?, ?, 1)
            """, (pattern_type, json.dumps(pattern_data)))
        
        conn.commit()
        conn.close()
    
    def get_patterns(self, pattern_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get learned user patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if pattern_type:
            cursor.execute("""
                SELECT pattern_type, pattern_data, frequency, last_seen
                FROM user_patterns
                WHERE pattern_type = ?
                ORDER BY frequency DESC, last_seen DESC
                LIMIT ?
            """, (pattern_type, limit))
        else:
            cursor.execute("""
                SELECT pattern_type, pattern_data, frequency, last_seen
                FROM user_patterns
                ORDER BY frequency DESC, last_seen DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        patterns = []
        for row in results:
            patterns.append({
                "pattern_type": row[0],
                "pattern_data": json.loads(row[1]),
                "frequency": row[2],
                "last_seen": row[3]
            })
        
        return patterns


class MemoryManager:
    """High-level memory management"""
    
    def __init__(self, db_path: str = "./data/memory.db"):
        self.db = MemoryDatabase(db_path)
    
    def record_interaction(
        self,
        interaction_type: str,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        importance: int = 5,
        tags: Optional[List[str]] = None
    ):
        """Record a new user interaction"""
        memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            interaction_type=interaction_type,
            content=content,
            context=context or {},
            importance=importance,
            tags=tags or []
        )
        self.db.add_memory(memory)
    
    def get_context_for_response(self, query: str, limit: int = 5) -> str:
        """Get relevant context from memory for generating response"""
        memories = self.db.search_memories(query, limit=limit)
        
        if not memories:
            memories = self.db.get_recent_memories(limit=limit)
        
        context_parts = []
        for memory in memories:
            context_parts.append(
                f"[{memory.interaction_type}] {memory.content}"
            )
        
        return "\n".join(context_parts)
    
    def learn_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Learn a user pattern"""
        self.db.update_pattern(pattern_type, pattern_data)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get learned user preferences"""
        patterns = self.db.get_patterns(limit=20)
        
        preferences = {
            "common_tasks": [],
            "preferred_times": [],
            "frequent_apps": []
        }
        
        for pattern in patterns:
            if pattern["pattern_type"] == "task":
                preferences["common_tasks"].append(pattern["pattern_data"])
            elif pattern["pattern_type"] == "time":
                preferences["preferred_times"].append(pattern["pattern_data"])
            elif pattern["pattern_type"] == "app":
                preferences["frequent_apps"].append(pattern["pattern_data"])
        
        return preferences
    
    def get_summary(self) -> str:
        """Get memory summary"""
        total = self.db.get_memory_count()
        recent = self.db.get_recent_memories(limit=5)
        
        summary = f"Total memories: {total}\n\nRecent interactions:\n"
        for memory in recent:
            summary += f"- [{memory.interaction_type}] {memory.content[:50]}...\n"
        
        return summary
