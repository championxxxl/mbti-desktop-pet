"""
Unit tests for Memory System

Comprehensive test coverage for:
- Memory initialization and database setup
- Memory recording and retrieval
- Memory search functionality
- User pattern learning
- User habit tracking
- Database operations
- Edge cases and error handling
"""

import pytest
import sys
import os
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.memory import MemoryManager, MemoryEntry, MemoryDatabase


# Fixtures
@pytest.fixture
def temp_db_path():
    """Create a temporary database path for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "test_memory.db")


@pytest.fixture
def memory_manager(temp_db_path):
    """Create a MemoryManager instance with temporary database"""
    return MemoryManager(temp_db_path)


@pytest.fixture
def memory_db(temp_db_path):
    """Create a MemoryDatabase instance with temporary database"""
    return MemoryDatabase(temp_db_path)


@pytest.mark.memory
class TestMemoryInitialization:
    """Test memory system initialization"""
    
    def test_memory_manager_initialization(self, temp_db_path):
        """Test memory manager initialization"""
        memory = MemoryManager(temp_db_path)
        assert os.path.exists(temp_db_path)
        assert memory.db is not None
    
    def test_database_initialization(self, temp_db_path):
        """Test database initialization"""
        db = MemoryDatabase(temp_db_path)
        assert os.path.exists(temp_db_path)
    
    def test_database_schema_creation(self, memory_db):
        """Test that database tables are created"""
        # Database should be initialized with tables
        count = memory_db.get_memory_count()
        assert count == 0  # No memories yet, but table exists


@pytest.mark.memory
class TestMemoryRecording:
    """Test memory recording functionality"""
    
    def test_record_interaction(self, memory_manager):
        """Test recording interactions"""
        memory_manager.record_interaction(
            interaction_type="text_input",
            content="Test message",
            importance=5
        )
        
        count = memory_manager.db.get_memory_count()
        assert count == 1
    
    def test_record_multiple_interactions(self, memory_manager):
        """Test recording multiple interactions"""
        for i in range(5):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Message {i}",
                importance=i
            )
        
        count = memory_manager.db.get_memory_count()
        assert count == 5
    
    def test_record_with_context(self, memory_manager):
        """Test recording interaction with context"""
        context = {"window": "VS Code", "activity": "coding"}
        memory_manager.record_interaction(
            interaction_type="coding",
            content="Writing Python code",
            context=context,
            importance=7
        )
        
        memories = memory_manager.db.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert memories[0].context == context
    
    def test_record_with_tags(self, memory_manager):
        """Test recording interaction with tags"""
        tags = ["python", "programming", "learning"]
        memory_manager.record_interaction(
            interaction_type="learning",
            content="Learning Python",
            tags=tags,
            importance=8
        )
        
        memories = memory_manager.db.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert memories[0].tags == tags
    
    def test_record_different_importance_levels(self, memory_manager):
        """Test recording with different importance levels"""
        for importance in range(1, 11):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Importance {importance}",
                importance=importance
            )
        
        count = memory_manager.db.get_memory_count()
        assert count == 10


@pytest.mark.memory
class TestMemoryRetrieval:
    """Test memory retrieval functionality"""
    
    def test_get_recent_memories(self, memory_manager):
        """Test retrieving recent memories"""
        # Add multiple memories
        for i in range(5):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Message {i}",
                importance=i
            )
        
        memories = memory_manager.db.get_recent_memories(limit=3)
        assert len(memories) == 3
        # Check all memories have the expected type
        assert all(mem.interaction_type == "test" for mem in memories)
    
    def test_get_recent_by_type(self, memory_manager):
        """Test retrieving recent memories by type"""
        memory_manager.record_interaction("type1", "Content 1", importance=5)
        memory_manager.record_interaction("type2", "Content 2", importance=5)
        memory_manager.record_interaction("type1", "Content 3", importance=5)
        
        type1_memories = memory_manager.db.get_recent_memories(
            limit=10,
            interaction_type="type1"
        )
        assert len(type1_memories) == 2
        assert all(m.interaction_type == "type1" for m in type1_memories)
    
    def test_memory_count(self, memory_manager):
        """Test getting total memory count"""
        assert memory_manager.db.get_memory_count() == 0
        
        memory_manager.record_interaction("test", "Content", importance=5)
        assert memory_manager.db.get_memory_count() == 1
        
        memory_manager.record_interaction("test", "Content 2", importance=5)
        assert memory_manager.db.get_memory_count() == 2


@pytest.mark.memory
class TestMemorySearch:
    """Test memory search functionality"""
    
    def test_search_memories(self, memory_manager):
        """Test searching memories"""
        memory_manager.record_interaction(
            interaction_type="test",
            content="Python programming",
            importance=7
        )
        
        memory_manager.record_interaction(
            interaction_type="test",
            content="JavaScript coding",
            importance=6
        )
        
        results = memory_manager.db.search_memories("Python")
        assert len(results) == 1
        assert "Python" in results[0].content
    
    def test_search_no_results(self, memory_manager):
        """Test searching with no results"""
        memory_manager.record_interaction("test", "Content", importance=5)
        
        results = memory_manager.db.search_memories("NonExistent")
        assert len(results) == 0
    
    def test_search_multiple_results(self, memory_manager):
        """Test searching with multiple results"""
        for i in range(3):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Python example {i}",
                importance=5
            )
        
        results = memory_manager.db.search_memories("Python")
        assert len(results) == 3
    
    def test_search_case_insensitive(self, memory_manager):
        """Test that search is case insensitive"""
        memory_manager.record_interaction(
            interaction_type="test",
            content="Python Programming",
            importance=5
        )
        
        results = memory_manager.db.search_memories("python")
        assert len(results) == 1
    
    def test_search_with_limit(self, memory_manager):
        """Test searching with result limit"""
        for i in range(10):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Test content {i}",
                importance=i
            )
        
        results = memory_manager.db.search_memories("content", limit=5)
        assert len(results) == 5


@pytest.mark.memory
class TestPatternLearning:
    """Test pattern learning functionality"""
    
    def test_learn_pattern(self, memory_manager):
        """Test pattern learning"""
        pattern_data = {"task": "coding", "time": "morning"}
        memory_manager.learn_pattern("task", pattern_data)
        
        patterns = memory_manager.db.get_patterns(pattern_type="task")
        assert len(patterns) == 1
        assert patterns[0]["frequency"] == 1
    
    def test_pattern_frequency_increment(self, memory_manager):
        """Test that pattern frequency increments"""
        pattern_data = {"task": "coding", "time": "morning"}
        
        # Learn same pattern multiple times
        memory_manager.learn_pattern("task", pattern_data)
        memory_manager.learn_pattern("task", pattern_data)
        memory_manager.learn_pattern("task", pattern_data)
        
        patterns = memory_manager.db.get_patterns(pattern_type="task")
        assert len(patterns) == 1
        assert patterns[0]["frequency"] == 3
    
    def test_multiple_pattern_types(self, memory_manager):
        """Test learning multiple pattern types"""
        memory_manager.learn_pattern("task", {"type": "coding"})
        memory_manager.learn_pattern("time", {"hour": 9})
        memory_manager.learn_pattern("app", {"name": "VSCode"})
        
        all_patterns = memory_manager.db.get_patterns(limit=10)
        assert len(all_patterns) == 3
    
    def test_get_patterns_by_type(self, memory_manager):
        """Test retrieving patterns by type"""
        memory_manager.learn_pattern("task", {"type": "coding"})
        memory_manager.learn_pattern("task", {"type": "writing"})
        memory_manager.learn_pattern("time", {"hour": 9})
        
        task_patterns = memory_manager.db.get_patterns(pattern_type="task")
        assert len(task_patterns) == 2


@pytest.mark.memory
class TestUserPreferences:
    """Test user preference learning"""
    
    def test_get_user_preferences(self, memory_manager):
        """Test getting user preferences"""
        # Learn some patterns
        memory_manager.learn_pattern("task", {"name": "coding"})
        memory_manager.learn_pattern("time", {"hour": 9})
        memory_manager.learn_pattern("app", {"name": "VSCode"})
        
        preferences = memory_manager.get_user_preferences()
        
        assert "common_tasks" in preferences
        assert "preferred_times" in preferences
        assert "frequent_apps" in preferences
    
    def test_preferences_empty_when_no_patterns(self, memory_manager):
        """Test preferences when no patterns learned"""
        preferences = memory_manager.get_user_preferences()
        
        assert len(preferences["common_tasks"]) == 0
        assert len(preferences["preferred_times"]) == 0
        assert len(preferences["frequent_apps"]) == 0


@pytest.mark.memory
class TestContextForResponse:
    """Test context retrieval for response generation"""
    
    def test_get_context_for_response(self, memory_manager):
        """Test getting context for response"""
        memory_manager.record_interaction(
            interaction_type="question",
            content="What is Python?",
            importance=5
        )
        
        context = memory_manager.get_context_for_response("Python")
        assert len(context) > 0
        assert "Python" in context
    
    def test_context_with_no_matching_memories(self, memory_manager):
        """Test context when no matching memories"""
        memory_manager.record_interaction(
            interaction_type="test",
            content="Some content",
            importance=5
        )
        
        context = memory_manager.get_context_for_response("NonExistent")
        # Should return recent memories as fallback
        assert len(context) > 0
    
    def test_context_limit(self, memory_manager):
        """Test context retrieval with limit"""
        for i in range(10):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Python example {i}",
                importance=5
            )
        
        context = memory_manager.get_context_for_response("Python", limit=3)
        # Should have at most 3 entries
        context_lines = context.split("\n")
        assert len([line for line in context_lines if line.strip()]) <= 3


@pytest.mark.memory
class TestMemorySummary:
    """Test memory summary generation"""
    
    def test_get_summary(self, memory_manager):
        """Test memory summary generation"""
        memory_manager.record_interaction(
            interaction_type="test",
            content="Test interaction",
            importance=5
        )
        
        summary = memory_manager.get_summary()
        assert "Total memories: 1" in summary
        assert "Test interaction" in summary
    
    def test_summary_with_multiple_memories(self, memory_manager):
        """Test summary with multiple memories"""
        for i in range(5):
            memory_manager.record_interaction(
                interaction_type="test",
                content=f"Interaction {i}",
                importance=i
            )
        
        summary = memory_manager.get_summary()
        assert "Total memories: 5" in summary
    
    def test_summary_empty_memory(self, memory_manager):
        """Test summary with no memories"""
        summary = memory_manager.get_summary()
        assert "Total memories: 0" in summary


@pytest.mark.memory
class TestMemoryEntry:
    """Test MemoryEntry data class"""
    
    def test_memory_entry_creation(self):
        """Test creating MemoryEntry"""
        entry = MemoryEntry(
            timestamp="2024-01-01T00:00:00",
            interaction_type="test",
            content="Test content",
            context={"key": "value"},
            importance=5,
            tags=["tag1", "tag2"]
        )
        
        assert entry.timestamp == "2024-01-01T00:00:00"
        assert entry.interaction_type == "test"
        assert entry.content == "Test content"
        assert entry.context == {"key": "value"}
        assert entry.importance == 5
        assert entry.tags == ["tag1", "tag2"]
    
    def test_memory_entry_to_dict(self):
        """Test converting MemoryEntry to dict"""
        entry = MemoryEntry(
            timestamp="2024-01-01T00:00:00",
            interaction_type="test",
            content="Test content",
            context={},
            importance=5,
            tags=[]
        )
        
        entry_dict = entry.to_dict()
        assert isinstance(entry_dict, dict)
        assert entry_dict["interaction_type"] == "test"
        assert entry_dict["content"] == "Test content"


@pytest.mark.memory
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_content(self, memory_manager):
        """Test recording memory with empty content"""
        memory_manager.record_interaction(
            interaction_type="test",
            content="",
            importance=5
        )
        
        count = memory_manager.db.get_memory_count()
        assert count == 1
    
    def test_very_long_content(self, memory_manager):
        """Test recording memory with very long content"""
        long_content = "test " * 1000
        memory_manager.record_interaction(
            interaction_type="test",
            content=long_content,
            importance=5
        )
        
        memories = memory_manager.db.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert memories[0].content == long_content
    
    def test_special_characters_in_content(self, memory_manager):
        """Test recording memory with special characters"""
        special_content = "Test!@#$%^&*()_+-=[]{}|;':\"<>?,./`~"
        memory_manager.record_interaction(
            interaction_type="test",
            content=special_content,
            importance=5
        )
        
        memories = memory_manager.db.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert memories[0].content == special_content
    
    def test_unicode_content(self, memory_manager):
        """Test recording memory with unicode content"""
        unicode_content = "Hello 世界 🌍 Привет"
        memory_manager.record_interaction(
            interaction_type="test",
            content=unicode_content,
            importance=5
        )
        
        memories = memory_manager.db.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert memories[0].content == unicode_content
    
    def test_importance_boundaries(self, memory_manager):
        """Test importance level boundaries"""
        # Test minimum importance
        memory_manager.record_interaction("test", "Min importance", importance=1)
        # Test maximum importance
        memory_manager.record_interaction("test", "Max importance", importance=10)
        
        count = memory_manager.db.get_memory_count()
        assert count == 2


# Run tests directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
