# Dashboard Setup Guide

## Quick Start

### 1. Install Dashboard Dependencies

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Configure AWS (Optional - for S3 storage)

Create `.env` file in `dashboard/` folder:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=cybersecurity-dashboard
SECRET_KEY=your-secret-key-here
```

**Note**: If AWS is not configured, files will be stored locally only.

### 3. Run the Dashboard

```bash
cd dashboard
python run.py
```

Access at: **http://localhost:5000**

**Default Login:**
- Username: `admin`
- Password: `admin123`

### 4. Setup Security Rules (Optional)

```bash
python setup_rules.py
```

This creates default security rules for your organization.

## Features

### ✅ Authentication System
- Organization-based login
- User role management (admin/user)
- Login attempt tracking

### ✅ File Upload & AWS Storage
- Admin can upload CSV log files
- Admin can upload MP4 video files
- Automatic upload to AWS S3
- Files stored with timestamps

### ✅ Real-time Monitoring
- Automatic processing after file upload
- Log Agent analyzes CSV files
- Vision Agent analyzes MP4 files
- Results stored in database

### ✅ Alert System
- Automatic alerts for violations:
  - **Unauthorized IP**: Login from IP not in whitelist
  - **Time Violation**: Login outside allowed hours
  - **IP Change**: Login from new IP address
  - **Organization Check**: User belongs to organization
- Alerts visible in dashboard
- Critical alerts highlighted

### ✅ Time-based Operations
- All operations timestamped
- Login time validation
- File processing timestamps
- Alert creation times

## Workflow

1. **Admin logs in** → Dashboard access
2. **Admin uploads files** → CSV logs or MP4 videos
3. **Files uploaded to AWS S3** → Cloud storage
4. **Agents process files** → Automatic analysis
5. **Alerts generated** → For violations/threats
6. **Admin reviews alerts** → Takes action

## Security Rules Configuration

Rules are stored in database and can be configured via `setup_rules.py`:

- **Allowed IPs**: Whitelist of IP addresses
- **Allowed Times**: Login time windows (e.g., 9 AM - 6 PM)
- **IP Change Alerts**: Detect new IP logins

## API Endpoints

- `GET /api/alerts/recent` - Get recent alerts (JSON)
- `GET /api/monitor/status` - Monitoring status (Admin only)

## Troubleshooting

### Database Issues
```bash
# Delete database and recreate
rm security_dashboard.db
python run.py
```

### AWS Connection Issues
- Check `.env` file credentials
- Verify AWS IAM permissions
- Files will still work locally if AWS fails

### Import Errors
Make sure you're in the dashboard directory:
```bash
cd dashboard
python run.py
```

## Next Steps

1. Configure AWS credentials for cloud storage
2. Set up organization-specific security rules
3. Add more users via admin panel
4. Monitor alerts in real-time
5. Review processed files and results


