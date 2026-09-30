"""FastAPI adapter for authoritative retention status."""

from typing import Annotated

from fastapi import APIRouter, Header

from application.session_status import GetSessionStatus, SessionStatus


def create_session_status_router(query: GetSessionStatus) -> APIRouter:
    """Create a status route that never extends session activity."""
    router = APIRouter(prefix="/api/v1/session", tags=["session"])

    @router.get("/status", response_model=SessionStatus)
    def get_status(
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> SessionStatus:
        return query.execute(session_id)

    return router