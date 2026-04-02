"""
Setup script to create organization security rules
"""
from app import app
from models import db, OrganizationRule
import json

def setup_default_rules():
    """Create default security rules for organizations"""
    with app.app_context():
        # Example: Allowed IPs for Default Organization
        if not OrganizationRule.query.filter_by(
            organization='Default Organization',
            rule_type='allowed_ips'
        ).first():
            rule = OrganizationRule(
                organization='Default Organization',
                rule_type='allowed_ips',
                rule_value=json.dumps(['192.168.1.0/24', '10.0.0.0/8']),
                is_active=True
            )
            db.session.add(rule)
        
        # Example: Allowed login times (9 AM to 6 PM)
        if not OrganizationRule.query.filter_by(
            organization='Default Organization',
            rule_type='allowed_times'
        ).first():
            rule = OrganizationRule(
                organization='Default Organization',
                rule_type='allowed_times',
                rule_value=json.dumps([
                    {'start': '09:00:00', 'end': '18:00:00'}
                ]),
                is_active=True
            )
            db.session.add(rule)
        
        # Enable IP change alerts
        if not OrganizationRule.query.filter_by(
            organization='Default Organization',
            rule_type='ip_change_alert'
        ).first():
            rule = OrganizationRule(
                organization='Default Organization',
                rule_type='ip_change_alert',
                rule_value=json.dumps({'enabled': True}),
                is_active=True
            )
            db.session.add(rule)
        
        db.session.commit()
        print("Default security rules created!")

if __name__ == '__main__':
    setup_default_rules()

