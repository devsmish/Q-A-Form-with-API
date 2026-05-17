from community_pulse.app.extensions import db
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class Model(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()
