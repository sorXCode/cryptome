from app import db
from datetime import datetime
import sqlalchemy_jsonfield
from sqlalchemy.dialects.sqlite import JSON

class CompletedTransaction(db.Model):
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

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_transaction_by_code(cls, code):
        return cls.query.filter_by(code=code).first()
    
    def set_webhook_data(self,webhook_data):
        self.webhook_data = webhook_data
        self.updated_at = datetime.now()
        self.save()