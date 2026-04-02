"""
Quick training script - trains model on a sample of data for faster testing
"""
from train_model import ThreatDetectionModel
from pathlib import Path
import config

if __name__ == "__main__":
    log_file = config.LOG_DIR / "cybersecurity_threat_detection_logs.csv"
    
    if not log_file.exists():
        print(f"Error: Log file not found at {log_file}")
        exit(1)
    
    print("="*60)
    print("QUICK TRAINING MODE")
    print("="*60)
    print("Training on 50,000 samples for faster results...")
    print("For full training, run: python train_model.py")
    print("="*60)
    
    model = ThreatDetectionModel()
    accuracy = model.train(
        csv_path=log_file,
        sample_size=50000,  # Quick training with 50k samples
        test_size=0.2
    )
    
    print(f"\n✅ Quick training complete! Accuracy: {accuracy:.4f}")
    print(f"Model saved to: {model.model_path}")



