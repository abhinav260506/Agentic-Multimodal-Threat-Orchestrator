# Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell or Command Prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `google-genai` - For AI model access
- `opencv-python` - For video processing

## Step 2: Run the Framework

### Option A: Full Scan (Recommended)
```bash
python main_orchestrator.py
```

This runs:
- ✅ Log analysis
- ✅ Video surveillance analysis  
- ✅ Network security analysis
- ✅ Unified threat assessment

### Option B: Quick Scan (Logs + Vision only)
Edit `main_orchestrator.py` and change the last line to:
```python
orchestrator.run_quick_scan()
```

### Option C: Run from Python
```python
from main_orchestrator import CyberOrchestrator

orchestrator = CyberOrchestrator()
orchestrator.run_full_scan()
```

## Step 3: What to Expect

The framework will:
1. Analyze security logs from `archive/cybersecurity_threat_detection_logs.csv`
2. Analyze video from `VIRAT_S_010204_05_000856_000890.mp4`
3. Check network connections (if enabled)
4. Provide a unified threat assessment

## Troubleshooting

### If you get "Module not found" errors:
```bash
pip install google-genai opencv-python
```

### If video file is not found:
- Make sure `VIRAT_S_010204_05_000856_000890.mp4` is in the project directory
- Or specify the path in `vision_agent.py`

### If log file is not found:
- Make sure `archive/cybersecurity_threat_detection_logs.csv` exists
- The agent will report a warning but continue

### Network analysis requires admin privileges:
- If network scan fails, it will skip automatically
- Or set `include_network=False` in `run_full_scan()`

## Example Output

```
============================================================
🚀 LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - FULL SCAN
============================================================

[1/3] Analyzing Security Logs...
  🟢 SECURE: No critical threats detected...

[2/3] Analyzing Video Surveillance...
  🟡 WARNING: Suspicious activity detected...

[3/4] Analyzing Network Security...
  🟢 SECURE: Network appears normal...

============================================================
🔍 FUSING MULTI-AGENT RESULTS...
============================================================

🟡 FINAL SECURITY STATUS: WARNING
   Confidence: Medium
   Summary: Multiple agents detected suspicious activity...
   Recommendations: Review video surveillance and log entries...
```




