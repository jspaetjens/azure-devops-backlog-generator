"""Controlled failures raised while processing backlog-input documentation."""


class DocumentationProcessingError(Exception):
    """Base class for controlled documentation-processing failures."""


class DocumentationReadError(DocumentationProcessingError):
    """Raised when an eligible source document cannot be read."""


class DocumentationValidationError(DocumentationProcessingError):
    """Raised when source documentation violates the input contract."""
