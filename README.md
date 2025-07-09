# Arch Reggie

A Python package for checking professional registration status across various certification bodies, particularly useful for architecture and design professionals.

## Features

- Check registration status across multiple Australian professional bodies
- Process CSV files containing registration data
- Output results in JSON format
- Extensible plugin system for adding new registration checkers
- Built-in web scraping with Selenium
- Configurable column mappings and data processing

## Installation

```bash
pip install arch-reggie
```

## Quick Start

```python
from reggie import RegistrationProcessor

# Initialize the processor
processor = RegistrationProcessor()

# Process a CSV file
results = processor.process_csv("path/to/your/registrations.csv")

# Save results as JSON
processor.save_json(results, "output.json")
```

## Supported Registration Bodies

- NSW Architects Registration Board
- Board of Architects of Queensland
- Northern Territory Architects Board
- Architects Registration Board of Victoria
- Registered Design Practitioner NSW

## Configuration

The package supports flexible configuration for column mappings and processing options:

```python
config = {
    "columns": {
        "email": "email_address",
        "full_name": "name",
        "reg_number": "registration_number"
    },
    "output_format": "json"
}

processor = RegistrationProcessor(config=config)
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
