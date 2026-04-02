"""
Alert Management System
"""
from datetime import datetime
from dashboard.models import db, Alert
import json

class AlertManager:
    """Manage security alerts"""
    
    def create_alert(self, user_id=None, alert_type='info', severity='info', 
                     message='', details=None):
        """Create a new alert"""
        alert = Alert(
            user_id=user_id,
            alert_type=alert_type,
            severity=severity,
            message=message,
            details=json.dumps(details) if details else None
        )
        db.session.add(alert)
        db.session.commit()
        
        # Send notification (can be extended with email/SMS)
        self._send_notification(alert)
        
        return alert
    
    def resolve_alert(self, alert_id: int):
        """Mark alert as resolved"""
        alert = Alert.query.get(alert_id)
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    def get_critical_alerts(self, limit=10):
        """Get recent critical alerts"""
        return Alert.query.filter_by(
            severity='critical',
            is_resolved=False
        ).order_by(Alert.created_at.desc()).limit(limit).all()
    
    def _send_notification(self, alert):
        """Send notification for alert (can be extended)"""
        # TODO: Implement email/SMS notifications
        print(f"[ALERT] {alert.severity.upper()}: {alert.message}")


