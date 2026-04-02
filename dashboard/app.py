"""
Main Flask Application for Cybersecurity Dashboard
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dashboard.models import User, Alert, LoginAttempt, db
from dashboard.monitor import SecurityMonitor
from dashboard.alert_manager import AlertManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///security_dashboard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize services
security_monitor = SecurityMonitor()
alert_manager = AlertManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@organization.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                organization='Default Organization'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: admin / admin123")

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Check if user belongs to organization
            if not user.is_active:
                flash('Account is inactive. Contact administrator.', 'error')
                return render_template('login.html')
            
            # Record login attempt
            login_attempt = LoginAttempt(
                user_id=user.id,
                ip_address=request.remote_addr,
                timestamp=datetime.utcnow(),
                success=True
            )
            db.session.add(login_attempt)
            db.session.commit()
            
            # Check for violations
            violations = security_monitor.check_login_violations(user, request.remote_addr)
            if violations:
                alert_manager.create_alert(
                    user_id=user.id,
                    alert_type='login_violation',
                    severity='warning',
                    message=f"Login violations detected: {', '.join(violations)}",
                    details={'violations': violations, 'ip': request.remote_addr}
                )
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get recent alerts
    recent_alerts = Alert.query.filter_by(
        user_id=current_user.id
    ).order_by(Alert.created_at.desc()).limit(10).all()
    
    # Get statistics
    stats = {
        'total_alerts': Alert.query.filter_by(user_id=current_user.id).count(),
        'critical_alerts': Alert.query.filter_by(
            user_id=current_user.id, 
            severity='critical'
        ).count(),
        'recent_logins': LoginAttempt.query.filter_by(
            user_id=current_user.id
        ).order_by(LoginAttempt.timestamp.desc()).limit(5).all()
    }
    
    return render_template('dashboard.html', alerts=recent_alerts, stats=stats)

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    all_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(50).all()
    
    return render_template('admin.html', users=users, alerts=all_alerts)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_files():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        file_type = request.form.get('file_type')
        
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Save file locally
        upload_dir = Path(app.config['UPLOAD_FOLDER']) / file_type
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = upload_dir / filename
        file.save(str(file_path))
        
        # Process file with agents
        try:
            if file_type == 'logs':
                security_monitor.process_log_file(str(file_path), app.app_context())
            elif file_type == 'videos':
                security_monitor.process_video_file(str(file_path), app.app_context())
            flash('File uploaded successfully and analysis started', 'success')
        except Exception as e:
            flash(f'Error during analysis: {str(e)}', 'error')
        
        return redirect(url_for('upload_files'))
    
    return render_template('upload.html')

@app.route('/alerts')
@login_required
def alerts():
    user_alerts = Alert.query.filter_by(user_id=current_user.id).order_by(
        Alert.created_at.desc()
    ).all()
    
    return render_template('alerts.html', alerts=user_alerts)

@app.route('/api/alerts/recent')
@login_required
def recent_alerts_api():
    """API endpoint for recent alerts"""
    alerts = Alert.query.filter_by(user_id=current_user.id).order_by(
        Alert.created_at.desc()
    ).limit(10).all()
    
    return jsonify([{
        'id': alert.id,
        'type': alert.alert_type,
        'severity': alert.severity,
        'message': alert.message,
        'created_at': alert.created_at.isoformat()
    } for alert in alerts])

@app.route('/api/monitor/status')
@login_required
def monitor_status():
    """API endpoint for monitoring status"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    status = security_monitor.get_status()
    return jsonify(status)

if __name__ == '__main__':
    # Create uploads directory
    Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'logs').mkdir(exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'videos').mkdir(exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'network').mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

