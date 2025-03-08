# FinAgent

A financial news and data agent for collecting, storing, and analyzing financial information.

## Installation

```bash
# From the root agents directory
pip install -e ./finagent

# Or directly from the finagent directory
pip install -e .
```

## Usage

FinAgent can be used through its command-line interface:

```bash
# List available commands
finagent --help

# Fetch news for a company using NewsAPI
finagent fetch-news --company "HDFC Bank" --limit 10

# Fetch news using Google News API
finagent fetch-gnews --company "HDFC Bank" --limit 10 --country "in"

# Display stored news for a company
finagent show-news --company "HDFC Bank"

# Process and save collected news to a JSON file
finagent process --company "HDFC Bank" --output "hdfc_news.json"

# List all companies with stored news
finagent list-companies

# Get or set configuration values
finagent config
finagent config set news_provider "gnews"
```

## Command Details

### `fetch-news`
Fetches news articles from NewsAPI and stores the raw responses.

```bash
finagent fetch-news --company "HDFC Bank" --limit 5 --raw-dir "./data/raw_data"
```

Options:
- `--company`, `-c`: Company name or ticker symbol (required)
- `--limit`: Maximum number of articles to fetch (default: 5)
- `--raw-dir`: Directory to store raw API responses

### `fetch-gnews`
Fetches news articles from Google News API and stores the raw responses.

```bash
finagent fetch-gnews --company "HDFC Bank" --limit 10 --language "en" --country "us"
```

Options:
- `--company`, `-c`: Company name or ticker symbol (required)
- `--limit`: Maximum number of articles to fetch (default: 10)
- `--language`: Language code (default: "en")
- `--country`: Country code (default: "us")
- `--raw-dir`: Directory to store raw API responses

### `show-news`
Displays stored news articles for a specific company.

```bash
finagent show-news --company "HDFC Bank" --source "newsapi"
```

Options:
- `--company`, `-c`: Company name or ticker symbol (required)
- `--raw-dir`: Directory to read raw API responses from
- `--source`: News source to display ("all", "newsapi", or "gnews") (default: "all")

### `process`
Processes stored news articles and saves them to a JSON file.

```bash
finagent process --company "HDFC Bank" --output "hdfc_processed.json"
```

Options:
- `--company`, `-c`: Company name or ticker symbol (required)
- `--raw-dir`: Directory to read raw API responses from
- `--output`, `-o`: Output JSON file path

## Configuration

Create a `.env` file in your working directory with the following variables:

```
NEWS_API_KEY=your_news_api_key_here
GNEWS_API_KEY=your_gnews_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Data Storage

By default, FinAgent stores data in JSON format in the following locations:

- Raw news data: `./data/raw_data/`
- Company-specific data: `./data/{COMPANY_NAME}.json`

## Development

To run tests:

```bash
pytest tests/
```

To build the package:

```bash
pip install -e .
```

## License

[MIT License](LICENSE)