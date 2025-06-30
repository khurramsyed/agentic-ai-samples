from typing import List, Dict
from ai_models import AIModel
from mcp_manager import MCPManager
from response_processor import ResponseProcessor

class QueryProcessor:
    def __init__(self, ai_model: AIModel, mcp_manager: MCPManager):
        self.ai_model = ai_model
        self.mcp_manager = mcp_manager
        self.response_processor = ResponseProcessor(mcp_manager)
    
    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        print(messages)
        tools = self.mcp_manager.get_available_tools()
        print(tools)
        response = await self.ai_model.generate_response(messages, tools)
        
        
        # Process based on model type
        if hasattr(response, 'content'):  # Anthropic
            results = await self.response_processor.process_anthropic_response(response)
        else:  # Bedrock
            results = await self.response_processor.process_bedrock_response(response)
        
        return "\n".join(results)