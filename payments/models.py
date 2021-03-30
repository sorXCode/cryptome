from app import db
from datetime import datetime
import sqlalchemy_jsonfield
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy import event

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    buttonId = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    checkout_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    webhook_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_transaction_by_code(cls, code):
        return cls.query.filter_by(code=code).first()
    
    def set_webhook_data(self,webhook_data):
        self.webhook_data = webhook_data
        self.completed = True
        self.add_reward_for_referral()
        self.updated_at = datetime.now()
        self.save()

    def add_reward_for_referral(self):
        if not self.completed:
            return None

        from user.models import UserInvitation
        unrewarded_inviter = UserInvitation.get_unrewarded_inviter(self.user_id)

        if not unrewarded_inviter:
            return None
        
        from rewards.models import Reward
        Reward.create_entry(unrewarded_inviter.id)
        UserInvitation.mark_invitation_as_rewarded(user_id=self.user_id)