# Sample Input and Output Data

This document shows example inputs and outputs for the Lightweight AgenticCyber Framework.

## 📥 Sample Input Data

### 1. Log Agent Input

**File**: `archive/cybersecurity_threat_detection_logs.csv`

**Sample CSV Format**:
```csv
timestamp,source_ip,destination_ip,port,protocol,action,status,user,event_type,severity,description
2024-01-15 10:23:45,192.168.1.100,10.0.0.5,443,TCP,ALLOW,SUCCESS,admin,CONNECTION,INFO,Successful HTTPS connection
2024-01-15 10:24:12,192.168.1.105,10.0.0.5,22,TCP,DENY,FAILED,unknown,SSH_ATTEMPT,HIGH,Multiple failed SSH login attempts
2024-01-15 10:25:30,192.168.1.200,external.com,80,TCP,ALLOW,SUCCESS,user1,HTTP_REQUEST,MEDIUM,Outbound HTTP connection
2024-01-15 10:26:15,10.0.0.5,192.168.1.50,3389,TCP,ALLOW,SUCCESS,admin,RDP_CONNECTION,INFO,Remote desktop connection
2024-01-15 10:27:45,192.168.1.100,10.0.0.5,445,TCP,DENY,FAILED,unknown,SMB_ATTEMPT,CRITICAL,Suspicious SMB connection attempt
2024-01-15 10:28:20,external.com,10.0.0.5,443,TCP,ALLOW,SUCCESS,admin,INBOUND_CONNECTION,MEDIUM,Inbound HTTPS from external source
2024-01-15 10:29:10,192.168.1.105,10.0.0.5,22,TCP,DENY,FAILED,unknown,SSH_ATTEMPT,HIGH,Repeated SSH brute force attempt
2024-01-15 10:30:00,192.168.1.200,malicious-site.com,443,TCP,ALLOW,SUCCESS,user2,HTTP_REQUEST,CRITICAL,Connection to known malicious domain
```

**Or Simple Text Format**:
```
2024-01-15 10:23:45 - INFO - Connection from 192.168.1.100 to 10.0.0.5:443 - ALLOWED
2024-01-15 10:24:12 - HIGH - Failed SSH login from 192.168.1.105 - DENIED
2024-01-15 10:25:30 - MEDIUM - HTTP request from 192.168.1.200 to external.com - ALLOWED
2024-01-15 10:27:45 - CRITICAL - Suspicious SMB connection attempt from 192.168.1.100 - DENIED
2024-01-15 10:29:10 - HIGH - SSH brute force attempt from 192.168.1.105 - DENIED
2024-01-15 10:30:00 - CRITICAL - Connection to malicious-site.com from 192.168.1.200 - ALLOWED
```

### 2. Vision Agent Input

**File**: `VIRAT_S_010204_05_000856_000890.mp4` (or any `.mp4` file)

**What it expects**:
- Video file in MP4 format
- Security camera footage
- The agent extracts a frame at 1 second (1000ms) by default

**Frame Content Examples**:
- Normal: Empty hallway, authorized personnel, normal activity
- Warning: Unauthorized person, loitering, unusual behavior
- Critical: Weapon visible, forced entry, security breach

### 3. Network Agent Input

**Live System Data** (from `netstat -an`):

**Sample Listening Ports**:
```
TCP    0.0.0.0:80             0.0.0.0:0              LISTENING
TCP    0.0.0.0:443            0.0.0.0:0              LISTENING
TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING
TCP    127.0.0.1:3306         0.0.0.0:0              LISTENING
TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING
TCP    0.0.0.0:4444           0.0.0.0:0              LISTENING  <-- Suspicious
```

**Sample Active Connections**:
```
TCP    192.168.1.100:52341    10.0.0.5:443           ESTABLISHED
TCP    192.168.1.105:52342    10.0.0.5:22            ESTABLISHED
TCP    10.0.0.5:3389          192.168.1.50:52340     ESTABLISHED
TCP    192.168.1.200:52343    malicious-site.com:443 ESTABLISHED  <-- Suspicious
```

---

## 📤 Sample Output Data

