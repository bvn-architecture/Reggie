"""Registration Checker - A package for checking professional registration status."""

from .checkers.base import BaseRegistrationChecker, RegistrationCheckerRegistry
from .core import RegistrationProcessor
from .models import Person, ProcessingConfig, Registration, RegistrationStatus

__version__ = "0.1.0"
__author__ = "Ben Doherty"
__email__ = "ben_doherty@bvn.com.au"

__all__ = [
    "BaseRegistrationChecker",
    "Person",
    "ProcessingConfig",
    "Registration",
    "RegistrationCheckerRegistry",
    "RegistrationProcessor",
    "RegistrationStatus",
]
