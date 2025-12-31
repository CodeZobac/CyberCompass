"""
Content Generator Tool for social media simulation.

Generates realistic social media posts with disinformation patterns
for educational purposes. All content is clearly marked as simulation.
"""

import random
from enum import Enum
from typing import List, Optional, Dict, Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ContentType(str, Enum):
    """Types of social media content."""
    POST = "post"
    COMMENT = "comment"
    THREAD = "thread"


class DisinformationType(str, Enum):
    """Types of disinformation patterns."""
    CLICKBAIT = "clickbait"
    FAKE_NEWS = "fake_news"
    CONSPIRACY = "conspiracy"
    EMOTIONAL_MANIPULATION = "emotional_manipulation"
    MISLEADING_STATISTICS = "misleading_statistics"
    HEALTH_MISINFO = "health_misinfo"
    POLITICAL_MISINFO = "political_misinfo"


class ContentGeneratorInput(BaseModel):
    """Input schema for content generation."""
    content_type: ContentType = Field(..., description="Type of content to generate")
    topic: str = Field(..., description="Topic for the content")
    disinfo_type: DisinformationType = Field(..., description="Type of disinformation pattern")
    include_red_flags: bool = Field(default=True, description="Include educational red flag markers")
    num_comments: Optional[int] = Field(default=5, description="Number of comments for threads")


class RedFlag(BaseModel):
    """Educational red flag marker."""
    flag_type: str = Field(..., description="Type of red flag")
    description: str = Field(..., description="Description of the red flag")
    location: str = Field(..., description="Where in content the flag appears")
    educational_note: str = Field(..., description="Educational explanation")


class SocialMediaPost(BaseModel):
    """Social media post with educational markers."""
    content: str = Field(..., description="Post content")
    author: str = Field(..., description="Author username")
    platform: str = Field(..., description="Social media platform")
    engagement: Dict[str, int] = Field(..., description="Engagement metrics")
    red_flags: List[RedFlag] = Field(default_factory=list, description="Educational red flags")
    educational_notes: List[str] = Field(default_factory=list, description="Educational notes")
    is_simulation: bool = Field(default=True, description="Simulation marker")


class Comment(BaseModel):
    """Social media comment."""
    author: str = Field(..., description="Comment author")
    content: str = Field(..., description="Comment content")
    viewpoint: str = Field(..., description="Viewpoint type")
    engagement: Dict[str, int] = Field(..., description="Comment engagement")


class CommentThread(BaseModel):
    """Comment thread with diverse viewpoints."""
    original_post: SocialMediaPost = Field(..., description="Original post")
    comments: List[Comment] = Field(default_factory=list, description="Thread comments")
    red_flags: List[RedFlag] = Field(default_factory=list, description="Thread red flags")
    educational_notes: List[str] = Field(default_factory=list, description="Educational notes")


