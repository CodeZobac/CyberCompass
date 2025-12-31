"""
Test script for ContentGeneratorTool.

Verifies that the tool meets all requirements for task 7.2:
- Generate realistic social media posts
- Create disinformation content with educational markers
- Generate comment threads with diverse viewpoints
"""

import asyncio
import json
from src.tools.content_generator import (
    ContentGenerator,
    ContentGeneratorTool,
    ContentType,
    DisinformationType,
)


def test_post_generation():
    """Test generating social media posts with disinformation patterns."""
    print("\n" + "="*80)
    print("TEST 1: Social Media Post Generation")
    print("="*80)
    
    generator = ContentGenerator()
    
    # Test different disinformation types
    disinfo_types = [
        DisinformationType.CLICKBAIT,
        DisinformationType.FAKE_NEWS,
        DisinformationType.CONSPIRACY,
        DisinformationType.HEALTH_MISINFO,
    ]
    
    for disinfo_type in disinfo_types:
        print(f"\n--- Testing {disinfo_type.value} ---")
        post = generator.generate_post(
            topic="artificial intelligence",
            disinfo_type=disinfo_type,
            include_red_flags=True
        )
        
        print(f"Author: {post.author}")
        print(f"Platform: {post.platform}")
        print(f"Content: {post.content}")
        print(f"Engagement: {post.engagement}")
        print(f"Is Simulation: {post.is_simulation}")
        print(f"Red Flags: {len(post.red_flags)}")
        
        for flag in post.red_flags:
            print(f"  - {flag.flag_type}: {flag.description}")
            print(f"    Educational Note: {flag.educational_note}")
        
        # Verify requirements
        assert post.content, "Post content should not be empty"
        assert post.author, "Post should have an author"
        assert post.is_simulation is True, "Post should be marked as simulation"
        assert len(post.red_flags) > 0, "Post should have red flags"
        assert len(post.educational_notes) > 0, "Post should have educational notes"
        assert post.engagement["likes"] > 0, "Post should have engagement metrics"
        
        print("✓ Post generation successful")


def test_comment_thread_generation():
    """Test generating comment threads with diverse viewpoints."""
    print("\n" + "="*80)
    print("TEST 2: Comment Thread Generation")
    print("="*80)
    
    generator = ContentGenerator()
    
    # Generate a post first
    post = generator.generate_post(
        topic="climate change",
        disinfo_type=DisinformationType.CONSPIRACY,
        include_red_flags=True
    )
    
    # Generate comment thread
    thread = generator.generate_comment_thread(
        post=post,
        num_comments=8,
        include_red_flags=True
    )
    
    print(f"\nOriginal Post: {thread.original_post.content}")
    print(f"Number of Comments: {len(thread.comments)}")
    print(f"Thread Red Flags: {len(thread.red_flags)}")
    
    # Check viewpoint diversity
    viewpoints = {}
    for comment in thread.comments:
        viewpoint = comment.viewpoint
        viewpoints[viewpoint] = viewpoints.get(viewpoint, 0) + 1
        print(f"\n  [{comment.viewpoint}] {comment.author}:")
        print(f"  {comment.content}")
        print(f"  Engagement: {comment.engagement}")
    
    print(f"\nViewpoint Distribution: {viewpoints}")
    
    # Display thread-level red flags
    print("\nThread Red Flags:")
    for flag in thread.red_flags:
        print(f"  - {flag.flag_type}: {flag.description}")
        print(f"    Educational Note: {flag.educational_note}")
    
    # Verify requirements
    assert len(thread.comments) == 8, "Should generate requested number of comments"
    assert len(viewpoints) > 1, "Should have diverse viewpoints"
    assert len(thread.red_flags) > 0, "Thread should have red flags"
    assert len(thread.educational_notes) > 0, "Thread should have educational notes"
    
    print("\n✓ Comment thread generation successful")


