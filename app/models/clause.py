import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDPrimaryKeyMixin


class Clause(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "clauses"
    __table_args__ = (UniqueConstraint("version_id", "position"),)

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("document_versions.id", ondelete="CASCADE"),
    )
    number: Mapped[str | None] = mapped_column(String(50))
    position: Mapped[int]
    text: Mapped[str] = mapped_column(Text)