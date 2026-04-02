# Example Usage

## Step-by-Step Example

### 1. Prepare Input Files

```bash
# Copy your log file to input folder
copy your_security_logs.csv input\logs\

# Copy your video file to input folder
copy surveillance_video.mp4 input\videos\
```

### 2. Run Processing

```bash
python process_input.py
```

### 3. Expected Output

```
============================================================
PROCESSING INPUT FILES
============================================================

Found input files:
  - Log files: 1
  - Video files: 1
  - Network files: 0

============================================================
PROCESSING LOG FILES
============================================================

Analyzing: your_security_logs.csv
  🟢 SECURE: All 1000 log entries analyzed...

============================================================
PROCESSING VIDEO FILES
============================================================

Analyzing: surveillance_video.mp4
  🟡 WARNING: Suspicious activity detected...

============================================================
PROCESSING NETWORK ANALYSIS
============================================================

No network files found. Using live system analysis...
  🟢 SECURE: Network appears normal...

============================================================
GENERATING FINAL ASSESSMENT
============================================================

✅ Results saved to:
   JSON: output\security_report_20240115_103000.json
   TXT:  output\security_report_20240115_103000.txt

============================================================
PROCESSING COMPLETE - SUMMARY
============================================================

🟡 Overall Threat Level: WARNING
   Confidence: Medium

   Summary: Multiple agents detected suspicious activity...
   
   Recommendations: Review video surveillance and log entries...

📊 Analysis Summary:
   - Log files analyzed: 1
   - Video files analyzed: 1
   - Network analyses: 1

📁 Results saved to: output
```

### 4. View Results

**JSON Report** (`output/security_report_*.json`):
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "log_analysis": [
    {
      "file": "your_security_logs.csv",
      "result": {
        "agent": "LogAgent",
        "threat_level": "SECURE",
        "details": "All 1000 log entries analyzed...",
        "confidence": 0.85
      }
    }
  ],
  "vision_analysis": [
    {
      "file": "surveillance_video.mp4",
      "result": {
        "agent": "VisionAgent",
        "threat_level": "WARNING",
        "details": "Suspicious activity detected...",
        "confidence": 0.75
      }
    }
  ],
  "final_assessment": {
    "threat_level": "WARNING",
    "confidence": "Medium",
    "summary": "Multiple agents detected suspicious activity...",
    "recommendations": "Review video surveillance and log entries..."
  }
}
```

**Text Report** (`output/security_report_*.txt`):
```
============================================================
CYBERSECURITY THREAT ASSESSMENT REPORT
============================================================

Generated: 2024-01-15T10:30:00

LOG ANALYSIS
------------------------------------------------------------
File: your_security_logs.csv
Threat Level: SECURE
Details: All 1000 log entries analyzed. No threats detected.
Confidence: 0.85

VISION ANALYSIS
------------------------------------------------------------
File: surveillance_video.mp4
Threat Level: WARNING
Details: Suspicious activity detected in video frame...
Confidence: 0.75

FINAL ASSESSMENT
============================================================
Threat Level: WARNING
Confidence: Medium

Summary:
Multiple agents detected suspicious activity. Video surveillance shows potential threat.

Recommendations:
Review video surveillance and log entries. Investigate suspicious activities.
```

## Multiple Files Example

If you have multiple files:

```
input/
├── logs/
│   ├── logs_jan.csv
│   ├── logs_feb.csv
│   └── logs_mar.csv
└── videos/
    ├── camera1.mp4
    └── camera2.mp4
```

All files will be processed and results combined in the final assessment.



