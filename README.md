# PDGA_Stats

A clean, layered Python project for scraping PDGA (Professional Disc Golf Association) tournament data from the PDGA Live API.

## Overview

This project demonstrates best practices for building data ingestion + analytics pipelines with strict separation of concerns:

```
API Client (HTTP only) 
    ↓
Data Models (pure data structures)
    ↓
Orchestration (coordinate + parse)
    ↓
Storage (persist models)
```

**Key benefit:** Each layer can be tested, extended, and debugged independently.

## Quick Start

### Command Line Usage

```bash
# Scrape a single event to SQLite
python main.py --event 59876 --db pdga_data.db

# Scrape multiple events
python main.py --events 59876 59877 59878 --db pdga_data.db --csv output/

# See all options
python main.py --help
```

### Python Script Usage

```python
from pdga_scraper.scraper import scrape_event
from pdga_scraper.storage import SQLiteWriter

# Get clean model objects (no HTTP or parsing concerns)
event, round_scores, players = scrape_event(59876)

# Store them (storage layer accepts model objects)
db = SQLiteWriter("pdga_data.db")
db.create_tables()
db.save_event(event)
db.save_players(players)
db.save_round_scores(round_scores)
```

### Jupyter Notebook Usage

```python
from pdga_scraper.scraper import scrape_event
from pdga_scraper.models import *
import pandas as pd

# Scrape and work with clean models
event, scores, players = scrape_event(59876)

# Analyze with standard tools
scores_df = pd.DataFrame([asdict(s) for s in scores])
print(f"Average score: {scores_df['total_score'].mean():.1f}")
```

## Project Structure

```
pdga_scraper/
├── scraper/
│   ├── client.py          # API client (HTTP layer only)
│   ├── event.py           # Orchestration + parsing functions
│   └── *.py               # Ready for expansion (players, rounds, etc)
│
├── models/
│   ├── event.py           # Event dataclass
│   ├── player.py          # Player dataclass
│   ├── score.py           # HoleScore, RoundScore dataclasses
│   ├── course.py          # Course, Layout dataclasses
│   └── __init__.py        # Model exports
│
├── storage/
│   ├── sqlite_writer.py   # SQLite database persistence
│   ├── csv_writer.py      # CSV file export
│   ├── parquet_writer.py  # Parquet export (requires pandas)
│   └── __init__.py        # Storage exports
│
├── main.py                # CLI interface + workflows
├── ARCHITECTURE.md        # Detailed architecture docs
├── USAGE_GUIDE.md         # Practical usage examples
└── ARCHITECTURE_CHECKLIST.md  # Dev guidelines
```

## Architecture Layers

### 1. Client Layer (`scraper/client.py`)
- ONLY handles HTTP requests to PDGA Live API
- No parsing, no business logic
- Returns raw JSON responses
- Easy to debug: call client directly to inspect API responses

### 2. Domain Layer (`models/`)
- Pure data structures as dataclasses
- No HTTP calls, no parsing, no storage logic
- Can be used in notebooks independently
- Easy to extend with new data types

### 3. Orchestration Layer (`scraper/event.py`)
- Coordinates API calls (using client)
- Parses JSON into model objects
- Defines scraping workflows
- No HTTP calls, no storage calls
- Easy to test and reuse

### 4. Storage Layer (`storage/`)
- Accepts model objects only
- Handles persistence (SQLite, CSV, Parquet)
- Must NOT make API calls or parse JSON
- Easy to add new storage formats

## Key Features

✅ **Clean separation of concerns** - No layer violates its responsibility  
✅ **Independent testing** - Test each layer in isolation  
✅ **No circular dependencies** - Unidirectional dependency flow  
✅ **Easy to debug** - Call client directly to see raw API responses  
✅ **Easy to extend** - Add new endpoints, models, or storage formats  
✅ **Batch processing** - One event failure doesn't stop others  
✅ **Multiple output formats** - SQLite, CSV, and Parquet support  
✅ **Jupyter-friendly** - Use models and analysis in notebooks  

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete architecture guide with diagrams
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Practical examples (CLI, Python, Jupyter)
- **[ARCHITECTURE_CHECKLIST.md](ARCHITECTURE_CHECKLIST.md)** - Dev guidelines and best practices

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests pandas pyarrow
```

## Usage Examples

### Scrape event with database storage
```bash
python main.py --event 59876 --db pdga_data.db
```

### Scrape batch of events
```bash
python main.py --events 59876 59877 59878 --db pdga_data.db
```

### Export to CSV
```bash
python main.py --event 59876 --csv output/
```

### Combined: database + CSV
```bash
python main.py --event 59876 --db pdga_data.db --csv output/
```

### See all options
```bash
python main.py --help
```

## Design Philosophy

This project prioritizes:

1. **Clarity** over cleverness
2. **Separation of concerns** over integration
3. **Debuggability** over abstraction
4. **Extensibility** over completeness
5. **Testability** over convenience

Think of each layer as independent, reusable building blocks that can be:
- Used separately (import client for just API calls)
- Tested independently (mock one layer, test another)
- Extended without affecting others (add new endpoint = update client only)
- Debugged step-by-step (inspect raw API responses, parsed models, storage)

## Extending the Project

To add a new API endpoint:
1. Add method to `PDGAClient` in `scraper/client.py`
2. Create parsing function in `scraper/event.py`
3. Add orchestration function if needed
4. Storage layer already handles new models!

No existing code needs modification.

## Testing

Run parsing functions with sample data:

```python
from pdga_scraper.scraper.event import parse_event

sample_json = {"TournID": 123, "TournName": "Test"}
event = parse_event(sample_json)
assert event.id == 123
```

Mock API for testing:

```python
from unittest.mock import patch
from pdga_scraper.scraper import scrape_event

with patch('pdga_scraper.scraper.event.PDGAClient') as mock_client:
    # Configure mock responses
    event, scores, players = scrape_event(59876)
    # Run assertions
```

## Contributing

Please follow the guidelines in [ARCHITECTURE_CHECKLIST.md](ARCHITECTURE_CHECKLIST.md):
- Maintain layer separation
- No circular dependencies
- Add type hints and docstrings
- Include error handling
- Write tests for new functionality

## License

MIT

## Project Stats

- **Lines of Code:** ~800 (core logic)
- **Documentation:** ~1000 lines (extensive guides)
- **Test Coverage:** Ready for testing framework integration
- **API Methods:** 4 core endpoints implemented
- **Storage Formats:** SQLite, CSV, Parquet
- **Python Version:** 3.8+
