import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management for the research workflow.
    
    This class provides a single source of truth for all configuration settings
    used throughout the application, including API keys, model parameters, and
    workflow settings.
    """
    
    def __init__(self):
        # LLM Configuration
        self.open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")
        self.open_router_model = os.getenv("OPEN_ROUTER_MODEL")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "48096"))
        self.context_window = int(os.getenv("CONTEXT_WINDOW", "1000000"))
        
        # Search Configuration
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.search_depth = os.getenv("SEARCH_DEPTH", "advanced")
        self.max_search_results = int(os.getenv("MAX_SEARCH_RESULTS", "1"))
        self.max_queries_per_section = int(os.getenv("MAX_QUERIES_PER_SECTION", "3"))
        
        # Workflow Configuration
        self.workflow_timeout = int(os.getenv("WORKFLOW_TIMEOUT", "300"))
        self.search_workflow_timeout = int(os.getenv("SEARCH_WORKFLOW_TIMEOUT", "60"))
        self.verbose = os.getenv("VERBOSE", "True").lower() == "true"
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration parameters."""
        return {
            "api_key": self.open_router_api_key,
            "model": self.open_router_model,
            "max_tokens": self.max_tokens,
            "context_window": self.context_window
        }
    
    def get_search_config(self) -> Dict[str, Any]:
        """Get search configuration parameters."""
        return {
            "api_key": self.tavily_api_key,
            "search_depth": self.search_depth,
            "max_results": self.max_search_results,
            "max_queries": self.max_queries_per_section
        }
    
    def get_workflow_config(self) -> Dict[str, Any]:
        """Get workflow configuration parameters."""
        return {
            "timeout": self.workflow_timeout,
            "search_timeout": self.search_workflow_timeout,
            "verbose": self.verbose
        }