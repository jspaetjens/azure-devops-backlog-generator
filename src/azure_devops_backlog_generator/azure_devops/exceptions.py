"""Controlled failures raised by the Azure DevOps REST Client Foundation."""


class AzureDevOpsRestClientError(Exception):
    """Base class for controlled Azure DevOps REST Client failures."""


class AzureDevOpsTransportError(AzureDevOpsRestClientError):
    """Raised when an Azure DevOps request cannot complete at the transport layer."""


class AzureDevOpsHttpError(AzureDevOpsRestClientError):
    """Raised when Azure DevOps returns an unexpected HTTP status."""

    def __init__(self, status: int) -> None:
        self.status = status
        super().__init__(f"Azure DevOps returned unexpected HTTP status {status}.")


class AzureDevOpsResponseError(AzureDevOpsRestClientError):
    """Raised when a successful Azure DevOps response cannot be used."""


class AzureDevOpsCompatibilityError(AzureDevOpsRestClientError):
    """Raised when supplied Azure DevOps metadata is structurally incompatible."""
