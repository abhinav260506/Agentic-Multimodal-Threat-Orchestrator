"""
Main Orchestrator for Lightweight AgenticCyber Framework
Coordinates multiple security agents and provides unified threat assessment
"""
import time
from typing import Dict, Any, List
from google import genai
import config
from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent


class CyberOrchestrator:
    """Main orchestrator that coordinates all security agents"""
    
    def __init__(self):
        self.client = genai.Client(
            api_key=config.API_KEY,
            http_options={'api_version': 'v1'}
        )
        self.model_id = config.DEFAULT_MODEL
        self.agents = {
            'log': LogAgent(),
            'vision': VisionAgent(),
            'network': NetworkAgent()
        }
        self.results = {}
    
    def run_full_scan(self, include_network: bool = True) -> Dict[str, Any]:
        """
        Run a full security scan with all available agents
        Args:
            include_network: Whether to include network agent (may require admin privileges)
        """
        print("=" * 60)
        print("🚀 LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - FULL SCAN")
        print("=" * 60)
        
        # Run all agents
        print("\n[1/3] Analyzing Security Logs...")
        self.results['log'] = self.agents['log'].analyze()
        self._print_agent_result('log')
        
        print("\n[2/3] Analyzing Video Surveillance...")
        self.results['vision'] = self.agents['vision'].analyze()
        self._print_agent_result('vision')
        
        if include_network:
            print("\n[3/4] Analyzing Network Security...")
            try:
                self.results['network'] = self.agents['network'].analyze()
                self._print_agent_result('network')
            except Exception as e:
                print(f"⚠️  Network analysis skipped: {e}")
                self.results['network'] = {
                    'threat_level': 'SECURE',
                    'details': 'Network analysis unavailable',
                    'status': 'skipped'
                }
        else:
            self.results['network'] = None
        
        # Fuse results
        print("\n" + "=" * 60)
        print("🔍 FUSING MULTI-AGENT RESULTS...")
        print("=" * 60)
        
        final_assessment = self._fuse_results()
        self._print_final_assessment(final_assessment)
        
        return final_assessment
    
    def run_quick_scan(self) -> Dict[str, Any]:
        """Run a quick scan with log and vision agents only"""
        print("=" * 60)
        print("⚡ LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - QUICK SCAN")
        print("=" * 60)
        
        print("\n[1/2] Analyzing Security Logs...")
        self.results['log'] = self.agents['log'].analyze()
        self._print_agent_result('log')
        
        print("\n[2/2] Analyzing Video Surveillance...")
        self.results['vision'] = self.agents['vision'].analyze()
        self._print_agent_result('vision')
        
        print("\n" + "=" * 60)
        print("🔍 FUSING RESULTS...")
        print("=" * 60)
        
        final_assessment = self._fuse_results()
        self._print_final_assessment(final_assessment)
        
        return final_assessment
    
    def _fuse_results(self) -> Dict[str, Any]:
        """Fuse results from all agents using LLM"""
        # Prepare fusion prompt
        agent_reports = []
        for agent_name, result in self.results.items():
            if result:
                agent_reports.append(
                    f"{agent_name.upper()}: {result.get('threat_level', 'UNKNOWN')} - {result.get('details', 'N/A')}"
                )
        
        fusion_prompt = f"""You are the Master Cybersecurity Orchestrator for a multi-agent security system.

Analyze and correlate the following agent reports:

{chr(10).join(agent_reports)}

Rules:
- If MULTIPLE agents report CRITICAL threats, output 'CRITICAL'
- If ANY agent reports CRITICAL, output 'CRITICAL'
- If MULTIPLE agents report WARNING, output 'WARNING'
- If ANY agent reports WARNING, output 'WARNING'
- Only output 'SECURE' if ALL agents report SECURE

Provide your final assessment in this format:
THREAT_LEVEL: [CRITICAL/WARNING/SECURE]
CONFIDENCE: [High/Medium/Low]
SUMMARY: [One sentence summary]
RECOMMENDATIONS: [Brief action items]"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=fusion_prompt
            )
            return self._parse_fusion_result(response.text)
        except Exception as e:
            return {
                'threat_level': 'WARNING',
                'confidence': 'Low',
                'summary': f'Orchestration error: {str(e)}',
                'recommendations': 'Review individual agent reports manually'
            }
    
    def _parse_fusion_result(self, result: str) -> Dict[str, Any]:
        """Parse the fusion result"""
        assessment = {
            'threat_level': 'SECURE',
            'confidence': 'Medium',
            'summary': result,
            'recommendations': 'No immediate action required'
        }
        
        # Extract threat level
        if 'CRITICAL' in result.upper():
            assessment['threat_level'] = 'CRITICAL'
        elif 'WARNING' in result.upper():
            assessment['threat_level'] = 'WARNING'
        
        # Extract confidence
        if 'HIGH' in result.upper():
            assessment['confidence'] = 'High'
        elif 'LOW' in result.upper():
            assessment['confidence'] = 'Low'
        
        # Extract summary and recommendations
        if 'SUMMARY:' in result:
            assessment['summary'] = result.split('SUMMARY:')[-1].split('RECOMMENDATIONS:')[0].strip()
        if 'RECOMMENDATIONS:' in result:
            assessment['recommendations'] = result.split('RECOMMENDATIONS:')[-1].strip()
        
        return assessment
    
    def _print_agent_result(self, agent_name: str):
        """Print formatted agent result"""
        result = self.results[agent_name]
        threat_level = result.get('threat_level', 'UNKNOWN')
        details = result.get('details', 'N/A')
        
        # Color coding
        if threat_level == 'CRITICAL':
            icon = '🔴'
        elif threat_level == 'WARNING':
            icon = '🟡'
        else:
            icon = '🟢'
        
        print(f"  {icon} {threat_level}: {details[:100]}...")
    
    def _print_final_assessment(self, assessment: Dict[str, Any]):
        """Print final assessment"""
        threat_level = assessment.get('threat_level', 'UNKNOWN')
        confidence = assessment.get('confidence', 'Medium')
        summary = assessment.get('summary', 'N/A')
        recommendations = assessment.get('recommendations', 'N/A')
        
        # Color coding
        if threat_level == 'CRITICAL':
            icon = '🔴'
            border = '=' * 60
        elif threat_level == 'WARNING':
            icon = '🟡'
            border = '-' * 60
        else:
            icon = '🟢'
            border = '-' * 60
        
        print(f"\n{border}")
        print(f"{icon} FINAL SECURITY STATUS: {threat_level}")
        print(f"   Confidence: {confidence}")
        print(f"\n   Summary: {summary}")
        print(f"\n   Recommendations: {recommendations}")
        print(f"{border}\n")


def run_multimodal_check():
    """Legacy function for backward compatibility"""
    orchestrator = CyberOrchestrator()
    orchestrator.run_quick_scan()


if __name__ == "__main__":
    orchestrator = CyberOrchestrator()
    
    # Run full scan with all agents
    orchestrator.run_full_scan(include_network=True)