class ContentGenerator:
    """
    Generates social media content with disinformation patterns.
    
    Creates realistic posts, comments, and threads for educational
    simulation of social media disinformation scenarios.
    """
    
    def __init__(self):
        """Initialize content generator with templates and patterns."""
        # Red flag patterns for different disinformation types
        self.red_flag_patterns = {
            DisinformationType.CLICKBAIT: [
                {
                    "type": "sensational_language",
                    "desc": "Excessive caps and exclamation marks",
                    "note": "Clickbait uses emotional language to manipulate clicks"
                },
                {
                    "type": "vague_promises",
                    "desc": "Vague promises without specifics",
                    "note": "Legitimate news provides concrete details upfront"
                },
                {
                    "type": "curiosity_gap",
                    "desc": "Withholds key information to force clicks",
                    "note": "Creates artificial curiosity to drive engagement"
                }
            ],
            DisinformationType.FAKE_NEWS: [
                {
                    "type": "no_sources",
                    "desc": "No credible sources cited",
                    "note": "Real news cites verifiable, authoritative sources"
                },
                {
                    "type": "false_urgency",
                    "desc": "Creates false sense of urgency",
                    "note": "Fake news pressures quick sharing before fact-checking"
                },
                {
                    "type": "unverified_claims",
                    "desc": "Makes extraordinary claims without evidence",
                    "note": "Extraordinary claims require extraordinary evidence"
                }
            ],
            DisinformationType.CONSPIRACY: [
                {
                    "type": "circular_logic",
                    "desc": "Uses circular reasoning",
                    "note": "Conspiracy theories often lack logical consistency"
                },
                {
                    "type": "pattern_seeking",
                    "desc": "Finds patterns in unrelated events",
                    "note": "Humans naturally seek patterns, even where none exist"
                },
                {
                    "type": "us_vs_them",
                    "desc": "Creates in-group vs out-group mentality",
                    "note": "Divides people into 'awakened' vs 'sheep'"
                }
            ],
            DisinformationType.EMOTIONAL_MANIPULATION: [
                {
                    "type": "fear_mongering",
                    "desc": "Uses fear to drive engagement",
                    "note": "Fear bypasses critical thinking"
                },
                {
                    "type": "outrage_bait",
                    "desc": "Designed to provoke anger",
                    "note": "Anger increases sharing without verification"
                }
            ],
            DisinformationType.MISLEADING_STATISTICS: [
                {
                    "type": "cherry_picking",
                    "desc": "Selectively presents data",
                    "note": "Context matters - look for complete data"
                },
                {
                    "type": "false_correlation",
                    "desc": "Implies causation from correlation",
                    "note": "Correlation does not equal causation"
                }
            ],
            DisinformationType.HEALTH_MISINFO: [
                {
                    "type": "anecdotal_evidence",
                    "desc": "Relies on personal stories over science",
                    "note": "Anecdotes are not scientific evidence"
                },
                {
                    "type": "miracle_cure",
                    "desc": "Promises unrealistic health outcomes",
                    "note": "Be skeptical of miracle cures and quick fixes"
                }
            ],
            DisinformationType.POLITICAL_MISINFO: [
                {
                    "type": "out_of_context",
                    "desc": "Uses quotes or images out of context",
                    "note": "Always verify the full context"
                },
                {
                    "type": "false_equivalence",
                    "desc": "Compares unequal things as equal",
                    "note": "Not all sides of an issue are equally valid"
                }
            ]
        }
        
        # Post templates for different disinformation types
        self.post_templates = {
            DisinformationType.CLICKBAIT: [
                "You WON'T BELIEVE what scientists discovered about {topic}! Click to find out!",
                "SHOCKING: The truth about {topic} that THEY don't want you to know!",
                "This ONE WEIRD TRICK about {topic} changes EVERYTHING! 😱",
                "What happened next with {topic} will BLOW YOUR MIND! 🤯",
                "Doctors HATE this simple {topic} secret! Number 7 will shock you!"
            ],
            DisinformationType.FAKE_NEWS: [
                "🚨 BREAKING: {topic} confirmed by anonymous sources!",
                "URGENT: {topic} happening RIGHT NOW - Share before deleted!",
                "EXCLUSIVE: The real truth about {topic} finally revealed!",
                "CONFIRMED: {topic} - mainstream media silent!",
                "ALERT: {topic} - government cover-up exposed!"
            ],
            DisinformationType.CONSPIRACY: [
                "Wake up sheeple! {topic} is all connected to the bigger plan...",
                "They don't want you to know the truth about {topic}! Do your own research!",
                "The mainstream media won't tell you about {topic}... ask yourself WHY!",
                "Connect the dots: {topic} is just the beginning. Open your eyes! 👁️",
                "If you still believe the official story about {topic}, you're asleep!"
            ],
            DisinformationType.EMOTIONAL_MANIPULATION: [
                "This will make you CRY! {topic} is destroying our children! 😭",
                "I'm FURIOUS about {topic} and you should be too! Share if you agree! 😡",
                "HEARTBREAKING: {topic} - this is what they've done to us!",
                "You won't believe how {topic} is RUINING everything we love!",
                "This makes me SO ANGRY! {topic} must be stopped NOW!"
            ],
            DisinformationType.MISLEADING_STATISTICS: [
                "STUDY SHOWS: 87% of people affected by {topic}! (They won't tell you this)",
                "The numbers don't lie: {topic} increased by 300%! Coincidence? I think not!",
                "FACT: {topic} causes 95% of problems - the data is clear!",
                "Statistics prove {topic} is the real issue - wake up!",
                "Research confirms: {topic} linked to everything! Share the truth!"
            ],
            DisinformationType.HEALTH_MISINFO: [
                "My aunt cured her {topic} with this natural remedy! Doctors don't want you to know!",
                "NATURAL CURE for {topic} - Big Pharma is hiding this from you!",
                "I reversed my {topic} in 3 days with this ONE simple trick!",
                "Stop taking medication for {topic}! Try this instead! 🌿",
                "The TRUTH about {topic} that medical industry doesn't want revealed!"
            ],
            DisinformationType.POLITICAL_MISINFO: [
                "LEAKED: What [politician] really said about {topic}! Media hiding this!",
                "Both sides are the same on {topic} - don't be fooled!",
                "The REAL agenda behind {topic} - follow the money!",
                "[Party] caught lying about {topic} AGAIN! When will people wake up?",
                "What they're not telling you about {topic} - the hidden truth!"
            ]
        }
        
        # Author name templates
        self.author_templates = [
            "TruthSeeker{num}",
            "WokePatriot{num}",
            "RealNews{num}",
            "FreedomFighter{num}",
            "AwakeningMind{num}",
            "QuestionEverything{num}",
            "RedPilled{num}",
            "InfoWarrior{num}"
        ]
        
        # Comment viewpoint templates
        self.comment_viewpoints = {
            "believer": [
                "This is SO true! I've been saying this for years!",
                "Finally someone speaking the TRUTH! Share this everywhere!",
                "Thank you for posting this! People need to wake up!",
                "I knew it! This confirms everything I suspected!",
                "Everyone needs to see this! The truth is coming out!"
            ],
            "skeptic": [
                "Do you have any credible sources for this claim?",
                "This seems misleading. Can you provide more context?",
                "I checked and this appears to be false. Here's why...",
                "Be careful sharing this - it's been debunked multiple times.",
                "This is taken out of context. The full story is different."
            ],
            "questioning": [
                "Interesting... but where did this information come from?",
                "I'm not sure about this. Has anyone verified it?",
                "This sounds extreme. Is there more to the story?",
                "Can someone explain this more clearly?",
                "I want to believe this but need more evidence."
            ],
            "amplifier": [
                "EVERYONE SHARE THIS NOW!!!",
                "This needs to go VIRAL! 🔥",
                "Repost before they delete it!",
                "Tag everyone you know! They need to see this!",
                "Don't let them silence this! SHARE!"
            ],
            "concerned": [
                "This is really worrying if true...",
                "I'm concerned about the implications of this.",
                "We should be careful about jumping to conclusions.",
                "This is serious. We need to verify this carefully.",
                "I hope this isn't true, but we should investigate."
            ]
        }

    def generate_post(
        self,
        topic: str,
        disinfo_type: DisinformationType,
        include_red_flags: bool = True
    ) -> SocialMediaPost:
        """
        Generate a social media post with disinformation patterns.
        
        Args:
            topic: Topic for the post
            disinfo_type: Type of disinformation pattern
            include_red_flags: Whether to include educational markers
            
        Returns:
            Generated social media post with educational markers
        """
        # Select random template
        templates = self.post_templates.get(disinfo_type, self.post_templates[DisinformationType.CLICKBAIT])
        content = random.choice(templates).format(topic=topic)
        
        # Generate author
        author = random.choice(self.author_templates).format(num=random.randint(100, 9999))
        
        # Generate engagement metrics (higher for disinformation)
        engagement = {
            "likes": random.randint(500, 50000),
            "shares": random.randint(200, 20000),
            "comments": random.randint(50, 5000)
        }
        
        # Generate red flags
        red_flags = []
        if include_red_flags:
            patterns = self.red_flag_patterns.get(disinfo_type, [])
            for pattern in patterns[:2]:  # Include top 2 red flags
                red_flag = RedFlag(
                    flag_type=pattern["type"],
                    description=pattern["desc"],
                    location="post_content",
                    educational_note=pattern["note"]
                )
                red_flags.append(red_flag)
        
        # Generate educational notes
        educational_notes = [
            "⚠️ SIMULATION: This is educational content demonstrating disinformation patterns",
            f"This post demonstrates {disinfo_type.value} tactics commonly used in disinformation",
            "Practice identifying red flags before engaging with or sharing content"
        ]
        
        return SocialMediaPost(
            content=content,
            author=author,
            platform="SimulatedSocial",
            engagement=engagement,
            red_flags=red_flags,
            educational_notes=educational_notes,
            is_simulation=True
        )

    def generate_comment_thread(
        self,
        post: SocialMediaPost,
        num_comments: int = 5,
        include_red_flags: bool = True
    ) -> CommentThread:
        """
        Generate a comment thread with diverse viewpoints.
        
        Args:
            post: Original post to comment on
            num_comments: Number of comments to generate
            include_red_flags: Whether to include educational markers
            
        Returns:
            Comment thread with diverse viewpoints
        """
        comments = []
        
        # Distribute viewpoints
        viewpoint_types = list(self.comment_viewpoints.keys())
        
        for i in range(num_comments):
            # Select viewpoint (weighted towards believer/amplifier for realism)
            weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # believer, skeptic, questioning, amplifier, concerned
            viewpoint = random.choices(viewpoint_types, weights=weights)[0]
            
            # Generate comment content
            content = random.choice(self.comment_viewpoints[viewpoint])
            
            # Generate author
            author = f"User{random.randint(1000, 9999)}"
            
            # Generate engagement
            engagement = {
                "likes": random.randint(0, 500),
                "replies": random.randint(0, 50)
            }
            
            comment = Comment(
                author=author,
                content=content,
                viewpoint=viewpoint,
                engagement=engagement
            )
            comments.append(comment)
        
        # Generate thread-level red flags
        thread_red_flags = []
        if include_red_flags:
            thread_red_flags.append(
                RedFlag(
                    flag_type="echo_chamber",
                    description="Notice how most comments agree without questioning",
                    location="comment_thread",
                    educational_note="Echo chambers amplify misinformation by suppressing critical voices"
                )
            )
            thread_red_flags.append(
                RedFlag(
                    flag_type="social_proof",
                    description="High engagement creates false legitimacy",
                    location="engagement_metrics",
                    educational_note="Popularity doesn't equal accuracy - verify independently"
                )
            )
        
        # Educational notes for thread
        educational_notes = [
            "Notice the diversity (or lack thereof) in viewpoints",
            "Observe how skeptical comments are often drowned out",
            "Pay attention to which comments get the most engagement",
            "Consider how algorithms might amplify certain viewpoints"
        ]
        
        return CommentThread(
            original_post=post,
            comments=comments,
            red_flags=thread_red_flags,
            educational_notes=educational_notes
        )

    def generate_content(
        self,
        content_type: ContentType,
        topic: str,
        disinfo_type: DisinformationType,
        include_red_flags: bool = True,
        num_comments: int = 5
    ) -> Dict[str, Any]:
        """
        Generate social media content based on type.
        
        Args:
            content_type: Type of content to generate
            topic: Topic for the content
            disinfo_type: Type of disinformation pattern
            include_red_flags: Whether to include educational markers
            num_comments: Number of comments for threads
            
        Returns:
            Generated content as dictionary
        """
        if content_type == ContentType.POST:
            post = self.generate_post(topic, disinfo_type, include_red_flags)
            return post.model_dump()
        
        elif content_type == ContentType.THREAD:
            post = self.generate_post(topic, disinfo_type, include_red_flags)
            thread = self.generate_comment_thread(post, num_comments, include_red_flags)
            return thread.model_dump()
        
        elif content_type == ContentType.COMMENT:
            # Generate a single comment
            viewpoint = random.choice(list(self.comment_viewpoints.keys()))
            content = random.choice(self.comment_viewpoints[viewpoint])
            comment = Comment(
                author=f"User{random.randint(1000, 9999)}",
                content=content,
                viewpoint=viewpoint,
                engagement={"likes": random.randint(0, 100), "replies": random.randint(0, 10)}
            )
            return comment.model_dump()
        
        return {}


