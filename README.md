# Agentic-Multimodal-Threat-Orchestrator

A powerful, modular, multi-agent cybersecurity framework that utilizes AI and machine learning to analyze security threats across multiple domains. This repository combines backend data analysis, threat detection via Large Language Models (LLMs), and an interactive web-based dashboard for real-time monitoring.

## 🎯 Features

- **Multi-Agent Architecture**: Highly specialized agents dedicated to different security domains.
- **ML-Powered Threat Detection**: Includes a trained Random Forest model aimed at high accuracy log analysis.
- **AI-Powered Analysis**: Utilizes Google Gemini models as a robust fallback for intelligent threat detection across images, network data, and structured logs.
- **Unified Orchestration**: Master orchestrator coordinates Log, Vision, and Network agents for a comprehensive security assessment.
- **Real-Time Dashboard**: Flask-based interactive web dashboard with an admin interface for log tracking, video analysis, and prompt alerting.

---

## 📦 Core Agents

### 1. LogAgent
Analyzes CSV security logs for threats, anomalies, and suspicious patterns. Primarily uses a trained Python ML model (Random Forest). Seamlessly falls back to LLM analysis if the model is unavailable or encounters unsupported data.

### 2. VisionAgent
Employs multimodal AI to interactively analyze video surveillance footage (`.mp4`) for security threats, unauthorized access, and suspicious activities.

### 3. NetworkAgent
Proactively monitors network traffic, open ports, and active connections for vulnerabilities and breaches.

---

## 🚀 Quick Start

### 1. Installation

Install all required Python dependencies:
```bash
pip install -r requirements.txt
cd dashboard
pip install -r requirements.txt
cd ..
```

### 2. Basic Configuration

Set up your Gemini API key (optional depending on your security setup):
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run the Dashboard

To start the interactive web UI and real-time monitoring system:
```bash
cd dashboard
python app.py
```
Access the dashboard at `http://localhost:5000`. Login with the default credentials (`admin` / `admin123`).

### 4. Run CLI Backend Processing 

You can also orchestrate the agents entirely via the Command Line Interface.
1. Place input files in the `input/` folder (e.g., `input/logs/*.csv` or `input/videos/*.mp4`).
2. Run the processor:
```bash
python process_input.py
```
3. Check the aggregated analysis in the `output/` directory.

---

## 📁 System Architecture

```text
Agentic-Multimodal-Threat-Orchestrator/
├── base_agent.py          # Base architectural class for agents
├── log_agent.py           # Core Security log analysis agent
├── vision_agent.py        # Core Video/image visual analysis agent
├── network_agent.py      # Core Network protocol security agent
├── main_orchestrator.py   # Synchronizes analysis across all agents
├── process_input.py       # Terminal input data processor
├── train_model.py         # Sci-kit learn training scripts
├── config.py              # Global runtime configuration
├── dashboard/             # Flask-based Real-time Web Dashboard Application
│   ├── app.py             # Dashboard entry point
│   ├── monitor.py         # Active Dashboard monitoring services
│   └── templates/         # Interactive UI templates
├── input/                 # Directory for dropping new evidence files
└── output/                # Directory for generated reports and threat scores
```

## 📋 Extending the Rules

You can add custom agents by inheriting from `BaseAgent` and loading your new class into `main_orchestrator.py`. Threat levels are globally recognized as **CRITICAL**, **WARNING**, or **SECURE**. Configuration rules for the web dashboard (like Whitelisted IP address and time-of-day access) can be updated in the Dashboard admin panel.

## 🤝 Contributing

Contributions are always welcome! Feel free to extend this framework with additional agents or enhancements. Create a pull request to submit changes.

## 📝 License

This project is built for educational and research purposes prioritizing AI-based multimodality in cybersecurity architectures.
