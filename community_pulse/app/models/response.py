from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from community_pulse.app.extensions import db
from community_pulse.app.models.base import Model
from community_pulse.app.models import Question


class Response(Model):
    is_agree: Mapped[bool] = mapped_column(db.Boolean, nullable=False)

    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'), nullable=False)
    # cycling import in typing (TYPE_CHECKING: True)
    question: Mapped["Question"] = relationship("Question", back_populates="responses")

    def __repr__(self):
        return f'Response for Question {self.question_id}: {"Agree" if self.is_agree else "Disagree"}'
