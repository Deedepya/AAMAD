# CrewAI Crew Configuration
# Loads agents and tasks from YAML and initializes the crew

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import logging

from crew.tools import TOOLS_REGISTRY

logger = logging.getLogger(__name__)


class CrewConfig:
    """Manages CrewAI crew configuration and initialization"""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize crew configuration.
        
        Args:
            config_dir: Directory containing agents.yaml and tasks.yaml
        """
        if config_dir is None:
            # Default to backend/config directory
            config_dir = Path(__file__).parent.parent / "config"
        
        self.config_dir = Path(config_dir)
        self.agents_config_path = self.config_dir / "agents.yaml"
        self.tasks_config_path = self.config_dir / "tasks.yaml"
        
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []
        self.crew: Crew = None
        
    def load_agents(self) -> Dict[str, Agent]:
        """
        Load agents from YAML configuration.
        
        Returns:
            Dictionary of agent_id -> Agent
        """
        if not self.agents_config_path.exists():
            raise FileNotFoundError(f"Agents config not found: {self.agents_config_path}")
        
        with open(self.agents_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        agents_config = config.get("agents", [])
        
        for agent_config in agents_config:
            agent_id = agent_config.get("id")
            if not agent_id:
                logger.warning("Agent missing 'id' field, skipping")
                continue
            
            # Get LLM configuration
            llm_config = agent_config.get("llm", {})
            llm_provider = llm_config.get("provider", "openai")
            llm_model = llm_config.get("model", "gpt-4")
            
            # Create LLM instance based on provider
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=llm_model, temperature=0.3)
            
            # Get tools for this agent
            tool_names = agent_config.get("tools", [])
            tools = []
            for tool_name in tool_names:
                if tool_name in TOOLS_REGISTRY:
                    tools.append(TOOLS_REGISTRY[tool_name])
                else:
                    logger.warning(f"Tool '{tool_name}' not found in registry for agent '{agent_id}'")
            
            # Create agent
            agent = Agent(
                role=agent_config.get("role", ""),
                goal=agent_config.get("goal", ""),
                backstory=agent_config.get("backstory", ""),
                llm=llm,
                allow_delegation=agent_config.get("allow_delegation", False),
                verbose=agent_config.get("verbose", False),
                max_iter=agent_config.get("max_iter", 12),
                max_execution_time=agent_config.get("max_execution_time", 300),
                tools=tools if tools else None,
                memory=agent_config.get("memory", False),
                max_retry_limit=agent_config.get("max_retry_limit", 2),
            )
            
            self.agents[agent_id] = agent
            logger.info(f"Loaded agent: {agent_id} ({agent_config.get('role')})")
        
        return self.agents
    
    def load_tasks(self) -> List[Task]:
        """
        Load tasks from YAML configuration.
        
        Returns:
            List of Task objects
        """
        if not self.tasks_config_path.exists():
            raise FileNotFoundError(f"Tasks config not found: {self.tasks_config_path}")
        
        with open(self.tasks_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        tasks_config = config.get("tasks", [])
        
        for task_config in tasks_config:
            task_id = task_config.get("id")
            agent_id = task_config.get("agent_id")
            
            if not task_id or not agent_id:
                logger.warning("Task missing 'id' or 'agent_id', skipping")
                continue
            
            if agent_id not in self.agents:
                logger.warning(f"Task '{task_id}' references unknown agent '{agent_id}', skipping")
                continue
            
            agent = self.agents[agent_id]
            
            # Create task
            task = Task(
                description=task_config.get("description", ""),
                agent=agent,
                expected_output=task_config.get("expected_output", ""),
                context=task_config.get("context", []),
                output_file=task_config.get("output_file"),
                human_input=task_config.get("human_input", False),
                async_execution=task_config.get("async_execution", False),
            )
            
            self.tasks.append(task)
            logger.info(f"Loaded task: {task_id} (assigned to {agent_id})")
        
        return self.tasks
    
    def create_crew(self, process: Process = Process.sequential) -> Crew:
        """
        Create CrewAI crew from loaded agents and tasks.
        
        Args:
            process: Process type (sequential, hierarchical, etc.)
            
        Returns:
            CrewAI Crew instance
        """
        if not self.agents:
            self.load_agents()
        
        if not self.tasks:
            self.load_tasks()
        
        if not self.agents or not self.tasks:
            raise ValueError("Cannot create crew: no agents or tasks loaded")
        
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            process=process,
            verbose=os.getenv("CREWAI_VERBOSE", "false").lower() == "true",
            max_rpm=int(os.getenv("MAX_RPM", "60")),
        )
        
        logger.info(f"Created crew with {len(self.agents)} agents and {len(self.tasks)} tasks")
        return self.crew
    
    def get_crew(self) -> Crew:
        """Get or create the crew"""
        if self.crew is None:
            self.create_crew()
        return self.crew


# Global crew instance (lazy initialization)
_crew_instance: CrewConfig = None


def get_crew_config() -> CrewConfig:
    """Get global crew configuration instance"""
    global _crew_instance
    if _crew_instance is None:
        _crew_instance = CrewConfig()
    return _crew_instance


def get_crew() -> Crew:
    """Get or create the crew"""
    return get_crew_config().get_crew()

