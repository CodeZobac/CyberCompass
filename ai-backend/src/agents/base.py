"""
Base agent classes with CrewAI Memory system integration and reasoning capabilities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from crewai import Agent
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory


class BaseAgentMemory:
    """
    Base memory management for agents with CrewAI Memory system integration.
    Provides context preservation and conversation history management.
    """
    
    def __init__(self):
        """Initialize memory systems."""
        self.long_term_memory = LongTermMemory()
        self.short_term_memory = ShortTermMemory()
        self.entity_memory = EntityMemory()
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_context: Dict[str, Any] = {}
        
    def add_to_conversation_history(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add a message to conversation history.
        
        Args:
            role: Role of the speaker ('user', 'agent', 'system')
            content: Message content
            metadata: Additional metadata about the message
        """
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self.conversation_history.append(entry)
        
        # Update short-term memory
        self.short_term_memory.save(entry)
    
    def get_conversation_context(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for context.
        
        Args:
            last_n: Number of recent messages to retrieve (None for all)
            
        Returns:
            List of conversation messages
        """
        if last_n is None:
            return self.conversation_history
        return self.conversation_history[-last_n:]
    
    def update_user_context(self, context: Dict[str, Any]):
        """
        Update user context information.
        
        Args:
            context: Dictionary containing user context data
        """
        self.user_context.update(context)
        
        # Store in entity memory for long-term tracking
        for key, value in context.items():
            self.entity_memory.save(key, value)
    
    def get_user_context(self) -> Dict[str, Any]:
        """Get current user context."""
        return self.user_context
    
    def clear_short_term_memory(self):
        """Clear short-term memory (e.g., at end of session)."""
        self.short_term_memory.reset()
        self.conversation_history.clear()
    
    def store_long_term_insight(self, key: str, value: Any):
        """
        Store an insight in long-term memory.
        
        Args:
            key: Identifier for the insight
            value: The insight data
        """
        self.long_term_memory.save({key: value})


class ReasoningEngine:
    """
    Reasoning capabilities for complex decision making.
    Provides structured thinking and decision analysis.
    """
    
    def __init__(self):
        """Initialize reasoning engine."""
        self.reasoning_history: List[Dict[str, Any]] = []
    
    def analyze_situation(
        self,
        context: Dict[str, Any],
        goals: List[str],
        constraints: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a situation and provide reasoning.
        
        Args:
            context: Current situation context
            goals: List of goals to achieve
            constraints: Optional constraints to consider
            
        Returns:
            Analysis results with reasoning steps
        """
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "goals": goals,
            "constraints": constraints or [],
            "reasoning_steps": [],
            "conclusion": None
        }
        
        # Step 1: Identify key factors
        key_factors = self._identify_key_factors(context)
        analysis["reasoning_steps"].append({
            "step": "identify_factors",
            "result": key_factors
        })
        
        # Step 2: Evaluate options
        options = self._evaluate_options(context, goals, constraints)
        analysis["reasoning_steps"].append({
            "step": "evaluate_options",
            "result": options
        })
        
        # Step 3: Make recommendation
        recommendation = self._make_recommendation(options, goals)
        analysis["reasoning_steps"].append({
            "step": "recommendation",
            "result": recommendation
        })
        
        analysis["conclusion"] = recommendation
        self.reasoning_history.append(analysis)
        
        return analysis
    
    def _identify_key_factors(self, context: Dict[str, Any]) -> List[str]:
        """Identify key factors from context."""
        # Extract important elements from context
        factors = []
        
        if "user_history" in context:
            factors.append("user_learning_history")
        
        if "difficulty_level" in context:
            factors.append("current_difficulty_level")
        
        if "previous_performance" in context:
            factors.append("performance_trends")
        
        return factors
    
    def _evaluate_options(
        self,
        context: Dict[str, Any],
        goals: List[str],
        constraints: Optional[List[str]]
    ) -> List[Dict[str, Any]]:
        """Evaluate available options."""
        # This is a simplified version - actual implementation would be more sophisticated
        options = []
        
        for goal in goals:
            option = {
                "goal": goal,
                "feasibility": "high",
                "alignment_with_context": self._check_alignment(goal, context),
                "constraint_violations": self._check_constraints(goal, constraints or [])
            }
            options.append(option)
        
        return options
    
    def _check_alignment(self, goal: str, context: Dict[str, Any]) -> str:
        """Check how well a goal aligns with context."""
        # Simplified alignment check
        return "aligned"
    
    def _check_constraints(self, goal: str, constraints: List[str]) -> List[str]:
        """Check if goal violates any constraints."""
        # Simplified constraint checking
        return []
    
    def _make_recommendation(
        self,
        options: List[Dict[str, Any]],
        goals: List[str]
    ) -> Dict[str, Any]:
        """Make a recommendation based on evaluated options."""
        # Select best option (simplified)
        if options:
            best_option = options[0]
            return {
                "recommended_action": best_option["goal"],
                "rationale": "Best alignment with goals and context",
                "confidence": 0.85
            }
        
        return {
            "recommended_action": "gather_more_information",
            "rationale": "Insufficient information to make recommendation",
            "confidence": 0.5
        }
    
    def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Get history of reasoning processes."""
        return self.reasoning_history


class PlanningSystem:
    """
    Strategic planning system for task execution.
    Breaks down complex tasks into manageable steps.
    """
    
    def __init__(self):
        """Initialize planning system."""
        self.active_plans: Dict[str, Dict[str, Any]] = {}
    
    def create_plan(
        self,
        task_id: str,
        objective: str,
        context: Dict[str, Any],
        constraints: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a strategic plan for achieving an objective.
        
        Args:
            task_id: Unique identifier for the task
            objective: The goal to achieve
            context: Current context and available resources
            constraints: Optional constraints on the plan
            
        Returns:
            Structured plan with steps and milestones
        """
        plan = {
            "task_id": task_id,
            "objective": objective,
            "created_at": datetime.utcnow().isoformat(),
            "context": context,
            "constraints": constraints or [],
            "steps": [],
            "milestones": [],
            "status": "created"
        }
        
        # Generate plan steps
        steps = self._generate_steps(objective, context)
        plan["steps"] = steps
        
        # Identify milestones
        milestones = self._identify_milestones(steps)
        plan["milestones"] = milestones
        
        self.active_plans[task_id] = plan
        return plan
    
    def _generate_steps(
        self,
        objective: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate execution steps for the objective."""
        # This is a template - actual implementation would use AI reasoning
        steps = [
            {
                "step_number": 1,
                "action": "analyze_requirements",
                "description": "Understand what needs to be achieved",
                "status": "pending"
            },
            {
                "step_number": 2,
                "action": "gather_resources",
                "description": "Collect necessary information and tools",
                "status": "pending"
            },
            {
                "step_number": 3,
                "action": "execute_main_task",
                "description": f"Work towards: {objective}",
                "status": "pending"
            },
            {
                "step_number": 4,
                "action": "validate_results",
                "description": "Verify the objective has been achieved",
                "status": "pending"
            }
        ]
        return steps
    
    def _identify_milestones(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify key milestones in the plan."""
        milestones = []
        
        # Create milestone for every 2-3 steps
        for i, step in enumerate(steps):
            if i % 2 == 0 or i == len(steps) - 1:
                milestones.append({
                    "milestone_id": f"milestone_{i}",
                    "step_number": step["step_number"],
                    "description": f"Complete {step['action']}",
                    "achieved": False
                })
        
        return milestones
    
    def update_step_status(self, task_id: str, step_number: int, status: str):
        """
        Update the status of a plan step.
        
        Args:
            task_id: Task identifier
            step_number: Step number to update
            status: New status ('pending', 'in_progress', 'completed', 'failed')
        """
        if task_id in self.active_plans:
            plan = self.active_plans[task_id]
            for step in plan["steps"]:
                if step["step_number"] == step_number:
                    step["status"] = status
                    break
    
    def get_plan(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a plan by task ID."""
        return self.active_plans.get(task_id)
    
    def get_next_step(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the next pending step in a plan."""
        plan = self.active_plans.get(task_id)
        if plan:
            for step in plan["steps"]:
                if step["status"] == "pending":
                    return step
        return None


class BaseEducationalAgent:
    """
    Base class for educational agents with memory, reasoning, and planning.
    Extends CrewAI Agent with educational-specific capabilities.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize base educational agent.
        
        Args:
            agent: CrewAI Agent instance
        """
        self.agent = agent
        self.memory = BaseAgentMemory()
        self.reasoning = ReasoningEngine()
        self.planning = PlanningSystem()
        self.locale = "en"
    
    def set_locale(self, locale: str):
        """
        Set the language locale for the agent.
        
        Args:
            locale: Language code ('en' or 'pt')
        """
        self.locale = locale
    
    def process_with_context(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process user input with full context awareness.
        
        Args:
            user_input: User's input message
            context: Additional context information
            
        Returns:
            Agent's response
        """
        # Update context
        if context:
            self.memory.update_user_context(context)
        
        # Add to conversation history
        self.memory.add_to_conversation_history("user", user_input)
        
        # Get conversation context for agent
        conversation_context = self.memory.get_conversation_context(last_n=10)
        
        # Process with agent (this would call the actual CrewAI agent)
        # For now, this is a placeholder
        response = f"Processing: {user_input}"
        
        # Add response to history
        self.memory.add_to_conversation_history("agent", response)
        
        return response
    
    def reason_about_situation(
        self,
        situation: Dict[str, Any],
        goals: List[str]
    ) -> Dict[str, Any]:
        """
        Use reasoning engine to analyze a situation.
        
        Args:
            situation: Current situation context
            goals: Goals to achieve
            
        Returns:
            Reasoning analysis
        """
        return self.reasoning.analyze_situation(
            context=situation,
            goals=goals,
            constraints=None
        )
    
    def create_learning_plan(
        self,
        objective: str,
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a learning plan for the user.
        
        Args:
            objective: Learning objective
            user_context: User's current context and history
            
        Returns:
            Structured learning plan
        """
        task_id = f"learning_plan_{datetime.utcnow().timestamp()}"
        return self.planning.create_plan(
            task_id=task_id,
            objective=objective,
            context=user_context
        )
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's memory state."""
        return {
            "conversation_length": len(self.memory.conversation_history),
            "user_context": self.memory.user_context,
            "reasoning_history_length": len(self.reasoning.reasoning_history),
            "active_plans": len(self.planning.active_plans)
        }
