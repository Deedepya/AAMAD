"""
CrewAI Configuration Loader
Loads agent and task configurations from YAML files and creates CrewAI crew
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from .tools.tool_registry import get_tools_registry

logger = logging.getLogger(__name__)


class CrewAIConfig:
    """Loads and manages CrewAI configuration from YAML files"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize CrewAI configuration loader
        
        Args:
            config_dir: Directory containing agents.yaml and tasks.yaml
                       Defaults to backend/config/
        """
        if config_dir is None:
            # Default to backend/config/ relative to this file
            base_dir = Path(__file__).parent.parent
            config_dir = str(base_dir / "config")
        
        self.config_dir = config_dir
        self.agents_config = None
        self.tasks_config = None
        self.tools_registry = get_tools_registry()
    
    def load_agents(self) -> List[Dict[str, Any]]:
        """Load agent configurations from agents.yaml"""
        agents_file = os.path.join(self.config_dir, "agents.yaml")
        
        if not os.path.exists(agents_file):
            raise FileNotFoundError(f"Agents config file not found: {agents_file}")
        
        with open(agents_file, 'r') as f:
            config = yaml.safe_load(f)
        
        self.agents_config = config.get("agents", [])
        logger.info(f"Loaded {len(self.agents_config)} agents from config")
        return self.agents_config
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load task configurations from tasks.yaml"""
        tasks_file = os.path.join(self.config_dir, "tasks.yaml")
        
        if not os.path.exists(tasks_file):
            raise FileNotFoundError(f"Tasks config file not found: {tasks_file}")
        
        with open(tasks_file, 'r') as f:
            config = yaml.safe_load(f)
        
        self.tasks_config = config.get("tasks", [])
        logger.info(f"Loaded {len(self.tasks_config)} tasks from config")
        return self.tasks_config
    
    def _create_llm(self, llm_config: Dict[str, str]) -> ChatOpenAI:
        """Create LLM instance from configuration"""
        provider = llm_config.get("provider", "openai")
        model = llm_config.get("model", "gpt-4o-mini")
        
        # Map provider to LLM class
        if provider == "openai":
            return ChatOpenAI(model=model, temperature=0.4)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _get_agent_tools(self, tool_names: List[str]) -> List:
        """Get tool instances by name"""
        tools = []
        for tool_name in tool_names:
            if tool_name in self.tools_registry:
                tools.append(self.tools_registry[tool_name])
            else:
                logger.warning(f"Tool '{tool_name}' not found in registry, skipping")
        return tools
    
    def create_agents(self) -> List[Agent]:
        """Create CrewAI Agent instances from configuration"""
        if not self.agents_config:
            self.load_agents()
        
        agents = []
        # Store agent_id to agent mapping for task assignment
        self._agent_map = {}
        
        for agent_config in self.agents_config:
            agent_id = agent_config.get("id")
            role = agent_config.get("role")
            goal = agent_config.get("goal")
            backstory = agent_config.get("backstory", "")
            
            # LLM configuration
            llm_config = agent_config.get("llm", {})
            llm = self._create_llm(llm_config)
            
            # Tools
            tool_names = agent_config.get("tools", [])
            tools = self._get_agent_tools(tool_names)
            
            # Agent parameters
            allow_delegation = agent_config.get("allow_delegation", False)
            verbose = agent_config.get("verbose", False)
            max_iter = agent_config.get("max_iter", 12)
            max_execution_time = agent_config.get("max_execution_time", 300)
            respect_context_window = agent_config.get("respect_context_window", True)
            max_retry_limit = agent_config.get("max_retry_limit", 2)
            memory = agent_config.get("memory", False)
            
            agent = Agent(
                role=role,
                goal=goal,
                backstory=backstory,
                llm=llm,
                tools=tools,
                allow_delegation=allow_delegation,
                verbose=verbose,
                max_iter=max_iter,
                max_execution_time=max_execution_time,
                respect_context_window=respect_context_window,
                max_retry_limit=max_retry_limit,
                memory=memory
            )
            
            agents.append(agent)
            # Store mapping for task assignment
            self._agent_map[agent_id] = agent
            logger.info(f"Created agent: {agent_id} ({role})")
        
        return agents
    
    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Create CrewAI Task instances from configuration"""
        if not self.tasks_config:
            self.load_tasks()
        
        # Use agent map created during agent creation
        if not hasattr(self, '_agent_map') or not self._agent_map:
            # Fallback: create map from agents list
            if not self.agents_config:
                self.load_agents()
            self._agent_map = {}
            for agent_config in self.agents_config:
                agent_id = agent_config.get("id")
                role = agent_config.get("role")
                # Find matching agent by role
                for agent in agents:
                    if agent.role == role:
                        self._agent_map[agent_id] = agent
                        break
        
        tasks = []
        for task_config in self.tasks_config:
            task_id = task_config.get("id")
            description = task_config.get("description", "")
            expected_output = task_config.get("expected_output", "")
            agent_id = task_config.get("agent_id")
            
            # Find agent by agent_id
            agent = self._agent_map.get(agent_id)
            
            if not agent:
                logger.warning(f"Could not find agent {agent_id} for task {task_id}, skipping")
                continue
            
            task = Task(
                description=description,
                expected_output=expected_output,
                agent=agent
            )
            
            tasks.append(task)
            logger.info(f"Created task: {task_id} for agent {agent.role}")
        
        return tasks
    
    def create_crew(self) -> Crew:
        """Create CrewAI Crew instance with all agents and tasks"""
        agents = self.create_agents()
        tasks = self.create_tasks(agents)
        
        if not agents:
            raise ValueError("No agents created from configuration")
        if not tasks:
            raise ValueError("No tasks created from configuration")
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        
        logger.info(f"Created crew with {len(agents)} agents and {len(tasks)} tasks")
        return crew

