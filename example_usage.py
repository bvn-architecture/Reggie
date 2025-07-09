#!/usr/bin/env python3
"""
Example usage of the Arch Reggie registration checker package.

This script demonstrates the basic usage patterns shown in the README.
"""

import sys
from pathlib import Path

# Add the package to the path for development
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from reggie import RegistrationProcessor, ProcessingConfig


def basic_usage_example():
    """Demonstrate basic usage with default configuration."""
    print("=== Basic Usage Example ===")

    # Initialize with default configuration
    processor = RegistrationProcessor()

    # Process a CSV file (using test data)
    csv_path = "tests/test_data/example_input.csv"

    if Path(csv_path).exists():
        print(f"Processing: {csv_path}")
        results = processor.process_csv(csv_path)

        # Save results as JSON
        processor.save_json(results, "example_output.json")

        print(f"Processed {len(results)} people")
        print("Results saved to: example_output.json")
    else:
        print(f"Test CSV file not found at: {csv_path}")


def custom_config_example():
    """Demonstrate usage with custom configuration."""
    print("\n=== Custom Configuration Example ===")

    # Create custom configuration
    config = ProcessingConfig(
        # Column mappings for CSV without headers
        column_names=[
            "Email",
            "Full Name",
            "LinkedIn URL",
            "State Board Name",
            "Registration Number",
            "State Board Code",
        ],
        # Column mappings
        email_column="Email",
        full_name_column="Full Name",
        reg_body_column="State Board Name",
        reg_number_column="Registration Number",
        # Processing options
        output_format="json",
        selenium_headless=True,  # Run browser in background
        check_registrations=True,  # Actually check registrations online
        selenium_implicit_wait=5,
    )

    processor = RegistrationProcessor(config=config)

    # Show supported registration bodies
    supported_bodies = processor.get_supported_bodies()
    print(f"Supported registration bodies: {supported_bodies}")


def main():
    """Run all examples."""
    print("Arch Reggie - Example Usage")
    print("=" * 40)

    try:
        basic_usage_example()
        custom_config_example()

        print("\n✅ Examples completed successfully!")

    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