def test_content_types():
    """Test all content types (post, comment, thread)."""
    print("\n" + "="*80)
    print("TEST 3: All Content Types")
    print("="*80)
    
    generator = ContentGenerator()
    
    # Test POST type
    print("\n--- Testing POST type ---")
    post_content = generator.generate_content(
        content_type=ContentType.POST,
        topic="cybersecurity",
        disinfo_type=DisinformationType.FAKE_NEWS,
        include_red_flags=True
    )
    assert "content" in post_content, "POST should have content field"
    assert "red_flags" in post_content, "POST should have red_flags field"
    print(f"✓ POST type: {post_content['content'][:100]}...")
    
    # Test THREAD type
    print("\n--- Testing THREAD type ---")
    thread_content = generator.generate_content(
        content_type=ContentType.THREAD,
        topic="vaccination",
        disinfo_type=DisinformationType.HEALTH_MISINFO,
        include_red_flags=True,
        num_comments=5
    )
    assert "original_post" in thread_content, "THREAD should have original_post"
    assert "comments" in thread_content, "THREAD should have comments"
    assert len(thread_content["comments"]) == 5, "THREAD should have requested comments"
    print(f"✓ THREAD type: {len(thread_content['comments'])} comments generated")
    
    # Test COMMENT type
    print("\n--- Testing COMMENT type ---")
    comment_content = generator.generate_content(
        content_type=ContentType.COMMENT,
        topic="politics",
        disinfo_type=DisinformationType.POLITICAL_MISINFO,
        include_red_flags=True
    )
    assert "content" in comment_content, "COMMENT should have content field"
    assert "viewpoint" in comment_content, "COMMENT should have viewpoint field"
    print(f"✓ COMMENT type: [{comment_content['viewpoint']}] {comment_content['content']}")
    
    print("\n✓ All content types working correctly")


def test_educational_markers():
    """Test that educational markers are properly included."""
    print("\n" + "="*80)
    print("TEST 4: Educational Markers")
    print("="*80)
    
    generator = ContentGenerator()
    
    # Test with red flags enabled
    print("\n--- With Educational Markers ---")
    post_with_flags = generator.generate_post(
        topic="5G technology",
        disinfo_type=DisinformationType.CONSPIRACY,
        include_red_flags=True
    )
    
    print(f"Red Flags: {len(post_with_flags.red_flags)}")
    print(f"Educational Notes: {len(post_with_flags.educational_notes)}")
    
    assert len(post_with_flags.red_flags) > 0, "Should have red flags when enabled"
    assert len(post_with_flags.educational_notes) > 0, "Should have educational notes"
    assert post_with_flags.is_simulation is True, "Should be marked as simulation"
    
    # Test without red flags
    print("\n--- Without Educational Markers ---")
    post_without_flags = generator.generate_post(
        topic="5G technology",
        disinfo_type=DisinformationType.CONSPIRACY,
        include_red_flags=False
    )
    
    print(f"Red Flags: {len(post_without_flags.red_flags)}")
    print(f"Educational Notes: {len(post_without_flags.educational_notes)}")
    
    assert len(post_without_flags.red_flags) == 0, "Should have no red flags when disabled"
    assert post_without_flags.is_simulation is True, "Should still be marked as simulation"
    
    print("\n✓ Educational markers working correctly")


def test_disinformation_categories():
    """Test all disinformation categories."""
    print("\n" + "="*80)
    print("TEST 5: All Disinformation Categories")
    print("="*80)
    
    generator = ContentGenerator()
    
    all_types = [
        DisinformationType.CLICKBAIT,
        DisinformationType.FAKE_NEWS,
        DisinformationType.CONSPIRACY,
        DisinformationType.EMOTIONAL_MANIPULATION,
        DisinformationType.MISLEADING_STATISTICS,
        DisinformationType.HEALTH_MISINFO,
        DisinformationType.POLITICAL_MISINFO,
    ]
    
    for disinfo_type in all_types:
        post = generator.generate_post(
            topic="technology",
            disinfo_type=disinfo_type,
            include_red_flags=True
        )
        
        print(f"\n{disinfo_type.value}:")
        print(f"  Content: {post.content[:80]}...")
        print(f"  Red Flags: {[flag.flag_type for flag in post.red_flags]}")
        
        assert post.content, f"{disinfo_type.value} should generate content"
        assert len(post.red_flags) > 0, f"{disinfo_type.value} should have red flags"
    
    print("\n✓ All disinformation categories working")


async def test_tool_async():
    """Test the CrewAI tool async interface."""
    print("\n" + "="*80)
    print("TEST 6: CrewAI Tool Async Interface")
    print("="*80)
    
    tool = ContentGeneratorTool()
    
    # Test async generation
    result = await tool._arun(
        content_type=ContentType.THREAD,
        topic="social media algorithms",
        disinfo_type=DisinformationType.EMOTIONAL_MANIPULATION,
        include_red_flags=True,
        num_comments=6
    )
    
    print(f"\nGenerated content type: {type(result)}")
    print(f"Has original_post: {'original_post' in result}")
    print(f"Number of comments: {len(result.get('comments', []))}")
    
    assert isinstance(result, dict), "Async result should be a dictionary"
    assert "original_post" in result, "Should have original_post"
    assert "comments" in result, "Should have comments"
    assert len(result["comments"]) == 6, "Should have requested number of comments"
    
    print("\n✓ Async tool interface working correctly")


