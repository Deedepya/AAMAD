"""
CrewAI Integration Module
Provides clean interface for CrewAI agent orchestration
"""

from .crew_service import CrewAIService, DocumentProcessingResult
from .crew_config import CrewAIConfig

__all__ = ["CrewAIService", "CrewAIConfig", "DocumentProcessingResult"]

