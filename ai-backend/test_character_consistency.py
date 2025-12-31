"""
Test script for CharacterConsistencyTool.

Tests character profile creation, red flag generation,
and consistency analysis for catfish simulation.
"""

import asyncio
import json
from src.tools.character_consistency import (
    CharacterConsistencyManager,
    CharacterConsistencyTool,
    RedFlagType,
    RedFlagSeverity,
)


def test_create_character_profile():
    """Test character profile creation with inconsistencies."""
    print("=" * 60)
    print("TEST 1: Creating Character Profile")
    print("=" * 60)
    
    manager = CharacterConsistencyManager()
    
    # Create profile for a claimed 15-year-old
    profile = manager.create_character_profile(target_age=15, difficulty_level="moderate")
    
    print(f"\n✓ Character Name: {profile.name}")
    print(f"✓ Claimed Age: {profile.claimed_age}")
    print(f"✓ Actual Age Indicators: {profile.actual_age_indicators}")
    print(f"✓ Location: {profile.location}")
    print(f"✓ Occupation: {profile.occupation}")
    print(f"✓ Interests: {', '.join(profile.interests)}")
    print(f"✓ Backstory: {profile.backstory}")
    
    print(f"\n✓ Total Inconsistencies: {len(profile.inconsistencies)}")
    for i, inc in enumerate(profile.inconsistencies, 1):
        print(f"\n  Inconsistency {i}:")
        print(f"    Type: {inc.inconsistency_type.value}")
        print(f"    Severity: {inc.severity.value}")
        print(f"    Original: {inc.original_claim}")
        print(f"    Contradiction: {inc.contradicting_claim}")
        print(f"    Note: {inc.educational_note}")
    
    return profile


def test_generate_responses_with_red_flags(profile):
    """Test response generation with red flag revelation."""
    print("\n" + "=" * 60)
    print("TEST 2: Generating Responses with Red Flags")
    print("=" * 60)
    
    manager = CharacterConsistencyManager()
    
    # Simulate a conversation
    user_messages = [
        "Hey! How's it going?",
        "What kind of music do you like?",
        "Tell me about your school",
        "What do you do for fun?",
        "Have you traveled anywhere cool?",
        "What's your favorite app?",
        "Do you have any siblings?",
        "What's the weather like there?",
    ]
    
    print("\n🗨️  Simulated Conversation:\n")
    
    for i, user_msg in enumerate(user_messages, 1):
        print(f"Turn {i}:")
        print(f"  User: {user_msg}")
        
        # Generate response
        result = manager.generate_response_with_red_flag(profile, user_msg)
        
        print(f"  {profile.name}: {result['response']}")
        
        if result['red_flag_revealed']:
            print(f"  🚩 RED FLAG REVEALED: {result['red_flag_revealed']}")
            if result['inconsistency']:
                print(f"     Educational Note: {result['inconsistency']['educational_note']}")
        
        print()
    
    return profile


def test_force_red_flag_revelation(profile):
    """Test forcing red flag revelation."""
    print("\n" + "=" * 60)
    print("TEST 3: Forcing Red Flag Revelation")
    print("=" * 60)
    
    manager = CharacterConsistencyManager()
    
    user_message = "What was your childhood like?"
    
    print(f"\nUser: {user_message}")
    
    # Force red flag revelation
    result = manager.generate_response_with_red_flag(
        profile,
        user_message,
        force_red_flag=True
    )
    
    print(f"{profile.name}: {result['response']}")
    
    if result['red_flag_revealed']:
        print(f"\n🚩 RED FLAG REVEALED: {result['red_flag_revealed']}")
        if result['inconsistency']:
            print(f"   Type: {result['inconsistency']['inconsistency_type']}")
            print(f"   Severity: {result['inconsistency']['severity']}")
            print(f"   Educational Note: {result['inconsistency']['educational_note']}")
    
    return profile


