import logging
import json
import time
from typing import Any, Dict

class AuditLogger:
    """
    Logs security-related events for the Phi-Chain network.
    """
    def __init__(self, log_file: str = "audit.log"):
        self.logger = logging.getLogger("AuditLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log a security event."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        }
        self.logger.info(json.dumps(event))
        
        # Trigger alerts for critical events
        if event_type == "CRITICAL_FAILURE" or event_type == "UNAUTHORIZED_ACCESS":
            self.trigger_alert(event)

    def trigger_alert(self, event: Dict[str, Any]):
        """Trigger an alert (e.g., Telegram, Slack, Email)."""
        print(f"ALERT: {event['event_type']} - {event['details']}")

if __name__ == "__main__":
    audit = AuditLogger()
    audit.log_event("LOGIN_SUCCESS", {"user": "admin", "ip": "127.0.0.1"})
    audit.log_event("UNAUTHORIZED_ACCESS", {"ip": "192.168.1.100", "resource": "wallet_api"})
