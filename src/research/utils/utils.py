import json
from typing import Dict, List, Any
from datetime import datetime

def format_search_results(results: Dict[str, Any]) -> str:
    """Format search results into a readable string format.
    
    Args:
        results: Dictionary containing search results
        
    Returns:
        Formatted string of search results
    """
    formatted_results = []
    
    for query, result in results.items():
        formatted_results.append(f"Query: {query}\n{result}\n")
    
    return "\n".join(formatted_results)

def log_execution_time(func_name: str, start_time: datetime = None) -> datetime:
    """Log the execution time of a function or operation.
    
    Args:
        func_name: Name of the function or operation
        start_time: Start time if ending an operation, None if starting
        
    Returns:
        Current datetime if starting an operation, None if ending
    """
    current_time = datetime.now()
    
    if start_time:
        elapsed = current_time - start_time
        print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - {func_name} completed in {elapsed.total_seconds():.2f} seconds")
        return None
    else:
        print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - {func_name} started")
        return current_time

def clean_search_item(item: Dict[str, Any], score_threshold: float = 0.6) -> Dict[str, Any]:
    """Clean up search result item and filter by relevance score.
    
    Args:
        item: Search result item
        score_threshold: Minimum score to include result
        
    Returns:
        Cleaned item or None if below threshold
    """
    if 'score' in item and item['score'] < score_threshold:
        return None
        
    return {
        'title': item.get('title', ''),
        'url': item.get('url', ''),
        'content': item.get('content', '')
    }

def parse_llm_response(text: str, output_type: str = 'list') -> List[str]:
    """Parse LLM response into desired format.
    
    Args:
        text: Raw LLM response text
        output_type: Type of output to parse ('list', 'json', etc.)
        
    Returns:
        Parsed output in requested format
    """
    if output_type == 'list':
        # Handle different list formats
        if ',' in text:
            # Comma-separated list
            return [item.strip() for item in text.split(',')]
        elif '\n' in text:
            # Newline-separated list
            return [item.strip() for item in text.split('\n') if item.strip()]
        else:
            # Single item
            return [text.strip()]
    elif output_type == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return []
    else:
        return [text]