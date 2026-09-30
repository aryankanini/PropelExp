"""Coordinate bounded upload, local validation, and transient case creation."""

from collections.abc import Iterable
from uuid import uuid4

from application.intake.cms2567_validator import Cms2567Validator
from application.intake.commands import AcceptedUpload, UploadCommand, UploadLimits
from application.intake.errors import ActiveUploadExistsError
from application.intake.inspector import DocumentInspector
from application.intake.preflight import validate_media_type, validate_preflight
from application.intake.upload_guard import UploadGuard
from application.intake.validation_result import DocumentRejected
from application.ports.case_repository import CaseRepository
from application.ports.workspace import UploadHandle, Workspace
from application.services.stream_upload import StreamUpload
from domain.case.aggregate import CaseAggregate


class UploadService:
    """Create one extraction-ready transient case from a bounded upload."""

    def __init__(
        self,
        repository: CaseRepository,
        workspace: Workspace,
        inspector: DocumentInspector,
        guard: UploadGuard,
        limits: UploadLimits = UploadLimits(),
    ) -> None:
        self._repository = repository
        self._workspace = workspace
        self._inspector = inspector
        self._guard = guard
        self._limits = limits
        self._stream_upload = StreamUpload(workspace, limits)
        self._validator = Cms2567Validator()

    def execute(
        self,
        command: UploadCommand,
        chunks: Iterable[bytes],
    ) -> AcceptedUpload | DocumentRejected:
        with self._guard.reserve(command.session_id):
            if self._repository.contains(command.session_id):
                raise ActiveUploadExistsError(command.session_id)
            validate_media_type(command.media_type)
            metadata = self._stream_upload.execute(
                session_id=command.session_id,
                client_filename=command.client_filename,
                chunks=chunks,
            )
            handle = UploadHandle(command.session_id, metadata.upload_id)
            try:
                inspection = self._inspector.inspect(
                    handle,
                    command.media_type,
                    self._limits.max_pages,
                )
                validate_preflight(command.media_type, inspection, self._limits)
                validation = self._validator.validate(inspection)
                if isinstance(validation, DocumentRejected):
                    self._workspace.discard(handle)
                    return validation

                case_id = uuid4().hex
                self._repository.add(
                    CaseAggregate(
                        session_id=command.session_id,
                        case_id=case_id,
                        documents=(metadata.upload_id,),
                    )
                )
                return AcceptedUpload(
                    case_id=case_id,
                    upload_id=metadata.upload_id,
                    size_bytes=metadata.size_bytes,
                    page_count=validation.page_count,
                )
            except Exception:
                self._workspace.discard(handle)
                raise