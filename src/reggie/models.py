"""Data models for the registration checker package."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from .constants import KNOWN_UNCHECKED_REGISTRATION_BODIES, DEFAULT_CONFIG


class RegistrationStatus(Enum):
    """Enumeration of possible registration statuses."""

    CURRENT_AND_ACTIVE = "current and active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    RETIRED = "retired"
    NOT_FOUND = "not found"
    UNKNOWN = "unknown"
    NOT_CHECKED_AUTOMATICALLY = "not checked automatically, check manually"
    ERROR = "error, check manually"


@dataclass
class Registration:
    """Represents a professional registration."""

    reg_body: Optional[str]
    reg_number: Optional[str]
    reg_status: Union[
        str, RegistrationStatus
    ]  # Accept string, will convert to enum in __post_init__
    additional_data: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Convert string status to enum if needed."""
        if isinstance(self.reg_status, str):
            # First, try to find matching enum value
            for status_enum in RegistrationStatus:
                if status_enum.value == self.reg_status:
                    self.reg_status = status_enum
                    return

            # If no match found, check if this is a known but unchecked body
            if self.reg_body and self.reg_body in KNOWN_UNCHECKED_REGISTRATION_BODIES:
                self.reg_status = RegistrationStatus.NOT_CHECKED_AUTOMATICALLY
                # Store the specific body message in additional_data
                if not self.additional_data:
                    self.additional_data = {}
                self.additional_data["status_message"] = (
                    f"{self.reg_body} is not checked automatically yet, check manually"
                )
                return

            # If no match found and not a known unchecked body, default to ERROR
            self.reg_status = RegistrationStatus.ERROR

    @property
    def status_message(self) -> str:
        """Get the status message, including dynamic body-specific messages."""
        if (
            self.reg_status == RegistrationStatus.NOT_CHECKED_AUTOMATICALLY
            and self.additional_data
            and "status_message" in self.additional_data
        ):
            return self.additional_data["status_message"]
        return self.reg_status.value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "reg_body": self.reg_body,
            "reg_number": self.reg_number,
            "reg_status": self.status_message,  # Use status_message for dynamic messages
        }
        if self.additional_data:
            # Don't include the status_message in additional_data since it's already in reg_status
            filtered_additional = {
                k: v for k, v in self.additional_data.items() if k != "status_message"
            }
            if filtered_additional:
                result.update(filtered_additional)
        return result


@dataclass
class Person:
    """Represents a person with their registrations."""

    full_name: str
    email: str
    linked_in_url: Optional[str] = None
    registrations: List[Registration] = field(default_factory=list)

    @property
    def live_rego_count(self) -> int:
        """Count of current and active registrations."""
        if not self.registrations:
            return 0
        return sum(
            1
            for reg in self.registrations
            if reg.reg_status == RegistrationStatus.CURRENT_AND_ACTIVE
        )

    def add_registration(self, registration: Registration) -> None:
        """Add a registration to this person."""
        self.registrations.append(registration)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "full_name": self.full_name,
            "email": self.email,
            "linked_in_url": self.linked_in_url,
            "registrations": [reg.to_dict() for reg in self.registrations],
            "live_rego_count": self.live_rego_count,
        }


@dataclass
class ProcessingConfig:
    """Configuration for the registration processor."""

    # Column mappings - defaults from centralized config
    email_column: str = DEFAULT_CONFIG["email_column"]
    full_name_column: str = DEFAULT_CONFIG["full_name_column"]
    linked_in_url_column: str = DEFAULT_CONFIG["linked_in_url_column"]
    reg_body_column: str = DEFAULT_CONFIG["reg_body_column"]
    reg_number_column: str = DEFAULT_CONFIG["reg_number_column"]
    state_column: str = DEFAULT_CONFIG["state_column"]

    # CSV handling options - default column names for headerless CSVs
    column_names: Optional[List[str]] = field(
        default_factory=lambda: DEFAULT_CONFIG["column_names"].copy()
    )

    # Processing options
    check_registrations: bool = DEFAULT_CONFIG["check_registrations"]
    output_format: str = DEFAULT_CONFIG["output_format"]
    selenium_headless: bool = DEFAULT_CONFIG["selenium_headless"]
    selenium_implicit_wait: int = DEFAULT_CONFIG["selenium_implicit_wait"]

    # File paths
    driver_cache_dir: str = DEFAULT_CONFIG["driver_cache_dir"]
    output_file: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "columns": {
                "email": self.email_column,
                "full_name": self.full_name_column,
                "linked_in_url": self.linked_in_url_column,
                "reg_body": self.reg_body_column,
                "reg_number": self.reg_number_column,
                "state": self.state_column,
            },
            "csv_handling": {
                "column_names": self.column_names,
            },
            "processing": {
                "check_registrations": self.check_registrations,
                "output_format": self.output_format,
                "selenium_headless": self.selenium_headless,
                "selenium_implicit_wait": self.selenium_implicit_wait,
            },
            "paths": {
                "driver_cache_dir": self.driver_cache_dir,
                "output_file": self.output_file,
            },
        }
