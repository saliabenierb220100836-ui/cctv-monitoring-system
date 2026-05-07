from app import db
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def manila_now():
    if ZoneInfo:
        try:
            return datetime.now(ZoneInfo('Asia/Manila'))
        except Exception:
            pass
    return datetime.now()


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150))

    action = db.Column(db.String(255))

    ip_address = db.Column(db.String(50))

    timestamp = db.Column(
        db.DateTime,
        default=manila_now
    )