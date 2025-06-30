from typing import List, Any
from mcp_manager import MCPManager

class ResponseProcessor:
    def __init__(self, mcp_manager: MCPManager):
        self.mcp_manager = mcp_manager
    
    async def process_anthropic_response(self, response: Any) -> List[str]:
        results = []
        for content in response.content:
            if content.type == 'text':
                results.append(content.text)
            elif content.type == 'tool_use':
                tool_result = await self.mcp_manager.execute_tool(content.name, content.input)
                results.append(f"Tool {content.name}: {tool_result}")
        return results
    
    async def process_bedrock_response(self, response: Any) -> List[str]:
        results = []
        if 'content' in response:
            for content in response['content']:
                if content['type'] == 'text':
                    results.append(content['text'])
                elif content['type'] == 'tool_use':
                    tool_result = await self.mcp_manager.execute_tool(
                        content['name'], content['input']
                    )
                    results.append(f"Tool {content['name']}: {tool_result}")
        return results