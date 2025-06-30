import os
from typing import Dict, List, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, Tool
from mcp.client.sse import sse_client

class MCPServerConfig:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

class MCPManager:
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.all_tools: List[Tool] = []
    
    async def connect_servers(self, configs: List[MCPServerConfig]):
        for config in configs:
            sse_transport = await self.exit_stack.enter_async_context(sse_client(config.url))
            sse, write = sse_transport
            session = await self.exit_stack.enter_async_context(ClientSession(sse, write))
            await session.initialize()
            
            self.sessions[config.name] = session
            
            response = await session.list_tools()
            self.all_tools.extend(response.tools)
    
    async def find_tool_session(self, tool_name: str) -> Optional[ClientSession]:
        for session in self.sessions.values():
            response = await session.list_tools()
            if any(tool.name == tool_name for tool in response.tools):
                return session
        return None
    
    def get_available_tools(self) -> List[Dict]:
        return [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in self.all_tools]
    
    async def execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        session = await self.find_tool_session(tool_name)
        if session:
            result = await session.call_tool(tool_name, tool_args)
            return result.content
        return f"Tool {tool_name} not found"
    
    async def cleanup(self):
        await self.exit_stack.aclose()