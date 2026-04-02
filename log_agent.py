"""
Log Analysis Agent for Lightweight AgenticCyber Framework
Analyzes security logs for threats and anomalies using trained ML model
"""
import os
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from base_agent import BaseAgent
import config

# Try to import ML model, fallback to LLM if not available
try:
    from train_model import ThreatDetectionModel
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


class LogAgent(BaseAgent):
    """Agent specialized in analyzing security logs"""
    
    def __init__(self, use_ml: bool = True):
        super().__init__("LogAgent", config.DEFAULT_MODEL)
        self.log_file = config.LOG_DIR / "cybersecurity_threat_detection_logs.csv"
        self.use_ml = use_ml and ML_AVAILABLE
        self.ml_model = None
        
        if self.use_ml:
            try:
                self.ml_model = ThreatDetectionModel()
                self.ml_model.load_model()
                print("ML model loaded successfully")
            except FileNotFoundError:
                print("Warning: Trained ML model not found. Falling back to LLM analysis.")
                print("Run 'python train_model.py' to train the model.")
                self.use_ml = False
    
    def analyze(self, log_file: Path = None, sample_size: int = 1000) -> Dict[str, Any]:
        """
        Analyze security logs for threats using ML model or LLM
        Args:
            log_file: Path to log file (defaults to configured log file)
            sample_size: Number of log entries to sample for analysis
        """
        self.status = "analyzing"
        
        if log_file is None:
            log_file = self.log_file
        
        if not log_file.exists():
            return self.format_report(
                "WARNING",
                f"Log file not found: {log_file}",
                0.0
            )
        
        try:
            # Use ML model if available
            if self.use_ml and self.ml_model:
                return self._analyze_with_ml(log_file, sample_size)
            else:
                # Fallback to LLM analysis
                return self._analyze_with_llm(log_file, sample_size)
            
        except Exception as e:
            self.status = "error"
            return self.format_report(
                "WARNING",
                f"Error analyzing logs: {str(e)}",
                0.0
            )
    
    def _analyze_with_ml(self, log_file: Path, sample_size: int) -> Dict[str, Any]:
        """Analyze logs using trained ML model"""
        # Load data
        df = pd.read_csv(log_file, nrows=sample_size)
        
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
            malicious_count = threat_counts.get('malicious', 0)
            suspicious_count = threat_counts.get('suspicious', 0)
            details = f"CRITICAL: {malicious_count} malicious threat(s) detected. {suspicious_count} suspicious activity(ies) found. Immediate action required."
        elif 'suspicious' in threat_counts.index:
            threat_level = "WARNING"
            suspicious_count = threat_counts.get('suspicious', 0)
            details = f"WARNING: {suspicious_count} suspicious activity(ies) detected. Review logs for potential threats."
        else:
            threat_level = "SECURE"
            details = f"SECURE: All {len(df)} log entries analyzed. No threats detected. All activities appear benign."
        
        # Add statistics
        details += f" Analyzed {len(df)} entries. Threat distribution: {dict(threat_counts)}. Model confidence: {max_prob:.2%}"
        
        self.status = "completed"
        return self.format_report(threat_level, details, float(max_prob))
    
    def _analyze_with_llm(self, log_file: Path, sample_size: int) -> Dict[str, Any]:
        """Fallback: Analyze logs using LLM"""
        # Sample log entries
        log_sample = self._sample_logs(log_file, sample_size)
        
        if not log_sample:
            return self.format_report(
                "SECURE",
                "No log entries found or file is empty",
                0.0
            )
        
        # Analyze with LLM
        analysis_prompt = self._create_analysis_prompt(log_sample)
        result = self._call_llm(analysis_prompt)
        
        # Parse result
        threat_level, details = self._parse_result(result)
        
        self.status = "completed"
        return self.format_report(threat_level, details, 0.8)
    
    def _sample_logs(self, log_file: Path, sample_size: int) -> List[str]:
        """Sample log entries from the file"""
        try:
            # Try to read as CSV first
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Check if it's CSV
                try:
                    reader = csv.reader(f)
                    headers = next(reader, None)
                    rows = []
                    count = 0
                    for row in reader:
                        if count >= sample_size:
                            break
                        rows.append(','.join(row[:10]))  # Limit columns
                        count += 1
                    return rows[:sample_size]
                except:
                    # If not CSV, read as text
                    f.seek(0)
                    lines = f.readlines()
                    return lines[:sample_size]
        except Exception as e:
            print(f"Error sampling logs: {e}")
            return []
    
    def _create_analysis_prompt(self, log_sample: List[str]) -> str:
        """Create prompt for log analysis"""
        sample_text = '\n'.join(log_sample[:50])  # Limit to 50 entries for prompt
        
        prompt = f"""You are a cybersecurity expert analyzing security logs.

Analyze the following log entries for security threats:
- Unauthorized access attempts
- Suspicious network activity
- Malware indicators
- Data exfiltration patterns
- Privilege escalation attempts
- Anomalous user behavior

Log Sample:
{sample_text}

Provide your analysis in this exact format:
THREAT_LEVEL: [CRITICAL/WARNING/SECURE]
DETAILS: [Brief explanation of findings]
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
        
        # Extract details section if present
        if "DETAILS:" in result:
            details = result.split("DETAILS:")[-1].strip()
        elif "THREAT_LEVEL:" in result:
            details = result.split("THREAT_LEVEL:")[-1].strip()
        
        return threat_level, details
    
    def get_log_report(self) -> str:
        """Legacy method for compatibility"""
        result = self.analyze()
        return f"{result['threat_level']}: {result['details']}"
