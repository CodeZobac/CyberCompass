"""
Agent Factory for loading and creating CrewAI agents from YAML configuration.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from crewai import Agent, LLM
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory

from ..tools import (
    DeepfakeAnalysisTool,
    MediaProcessingTool,
    ContentGeneratorTool,
    DisinformationPatternTool,
    EngagementAnalysisTool,
    ProfileInconsistencyTool,
    TypingDelayTool,
    RedFlagGeneratorTool,
    CharacterConsistencyTool,
    ProgressAnalysisTool,
    CompetencyScoringTool,
    RecommendationEngineTool,
    ConversationStateTool,
)


class AgentFactory:
    """Factory class for creating and managing CrewAI agents from configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the agent factory.
        
        Args:
            config_path: Path to the agents.yaml configuration file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "agents.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.agents: Dict[str, Agent] = {}
        self.llm_instances: Dict[str, LLM] = {}
        self.tool_registry = self._initialize_tool_registry()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load agent configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Agent configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing agent configuration: {e}")
    
    def _initialize_tool_registry(self) -> Dict[str, Any]:
        """Initialize registry of available tools."""
        return {
            "DeepfakeAnalysisTool": DeepfakeAnalysisTool,
            "MediaProcessingTool": MediaProcessingTool,
            "ContentGeneratorTool": ContentGeneratorTool,
            "DisinformationPatternTool": DisinformationPatternTool,
            "EngagementAnalysisTool": EngagementAnalysisTool,
            "ProfileInconsistencyTool": ProfileInconsistencyTool,
            "TypingDelayTool": TypingDelayTool,
            "RedFlagGeneratorTool": RedFlagGeneratorTool,
            "CharacterConsistencyTool": CharacterConsistencyTool,
            "ProgressAnalysisTool": ProgressAnalysisTool,
            "CompetencyScoringTool": CompetencyScoringTool,
            "RecommendationEngineTool": RecommendationEngineTool,
            "ConversationStateTool": ConversationStateTool,
        }
    
    def _get_or_create_llm(self, llm_name: str) -> LLM:
        """Get or create an LLM instance based on configuration."""
        if llm_name in self.llm_instances:
            return self.llm_instances[llm_name]
        
        llm_config = self.config.get("llm_configs", {}).get(llm_name, {})
        
        llm = LLM(
            model=llm_config.get("model", llm_name),
            temperature=llm_config.get("temperature", 0.7),
            max_tokens=llm_config.get("max_tokens", 2000),
            top_p=llm_config.get("top_p", 0.9),
        )
        
        self.llm_instances[llm_name] = llm
        return llm
    
    def _create_tools(self, tool_names: List[str]) -> List[Any]:
        """Create tool instances from tool names."""
        tools = []
        for tool_name in tool_names:
            if tool_name in self.tool_registry:
                tool_class = self.tool_registry[tool_name]
                tools.append(tool_class())
            else:
                print(f"Warning: Tool '{tool_name}' not found in registry")
        return tools
    
    def create_agent(self, agent_name: str, locale: str = "en") -> Agent:
        """
        Create a single agent from configuration.
        
        Args:
            agent_name: Name of the agent to create (e.g., 'ethics_mentor')
            locale: Language locale for the agent ('en' or 'pt')
            
        Returns:
            Configured CrewAI Agent instance
        """
        agent_config = self.config.get("agents", {}).get(agent_name)
        
        if not agent_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")
        
        # Check if agent supports the requested locale
        supported_languages = agent_config.get("languages", ["en"])
        if locale not in supported_languages:
            print(f"Warning: Agent '{agent_name}' does not support locale '{locale}', using 'en'")
            locale = "en"
        
        # Get or create LLM instance
        llm = self._get_or_create_llm(agent_config.get("llm", "gpt-4"))
        
        # Create tools
        tool_names = agent_config.get("tools", [])
        tools = self._create_tools(tool_names)
        
        # Adapt backstory for locale if needed
        backstory = agent_config.get("backstory", "")
        if locale == "pt":
            backstory = f"{backstory}\n\nI communicate in Portuguese and provide culturally relevant examples for Portuguese-speaking learners."
        
        # Create agent
        agent = Agent(
            role=agent_config.get("role"),
            goal=agent_config.get("goal"),
            backstory=backstory,
            llm=llm,
            tools=tools,
            memory=agent_config.get("memory", True),
            verbose=agent_config.get("verbose", True),
            allow_delegation=agent_config.get("allow_delegation", False),
            max_iter=agent_config.get("max_iter", 5),
        )
        
        return agent
    
    def create_all_agents(self, locale: str = "en") -> Dict[str, Agent]:
        """
        Create all agents defined in the configuration.
        
        Args:
            locale: Language locale for all agents ('en' or 'pt')
            
        Returns:
            Dictionary mapping agent names to Agent instances
        """
        agents = {}
        agent_configs = self.config.get("agents", {})
        
        for agent_name in agent_configs.keys():
            try:
                agents[agent_name] = self.create_agent(agent_name, locale)
                print(f"✓ Created agent: {agent_name}")
            except Exception as e:
                print(f"✗ Failed to create agent '{agent_name}': {e}")
        
        self.agents = agents
        return agents
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get a previously created agent by name."""
        return self.agents.get(agent_name)
    
    def reload_config(self):
        """Reload configuration from file and recreate agents."""
        self.config = self._load_config()
        self.agents.clear()
        self.llm_instances.clear()
        print("Configuration reloaded. Call create_all_agents() to recreate agents.")
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory configuration from config file."""
        return self.config.get("memory_config", {})
