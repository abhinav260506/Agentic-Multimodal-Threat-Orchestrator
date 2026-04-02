"""
Test script to demonstrate sample inputs and outputs for each agent
"""
from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent
from pathlib import Path
import json

def print_result(agent_name, result):
    """Pretty print agent result"""
    print(f"\n{'='*60}")
    print(f"{agent_name} Result:")
    print(f"{'='*60}")
    print(f"Agent: {result['agent']}")
    print(f"Threat Level: {result['threat_level']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Status: {result['status']}")
    print(f"\nDetails:")
    print(f"{result['details']}")
    print(f"{'='*60}\n")

def test_log_agent():
    """Test Log Agent with sample data"""
    print("\n" + "="*60)
    print("TESTING LOG AGENT")
    print("="*60)
    
    log_agent = LogAgent()
    
    # Test with default log file
    result = log_agent.analyze()
    print_result("Log Agent", result)
    
    # Test with sample log file if it exists
    sample_log = Path("archive/sample_logs.csv")
    if sample_log.exists():
        print("\nTesting with sample_logs.csv...")
        result = log_agent.analyze(log_file=sample_log, sample_size=10)
        print_result("Log Agent (Sample)", result)

def test_vision_agent():
    """Test Vision Agent"""
    print("\n" + "="*60)
    print("TESTING VISION AGENT")
    print("="*60)
    
    vision_agent = VisionAgent()
    
    # Test with video file in directory
    result = vision_agent.analyze()
    print_result("Vision Agent", result)

def test_network_agent():
    """Test Network Agent"""
    print("\n" + "="*60)
    print("TESTING NETWORK AGENT")
    print("="*60)
    
    network_agent = NetworkAgent()
    
    try:
        result = network_agent.analyze()
        print_result("Network Agent", result)
    except Exception as e:
        print(f"Network Agent Error: {e}")
        print("(This may require admin privileges)")

def main():
    """Run all agent tests"""
    print("\n" + "="*60)
    print("LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - SAMPLE TEST")
    print("="*60)
    
    # Test each agent
    test_log_agent()
    test_vision_agent()
    test_network_agent()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nCheck SAMPLES.md for detailed input/output examples")

if __name__ == "__main__":
    main()




