# SPDX-License-Identifier: MIT

"""Custom exception classes for domain errors."""


class DomainError(Exception):
    """Base class for all domain-specific errors."""


class DataValidationError(DomainError):
    """Raised when input data fails domain validation rules."""


class DataNotAvailableError(DomainError):
    """Raised when required data is missing from an external source."""
