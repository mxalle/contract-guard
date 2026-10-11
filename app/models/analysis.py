import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class AnalysisStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def _in_list(column: str, enum: type[StrEnum]) -> str:
    values = ", ".join(f"'{member.value}'" for member in enum)
    return f"{column} IN ({values})"


class Analysis(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "analyses"
    __table_args__ = (
        CheckConstraint(_in_list("status", AnalysisStatus), name="status_valid"),
    )

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("document_versions.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        server_default=AnalysisStatus.PENDING.value,
    )
    model: Mapped[str] = mapped_column(String(100))
    input_tokens: Mapped[int | None]
    output_tokens: Mapped[int | None]
    error: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Finding(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "findings"
    __table_args__ = (
        CheckConstraint(_in_list("severity", Severity), name="severity_valid"),
    )

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analyses.id", ondelete="CASCADE"),
        index=True,
    )
    clause_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("clauses.id", ondelete="CASCADE"),
        index=True,
    )
    severity: Mapped[str] = mapped_column(String(10))
    category: Mapped[str] = mapped_column(String(50))
    explanation: Mapped[str] = mapped_column(Text)
    suggested_text: Mapped[str | None] = mapped_column(Text)