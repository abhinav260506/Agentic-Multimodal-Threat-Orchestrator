# Cybersecurity Dashboard

Web-based dashboard for real-time security monitoring.

## Features

- **Authentication**: Organization-based login system
- **File Upload**: Admin interface to upload CSV logs and MP4 video files
- **Real-time Monitoring**: Automatic processing with log and vision agents
- **Alert System**: Automatic alerts for security violations
- **Violation Detection**:
  - Unauthorized IP addresses
  - Login outside allowed time windows
  - IP address changes
  - User organization validation

## Setup

### 1. Install Dependencies

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Configure Settings

Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///security_dashboard.db
```

### 3. Run the Application

```bash
python app.py
```

Access at: http://localhost:5000

**Default Login:**
- Username: `admin`
- Password: `admin123`

## Usage

### Admin Functions

1. **Upload Files**: Go to "Upload Files" menu
   - Upload CSV log files
   - Upload MP4 video files
   - Agents process files automatically

2. **View Alerts**: Check "Alerts" section for security violations

3. **Manage Users**: Admin panel shows all users and their organizations

### Security Rules

Configure organization rules in the database:
- **Allowed IPs**: Whitelist IP addresses
- **Allowed Times**: Define login time windows
- **IP Change Alerts**: Detect login from new IPs

## API Endpoints

- `GET /api/alerts/recent` - Get recent alerts (JSON)
- `GET /api/monitor/status` - Get monitoring status (Admin only)

## Architecture

```
dashboard/
├── app.py              # Main Flask application
├── models.py           # Database models
├── monitor.py          # Security monitoring
├── alert_manager.py    # Alert management
└── templates/          # HTML templates
```

## Background Processing

Files are processed automatically after upload:
- Log files → LogAgent analysis
- Video files → VisionAgent analysis
- Alerts created for detected threats

