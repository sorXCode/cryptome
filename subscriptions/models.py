import enum
from app import db
from datetime import datetime, timedelta


class SourceEnum(enum.Enum):
    coinbase = "COINBASE"
    rewards = "REWARDS"

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    code = db.Column(db.String)
    source = db.Column(db.Enum(SourceEnum), default=SourceEnum.coinbase)
    starts = db.Column(db.DateTime)
    ends = db.Column(db.DateTime)

    @classmethod
    def create_monthly_subscription(cls, user_id, code=None, source=SourceEnum.coinbase):
        subscription = cls(user_id=user_id, code=code)
        subscription.source = source
        subscription.starts = datetime.now()
        subscription.ends = subscription.starts + timedelta(days=30)
        
        subscription.save()
        return subscription
    
    @classmethod
    def has_active_subscription(cls, user_id):
        return Subscription.query.filter(cls.user_id==user_id, cls.ends >= datetime.today()).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

