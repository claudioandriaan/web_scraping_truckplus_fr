 
Web-scraping template that follows SOLID principles. This repository provides a small, opinionated structure for building scrapers with clear separation of concerns: HTTP client, parsing logic, repository (persistence) and service orchestration.

## Requirements
- Python 3.10+

## Installation
1. Create a virtual environment and activate it:

```powershell
python -m venv myenv
```

2. Install dependencies

```powershell
pip install -r requirements.txt  
```

## Project layout
- `main.py` — CLI / entrypoint for running the scraper
- `http_client.py` — thin HTTP abstraction for requests
- `parser.py` — parsing rules and extraction logic
- `repository.py` — persistence/storage abstraction
- `service.py` — business logic that composes client/parser/repository
- `tests/` — unit tests for `parser`, `repository`, and `service`

## Usage
- Run the scraper:

```powershell
python main.py
```


