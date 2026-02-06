# Agent Instructions for MBTI Desktop Pet

## Purpose

This file provides guidance for GitHub Copilot coding agents working on the MBTI Desktop Pet project. These instructions help ensure that automated code changes align with project goals and maintain code quality.

## Project Context

**Project Name**: MBTI Desktop Pet  
**Description**: An intelligent desktop pet assistant that exhibits different personality traits based on MBTI personality types  
**Primary Goal**: Create an engaging, AI-powered desktop companion with authentic MBTI personality behaviors

## What Agents Should Prioritize

### 1. Code Quality
- Write maintainable, well-structured code
- Follow established patterns in the codebase
- Add appropriate error handling
- Include meaningful comments for complex logic

### 2. Personality Authenticity
- Ensure MBTI personality implementations are accurate and consistent
- Each of the 16 personality types should have distinct, recognizable traits
- Personality behaviors should be data-driven and configurable
- Document the reasoning behind personality trait implementations

### 3. User Experience
- Keep the desktop pet non-intrusive and user-friendly
- Implement smooth animations and interactions
- Provide clear user controls and settings
- Ensure responsive performance

### 4. Security & Privacy
- Never hardcode API keys, tokens, or credentials
- Implement secure storage for sensitive data
- Validate and sanitize all user inputs
- Follow security best practices for AI/ML integrations

## What Agents Should NOT Do

### Critical Restrictions
- **Never remove or modify existing personality implementations** without explicit instructions
- **Don't change the core MBTI type system** (16 types with their cognitive functions)
- **Avoid altering configuration files** without understanding their impact
- **Don't introduce breaking changes** to existing APIs or interfaces

### Code Modifications
- Don't refactor working code unless explicitly requested
- Don't change coding style inconsistently across the codebase
- Don't remove tests or reduce test coverage
- Don't add unnecessary dependencies

### Content & Behavior
- Don't generate personality responses that could be offensive or inappropriate
- Don't make assumptions about user preferences without configuration options
- Don't hardcode personality traits - keep them configurable
- Don't mix concerns (e.g., UI logic with personality logic)

## Building & Testing

### Before Making Changes
1. Review existing code structure and patterns
2. Check for existing tests related to your changes
3. Understand the impact of your modifications

### After Making Changes
1. **Run tests**: Execute the test suite to ensure no regressions
2. **Test personality behaviors**: Verify that personality types still work as expected
3. **Check formatting**: Ensure code follows the project's style guide
4. **Validate functionality**: Test the feature in the actual application

### Testing Commands
(To be updated once build system is established)
```bash
# Run all tests
npm test  # or appropriate command

# Run specific personality tests
npm test personality

# Build the application
npm run build

# Run linter
npm run lint
```

## Change Validation Checklist

When making changes, agents should verify:

- [ ] Code compiles/runs without errors
- [ ] All tests pass
- [ ] No new security vulnerabilities introduced
- [ ] Documentation updated if needed
- [ ] Personality behaviors remain consistent
- [ ] No hardcoded secrets or sensitive data
- [ ] Changes follow existing code patterns
- [ ] User experience is not degraded

## Personality Implementation Guidelines

### MBTI Type Structure
Each personality type should implement:
- **Cognitive Functions**: Primary, auxiliary, tertiary, and inferior functions
- **Communication Style**: How the pet interacts with users
- **Decision Making**: How the pet processes information and makes choices
- **Emotional Expression**: How the pet displays emotions and reactions

### Testing Personalities
When modifying personality code:
1. Test the specific MBTI type affected
2. Verify it remains distinct from other types
3. Check for consistency in responses
4. Validate against MBTI theory documentation

## Communication & Collaboration

### When Uncertain
- Leave TODO comments for unclear requirements
- Prefer asking for clarification over making assumptions
- Document any trade-offs or decisions made

### Code Review Considerations
- Explain the reasoning behind complex changes
- Highlight any potential breaking changes
- Note any new dependencies added
- Document any deviation from established patterns

## Resources

- MBTI Theory: Research official MBTI documentation for personality type accuracy
- Desktop App Best Practices: Follow platform-specific guidelines (Windows, macOS, Linux)
- AI Safety Guidelines: Ensure appropriate and safe AI responses

## Version History

- **v1.0** (2026-02-06): Initial agent instructions setup
