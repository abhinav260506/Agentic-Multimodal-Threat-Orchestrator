"""
Database Models for Security Dashboard
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, user
    organization = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    login_attempts = db.relationship('LoginAttempt', backref='user', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class LoginAttempt(db.Model):
    """Login attempt tracking"""
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=False)
    user_agent = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<LoginAttempt {self.user_id} from {self.ip_address}>'

class Alert(db.Model):
    """Security alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)  # login_violation, suspicious_activity, etc.
    severity = db.Column(db.String(20), default='info')  # critical, warning, info
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text)  # JSON string
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Alert {self.alert_type} - {self.severity}>'

class OrganizationRule(db.Model):
    """Organization-specific security rules"""
    __tablename__ = 'organization_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # allowed_ips, allowed_times, etc.
    rule_value = db.Column(db.Text, nullable=False)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OrganizationRule {self.organization} - {self.rule_type}>'