class ContentGeneratorTool(BaseTool):
    """
    CrewAI tool for generating social media content with disinformation patterns.
    
    Used by agents to create realistic social media simulations for
    educational purposes.
    """
    
    name: str = "content_generator"
    description: str = (
        "Generates realistic social media posts, comments, and threads with "
        "disinformation patterns for educational simulation. Includes red flags "
        "and educational markers."
    )
    args_schema: type[BaseModel] = ContentGeneratorInput
    generator: ContentGenerator = ContentGenerator()
    
    def __init__(self):
        """Initialize content generator tool."""
        super().__init__()
    
    def _run(
        self,
        content_type: ContentType,
        topic: str,
        disinfo_type: DisinformationType,
        include_red_flags: bool = True,
        num_comments: int = 5
    ) -> str:
        """
        Generate content (synchronous).
        
        Args:
            content_type: Type of content to generate
            topic: Topic for the content
            disinfo_type: Type of disinformation pattern
            include_red_flags: Whether to include educational markers
            num_comments: Number of comments for threads
            
        Returns:
            Generated content as formatted string
        """
        content = self.generator.generate_content(
            content_type, topic, disinfo_type, include_red_flags, num_comments
        )
        
        # Format output
        import json
        return json.dumps(content, indent=2)
    
    async def _arun(
        self,
        content_type: ContentType,
        topic: str,
        disinfo_type: DisinformationType,
        include_red_flags: bool = True,
        num_comments: int = 5
    ) -> Dict[str, Any]:
        """
        Generate content (asynchronous).
        
        Args:
            content_type: Type of content to generate
            topic: Topic for the content
            disinfo_type: Type of disinformation pattern
            include_red_flags: Whether to include educational markers
            num_comments: Number of comments for threads
            
        Returns:
            Generated content as dictionary
        """
        return self.generator.generate_content(
            content_type, topic, disinfo_type, include_red_flags, num_comments
        )


# Global instance
content_generator_tool = ContentGeneratorTool()
