"""Typed failures for bounded document intake."""


class IntakeRejectedError(Exception):
    """Base failure for an upload rejected before provider processing."""


class ByteLimitExceededError(IntakeRejectedError):
    """Report content that exceeds the configured byte boundary."""

    def __init__(self, max_bytes: int) -> None:
        super().__init__(f"upload exceeds the {max_bytes}-byte limit")
        self.max_bytes = max_bytes


class PageLimitExceededError(IntakeRejectedError):
    """Report a document that exceeds the configured page boundary."""

    def __init__(self, max_pages: int) -> None:
        super().__init__(f"document exceeds the {max_pages}-page limit")
        self.max_pages = max_pages


class ActiveUploadExistsError(IntakeRejectedError):
    """Report a second upload submitted for an active session."""


class UnsupportedMediaTypeError(IntakeRejectedError):
    """Report content whose declared media type is unsupported."""


class UnreadableDocumentError(IntakeRejectedError):
    """Report content whose document structure cannot be read safely."""


class InvalidCms2567Error(IntakeRejectedError):
    """Report readable content that is not identifiable as CMS-2567."""