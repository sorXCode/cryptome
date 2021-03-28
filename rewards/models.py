from datetime import datetime
from app import db


class Reward(db.Model):
    id = db.Column(db.Integer, pk=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), index=True, nullable=False)
    completed = db.Column()
    created_at = db.Column()
    used_at = db.Column()
    is_used = db.Column()

    __mapper_args__ = {
        "order_by": created_at.desc()
    }

    @classmethod
    def create_entry(cls, user_id):
        latest_user_record = cls.query.filter_by(user_id=user_id).first()

        if latest_user_record and latest_user_record.completed < 3:
            latest_user_record.completed += 1

        else:
            # create a new record if there's no user reward record, or record.completed==3 already
            latest_user_record = cls(user_id=user_id, completed=1)

        latest_user_record.save()
        return latest_user_record

    @classmethod
    def user_unused_reward(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_used=False, used_at=None, completed=3).first()

    def mark_as_used(self):
        self.used_at = datetime.now()
        self.is_used = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