def test_analyze_consistency(profile):
    """Test consistency analysis."""
    print("\n" + "=" * 60)
    print("TEST 4: Analyzing Character Consistency")
    print("=" * 60)
    
    manager = CharacterConsistencyManager()
    
    analysis = manager.analyze_consistency(profile)
    
    print(f"\n📊 Consistency Analysis:")
    print(f"  Total Inconsistencies: {analysis['total_inconsistencies']}")
    print(f"  Red Flags Revealed: {analysis['revealed_count']}")
    print(f"  Detection Rate: {analysis['detection_rate']:.1%}")
    print(f"  Conversation Turns: {analysis['conversation_turns']}")
    
    print(f"\n  Severity Breakdown:")
    for severity, count in analysis['severity_breakdown'].items():
        print(f"    {severity}: {count}")
    
    print(f"\n  Red Flags by Type:")
    for flag_type in analysis['red_flags_by_type']:
        print(f"    • {flag_type}")
    
    print(f"\n  📚 Educational Insights:")
    for insight in analysis['educational_insights']:
        print(f"    • {insight}")
    
    if analysis['unrevealed_red_flags']:
        print(f"\n  ⚠️  Unrevealed Red Flags: {len(analysis['unrevealed_red_flags'])}")
        for flag in analysis['unrevealed_red_flags']:
            print(f"    • {flag['inconsistency_type']}: {flag['contradicting_claim']}")


def test_crewai_tool_integration():
    """Test CrewAI tool integration."""
    print("\n" + "=" * 60)
    print("TEST 5: CrewAI Tool Integration")
    print("=" * 60)
    
    tool = CharacterConsistencyTool()
    
    # Test create_profile action
    print("\n1. Creating profile via tool:")
    result = tool._run(
        action="create_profile",
        target_age=16,
        difficulty_level="obvious"
    )
    profile_data = json.loads(result)
    print(f"   ✓ Created profile for: {profile_data['name']}")
    print(f"   ✓ Claimed age: {profile_data['claimed_age']}")
    print(f"   ✓ Inconsistencies: {len(profile_data['inconsistencies'])}")
    
    # Test generate_response action
    print("\n2. Generating response via tool:")
    result = tool._run(
        action="generate_response",
        profile=profile_data,
        user_message="What's your favorite movie?"
    )
    response_data = json.loads(result)
    print(f"   ✓ Response: {response_data['response']}")
    if response_data['red_flag_revealed']:
        print(f"   ✓ Red flag revealed: {response_data['red_flag_revealed']}")
    
    # Update profile with new conversation turn
    profile_data = response_data['profile']
    
    # Test reveal_red_flag action
    print("\n3. Forcing red flag via tool:")
    result = tool._run(
        action="reveal_red_flag",
        profile=profile_data,
        user_message="Tell me about your past"
    )
    response_data = json.loads(result)
    print(f"   ✓ Response: {response_data['response']}")
    print(f"   ✓ Red flag revealed: {response_data['red_flag_revealed']}")
    
    # Update profile
    profile_data = response_data['profile']
    
    # Test analyze_consistency action
    print("\n4. Analyzing consistency via tool:")
    result = tool._run(
        action="analyze_consistency",
        profile=profile_data
    )
    analysis_data = json.loads(result)
    print(f"   ✓ Detection rate: {analysis_data['detection_rate']:.1%}")
    print(f"   ✓ Red flags revealed: {analysis_data['revealed_count']}/{analysis_data['total_inconsistencies']}")


async def test_async_tool_integration():
    """Test async CrewAI tool integration."""
    print("\n" + "=" * 60)
    print("TEST 6: Async CrewAI Tool Integration")
    print("=" * 60)
    
    tool = CharacterConsistencyTool()
    
    # Test async create_profile
    print("\n1. Creating profile async:")
    profile_data = await tool._arun(
        action="create_profile",
        target_age=14,
        difficulty_level="subtle"
    )
    print(f"   ✓ Created profile for: {profile_data['name']}")
    
    # Test async generate_response
    print("\n2. Generating response async:")
    response_data = await tool._arun(
        action="generate_response",
        profile=profile_data,
        user_message="What do you like to do?"
    )
    print(f"   ✓ Response: {response_data['response']}")
    
    # Test async analyze
    profile_data = response_data['profile']
    print("\n3. Analyzing consistency async:")
    analysis_data = await tool._arun(
        action="analyze_consistency",
        profile=profile_data
    )
    print(f"   ✓ Analysis complete: {analysis_data['revealed_count']} red flags revealed")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CHARACTER CONSISTENCY TOOL - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Create character profile
    profile = test_create_character_profile()
    
    # Test 2: Generate responses with red flags
    profile = test_generate_responses_with_red_flags(profile)
    
    # Test 3: Force red flag revelation
    profile = test_force_red_flag_revelation(profile)
    
    # Test 4: Analyze consistency
    test_analyze_consistency(profile)
    
    # Test 5: CrewAI tool integration
    test_crewai_tool_integration()
    
    # Test 6: Async tool integration
    print("\n" + "=" * 60)
    print("Running async tests...")
    print("=" * 60)
    asyncio.run(test_async_tool_integration())
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
