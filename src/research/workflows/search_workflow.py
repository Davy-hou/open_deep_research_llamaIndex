from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)

from typing import List, Dict
import asyncio
import json
from tavily import AsyncTavilyClient
from ..utils.prompts import search_query_prompt
from ..utils.utils import clean_search_item, parse_llm_response
class SearchQueryEvent(Event):
    query: str
    queries: List[str]

class SearchResultEvent(Event):
    results: Dict[str, str]

class SearchWorkflow(Workflow):
    def __init__(self, llm, config, verbose: bool = False):
        super().__init__(timeout=60, verbose=verbose)
        self.llm = llm
        self.tavily_client = AsyncTavilyClient(api_key=config["api_key"])
        self.config = config

    @step
    async def generate_queries(self, ctx: Context, ev: StartEvent) -> SearchQueryEvent:
        """Step 1: Generate search queries based on the section description"""
        try:
            # Use LLM to generate queries
            prompt = search_query_prompt.format(query=ev.query)
            
            try:
                response = await self.llm.acomplete(prompt)
                queries = parse_llm_response(response.text, 'list')
                if queries and len(queries) > self.config["max_queries"]:
                    queries = queries[: self.config["max_queries"]]
                return SearchQueryEvent(query=ev.query, queries=queries)
            except Exception as e:
                print(f"Error in LLM response: {e}")
                return SearchQueryEvent(query=ev.query, queries=[])
        except Exception as e:
            print(f"Error generating queries: {e}")
            return SearchQueryEvent(query=ev.query, queries=[])

    @step
    async def perform_searches(self, ctx: Context, ev: SearchQueryEvent) -> StopEvent:
        """Step 2: Perform parallel searches for each query"""
        try:
            if not self.tavily_client:
                return StopEvent(result={ev.query: f"No search client available for query: {ev.query}"})

            # Create search tasks list
            search_tasks = [
                self.tavily_client.search(
                    query,
                    search_depth= self.config["search_depth"],
                    max_results= self.config["max_results"]
                ) for query in ev.queries
            ]
            
            # Execute all searches in parallel
            search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Process results
            results = {}
            for query, result in zip(ev.queries, search_results):
                try:
                    if isinstance(result, Exception):
                        print(f"Error in Tavily search for query '{query}': {result}")
                        results[query] = f"Error performing search: {str(result)}"
                        continue
                        
                    content = []
                    if isinstance(result, dict) and 'results' in result:
                        for item in result['results']:
                            cleaned_item = clean_search_item(item)
                            if cleaned_item:
                                content.append(json.dumps(cleaned_item, ensure_ascii=False))
                    results[query] = "\n".join(content) if content else f"No detailed results found for query: {query}"
                except Exception as e:
                    print(f"Error processing result for query '{query}': {e}")
                    results[query] = f"Error processing search result: {str(e)}"
            
            return StopEvent(result=results)
        except Exception as e:
            print(f"Error performing searches: {e}")
            return StopEvent(result={})