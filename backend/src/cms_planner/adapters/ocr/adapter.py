"""Guard outbound OCR invocation and map provider failures safely."""

from cms_planner.adapters.ocr.validation import validate_ocr_success
from cms_planner.application.ports.ocr import OcrPort
from cms_planner.application.ports.ocr_types import (
    OcrFailure,
    OcrPageRequest,
    OcrResult,
    OcrSuccess,
)
from cms_planner.application.provider_approval import (
    ProviderApproval,
    ProviderNotApprovedError,
    require_provider_approval,
)


class GuardedOcrAdapter:
    """Invoke an OCR provider only when its configuration is approved."""

    def __init__(
        self,
        provider: OcrPort,
        *,
        approval: ProviderApproval | None = None,
        approved: bool | None = None,
    ) -> None:
        self._provider = provider
        if approval is None:
            legacy_approval = bool(approved)
            approval = ProviderApproval(
                baa=legacy_approval,
                retention=legacy_approval,
                training_use=legacy_approval,
                risk=legacy_approval,
            )
        self._approval = approval

    async def recognize(self, request: OcrPageRequest) -> OcrResult:
        page_number = request.classification.page_number
        try:
            require_provider_approval(self._approval)
        except ProviderNotApprovedError:
            return OcrFailure(
                page_number=page_number,
                code="provider-not-approved",
            )

        try:
            response = await self._provider.recognize(request)
            if not isinstance(response, OcrSuccess):
                return response
            return validate_ocr_success(request, response)
        except ValueError:
            return OcrFailure(
                page_number=page_number,
                code="invalid-provider-response",
            )
        except Exception:
            return OcrFailure(page_number=page_number, code="provider-failed")