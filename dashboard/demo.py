"""
Simple demonstration script - processes sample data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent

def demo():
    print("="*60)
    print("CYBERSECURITY FRAMEWORK DEMONSTRATION")
    print("="*60)
    
    # Sample log file
    log_file = Path("dashboard/sample_data/sample_security_logs.csv")
    
    # Sample video file (use existing if available)
    video_file = Path("input/videos/VIRAT_S_010204_05_000856_000890.mp4")
    if not video_file.exists():
        video_file = Path("VIRAT_S_010204_05_000856_000890.mp4")
    
    print("\n[1] Processing Log File...")
    print(f"   File: {log_file}")
    if log_file.exists():
        log_agent = LogAgent()
        log_result = log_agent.analyze(log_file=log_file, sample_size=100)
        print(f"   Threat Level: {log_result.get('threat_level', 'UNKNOWN')}")
        print(f"   Details: {log_result.get('details', '')[:100]}...")
    else:
        print("   [SKIP] Log file not found")
    
    print("\n[2] Processing Video File...")
    print(f"   File: {video_file}")
    if video_file.exists():
        vision_agent = VisionAgent()
        vision_result = vision_agent.analyze(video_path=video_file)
        print(f"   Threat Level: {vision_result.get('threat_level', 'UNKNOWN')}")
        print(f"   Details: {vision_result.get('details', '')[:100]}...")
    else:
        print("   [SKIP] Video file not found")
    
    print("\n[3] Network Analysis...")
    network_agent = NetworkAgent()
    try:
        network_result = network_agent.analyze()
        print(f"   Threat Level: {network_result.get('threat_level', 'UNKNOWN')}")
        print(f"   Details: {network_result.get('details', '')[:100]}...")
    except Exception as e:
        print(f"   [SKIP] Network analysis error: {e}")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nTo use the web dashboard:")
    print("  1. Go to http://localhost:5000")
    print("  2. Login: admin / admin123")
    print("  3. Upload files via 'Upload Files' menu")
    print("  4. View alerts and results")

if __name__ == "__main__":
    demo()


