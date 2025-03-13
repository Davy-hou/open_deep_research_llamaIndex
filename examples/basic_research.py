import asyncio
from research.workflows.research_workflow import ResearchWorkflow, ProgressEvent
from research.workflows.search_workflow import SearchWorkflow
from research.config.config import Config
from llama_index.llms.openrouter import OpenRouter

async def run_research(topic: str, config=None):
    """Run the research workflow with the given topic.
    
    Args:
        topic: The research topic
        config: Optional configuration object
        
    Returns:
        The final research report
    """
    # Load configuration
    if config is None:
        config = Config()
    llm_config = config.get_llm_config()
    workflow_config = config.get_workflow_config()
    search_config = config.get_search_config()
    
    # Initialize main workflow
    workflow = ResearchWorkflow(
        llm=OpenRouter(
            api_key=llm_config["api_key"],
            model=llm_config["model"],
            max_tokens=llm_config["max_tokens"],
            context_window=llm_config["context_window"],
        ),
        verbose=workflow_config["verbose"]
    )

    # Initialize search workflow
    search_workflow = SearchWorkflow(
        llm=workflow.llm, 
        config=search_config,
        verbose=workflow._verbose
    )
    
    # Add search workflow to main workflow
    workflow.add_workflows(search_workflow=search_workflow)
    
    # Run workflow with topic
    handler = workflow.run(input=topic)
    
    # Return handler for further processing
    return handler

async def main():
    # Example usage
    topic = "AI policy"
    handler = await run_research(topic)
    
    # Process streaming events
    async for event in handler.stream_events():
        if isinstance(event, ProgressEvent):
            print(event.msg)
    
    # Get final result
    final_result = await handler
    print("final_result:", final_result)
    # draw_all_possible_flows(ResearchWorkflow, filename="workflow.html")

# Example usage
if __name__ == "__main__":
    asyncio.run(main())