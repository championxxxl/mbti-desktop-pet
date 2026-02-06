# Copilot Instructions for MBTI Desktop Pet

## Project Overview

This is an intelligent desktop pet assistant with MBTI (Myers-Briggs Type Indicator) personality types. The project aims to create an AI-powered desktop companion that exhibits different personality traits based on MBTI types.

## Technology Stack

- **Primary Language**: To be determined (likely Python, JavaScript/TypeScript, or Electron for desktop)
- **AI/ML Framework**: For natural language processing and personality simulation
- **Desktop Framework**: For cross-platform desktop application development
- **MBTI Integration**: Personality type system implementation

## Project Structure

```
mbti-desktop-pet/
├── .github/              # GitHub configuration and Copilot instructions
├── README.md            # Project documentation
└── (source code to be added)
```

## Coding Guidelines

### General Principles
- Write clean, maintainable, and well-documented code
- Follow the Single Responsibility Principle
- Use descriptive variable and function names
- Add comments for complex logic, especially in personality algorithms

### Code Style
- Use consistent formatting throughout the project
- Follow the language-specific style guide once the tech stack is established
- Keep functions small and focused
- Use meaningful commit messages following conventional commits format

### MBTI-Specific Guidelines
- Each MBTI personality type (16 types total) should have distinct behavioral patterns
- Personality traits should be modular and configurable
- Use data-driven approaches for personality responses
- Document personality characteristics and how they influence behavior

### AI/ML Guidelines
- Ensure AI responses are appropriate and safe
- Implement proper error handling for API calls
- Consider offline fallback behavior
- Test personality consistency across different interactions

## Development Workflow

1. **Branching**: Use feature branches for new features (e.g., `feature/add-intj-personality`)
2. **Commits**: Write clear, descriptive commit messages
3. **Testing**: Add tests for new features, especially personality behaviors
4. **Documentation**: Update README and inline documentation with changes

## What to Avoid

- Don't hardcode API keys or sensitive information
- Avoid creating overly complex personality algorithms without documentation
- Don't mix personality logic with UI code - keep them separated
- Avoid using offensive or inappropriate content in personality responses

## Testing Considerations

- Test all 16 MBTI personality types
- Verify personality consistency across sessions
- Test edge cases in user interactions
- Validate AI response quality and appropriateness

## Accessibility & UX

- Ensure the desktop pet is non-intrusive
- Provide clear user controls for pet behavior
- Support customization of appearance and behavior
- Consider different screen sizes and resolutions
