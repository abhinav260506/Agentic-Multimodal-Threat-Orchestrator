"""
Base Agent Class for Lightweight AgenticCyber Framework
Provides common functionality for all security agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from google import genai
import config


class BaseAgent(ABC):
    """Base class for all cybersecurity agents"""
    
    def __init__(self, agent_name: str, model_id: str = "models/gemini-2.5-flash"):
        self.agent_name = agent_name
        self.model_id = model_id
        self.client = genai.Client(
            api_key=config.API_KEY, 
            http_options={'api_version': 'v1'}
        )
        self.status = "initialized"
    
    @abstractmethod
    def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - must be implemented by subclasses
        Returns a dictionary with analysis results
        """
        pass
    
    def _call_llm(self, prompt: str, contents: Optional[list] = None) -> str:
        """Helper method to call the LLM"""
        try:
            if contents:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents
                )
            else:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
            return response.text
        except Exception as e:
            self.status = "error"
            return f"Error: {str(e)}"
    
    def get_status(self) -> str:
        """Get current agent status"""
        return self.status
    
    def format_report(self, threat_level: str, details: str, confidence: float = 0.0) -> Dict[str, Any]:
        """Format a standardized report"""
        return {
            "agent": self.agent_name,
            "threat_level": threat_level,  # CRITICAL, WARNING, SECURE
            "details": details,
            "confidence": confidence,
            "status": self.status
        }

