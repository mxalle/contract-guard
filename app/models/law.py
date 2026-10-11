import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class LawArticle(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "law_articles"
    __table_args__ = (UniqueConstraint("code", "article_number"),)

    code: Mapped[str] = mapped_column(String(50))
    article_number: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)


class FindingLawRef(Base):
    __tablename__ = "finding_law_refs"

    finding_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("findings.id", ondelete="CASCADE"),
        primary_key=True,
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("law_articles.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )