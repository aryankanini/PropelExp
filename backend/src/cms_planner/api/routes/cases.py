"""FastAPI adapter for streamed case intake."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, File, Header, UploadFile, status
from fastapi.responses import JSONResponse

from application.inactivity_policy import InactivityPolicy
from application.intake.commands import AcceptedUpload, UploadCommand
from application.intake.errors import (
    ActiveUploadExistsError,
    ByteLimitExceededError,
    PageLimitExceededError,
    UnsupportedMediaTypeError,
    UnreadableDocumentError,
)
from application.intake.upload_service import UploadService
from application.intake.validation_result import DocumentRejected
from cms_planner.api.schemas.intake import IntakeAccepted, IntakeProblem

UPLOAD_CHUNK_BYTES = 64 * 1024


def create_cases_router(
    upload_service: UploadService,
    inactivity_policy: InactivityPolicy,
) -> APIRouter:
    """Create the case intake route with application dependencies."""
    router = APIRouter(prefix="/api/v1/cases", tags=["cases"])

    @router.post(
        "",
        response_model=IntakeAccepted,
        status_code=status.HTTP_201_CREATED,
        responses={
            409: {"model": IntakeProblem},
            413: {"model": IntakeProblem},
            415: {"model": IntakeProblem},
            422: {"model": IntakeProblem},
        },
    )
    def upload_case(
        file: Annotated[UploadFile, File(description="CMS-2567 document")],
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> IntakeAccepted | JSONResponse:
        command = UploadCommand(
            session_id=session_id,
            client_filename=file.filename or "upload",
            media_type=file.content_type or "application/octet-stream",
        )
        try:
            result = upload_service.execute(command, _read_chunks(file))
        except ActiveUploadExistsError:
            return _problem(409, "active_upload_exists", "An active case already exists")
        except ByteLimitExceededError:
            return _problem(413, "byte_limit_exceeded", "The file exceeds 50 MB")
        except PageLimitExceededError:
            return _problem(422, "page_limit_exceeded", "The document exceeds 200 pages")
        except UnsupportedMediaTypeError:
            return _problem(415, "unsupported_media_type", "The file type is unsupported")
        except UnreadableDocumentError:
            return _problem(422, "unreadable", "The document could not be read")
        finally:
            file.file.close()

        if isinstance(result, DocumentRejected):
            message = (
                "The document could not be read"
                if result.reason == "unreadable"
                else "The document is not identifiable as CMS-2567"
            )
            return _problem(422, result.reason, message)

        inactivity_policy.start(session_id)
        return _accepted_response(result)

    return router


def _read_chunks(file: UploadFile) -> Iterator[bytes]:
    while chunk := file.file.read(UPLOAD_CHUNK_BYTES):
        yield chunk


def _accepted_response(result: AcceptedUpload) -> IntakeAccepted:
    return IntakeAccepted(**result.model_dump())


def _problem(status_code: int, code: str, message: str) -> JSONResponse:
    problem = IntakeProblem(code=code, message=message)
    return JSONResponse(status_code=status_code, content=problem.model_dump())