"""
Simple runner script for the Lightweight AgenticCyber Framework
"""
from main_orchestrator import CyberOrchestrator

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Welcome to Lightweight AgenticCyber Framework")
    print("="*60 + "\n")
    
    orchestrator = CyberOrchestrator()
    
    # Ask user what type of scan they want
    print("Select scan type:")
    print("1. Full Scan (Logs + Vision + Network)")
    print("2. Quick Scan (Logs + Vision only)")
    print("3. Exit\n")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("\nRunning Full Scan...\n")
        orchestrator.run_full_scan(include_network=True)
    elif choice == "2":
        print("\nRunning Quick Scan...\n")
        orchestrator.run_quick_scan()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Running Full Scan by default...\n")
        orchestrator.run_full_scan(include_network=True)