def test_tool_sync():
    """Test the CrewAI tool sync interface."""
    print("\n" + "="*80)
    print("TEST 7: CrewAI Tool Sync Interface")
    print("="*80)
    
    tool = ContentGeneratorTool()
    
    # Test sync generation
    result = tool._run(
        content_type=ContentType.POST,
        topic="data privacy",
        disinfo_type=DisinformationType.CLICKBAIT,
        include_red_flags=True,
        num_comments=5
    )
    
    print(f"\nGenerated content type: {type(result)}")
    print(f"Result length: {len(result)} characters")
    
    # Parse JSON result
    parsed = json.loads(result)
    print(f"Parsed content: {parsed.get('content', '')[:80]}...")
    
    assert isinstance(result, str), "Sync result should be a string"
    assert len(result) > 0, "Result should not be empty"
    
    parsed_data = json.loads(result)
    assert "content" in parsed_data, "Parsed result should have content"
    assert "red_flags" in parsed_data, "Parsed result should have red_flags"
    
    print("\n✓ Sync tool interface working correctly")


def test_requirements_compliance():
    """Verify compliance with requirements 5.1, 5.2, 5.4."""
    print("\n" + "="*80)
    print("TEST 8: Requirements Compliance")
    print("="*80)
    
    generator = ContentGenerator()
    
    # Requirement 5.1: Generate realistic social media feed
    print("\n--- Requirement 5.1: Realistic Social Media Feed ---")
    posts = []
    for i in range(3):
        post = generator.generate_post(
            topic=f"topic_{i}",
            disinfo_type=DisinformationType.FAKE_NEWS,
            include_red_flags=True
        )
        posts.append(post)
    
    assert len(posts) == 3, "Should generate multiple posts"
    print(f"✓ Generated {len(posts)} realistic posts")
    
    # Requirement 5.2: Multiple disinformation categories
    print("\n--- Requirement 5.2: Multiple Disinformation Categories ---")
    categories = [
        DisinformationType.HEALTH_MISINFO,
        DisinformationType.POLITICAL_MISINFO,
        DisinformationType.CONSPIRACY,
    ]
    
    for category in categories:
        post = generator.generate_post(
            topic="test",
            disinfo_type=category,
            include_red_flags=True
        )
        assert post.content, f"Should generate {category.value} content"
        print(f"✓ {category.value} content generated")
    
    # Requirement 5.4: Diverse viewpoints in comment threads
    print("\n--- Requirement 5.4: Diverse Viewpoints ---")
    post = generator.generate_post(
        topic="test",
        disinfo_type=DisinformationType.FAKE_NEWS,
        include_red_flags=True
    )
    
    thread = generator.generate_comment_thread(
        post=post,
        num_comments=10,
        include_red_flags=True
    )
    
    viewpoints = set(comment.viewpoint for comment in thread.comments)
    print(f"Viewpoints found: {viewpoints}")
    assert len(viewpoints) >= 2, "Should have diverse viewpoints"
    print(f"✓ Generated {len(viewpoints)} different viewpoints")
    
    # Requirement 5.6: Educational markers
    print("\n--- Requirement 5.6: Educational Markers ---")
    assert post.is_simulation is True, "Content should be marked as simulation"
    assert len(post.educational_notes) > 0, "Should have educational notes"
    assert len(post.red_flags) > 0, "Should have red flags"
    print("✓ Educational markers present")
    
    print("\n" + "="*80)
    print("✓ ALL REQUIREMENTS VERIFIED")
    print("="*80)


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("CONTENT GENERATOR TOOL - COMPREHENSIVE TEST SUITE")
    print("Task 7.2: Build ContentGeneratorTool for social media simulation")
    print("="*80)
    
    try:
        # Run synchronous tests
        test_post_generation()
        test_comment_thread_generation()
        test_content_types()
        test_educational_markers()
        test_disinformation_categories()
        test_tool_sync()
        
        # Run async tests
        asyncio.run(test_tool_async())
        
        # Final requirements check
        test_requirements_compliance()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print("\nTask 7.2 Implementation Verified:")
        print("✓ Create tool for generating realistic social media posts")
        print("✓ Implement disinformation content creation with educational markers")
        print("✓ Add comment thread generation with diverse viewpoints")
        print("✓ Requirements 5.1, 5.2, 5.4 satisfied")
        print("="*80)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
