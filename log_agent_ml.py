"""
ML-Powered Log Analysis Agent for Lightweight AgenticCyber Framework
Uses trained machine learning model for threat detection
"""
import pandas as pd  # pyright: ignore[reportMissingImports]
import numpy as np
from pathlib import Path
from typing import Dict, Any
from base_agent import BaseAgent
import config
from train_model import ThreatDetectionModel


class LogAgentML(BaseAgent):
    """ML-powered agent specialized in analyzing security logs"""
    
    def __init__(self):
        super().__init__("LogAgentML", config.DEFAULT_MODEL)
        self.log_file = config.LOG_DIR / "cybersecurity_threat_detection_logs.csv"
        self.ml_model = ThreatDetectionModel()
        
        # Try to load trained model
        try:
            self.ml_model.load_model()
            self.model_loaded = True
        except FileNotFoundError:
            print("Warning: Trained model not found. Please run train_model.py first.")
            self.model_loaded = False
    
    def analyze(self, log_file: Path = None, sample_size: int = 1000) -> Dict[str, Any]:
        """
        Analyze security logs using trained ML model
        Args:
            log_file: Path to log file (defaults to configured log file)
            sample_size: Number of log entries to analyze
        """
        self.status = "analyzing"
        
        if not self.model_loaded:
            return self.format_report(
                "WARNING",
                "ML model not loaded. Please train the model first using train_model.py",
                0.0
            )
        
        if log_file is None:
            log_file = self.log_file
        
        if not log_file.exists():
            return self.format_report(
                "WARNING",
                f"Log file not found: {log_file}",
                0.0
            )
        
        try:
            # Load and preprocess data
            df = self._load_logs(log_file, sample_size)
            
            if df is None or len(df) == 0:
                return self.format_report(
                    "SECURE",
                    "No log entries found or file is empty",
                    0.0
                )
            
            # Preprocess features
            X, _ = self.ml_model.preprocess_features(df, is_training=False)
            
            # Make predictions
            predictions, probabilities = self.ml_model.predict(X)
            
            # Analyze results
            threat_counts = pd.Series(predictions).value_counts()
            max_prob = probabilities.max(axis=1).mean()
            
            # Determine threat level
            if 'malicious' in threat_counts.index:
                threat_level = "CRITICAL"
                details = f"CRITICAL: {threat_counts.get('malicious', 0)} malicious threats detected. {threat_counts.get('suspicious', 0)} suspicious activities found."
            elif 'suspicious' in threat_counts.index:
                threat_level = "WARNING"
                details = f"WARNING: {threat_counts.get('suspicious', 0)} suspicious activities detected. Review logs for potential threats."
            else:
                threat_level = "SECURE"
                details = f"SECURE: All {len(df)} log entries analyzed. No threats detected. All activities appear benign."
            
            # Add statistics
            details += f" Analyzed {len(df)} entries. Threat distribution: {dict(threat_counts)}. Average confidence: {max_prob:.2%}"
            
            self.status = "completed"
            return self.format_report(threat_level, details, float(max_prob))
            
        except Exception as e:
            self.status = "error"
            return self.format_report(
                "WARNING",
                f"Error analyzing logs: {str(e)}",
                0.0
            )
    
    def _load_logs(self, log_file: Path, sample_size: int):
        """Load log entries from file"""
        try:
            # Load CSV
            df = pd.read_csv(log_file, nrows=sample_size)
            return df
        except Exception as e:
            print(f"Error loading logs: {e}")
            return None
    
    def get_log_report(self) -> str:
        """Legacy method for compatibility"""
        result = self.analyze()
        return f"{result['threat_level']}: {result['details']}"

