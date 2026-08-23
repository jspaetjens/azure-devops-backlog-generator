"""Configuration-specific exceptions."""


class ConfigurationError(Exception):
    """Base class for controlled configuration failures."""


class ConfigurationFileError(ConfigurationError):
    """Raised when the selected configuration file cannot be used."""


class ConfigurationValidationError(ConfigurationError):
    """Raised when configuration does not meet the Version 1.0 contract."""


class ConfigurationUsageError(ConfigurationError):
    """Raised for invalid use of the supported configuration CLI option."""
