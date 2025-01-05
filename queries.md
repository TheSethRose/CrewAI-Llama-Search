# Query Log

This file tracks user queries to help improve agent prompts and performance.

## Query List

1. "Whats the latest AI news?"
   - Time frame: Latest/Current
   - Topic: AI
   - Focus: News/Updates
   - Note: User pointed out that 2022 results were too old (current date: Jan 4, 2025)

2. "Whats the latest AI news" (variation without question mark)
   - Time frame: Latest/Current
   - Topic: AI
   - Focus: News/Updates
   - Note: Query planner misinterpreted this as being about "industry" in general

3. "Who is Seth Rose?"
   - Type: Person/Identity query
   - Topic: Specific person
   - Focus: Biographical information
   - Note: Results were poor quality, suggesting issues with person-specific queries

4. "What did Sam Altman say about AI in his 2025 New Year message?"
   - Type: Person + Time-specific query
   - Topic: AI industry leadership
   - Focus: Recent statement/announcement
   - Note: Search tool had formatting issues with complex queries

5. "Which Walmart stores are open late near me?"
   - Type: Location + Time-specific query
   - Topic: Business hours
   - Focus: Local information
   - Note: System cannot handle location-based queries effectively
   - Issue: Query planner gave irrelevant climate change response

6. "Tokyo restaurants AND top-rated"
   - Type: Location + Rating query
   - Topic: Restaurant recommendations
   - Focus: Quality assessment
   - Issue: Search tool rejected array of queries
   - Note: Agent tried to batch multiple related searches

7. "What's the most unusual combination of toppings there's ever been on a pizza?"
   - Type: Superlative + Historical query
   - Topic: Food/Culinary
   - Focus: Extreme/Notable examples
   - Challenge: Requires comparison across many sources
   - Note: Subjective assessment ("unusual") needs clear criteria

## Patterns Observed

1. Tool Input Issues:
   - Agents trying to batch multiple related queries
   - Complex JSON formatting causing errors
   - Boolean values in wrong case (true vs True)
   - Array structures being rejected
   - Need for simpler, single-query approach

2. Query Processing:
   - Agents should process one query at a time
   - Sequential processing more reliable than batching
   - Need better error handling for complex queries
   - Temperature settings affecting query processing

3. Agent Behavior:
   - Topic drift in responses
   - Over-complex search strategies
   - Trying to handle unsupported features
   - Inconsistent response quality

4. Superlative Query Challenges:
   - Words like "most", "best", "worst" need clear criteria
   - Historical scope ("ever been") requires broader search
   - Subjective assessments need objective metrics
   - Need to compare across multiple sources
   - Must explain ranking/selection criteria

## Recommendations

1. Search Tool Configuration:
   - Accept only single, plain text queries
   - Remove JSON structure requirements
   - Better error messages for invalid inputs
   - Implement retry logic with simpler queries
   - Log failed queries for analysis

2. Agent Improvements:
   - Remove query validation/limitation checks
   - Process one search at a time
   - Simplify search strategies
   - Focus on core query intent
   - Better handling of all query types
   - Maintain context throughout chain

3. Response Quality:
   - Always attempt to answer query
   - Provide partial results when possible
   - Clear explanation of any limitations
   - Focus on most relevant information first
   - Better source filtering

4. Implementation Changes:
   - Simplify tool input handling
   - Better error recovery
   - Consistent query processing
   - Improved context maintenance
   - More robust search patterns

5. Superlative Query Handling:
   - Define clear criteria for subjective terms
   - Use multiple search variations
   - Include fact-checking of extreme claims
   - Compare across different time periods
   - Document selection methodology
   - Explain why choices meet criteria

6. Historical Search Improvements:
   - Search across different time periods
   - Use varied terminology for different eras
   - Cross-reference historical claims
   - Document earliest known instances
   - Track evolution over time
