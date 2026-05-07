from app import db
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def get_pht_now():
    """Returns current time in Philippine Time."""
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo('Asia/Manila'))
    return datetime.now(timedelta(hours=8))


class AuditLog(db.Model): # Must be 'AuditLog' to match your main_routes.py import
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=get_pht_now)
    # This is the line the error is complaining about:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

    def __repr__(self):
        return f"<Log {self.action} by {self.user_id} at {self.timestamp}>"