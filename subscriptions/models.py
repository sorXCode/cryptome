from app import db
from datetime import datetime, timedelta

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    code = db.Column(db.String)
    starts = db.Column(db.DateTime)
    ends = db.Column(db.DateTime)

    @classmethod
    def create_monthly_subscription(cls, user_id, code):
        subscription = cls(user_id=user_id, code=code)
        subscription.starts = datetime.now()
        subscription.ends = subscription.starts + timedelta(days=30)
        
        subscription.save()
        return subscription
    
    def save(self):
        db.session.add(self)
        db.session.commit()