### 1. Log Agent Output

**Example 1: Secure Logs**
```python
{
    "agent": "LogAgent",
    "threat_level": "SECURE",
    "details": "No critical security threats detected in log analysis. All connections appear normal and authorized.",
    "confidence": 0.8,
    "status": "completed"
}
```

**Example 2: Warning Detected**
```python
{
    "agent": "LogAgent",
    "threat_level": "WARNING",
    "details": "Multiple failed SSH login attempts detected from IP 192.168.1.105. Possible brute force attack. 3 failed attempts in 5 minutes.",
    "confidence": 0.8,
    "status": "completed"
}
```

**Example 3: Critical Threat**
```python
{
    "agent": "LogAgent",
    "threat_level": "CRITICAL",
    "details": "CRITICAL: Connection to known malicious domain (malicious-site.com) detected from internal IP 192.168.1.200. Suspicious SMB connection attempts from 192.168.1.100. Immediate investigation required.",
    "confidence": 0.8,
    "status": "completed"
}
```

### 2. Vision Agent Output

**Example 1: Secure Scene**
```python
{
    "agent": "VisionAgent",
    "threat_level": "SECURE",
    "details": "THREAT_LEVEL: SECURE\nDETAILS: Normal security camera view showing empty hallway with no suspicious activity. No unauthorized persons or objects detected.\nOBJECTS: Door, hallway, ceiling lights",
    "confidence": 0.75,
    "status": "completed"
}
```

**Example 2: Warning Detected**
```python
{
    "agent": "VisionAgent",
    "threat_level": "WARNING",
    "details": "THREAT_LEVEL: WARNING\nDETAILS: Unauthorized person detected loitering near restricted area. Individual appears to be examining door access panel.\nOBJECTS: Person, door, access panel, security camera",
    "confidence": 0.75,
    "status": "completed"
}
```

**Example 3: Critical Threat**
```python
{
    "agent": "VisionAgent",
    "threat_level": "CRITICAL",
    "details": "THREAT_LEVEL: CRITICAL\nDETAILS: Security breach detected. Individual with suspicious object near entrance. Possible forced entry attempt. Immediate security response required.\nOBJECTS: Person, suspicious object, door, security system",
    "confidence": 0.75,
    "status": "completed"
}
```

### 3. Network Agent Output

**Example 1: Secure Network**
```python
{
    "agent": "NetworkAgent",
    "threat_level": "SECURE",
    "details": "THREAT_LEVEL: SECURE\nDETAILS: Network appears normal. All listening ports are standard services (HTTP, HTTPS, RDP). No suspicious outbound connections detected.",
    "confidence": 0.7,
    "status": "completed"
}
```

**Example 2: Warning Detected**
```python
{
    "agent": "NetworkAgent",
    "threat_level": "WARNING",
    "details": "THREAT_LEVEL: WARNING\nDETAILS: Unusual listening port detected on 4444. This port is commonly used for backdoors. Review if this service is authorized. Multiple outbound connections to external IPs.",
    "confidence": 0.7,
    "status": "completed"
}
```

**Example 3: Critical Threat**
```python
{
    "agent": "NetworkAgent",
    "threat_level": "CRITICAL",
    "details": "THREAT_LEVEL: CRITICAL\nDETAILS: CRITICAL: Active connection to known malicious domain (malicious-site.com) detected. Unauthorized port 4444 listening. Possible malware communication or data exfiltration. Immediate network isolation recommended.",
    "confidence": 0.7,
    "status": "completed"
}
```

---

## 🎯 Sample Final Orchestrated Output

### Scenario 1: All Secure
```
============================================================
⚡ LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - QUICK SCAN
============================================================

[1/2] Analyzing Security Logs...
  🟢 SECURE: No critical security threats detected in log analysis...

[2/2] Analyzing Video Surveillance...
  🟢 SECURE: Normal security camera view showing empty hallway...

============================================================
🔍 FUSING RESULTS...
============================================================

------------------------------------------------------------
🟢 FINAL SECURITY STATUS: SECURE
   Confidence: High

   Summary: All security agents report normal operations. No threats detected across logs and video surveillance.

   Recommendations: Continue monitoring. System appears secure.
------------------------------------------------------------
```

