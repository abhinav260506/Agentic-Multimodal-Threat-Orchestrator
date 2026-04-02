# Usage Guide - Input/Output Workflow

## Overview

The framework processes input files from the `input/` folder and saves results to the `output/` folder.

## Quick Start

### 1. Prepare Input Files

Place your files in the appropriate input subdirectories:

```
input/
├── logs/
│   └── your_security_logs.csv
├── videos/
│   └── your_surveillance_video.mp4
└── network/
    └── network_data.txt (optional)
```

### 2. Run Processing

```bash
python process_input.py
```

### 3. Check Results

Results are saved in the `output/` folder, organized by input type:

**Individual Reports** (one per input file):
- `output/logs/{filename}_report_{timestamp}.json` - Log analysis JSON
- `output/logs/{filename}_report_{timestamp}.txt` - Log analysis text
- `output/videos/{filename}_report_{timestamp}.json` - Video analysis JSON
- `output/videos/{filename}_report_{timestamp}.txt` - Video analysis text
- `output/network/{source}_report_{timestamp}.json` - Network analysis JSON
- `output/network/{source}_report_{timestamp}.txt` - Network analysis text

**Comprehensive Report** (all analyses combined):
- `output/comprehensive_report_{timestamp}.json` - Complete JSON report
- `output/comprehensive_report_{timestamp}.txt` - Complete text report

## Input File Requirements

### Log Files (`input/logs/`)

- **Format**: CSV
- **Required Columns**: 
  - `timestamp`, `source_ip`, `dest_ip`, `protocol`, `action`, `threat_label`, `log_type`, `bytes_transferred`, `user_agent`, `request_path`
- **Example**: `cybersecurity_threat_detection_logs.csv`

### Video Files (`input/videos/`)

- **Format**: MP4
- **Content**: Security camera footage
- **Example**: `surveillance_video.mp4`

### Network Files (`input/network/`)

- **Format**: Text or CSV
- **Content**: Network connection data (optional)
- **Note**: If no network file is provided, the system will analyze live network connections

## Output Format

### JSON Report Structure

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "log_analysis": [
    {
      "file": "security_logs.csv",
      "result": {
        "agent": "LogAgent",
        "threat_level": "WARNING",
        "details": "...",
        "confidence": 0.85
      }
    }
  ],
  "vision_analysis": [...],
  "network_analysis": [...],
  "final_assessment": {
    "threat_level": "WARNING",
    "confidence": "Medium",
    "summary": "...",
    "recommendations": "..."
  }
}
```

### Text Report

Human-readable report with:
- Individual agent results
- Threat levels
- Details and recommendations
- Final unified assessment

## Example Workflow

1. **Copy your log file**:
   ```bash
   cp your_logs.csv input/logs/
   ```

2. **Copy your video file**:
   ```bash
   cp surveillance.mp4 input/videos/
   ```

3. **Run processing**:
   ```bash
   python process_input.py
   ```

4. **View results**:
   ```bash
   # View individual log report
   cat output/logs/sample_logs_report_*.txt
   
   # View individual video report
   cat output/videos/surveillance_report_*.txt
   
   # View comprehensive report
   cat output/comprehensive_report_*.txt
   ```

## Processing Multiple Files

The system automatically processes:
- **All CSV files** in `input/logs/`
- **All MP4 files** in `input/videos/`
- **Network data** (from files or live system)

Each file is analyzed independently, and results are combined in the final assessment.

## Troubleshooting

### No Input Files Found

**Error**: "No input files found!"

**Solution**: 
- Check that files are in the correct subdirectories
- Verify file extensions (.csv for logs, .mp4 for videos)
- Check file permissions

### Processing Errors

**Error**: "Error analyzing logs: ..."

**Solution**:
- Verify file format matches expected structure
- Check file is not corrupted
- Ensure sufficient disk space in output folder

## Advanced Usage

### Process Specific Files

Modify `process_input.py` to process specific files:

```python
processor = InputProcessor()
result = processor.process_log_file(Path("input/logs/specific_file.csv"))
```

### Custom Output Location

Modify `config.py` to change output directory:

```python
OUTPUT_DIR = BASE_DIR / "custom_output"
```

