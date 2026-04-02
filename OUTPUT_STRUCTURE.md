# Output Folder Structure

## Overview

Reports are saved in the `output/` folder, organized to correspond with input files.

## Folder Structure

```
output/
├── logs/                          # Log analysis reports
│   ├── sample_logs_report_20240115_103000.json
│   ├── sample_logs_report_20240115_103000.txt
│   ├── security_logs_report_20240115_103000.json
│   └── security_logs_report_20240115_103000.txt
│
├── videos/                        # Video analysis reports
│   ├── surveillance_report_20240115_103000.json
│   ├── surveillance_report_20240115_103000.txt
│   ├── camera1_report_20240115_103000.json
│   └── camera1_report_20240115_103000.txt
│
├── network/                       # Network analysis reports
│   ├── live_system_report_20240115_103000.json
│   └── live_system_report_20240115_103000.txt
│
└── comprehensive_report_20240115_103000.json  # Combined report
    comprehensive_report_20240115_103000.txt
```

## Report Types

### 1. Individual Reports

Each input file gets its own report saved in the corresponding subfolder:

- **Log files** → `output/logs/{filename}_report_{timestamp}.json/txt`
- **Video files** → `output/videos/{filename}_report_{timestamp}.json/txt`
- **Network data** → `output/network/{source}_report_{timestamp}.json/txt`

### 2. Comprehensive Report

A combined report with all analyses:
- `output/comprehensive_report_{timestamp}.json`
- `output/comprehensive_report_{timestamp}.txt`

## File Naming Convention

- **Format**: `{input_filename}_report_{YYYYMMDD_HHMMSS}.{ext}`
- **Example**: `sample_logs_report_20240115_103000.json`

## Report Contents

### Individual Report (JSON)
```json
{
  "input_file": "sample_logs.csv",
  "timestamp": "2024-01-15T10:30:00",
  "analysis": {
    "agent": "LogAgent",
    "threat_level": "WARNING",
    "details": "...",
    "confidence": 0.85,
    "status": "completed"
  }
}
```

### Individual Report (TXT)
```
============================================================
LOG ANALYSIS REPORT
============================================================

Input File: sample_logs.csv
Generated: 2024-01-15T10:30:00

Agent: LogAgent
Threat Level: WARNING
Confidence: 0.85
Status: completed

Details:
------------------------------------------------------------
WARNING: 5 suspicious activities detected...
```

### Comprehensive Report

Contains all individual analyses plus final unified assessment.

## Benefits

1. **Easy Tracking**: Each input file has a corresponding output report
2. **Organized Structure**: Reports grouped by type (logs, videos, network)
3. **Timestamped**: Each run creates new reports with timestamps
4. **Dual Format**: Both JSON (machine-readable) and TXT (human-readable)

## Example Workflow

1. **Input**:
   ```
   input/logs/security_logs.csv
   input/videos/surveillance.mp4
   ```

2. **Processing**:
   ```bash
   python process_input.py
   ```

3. **Output**:
   ```
   output/logs/security_logs_report_20240115_103000.json
   output/logs/security_logs_report_20240115_103000.txt
   output/videos/surveillance_report_20240115_103000.json
   output/videos/surveillance_report_20240115_103000.txt
   output/comprehensive_report_20240115_103000.json
   output/comprehensive_report_20240115_103000.txt
   ```