### Scenario 2: Warning Detected
```
============================================================
⚡ LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - QUICK SCAN
============================================================

[1/2] Analyzing Security Logs...
  🟡 WARNING: Multiple failed SSH login attempts detected from IP 192.168.1.105...

[2/2] Analyzing Video Surveillance...
  🟢 SECURE: Normal security camera view showing empty hallway...

============================================================
🔍 FUSING RESULTS...
============================================================

------------------------------------------------------------
🟡 FINAL SECURITY STATUS: WARNING
   Confidence: Medium

   Summary: Log analysis detected suspicious SSH brute force attempts. Video surveillance shows normal activity. Recommend investigating failed login attempts and reviewing access controls.

   Recommendations: 1. Block IP 192.168.1.105 temporarily. 2. Review SSH access logs. 3. Check for compromised credentials. 4. Enable SSH key authentication.
------------------------------------------------------------
```

### Scenario 3: Critical Threat
```
============================================================
⚡ LIGHTWEIGHT AGENTIC CYBER FRAMEWORK - FULL SCAN
============================================================

[1/3] Analyzing Security Logs...
  🔴 CRITICAL: Connection to known malicious domain detected...

[2/3] Analyzing Video Surveillance...
  🔴 CRITICAL: Security breach detected. Individual with suspicious object...

[3/4] Analyzing Network Security...
  🔴 CRITICAL: Active connection to malicious domain detected...

============================================================
🔍 FUSING MULTI-AGENT RESULTS...
============================================================

============================================================
🔴 FINAL SECURITY STATUS: CRITICAL
   Confidence: High

   Summary: Multiple agents have detected critical security threats. Logs show connections to malicious domains, video surveillance shows security breach, and network analysis confirms active malicious connections. Immediate action required.

   Recommendations: 1. Isolate affected systems immediately. 2. Block malicious IPs and domains. 3. Activate security response team. 4. Preserve logs for forensic analysis. 5. Review all recent network connections.
============================================================
```

---

## 📝 Creating Test Data

### Create Sample Log File

Save this as `archive/test_logs.csv`:
```csv
timestamp,source_ip,destination_ip,port,protocol,action,status,user,event_type,severity,description
2024-01-15 10:23:45,192.168.1.100,10.0.0.5,443,TCP,ALLOW,SUCCESS,admin,CONNECTION,INFO,Successful HTTPS connection
2024-01-15 10:24:12,192.168.1.105,10.0.0.5,22,TCP,DENY,FAILED,unknown,SSH_ATTEMPT,HIGH,Multiple failed SSH login attempts
2024-01-15 10:25:30,192.168.1.200,10.0.0.5,80,TCP,ALLOW,SUCCESS,user1,HTTP_REQUEST,MEDIUM,Outbound HTTP connection
2024-01-15 10:27:45,192.168.1.100,10.0.0.5,445,TCP,DENY,FAILED,unknown,SMB_ATTEMPT,CRITICAL,Suspicious SMB connection attempt
2024-01-15 10:30:00,192.168.1.200,malicious-site.com,443,TCP,ALLOW,SUCCESS,user2,HTTP_REQUEST,CRITICAL,Connection to known malicious domain
```

### Test Individual Agents

```python
# Test Log Agent
from log_agent import LogAgent
log_agent = LogAgent()
result = log_agent.analyze()
print(result)

# Test Vision Agent
from vision_agent import VisionAgent
vision_agent = VisionAgent()
result = vision_agent.analyze()
print(result)

# Test Network Agent
from network_agent import NetworkAgent
network_agent = NetworkAgent()
result = network_agent.analyze()
print(result)
```

---

## 🔍 Understanding Output Format

All agents return a standardized dictionary:
- `agent`: Name of the agent
- `threat_level`: `CRITICAL`, `WARNING`, or `SECURE`
- `details`: Human-readable analysis
- `confidence`: Float between 0.0 and 1.0
- `status`: `completed`, `analyzing`, `error`, or `initialized`

The orchestrator fuses these results and provides a unified assessment.




