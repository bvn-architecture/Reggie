# Arch Reggie

A Python package for checking professional registration status across various certification bodies, particularly useful for architecture.

It can check the NSW and QLD ARBs at the moment, but there's potential to add more in the future.

## Installation

```bash
pip install arch-reggie
```

## Quick Start

```python
from reggie import RegistrationProcessor, ProcessingConfig

# Initialize with default configuration
processor = RegistrationProcessor()

# Process a CSV file
results = processor.process_csv("path/to/your/registrations.csv")

# Save results as JSON
processor.save_json(results, "output.json")
```

## Supported Registration Bodies

- NSW Architects Registration Board
- Board of Architects of Queensland
- ~Northern Territory Architects Board~ not yet
- ~Architects Registration Board of Victoria~ not yet
- ~Registered Design Practitioner NSW~ not yet

## Configuration

The package supports flexible configuration for column mappings and processing options:

```python
from reggie import RegistrationProcessor, ProcessingConfig

# Create custom configuration
config = ProcessingConfig(
    # Column mappings for your CSV
    email_column="email_address",
    full_name_column="name", 
    reg_body_column="registration_body",
    reg_number_column="registration_number",
    
    # Processing options
    output_format="json",
    selenium_headless=True,
    check_registrations=True
)

processor = RegistrationProcessor(config=config)
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
