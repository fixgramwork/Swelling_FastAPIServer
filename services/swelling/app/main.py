from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from swelling_common.health import health_payload


app = FastAPI(title="Swelling Service", version="0.1.0")


class SwellingReportCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    body_part: str = Field(..., min_length=1, max_length=80)
    severity: int = Field(..., ge=1, le=5)
    memo: str | None = Field(default=None, max_length=500)


class SwellingReport(BaseModel):
    id: str
    user_id: str
    body_part: str
    severity: int
    memo: str | None
    created_at: datetime


reports: dict[str, SwellingReport] = {}


@app.get("/health", tags=["health"])
async def health() -> dict[str, object]:
    return health_payload("swelling")


@app.post(
    "/reports",
    response_model=SwellingReport,
    status_code=status.HTTP_201_CREATED,
    tags=["reports"],
)
async def create_report(payload: SwellingReportCreate) -> SwellingReport:
    report = SwellingReport(
        id=str(uuid4()),
        user_id=payload.user_id,
        body_part=payload.body_part,
        severity=payload.severity,
        memo=payload.memo,
        created_at=datetime.now(UTC),
    )
    reports[report.id] = report
    return report


@app.get("/reports", response_model=list[SwellingReport], tags=["reports"])
async def list_reports() -> list[SwellingReport]:
    return list(reports.values())


@app.get("/reports/{report_id}", response_model=SwellingReport, tags=["reports"])
async def get_report(report_id: str) -> SwellingReport:
    report = reports.get(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.get("/users/{user_id}/reports", response_model=list[SwellingReport], tags=["reports"])
async def list_user_reports(user_id: str) -> list[SwellingReport]:
    return [report for report in reports.values() if report.user_id == user_id]
