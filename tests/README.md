# Test Documentation

This directory contains comprehensive unit tests for the MBTI Desktop Pet project.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Adding New Tests](#adding-new-tests)
- [Test Categories](#test-categories)
- [Best Practices](#best-practices)

## Overview

The test suite uses **pytest** as the testing framework and includes comprehensive coverage for:

- **Intent Recognition System** (`test_intent.py`)
- **MBTI Personality System** (`test_personality.py`)
- **Memory Management System** (`test_memory.py`)

All tests are designed to be independent, deterministic, and fast-running.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_intent.py             # Intent recognition tests (25+ test cases)
├── test_personality.py        # Personality system tests (25+ test cases)
├── test_memory.py             # Memory system tests (25+ test cases)
└── README.md                  # This file
```

## Running Tests

### Prerequisites

Install testing dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/

# Run with coverage report
pytest tests/ --cov=src/mbti_pet --cov-report=html

# Run with detailed output
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Run only intent recognition tests
pytest tests/test_intent.py

# Run only personality tests
pytest tests/test_personality.py

# Run only memory tests
pytest tests/test_memory.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_intent.py::TestBasicIntents

# Run a specific test function
pytest tests/test_intent.py::TestBasicIntents::test_help_request_intent

# Run tests matching a pattern
pytest tests/ -k "help_request"
```

### Run Tests by Markers

Tests are organized with pytest markers for easy filtering:

```bash
# Run only intent-related tests
pytest tests/ -m intent

# Run only personality-related tests
pytest tests/ -m personality

# Run only memory-related tests
pytest tests/ -m memory

# Run integration tests (when available)
pytest tests/ -m integration

# Exclude slow tests
pytest tests/ -m "not slow"
```

## Test Coverage

### Intent Recognition Tests (`test_intent.py`)

**Coverage:** 25+ test cases

- ✅ Basic intent types (help, task, information query)
- ✅ Advanced intents (automation, file operations, web search, code assistance, writing assistance, system commands)
- ✅ Entity extraction (file paths, URLs, emails, numbers, time values)
- ✅ Context-aware recognition (coding, web browsing, writing contexts)
- ✅ Edge cases (empty input, long input, special characters, mixed languages)
- ✅ Confidence score validation
- ✅ Chinese language support

**Test Classes:**
- `TestBasicIntents` - Tests for fundamental intent types
- `TestAdvancedIntents` - Tests for specialized intent types
- `TestEntityExtraction` - Tests for extracting structured data
- `TestContextAwareRecognition` - Tests for context-based intent detection
- `TestEdgeCases` - Tests for boundary conditions
- `TestIntentDataClass` - Tests for Intent data structure

### Personality System Tests (`test_personality.py`)

**Coverage:** 25+ test cases

- ✅ All 16 MBTI personality types (INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP)
- ✅ Personality creation and initialization
- ✅ Personality traits validation
- ✅ Greeting generation for all types
- ✅ Response formatting
- ✅ Personality descriptions
- ✅ Factory methods (from_string)
- ✅ Personality switching
- ✅ Edge cases and validation

**Test Classes:**
- `TestPersonalityCreation` - Tests for personality initialization
- `TestAllPersonalityTypes` - Tests for all 16 types (Analysts, Diplomats, Sentinels, Explorers)
- `TestPersonalityTraits` - Tests for trait validation
- `TestGreetingGeneration` - Tests for greeting messages
- `TestResponseFormatting` - Tests for message formatting
- `TestPersonalityDescription` - Tests for description generation
- `TestPersonalityFactory` - Tests for factory methods
- `TestPersonalitySwitching` - Tests for type switching
- `TestEdgeCases` - Tests for edge cases

### Memory System Tests (`test_memory.py`)

**Coverage:** 30+ test cases

- ✅ Memory initialization and database setup
- ✅ Memory recording with different parameters
- ✅ Memory retrieval (recent, by type)
- ✅ Memory search functionality
- ✅ Pattern learning and frequency tracking
- ✅ User preference learning
- ✅ Context retrieval for responses
- ✅ Memory summaries
- ✅ Database operations
- ✅ Edge cases (empty content, long content, special characters, unicode)

**Test Classes:**
- `TestMemoryInitialization` - Tests for database setup
- `TestMemoryRecording` - Tests for saving memories
- `TestMemoryRetrieval` - Tests for retrieving memories
- `TestMemorySearch` - Tests for search functionality
- `TestPatternLearning` - Tests for pattern detection
- `TestUserPreferences` - Tests for preference learning
- `TestContextForResponse` - Tests for context retrieval
- `TestMemorySummary` - Tests for summary generation
- `TestMemoryEntry` - Tests for data structures
- `TestEdgeCases` - Tests for boundary conditions

## Adding New Tests

### Test File Structure

Follow this structure when creating new test files:

```python
"""
Unit tests for [Component Name]

Brief description of what is being tested
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mbti_pet.module import ComponentToTest


# Fixtures
@pytest.fixture
def component_instance():
    """Create a component instance for testing"""
    return ComponentToTest()


# Test classes
@pytest.mark.category_name
class TestFeatureName:
    """Test feature description"""
    
    def test_specific_behavior(self, component_instance):
        """Test a specific behavior"""
        # Arrange
        input_data = "test input"
        
        # Act
        result = component_instance.method(input_data)
        
        # Assert
        assert result is not None
        assert result.expected_property == "expected_value"


# Run tests directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Writing Good Tests

Follow these principles:

1. **AAA Pattern** (Arrange, Act, Assert)
   ```python
   def test_feature(self):
       # Arrange - Set up test data
       input_data = "test"
       
       # Act - Execute the code
       result = function(input_data)
       
       # Assert - Verify expectations
       assert result == "expected"
   ```

2. **Use Descriptive Names**
   ```python
   # Good
   def test_greeting_contains_personality_emoji(self):
       pass
   
   # Bad
   def test_greeting(self):
       pass
   ```

3. **Test One Thing Per Test**
   ```python
   # Good - Tests one specific behavior
   def test_search_returns_matching_results(self):
       results = search("Python")
       assert len(results) > 0
   
   # Bad - Tests multiple things
   def test_search_and_filter_and_sort(self):
       # Too much in one test
       pass
   ```

4. **Use Fixtures for Common Setup**
   ```python
   @pytest.fixture
   def memory_manager():
       return MemoryManager(":memory:")
   
   def test_something(memory_manager):
       # Use the fixture
       memory_manager.record(...)
   ```

5. **Test Edge Cases**
   ```python
   def test_empty_input(self):
       result = function("")
       assert result is not None
   
   def test_very_long_input(self):
       result = function("x" * 10000)
       assert result is not None
   ```

### Using Markers

Add markers to categorize tests:

```python
@pytest.mark.intent
@pytest.mark.slow
def test_complex_intent_recognition(self):
    # This test is marked as both 'intent' and 'slow'
    pass
```

Available markers (defined in `pytest.ini`):
- `@pytest.mark.intent` - Intent recognition tests
- `@pytest.mark.personality` - Personality system tests
- `@pytest.mark.memory` - Memory system tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests

## Test Categories

### Unit Tests

Test individual components in isolation:
- Functions return expected values
- Classes initialize correctly
- Methods handle edge cases

### Integration Tests

Test how components work together:
- Intent system + Personality system
- Memory system + Intent recognition
- End-to-end workflows

### Edge Case Tests

Test boundary conditions:
- Empty inputs
- Very long inputs
- Special characters
- Invalid data
- Null/None values

## Best Practices

### Do's ✅

- **Write tests first** (TDD) or alongside code
- **Keep tests independent** - No test should depend on another
- **Use meaningful assertions** - Test actual behavior, not implementation
- **Clean up resources** - Use fixtures and context managers
- **Test edge cases** - Empty, null, invalid inputs
- **Document complex tests** - Add docstrings explaining why
- **Run tests frequently** - Before commits, after changes

### Don'ts ❌

- **Don't test implementation details** - Test behavior, not internals
- **Don't use real external services** - Mock APIs, databases, files
- **Don't write slow tests** - Keep tests fast (< 1 second each)
- **Don't skip error handling** - Test both success and failure paths
- **Don't hardcode paths** - Use temporary directories for file tests
- **Don't leave debug code** - Remove print statements and breakpoints

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Manual workflow dispatch

### Coverage Requirements

Aim for:
- **Minimum 80% code coverage**
- **100% coverage for critical paths**
- Focus on quality over quantity

### Test Reports

After running tests with coverage:

```bash
pytest tests/ --cov=src/mbti_pet --cov-report=html
```

Open `htmlcov/index.html` to view detailed coverage report.

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Make sure src is in Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

**Database locked errors:**
```python
# Use temporary in-memory database for tests
db_path = ":memory:"  # or use pytest fixtures with tempfile
```

**Tests pass locally but fail in CI:**
- Check for hardcoded paths
- Verify all dependencies in requirements.txt
- Check for timezone/locale dependencies

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Python Testing Best Practices](https://realpython.com/python-testing/)

## Contact

For questions about tests or to report issues:
- Open an issue on GitHub
- Review existing test examples
- Consult the project documentation

---

**Last Updated:** 2026-02-06
**Test Framework:** pytest 8.0.0
**Python Version:** >= 3.8
