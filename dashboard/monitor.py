"""
Real-time Security Monitoring System
"""
from datetime import datetime, time
from pathlib import Path
import sys
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dashboard.models import db, Alert, OrganizationRule, LoginAttempt
from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent

class SecurityMonitor:
    """Monitor security events and detect violations"""
    
    def __init__(self):
        self.log_agent = LogAgent()
        self.vision_agent = VisionAgent()
        self.network_agent = NetworkAgent()
    
    def check_login_violations(self, user, ip_address: str) -> list:
        """
        Check if login violates any security rules
        Returns list of violation messages
        """
        violations = []
        
        # Check if IP is allowed for organization
        org_rules = OrganizationRule.query.filter_by(
            organization=user.organization,
            is_active=True
        ).all()
        
        for rule in org_rules:
            if rule.rule_type == 'allowed_ips':
                allowed_ips = json.loads(rule.rule_value)
                if ip_address not in allowed_ips:
                    violations.append(f"Login from unauthorized IP: {ip_address}")
            
            elif rule.rule_type == 'allowed_times':
                time_ranges = json.loads(rule.rule_value)
                current_time = datetime.now().time()
                is_allowed = False
                
                for time_range in time_ranges:
                    start = time.fromisoformat(time_range['start'])
                    end = time.fromisoformat(time_range['end'])
                    if start <= current_time <= end:
                        is_allowed = True
                        break
                
                if not is_allowed:
                    violations.append(f"Login outside allowed time window")
            
            elif rule.rule_type == 'ip_change_alert':
                # Check if user logged in from different IP recently
                recent_logins = LoginAttempt.query.filter_by(
                    user_id=user.id,
                    success=True
                ).order_by(LoginAttempt.timestamp.desc()).limit(5).all()
                
                if recent_logins:
                    previous_ips = set(la.ip_address for la in recent_logins)
                    if ip_address not in previous_ips and len(previous_ips) > 0:
                        violations.append(f"Login from new IP address: {ip_address}")
        
        # Check if user belongs to organization
        if not user.organization:
            violations.append("User does not belong to any organization")
        
        return violations
    
    def process_log_file(self, file_path: str, app_context=None):
        """Process log file with log agent"""
        try:
            if app_context:
                with app_context:
                    result = self.log_agent.analyze(log_file=Path(file_path))
                    
                    # Check for threats
                    if result.get('threat_level') in ['CRITICAL', 'WARNING']:
                        # Create alert
                        alert = Alert(
                            alert_type='log_analysis_threat',
                            severity=result.get('threat_level', 'warning').lower(),
                            message=f"Threat detected in log file: {result.get('details', '')[:200]}",
                            details=json.dumps(result)
                        )
                        db.session.add(alert)
                        db.session.commit()
                    
                    return result
            else:
                # Process without database context
                result = self.log_agent.analyze(log_file=Path(file_path))
                return result
        except Exception as e:
            print(f"Error processing log file: {e}")
            return None
    
    def process_video_file(self, file_path: str, app_context=None):
        """Process video file with vision agent"""
        try:
            if app_context:
                with app_context:
                    result = self.vision_agent.analyze(video_path=Path(file_path))
                    
                    # Check for threats
                    if result.get('threat_level') in ['CRITICAL', 'WARNING']:
                        # Create alert
                        alert = Alert(
                            alert_type='vision_analysis_threat',
                            severity=result.get('threat_level', 'warning').lower(),
                            message=f"Threat detected in video: {result.get('details', '')[:200]}",
                            details=json.dumps(result)
                        )
                        db.session.add(alert)
                        db.session.commit()
                    
                    return result
            else:
                # Process without database context
                result = self.vision_agent.analyze(video_path=Path(file_path))
                return result
        except Exception as e:
            print(f"Error processing video file: {e}")
            return None
    
    def get_status(self) -> dict:
        """Get monitoring system status"""
        return {
            'status': 'active',
            'agents': {
                'log_agent': 'ready',
                'vision_agent': 'ready',
                'network_agent': 'ready'
            },
            'last_check': datetime.utcnow().isoformat()
        }

