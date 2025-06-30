import asyncio
import os
from typing import List
from dotenv import load_dotenv

from ai_models import AnthropicModel, BedrockModel
from mcp_manager import MCPManager, MCPServerConfig
from query_processor import QueryProcessor
from chat_interface import ChatInterface

load_dotenv()

class MCPClient:
    def __init__(self, model_provider: str = "anthropic", aws_region: str = "us-east-1"):
        self.mcp_manager = MCPManager()
        
        if model_provider == "anthropic":
            self.ai_model = AnthropicModel()
        else:
            self.ai_model = BedrockModel(aws_region)
        
        self.query_processor = QueryProcessor(self.ai_model, self.mcp_manager)
        self.chat_interface = ChatInterface(self.query_processor)
    
    async def connect_to_servers(self, server_configs: List[dict] = None):
        if server_configs is None:
            server_configs = [{"name": "default", "url": os.getenv("MCP_SERVER")}]
        
        configs = [MCPServerConfig(cfg["name"], cfg["url"]) for cfg in server_configs]
        await self.mcp_manager.connect_servers(configs)
    
    async def chat_loop(self):
        await self.chat_interface.run_chat_loop()
    
    async def cleanup(self):
        await self.mcp_manager.cleanup()

async def main():
    server_configs = None 
    #[
    #    {"name": "server1", "url": os.getenv("MCP_SERVER_1", "sse://localhost:3001")},
    #    {"name": "server2", "url": os.getenv("MCP_SERVER_2", "sse://localhost:3002")}
    #]

    
    #client = MCPClient(model_provider="bedrock", aws_region="us-east-1")
    
    client = MCPClient(model_provider="anthropic")
    try:
        await client.connect_to_servers(server_configs)
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())