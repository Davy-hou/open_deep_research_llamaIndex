# A package for AI research using LLM workflows

__version__ = '0.1.0'

# Export main functionality
from .workflows.research_workflow import ResearchWorkflow, ProgressEvent
from .workflows.search_workflow import SearchWorkflow
from .config.config import Config

# Make these classes and functions available when importing the package
__all__ = ['ResearchWorkflow', 'SearchWorkflow', 'Config', 'ProgressEvent']