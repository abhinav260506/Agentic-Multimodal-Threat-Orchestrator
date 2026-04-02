"""
Network Security Agent for Lightweight AgenticCyber Framework
Monitors network traffic and analyzes network security
"""
import socket
import subprocess
from typing import Dict, Any, List
from base_agent import BaseAgent
import config


class NetworkAgent(BaseAgent):
    """Agent specialized in network security monitoring"""
    
    def __init__(self):
        super().__init__("NetworkAgent", config.DEFAULT_MODEL)
    
    def analyze(self, check_ports: bool = True, check_connections: bool = True) -> Dict[str, Any]:
        """
        Analyze network security
        Args:
            check_ports: Check for open/listening ports
            check_connections: Check active network connections
        """
        self.status = "analyzing"
        
        try:
            network_data = {}
            
            if check_ports:
                network_data['listening_ports'] = self._get_listening_ports()
            
            if check_connections:
                network_data['active_connections'] = self._get_active_connections()
            
            # Analyze with LLM
            analysis_prompt = self._create_analysis_prompt(network_data)
            result = self._call_llm(analysis_prompt)
            
            # Parse result
            threat_level, details = self._parse_result(result)
            
            self.status = "completed"
            return self.format_report(threat_level, details, 0.7)
            
        except Exception as e:
            self.status = "error"
            return self.format_report(
                "WARNING",
                f"Error analyzing network: {str(e)}",
                0.0
            )
    
    def _get_listening_ports(self) -> List[Dict[str, Any]]:
        """Get list of listening ports"""
        try:
            # Use netstat on Windows
            result = subprocess.run(
                ['netstat', '-an'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            listening = []
            for line in result.stdout.split('\n'):
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        addr = parts[1]
                        listening.append({'address': addr, 'status': 'LISTENING'})
            
            return listening[:20]  # Limit to 20 entries
        except Exception as e:
            print(f"Error getting listening ports: {e}")
            return []
    
    def _get_active_connections(self) -> List[Dict[str, Any]]:
        """Get active network connections"""
        try:
            result = subprocess.run(
                ['netstat', '-an'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            connections = []
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        local = parts[1]
                        remote = parts[2] if len(parts) > 2 else 'N/A'
                        connections.append({
                            'local': local,
                            'remote': remote,
                            'status': 'ESTABLISHED'
                        })
            
            return connections[:20]  # Limit to 20 entries
        except Exception as e:
            print(f"Error getting active connections: {e}")
            return []
    
    def _create_analysis_prompt(self, network_data: Dict[str, Any]) -> str:
        """Create prompt for network analysis"""
        prompt = f"""You are a network security expert. Analyze the following network data for security threats:

Listening Ports: {network_data.get('listening_ports', [])}
Active Connections: {network_data.get('active_connections', [])}

Look for:
- Unusual or unauthorized listening ports
- Suspicious outbound connections
- Ports that should not be open
- Connections to unknown or suspicious IPs
- Potential backdoors or malware communication

Provide analysis in this format:
THREAT_LEVEL: [CRITICAL/WARNING/SECURE]
DETAILS: [Description of findings]
"""
        return prompt
    
    def _parse_result(self, result: str) -> tuple:
        """Parse LLM result to extract threat level and details"""
        threat_level = "SECURE"
        details = result
        
        if "CRITICAL" in result.upper():
            threat_level = "CRITICAL"
        elif "WARNING" in result.upper() or "SUSPICIOUS" in result.upper():
            threat_level = "WARNING"
        
        if "DETAILS:" in result:
            details = result.split("DETAILS:")[-1].strip()
        elif "THREAT_LEVEL:" in result:
            details = result.split("THREAT_LEVEL:")[-1].strip()
        
        return threat_level, details




