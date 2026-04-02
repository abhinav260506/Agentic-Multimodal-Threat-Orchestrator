# Lightweight AgenticCyber Framework

A modular, lightweight multi-agent cybersecurity framework that uses AI agents to analyze security threats across multiple domains.

## 🎯 Features

- **Multi-Agent Architecture**: Specialized agents for different security domains
- **ML-Powered Threat Detection**: Trained Random Forest model for accurate log analysis
- **Modular Design**: Easy to extend with new agents
- **AI-Powered Analysis**: Uses Google Gemini models for intelligent threat detection
- **Unified Orchestration**: Coordinates multiple agents for comprehensive security assessment
- **Hybrid Approach**: ML model for logs, LLM for vision and network analysis

## 📦 Agents

### LogAgent
Analyzes security logs for threats, anomalies, and suspicious patterns. Uses trained ML model (Random Forest) for accurate threat detection. Falls back to LLM analysis if model not trained.

### VisionAgent
Analyzes video surveillance footage for security threats and suspicious activities.

### NetworkAgent
Monitors network traffic, open ports, and active connections for security issues.

## 🚀 Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train the ML model (recommended for better accuracy):
```bash
# Quick training (50k samples, faster)
python quick_train.py

# Full training (entire dataset, better accuracy)
python train_model.py
```

3. Set up your API key (optional, defaults to hardcoded key):
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

### Usage

#### Process Input Files (Recommended)

1. Place your files in the `input/` folder:
   - Log files: `input/logs/*.csv`
   - Video files: `input/videos/*.mp4`

2. Run the processor:
```bash
python process_input.py
```

3. Check results in `output/` folder

#### Full Security Scan (Legacy)
```python
from main_orchestrator import CyberOrchestrator

orchestrator = CyberOrchestrator()
orchestrator.run_full_scan(include_network=True)
```

#### Quick Scan (Logs + Vision only)
```python
orchestrator = CyberOrchestrator()
orchestrator.run_quick_scan()
```

#### Use Individual Agents
```python
from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent

# Log analysis
log_agent = LogAgent()
result = log_agent.analyze()

# Vision analysis
vision_agent = VisionAgent()
result = vision_agent.analyze(video_path="path/to/video.mp4")

# Network analysis
network_agent = NetworkAgent()
result = network_agent.analyze()
```

## 📁 Project Structure

```
crypto_pro/
├── base_agent.py          # Base class for all agents
├── log_agent.py           # Security log analysis agent
├── vision_agent.py        # Video/image analysis agent
├── network_agent.py      # Network security agent
├── main_orchestrator.py   # Main orchestrator
├── process_input.py       # Main input processing script
├── train_model.py         # ML model training script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── input/                 # Input files directory
│   ├── logs/              # Place CSV log files here
│   ├── videos/            # Place MP4 video files here
│   └── network/           # Optional network data files
├── archive/               # Legacy log files directory
└── output/                # Results output directory
```

## ⚙️ Configuration

Edit `config.py` to customize:
- API keys and models
- File paths
- Agent timeouts and retries
- Output directories

## 🔧 Extending the Framework

To add a new agent:

1. Create a new agent class inheriting from `BaseAgent`:
```python
from base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyCustomAgent")
    
    def analyze(self, *args, **kwargs):
        # Your analysis logic
        result = self._call_llm(prompt)
        return self.format_report(threat_level, details, confidence)
```

2. Register it in `main_orchestrator.py`:
```python
self.agents['custom'] = MyCustomAgent()
```

## 📊 Threat Levels

- **CRITICAL**: Immediate security threat detected
- **WARNING**: Suspicious activity that requires attention
- **SECURE**: No threats detected

## 🛠️ Requirements

- Python 3.8+
- Google Gemini API key
- OpenCV (for video processing)

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Feel free to extend this framework with additional agents or improvements!


