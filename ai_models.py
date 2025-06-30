import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from anthropic import Anthropic
import boto3

class AIModel(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict], tools: List[Dict]) -> Any:
        pass

class AnthropicModel(AIModel):
    def __init__(self):
        self.client = Anthropic()
    
    async def generate_response(self, messages: List[Dict], tools: List[Dict]) -> Any:
        return self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=messages,
            tools=tools
        )

class BedrockModel(AIModel):
    def __init__(self, region: str = "us-east-1", model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.client = boto3.client('bedrock-runtime', region_name=region)
        self.model_id = model_id
    
    async def generate_response(self, messages: List[Dict], tools: List[Dict]) -> Any:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages,
            "tools": tools
        }
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )
        
        return json.loads(response['body'].read())