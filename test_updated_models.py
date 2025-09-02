#!/usr/bin/env python3
"""Test the updated models with known unchecked registration bodies."""

from src.reggie.models import (
    Registration,
    RegistrationStatus,
    KNOWN_UNCHECKED_REGISTRATION_BODIES,
)


def test_known_unchecked_body():
    """Test that known unchecked bodies get the correct status and message."""
    # Test with a known unchecked body
    reg = Registration(
        reg_body="Victorian Architects Registration Board",
        reg_number="12345",
        reg_status="some unknown status",  # This should trigger the unchecked body logic
    )

    print(f"Registration body: {reg.reg_body}")
    print(f"Status enum: {reg.reg_status}")
    print(f"Status message: {reg.status_message}")
    print(f"Additional data: {reg.additional_data}")
    print(f"To dict: {reg.to_dict()}")
    print()


def test_unknown_body():
    """Test that unknown bodies still get ERROR status."""
    reg = Registration(
        reg_body="Unknown Registration Board",
        reg_number="12345",
        reg_status="some unknown status",
    )

    print(f"Registration body: {reg.reg_body}")
    print(f"Status enum: {reg.reg_status}")
    print(f"Status message: {reg.status_message}")
    print(f"Additional data: {reg.additional_data}")
    print(f"To dict: {reg.to_dict()}")
    print()


def test_existing_valid_status():
    """Test that existing valid statuses still work."""
    reg = Registration(
        reg_body="NSW Architects Registration Board",
        reg_number="12345",
        reg_status="current and active",
    )

    print(f"Registration body: {reg.reg_body}")
    print(f"Status enum: {reg.reg_status}")
    print(f"Status message: {reg.status_message}")
    print(f"Additional data: {reg.additional_data}")
    print(f"To dict: {reg.to_dict()}")
    print()


if __name__ == "__main__":
    print("Known unchecked registration bodies:")
    for body in KNOWN_UNCHECKED_REGISTRATION_BODIES:
        print(f"  - {body}")
    print()

    print("=== Testing known unchecked body ===")
    test_known_unchecked_body()

    print("=== Testing unknown body ===")
    test_unknown_body()

    print("=== Testing existing valid status ===")
    test_existing_valid_status()
