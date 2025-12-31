"""
Example usage of CrewAI Flows for educational scenarios.

This module demonstrates how to use the three main flows:
1. DeepfakeDetectionFlow - For deepfake detection training
2. SocialMediaSimulationFlow - For disinformation detection training
3. CatfishDetectionFlow - For catfishing detection training
"""

import asyncio
from typing import Dict, Any

from .deepfake_detection_flow import DeepfakeDetectionFlow
from .social_media_simulation_flow import SocialMediaSimulationFlow
from .catfish_detection_flow import CatfishDetectionFlow
from ..agents.factory import AgentFactory
from ..models.requests import (
    DeepfakeChallengeRequest,
    DeepfakeSubmissionRequest,
    SocialMediaSimulationRequest,
    CatfishChatStartRequest,
    MediaType,
    DisinformationType,
    LocaleEnum,
)


class FlowExamples:
    """Examples demonstrating flow usage."""
    
    def __init__(self, agent_factory: AgentFactory):
        """
        Initialize flow examples.
        
        Args:
            agent_factory: Factory for creating agents
        """
        self.agent_factory = agent_factory
    
    def example_deepfake_detection_flow(self) -> Dict[str, Any]:
        """
        Example: Complete deepfake detection challenge workflow.
        
        Returns:
            Results from the flow execution
        """
        print("\n=== Deepfake Detection Flow Example ===\n")
        
        # Initialize the flow
        flow = DeepfakeDetectionFlow(self.agent_factory, locale="en")
        
        # Step 1: Initialize a challenge
        challenge_request = DeepfakeChallengeRequest(
            user_id="user_123",
            difficulty_level=2,
            media_type=MediaType.VIDEO,
            locale=LocaleEnum.EN,
        )
        
        print("1. Initializing deepfake challenge...")
        challenge_state = flow.initialize_challenge(challenge_request)
        print(f"   Challenge ID: {challenge_state['challenge']['challenge_id']}")
        print(f"   Media Type: {challenge_state['challenge']['media_type']}")
        print(f"   Difficulty: {challenge_state['challenge']['difficulty_level']}")
        
        # Step 2: Await user submission (simulated)
        print("\n2. Waiting for user submission...")
        await_state = flow.await_user_submission(challenge_state)
        print(f"   Ready for submission: {await_state['ready_for_submission']}")
        
        # Step 3: Process user submission
        print("\n3. Processing user submission...")
        submission = DeepfakeSubmissionRequest(
            challenge_id=challenge_state['challenge']['challenge_id'],
            user_id="user_123",
            is_deepfake=True,
            confidence=0.75,
            reasoning="I noticed unnatural facial movements and audio sync issues",
        )
        
        feedback_state = flow.process_submission(submission)
        print(f"   Correct: {feedback_state['feedback']['correct']}")
        print(f"   Score: {feedback_state['feedback']['score']}")
        print(f"   Feedback: {feedback_state['feedback']['feedback'][:100]}...")
        
        # Step 4: Determine next action
        print("\n4. Determining next action...")
        next_action = flow.determine_next_action(feedback_state)
        print(f"   Next action: {next_action}")
        
        return {
            "flow_type": "deepfake_detection",
            "challenge_state": challenge_state,
            "feedback_state": feedback_state,
            "next_action": next_action,
        }
    
    def example_social_media_simulation_flow(self) -> Dict[str, Any]:
        """
        Example: Social media disinformation simulation workflow.
        
        Returns:
            Results from the flow execution
        """
        print("\n=== Social Media Simulation Flow Example ===\n")
        
        # Initialize the flow
        flow = SocialMediaSimulationFlow(self.agent_factory, locale="en")
        
        # Step 1: Initialize simulation
        sim_request = SocialMediaSimulationRequest(
            user_id="user_123",
            session_duration_minutes=15,
            disinformation_ratio=0.3,
            categories=[
                DisinformationType.HEALTH,
                DisinformationType.POLITICS,
            ],
            locale=LocaleEnum.EN,
        )
        
        print("1. Initializing social media simulation...")
        init_state = flow.initialize_simulation(sim_request)
        print(f"   Session ID: {init_state['session_id']}")
        print(f"   Total posts: {init_state['total_posts']}")
        print(f"   Disinformation posts: {init_state['disinformation_count']}")
        
        # Step 2: Start tracking engagement
        print("\n2. Starting engagement tracking...")
        tracking_state = flow.track_user_engagement(init_state)
        print(f"   Tracking active: {tracking_state['tracking_active']}")
        
        # Step 3: Simulate user interactions
        print("\n3. Simulating user interactions...")
        
        # User likes a post (could be disinformation)
        post_id = init_state['feed'][0]['post_id']
        interaction1 = flow.record_interaction(
            session_id=init_state['session_id'],
            user_id="user_123",
            post_id=post_id,
            interaction_type="like",
        )
        print(f"   Interaction 1: {interaction1['interaction']['interaction_type']}")
        print(f"   Algorithm feedback: {interaction1['algorithm_feedback']['message'][:80]}...")
        
        # User reports a suspicious post
        post_id_2 = init_state['feed'][1]['post_id']
        interaction2 = flow.record_interaction(
            session_id=init_state['session_id'],
            user_id="user_123",
            post_id=post_id_2,
            interaction_type="report",
        )
        print(f"   Interaction 2: {interaction2['interaction']['interaction_type']}")
        
        # Step 4: Check session status
        print("\n4. Checking session status...")
        status = flow.check_session_status(tracking_state)
        print(f"   Session status: {status}")
        
        return {
            "flow_type": "social_media_simulation",
            "init_state": init_state,
            "tracking_state": tracking_state,
            "interactions": [interaction1, interaction2],
        }
    
    def example_catfish_detection_flow(self) -> Dict[str, Any]:
        """
        Example: Catfish detection chat simulation workflow.
        
        Returns:
            Results from the flow execution
        """
        print("\n=== Catfish Detection Flow Example ===\n")
        
        # Initialize the flow
        flow = CatfishDetectionFlow(self.agent_factory, locale="en")
        
        # Step 1: Initialize character
        chat_request = CatfishChatStartRequest(
            user_id="user_123",
            difficulty_level=2,
            character_age_range="13-17",
            locale=LocaleEnum.EN,
        )
        
        print("1. Initializing catfish character...")
        char_state = flow.initialize_character(chat_request)
        print(f"   Session ID: {char_state['session_id']}")
        print(f"   Character: {char_state['character_profile']['name']}")
        print(f"   Age: {char_state['character_profile']['age']}")
        print(f"   Red flags count: {char_state['red_flags_count']}")
        
        # Step 2: Start conversation
        print("\n2. Starting conversation...")
        conv_state = flow.start_conversation(char_state)
        print(f"   Opening message: {conv_state['opening_message']['content'][:80]}...")
        print(f"   Typing delay: {conv_state['opening_message']['typing_delay']:.2f}s")
        
        # Step 3: Manage conversation flow
        print("\n3. Managing conversation flow...")
        flow_state = flow.manage_conversation_flow(conv_state)
        print(f"   Status: {flow_state['status']}")
        print(f"   Awaiting user message: {flow_state['awaiting_user_message']}")
        
        # Step 4: Process user messages (simulated conversation)
        print("\n4. Processing user messages...")
        
        # User sends first message
        response1 = flow.process_user_message(
            session_id=char_state['session_id'],
            user_id="user_123",
            message_content="Hi! What school do you go to?",
        )
        print(f"   User asks about school")
        print(f"   Character response: {response1['response']['content'][:80]}...")
        print(f"   Typing delay: {response1['typing_delay']:.2f}s")
        
        # User sends probing question
        response2 = flow.process_user_message(
            session_id=char_state['session_id'],
            user_id="user_123",
            message_content="Can we do a video call?",
        )
        print(f"\n   User asks for video call (probing question)")
        print(f"   Character response: {response2['response']['content'][:80]}...")
        print(f"   Red flags revealed: {response2['red_flags_revealed']}")
        
        # Step 5: Check conversation status
        print("\n5. Checking conversation status...")
        status = flow.check_conversation_status(flow_state)
        print(f"   Conversation status: {status}")
        
        return {
            "flow_type": "catfish_detection",
            "char_state": char_state,
            "conv_state": conv_state,
            "responses": [response1, response2],
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """
        Run all flow examples.
        
        Returns:
            Combined results from all examples
        """
        print("\n" + "="*60)
        print("Running All CrewAI Flow Examples")
        print("="*60)
        
        results = {}
        
        try:
            results["deepfake"] = self.example_deepfake_detection_flow()
        except Exception as e:
            print(f"\nError in deepfake flow: {e}")
            results["deepfake"] = {"error": str(e)}
        
        try:
            results["social_media"] = self.example_social_media_simulation_flow()
        except Exception as e:
            print(f"\nError in social media flow: {e}")
            results["social_media"] = {"error": str(e)}
        
        try:
            results["catfish"] = self.example_catfish_detection_flow()
        except Exception as e:
            print(f"\nError in catfish flow: {e}")
            results["catfish"] = {"error": str(e)}
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60 + "\n")
        
        return results


def main():
    """Main function to run examples."""
    # Initialize agent factory
    agent_factory = AgentFactory()
    
    # Create examples instance
    examples = FlowExamples(agent_factory)
    
    # Run all examples
    results = examples.run_all_examples()
    
    # Print summary
    print("\n=== Summary ===")
    for flow_type, result in results.items():
        if "error" in result:
            print(f"{flow_type}: ERROR - {result['error']}")
        else:
            print(f"{flow_type}: SUCCESS")


if __name__ == "__main__":
    main()
