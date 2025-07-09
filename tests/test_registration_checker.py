"""Tests for the registration checker package."""

import pytest
import pandas as pd
from reggie.models import Person, Registration, ProcessingConfig
from reggie.core import RegistrationProcessor


def test_person_creation():
    """Test creating a Person object."""
    person = Person(
        full_name="John Doe",
        email="john@example.com",
        linked_in_url="https://linkedin.com/in/johndoe",
    )

    assert person.full_name == "John Doe"
    assert person.email == "john@example.com"
    assert person.live_rego_count == 0
    assert len(person.registrations) == 0


def test_registration_creation():
    """Test creating a Registration object."""
    reg = Registration(
        reg_body="NSW Architects Registration Board",
        reg_number="12345",
        reg_status="current and active",
    )

    assert reg.reg_body == "NSW Architects Registration Board"
    assert reg.reg_number == "12345"
    assert reg.reg_status == "current and active"


def test_person_with_registration():
    """Test person with registrations."""
    person = Person(full_name="Jane Doe", email="jane@example.com")

    reg = Registration(
        reg_body="NSW Architects Registration Board",
        reg_number="54321",
        reg_status="current and active",
    )

    person.add_registration(reg)

    assert len(person.registrations) == 1
    assert person.live_rego_count == 1


def test_processor_config():
    """Test processor configuration."""
    config = ProcessingConfig(email_column="email_address", check_registrations=False)

    processor = RegistrationProcessor(config=config)

    assert processor.config.email_column == "email_address"
    assert processor.config.check_registrations is False


def test_person_to_dict():
    """Test converting person to dictionary."""
    person = Person(full_name="Test Person", email="test@example.com")

    reg = Registration(
        reg_body="Test Body", reg_number="123", reg_status="current and active"
    )

    person.add_registration(reg)

    data = person.to_dict()

    assert data["full_name"] == "Test Person"
    assert data["email"] == "test@example.com"
    assert data["live_rego_count"] == 1
    assert len(data["registrations"]) == 1
    assert data["registrations"][0]["reg_body"] == "Test Body"
