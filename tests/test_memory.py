"""
Unit tests for Memory System
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.memory import MemoryManager, MemoryEntry


def test_memory_initialization():
    """Test memory manager initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        assert os.path.exists(db_path)
    print("✓ Memory initialization test passed")


def test_record_interaction():
    """Test recording interactions"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        
        memory.record_interaction(
            interaction_type="text_input",
            content="Test message",
            importance=5
        )
        
        count = memory.db.get_memory_count()
        assert count == 1
    print("✓ Record interaction test passed")


def test_get_recent_memories():
    """Test retrieving recent memories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        
        # Add multiple memories
        for i in range(5):
            memory.record_interaction(
                interaction_type="test",
                content=f"Message {i}",
                importance=i
            )
        
        memories = memory.db.get_recent_memories(limit=3)
        assert len(memories) == 3
        # Just verify we got 3 memories
        assert all(mem.interaction_type == "test" for mem in memories)
    print("✓ Get recent memories test passed")


def test_search_memories():
    """Test searching memories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        
        memory.record_interaction(
            interaction_type="test",
            content="Python programming",
            importance=7
        )
        
        memory.record_interaction(
            interaction_type="test",
            content="JavaScript coding",
            importance=6
        )
        
        results = memory.db.search_memories("Python")
        assert len(results) == 1
        assert "Python" in results[0].content
    print("✓ Search memories test passed")


def test_pattern_learning():
    """Test pattern learning"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        
        pattern_data = {"task": "coding", "time": "morning"}
        memory.learn_pattern("task", pattern_data)
        
        patterns = memory.db.get_patterns(pattern_type="task")
        assert len(patterns) == 1
        assert patterns[0]["frequency"] == 1
    print("✓ Pattern learning test passed")


def test_memory_summary():
    """Test memory summary generation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        memory = MemoryManager(db_path)
        
        memory.record_interaction(
            interaction_type="test",
            content="Test interaction",
            importance=5
        )
        
        summary = memory.get_summary()
        assert "Total memories: 1" in summary
        assert "Test interaction" in summary
    print("✓ Memory summary test passed")


if __name__ == "__main__":
    print("Running Memory System Tests...")
    print("=" * 50)
    
    test_memory_initialization()
    test_record_interaction()
    test_get_recent_memories()
    test_search_memories()
    test_pattern_learning()
    test_memory_summary()
    
    print("=" * 50)
    print("All tests passed! ✓")
