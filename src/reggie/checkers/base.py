"""Base classes for registration checkers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from selenium.webdriver.chrome.webdriver import WebDriver

from ..constants import ResultKeys, StatusValues

# Global registry for checker classes
_CHECKER_CLASSES: list[type[BaseRegistrationChecker]] = []


def register_checker(
    checker_class: type[BaseRegistrationChecker],
) -> type[BaseRegistrationChecker]:
    """
    Decorator to register a checker class.

    Args:
        checker_class: The checker class to register

    Returns:
        The same checker class (for decorator chaining)
    """
    _CHECKER_CLASSES.append(checker_class)
    return checker_class


def get_registered_checkers() -> list[type[BaseRegistrationChecker]]:
    """
    Get all registered checker classes.

    Returns:
        List of registered checker classes
    """
    return _CHECKER_CLASSES.copy()


class BaseRegistrationChecker(ABC):
    """Abstract base class for registration checkers."""

    def __init__(self, driver: WebDriver | None):
        """
        Initialize the checker with a WebDriver instance.

        Args:
            driver: WebDriver instance. Can be None for getting metadata only.
        """
        self.driver = driver

    @property
    @abstractmethod
    def registration_body_name(self) -> str:
        """Return the name of the registration body this checker handles."""

    @abstractmethod
    def check_registration(self, reg_number: str, **kwargs) -> dict[str, Any]:
        """
        Check registration status for the given registration number.

        Args:
            reg_number: The registration number to check
            **kwargs: Additional parameters specific to the checker

        Returns:
            Dictionary with registration details including status
        """

    # def create_registration(
    #     self, reg_body: str, reg_number: str, status_data: Dict[str, Any]
    # ) -> Registration:
    #     """
    #     Create a Registration object from status data.

    #     Args:
    #         reg_body: Name of the registration body
    #         reg_number: Registration number
    #         status_data: Data returned from check_registration

    #     Returns:
    #         Registration object
    #     """
    #     status = status_data.get("status", "unknown")
    #     additional_data = {k: v for k, v in status_data.items() if k != "status"}

    #     return Registration(
    #         reg_body=reg_body,
    #         reg_number=reg_number,
    #         reg_status=status,
    #         additional_data=additional_data if additional_data else None,
    #     )

    def handle_error(self, reg_number: str, error: Exception) -> dict[str, Any]:
        """
        Handle errors during registration checking.

        Args:
            reg_number: The registration number being checked
            error: The exception that occurred

        Returns:
            Error status dictionary
        """
        return {
            ResultKeys.STATUS: StatusValues.ERROR,
            ResultKeys.ERROR_MESSAGE: str(error),
            ResultKeys.REG_NUMBER: reg_number,
        }


class RegistrationCheckerRegistry:
    """Registry for managing registration checkers."""

    def __init__(self):
        """Initialize the registry."""
        self._checkers: dict[str, BaseRegistrationChecker] = {}

    def register(self, checker: BaseRegistrationChecker) -> None:
        """Register a checker for a registration body."""
        self._checkers[checker.registration_body_name] = checker

    def get_checker(self, registration_body: str) -> BaseRegistrationChecker | None:
        """Get a checker for the specified registration body."""
        return self._checkers.get(registration_body)

    def list_supported_bodies(self) -> list[str]:
        """List all supported registration bodies."""
        return list(self._checkers.keys())

    def is_supported(self, registration_body: str) -> bool:
        """Check if a registration body is supported."""
        return registration_body in self._checkers
