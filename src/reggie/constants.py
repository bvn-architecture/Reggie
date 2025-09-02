"""Constants and default configurations for the registration checker package."""

from typing import List, Dict, Any

# Known registration bodies that are not yet automatically checked
KNOWN_UNCHECKED_REGISTRATION_BODIES = {
    "Victorian Architects Registration Board",
    "South Australian Architects Board",
    "Western Australian Architects Board",
    "Tasmanian Architects Board",
    "Northern Territory Architects Registration Board",
    "ACT Architects Registration Board",
    "Engineers Australia",
    "Australian Institute of Building Surveyors",
    # Add more known bodies here as needed
}

# Default configuration values - all in one place
DEFAULT_CONFIG = {
    # CSV column names for headerless CSV files
    "column_names": [
        "email",
        "full_name",
        "linkedin_url",
        "reg_body",
        "reg_number",
        "state_board_code",
    ],
    # Column mappings
    "email_column": "email",
    "full_name_column": "full_name",
    "linked_in_url_column": "linkedin_url",
    "reg_body_column": "reg_body",
    "reg_number_column": "reg_number",
    "state_column": "state_board_code",
    # Processing options
    "check_registrations": True,
    "output_format": "json",
    "selenium_headless": True,
    "selenium_implicit_wait": 10,
    "driver_cache_dir": "driver",
}


# Result keys used by registration checkers
class ResultKeys:
    """Standard keys used in registration checker result dictionaries."""

    STATUS = "status"
    NAME = "name"
    REG_NUMBER = "reg_number"
    ORIGINAL_STATUS = "original_status"
    ERROR_MESSAGE = "error_message"


# Common status values
class StatusValues:
    """Common status values returned by checkers."""

    NOT_FOUND = "not found"
    ERROR = "error"
    CURRENT_AND_ACTIVE = "current and active"


def get_default_config(**overrides) -> Dict[str, Any]:
    """
    Get the default configuration with optional overrides.

    Args:
        **overrides: Any configuration values to override

    Returns:
        Dict containing the default configuration with overrides applied

    Example:
        # Get default config with custom column names
        config_dict = get_default_config(
            column_names=["email", "name", "linkedin", "body", "number", "state"],
            selenium_headless=False
        )
        config = ProcessingConfig(**config_dict)
    """
    config = DEFAULT_CONFIG.copy()
    config.update(overrides)
    return config
