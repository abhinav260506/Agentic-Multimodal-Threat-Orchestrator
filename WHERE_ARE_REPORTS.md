# Where Are the Generated Reports?

## Report Location

Reports are saved in the **`output/`** folder, organized by input type.

## Folder Structure

```
output/
├── logs/                          # Log analysis reports
│   └── {filename}_report_{timestamp}.json
│   └── {filename}_report_{timestamp}.txt
│
├── videos/                        # Video analysis reports
│   └── {filename}_report_{timestamp}.json
│   └── {filename}_report_{timestamp}.txt
│
├── network/                       # Network analysis reports
│   └── {source}_report_{timestamp}.json
│   └── {source}_report_{timestamp}.txt
│
└── comprehensive_report_{timestamp}.json  # Combined report
    comprehensive_report_{timestamp}.txt
```

## How to Generate Reports

### Step 1: Place Input Files

Put your files in the `input/` folder:
- Log files: `input/logs/*.csv`
- Video files: `input/videos/*.mp4`

### Step 2: Run Processing

```bash
python process_input.py
```

### Step 3: Find Reports

After processing, reports will be in:
- **Individual reports**: `output/logs/`, `output/videos/`, `output/network/`
- **Comprehensive report**: `output/comprehensive_report_*.json/txt`

## Example

**If you have:**
- `input/logs/security_logs.csv`
- `input/videos/surveillance.mp4`

**After running `python process_input.py`, you'll get:**
- `output/logs/security_logs_report_20240115_103000.json`
- `output/logs/security_logs_report_20240115_103000.txt`
- `output/videos/surveillance_report_20240115_103000.json`
- `output/videos/surveillance_report_20240115_103000.txt`
- `output/comprehensive_report_20240115_103000.json`
- `output/comprehensive_report_20240115_103000.txt`

## Quick Check

To see if reports exist:
```bash
# Windows PowerShell
Get-ChildItem output -Recurse -File

# Or check specific folders
dir output\logs
dir output\videos
dir output\comprehensive_report_*
```

## Current Status

If the `output/` folder is empty, it means:
1. No processing has been run yet, OR
2. No input files were found

To generate reports:
1. Place files in `input/logs/` and/or `input/videos/`
2. Run: `python process_input.py`
3. Check the `output/` folder for results



