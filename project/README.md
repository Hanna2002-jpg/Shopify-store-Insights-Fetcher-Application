# Shopify Store Insights Fetcher

A comprehensive Python web application that extracts and organizes data from Shopify websites without using the official Shopify API. The application provides detailed brand insights through a RESTful API interface.

## 🌟 Features

### Core Functionality
- **Complete Product Catalog**: Extracts all products using Shopify's JSON API and HTML parsing
- **Hero Products**: Identifies featured products from the homepage
- **Policy Information**: Extracts privacy, return, refund, and terms of service policies
- **FAQ Extraction**: Structured question-answer pairs from FAQ pages
- **Contact Information**: Email addresses, phone numbers, social media handles
- **Brand Context**: About us content, mission, and brand story
- **Important Links**: Order tracking, contact pages, blogs, careers

### Technical Features
- **Asynchronous Processing**: Fast, concurrent data extraction
- **Intelligent Content Detection**: Adapts to different Shopify themes
- **Error Handling**: Comprehensive error handling with graceful fallbacks
- **Data Validation**: Pydantic models for robust data validation
- **Rate Limiting**: Respectful scraping practices
- **RESTful API**: Clean, documented API endpoints

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd shopify-insights-fetcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoint

**POST /api/fetch-insights**

Extract comprehensive insights from a Shopify store.

```json
{
  "website_url": "https://memy.co.in",
  "include_products": true,
  "include_policies": true,
  "include_faqs": true,
  "include_contact": true,
  "max_products": 100
}
```

**Response:**
```json
{
  "status": "success",
  "brand_name": "Memy",
  "website_url": "https://memy.co.in",
  "data": {
    "products": {
      "catalog": [...],
      "hero_products": [...],
      "total_count": 50,
      "featured_collections": [...]
    },
    "policies": {
      "privacy_policy": "...",
      "return_policy": "...",
      "refund_policy": "..."
    },
    "faqs": [
      {
        "question": "Do you have COD as a payment option?",
        "answer": "Yes, we do have COD available"
      }
    ],
    "contact_info": {
      "emails": ["contact@memy.co.in"],
      "phones": ["+91-1234567890"],
      "social_handles": {
        "instagram": "memy_official",
        "facebook": "memyofficial"
      }
    },
    "brand_context": {
      "about": "Memy is a premium lifestyle brand...",
      "mission": "To provide high-quality products..."
    },
    "important_links": {
      "order_tracking": "https://memy.co.in/pages/track-order",
      "contact_us": "https://memy.co.in/pages/contact",
      "blog": "https://memy.co.in/blogs/news"
    }
  },
  "extraction_timestamp": "2024-01-01T12:00:00Z",
  "processing_time_seconds": 15.32,
  "errors": [],
  "warnings": []
}
```

### Additional Endpoints

**GET /api/validate-url**
```
GET /api/validate-url?website_url=https://example.com
```

**GET /api/supported-features**
```
GET /api/supported-features
```

## 🔧 Configuration

The application can be configured through `core/config.py`:

- `REQUEST_TIMEOUT`: Timeout for HTTP requests (default: 30s)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)
- `RATE_LIMIT_DELAY`: Delay between requests (default: 1s)

## 🧪 Testing

Test the API using the provided examples:

### Using cURL
```bash
curl -X POST "http://localhost:8000/api/fetch-insights" \
  -H "Content-Type: application/json" \
  -d '{"website_url": "https://memy.co.in"}'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/api/fetch-insights",
    json={"website_url": "https://memy.co.in"}
)

data = response.json()
print(f"Extracted {data['data']['products']['total_count']} products")
```

## 📁 Project Structure

```
shopify-insights-fetcher/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── core/
│   ├── __init__.py
│   └── config.py          # Application configuration
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic data models
├── services/
│   ├── __init__.py
│   ├── web_scraper.py     # Web scraping functionality
│   └── insights_service.py # Business logic for insights extraction
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
└── api/
    ├── __init__.py
    └── routes.py          # API endpoints
```

## 🛠️ Architecture

The application follows SOLID principles with clean separation of concerns:

- **Models**: Pydantic schemas for data validation
- **Services**: Business logic for web scraping and data extraction
- **API**: RESTful endpoints with comprehensive error handling
- **Utils**: Helper functions for text processing and validation
- **Core**: Application configuration and settings

## ⚡ Performance Features

- **Asynchronous Processing**: Uses async/await for concurrent operations
- **Smart Extraction**: Tries JSON API first, falls back to HTML parsing
- **Rate Limiting**: Respects website resources with configurable delays
- **Caching Ready**: Architecture supports future caching implementation
- **Error Recovery**: Graceful handling of failed extractions

## 🔍 Supported Shopify Stores

The application works with various Shopify store configurations:
- Custom domains (e.g., memy.co.in)
- myshopify.com subdomain stores
- Different Shopify themes and layouts
- Stores with custom navigation structures

### Tested Examples
- memy.co.in
- hairoriginals.com
- Any store from the top 100 successful Shopify stores

## 📋 Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Timeout and connection error handling
- **Invalid URLs**: URL format validation
- **Content Parsing**: Graceful handling of missing content
- **Rate Limiting**: Automatic retry with backoff
- **Partial Success**: Returns available data even if some extractions fail

## 🚦 Status Codes

- `200`: Successful extraction
- `400`: Invalid request parameters
- `404`: Website not found
- `408`: Request timeout
- `500`: Internal server error

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include type hints
4. Write descriptive docstrings
5. Test with multiple Shopify stores

## 📄 License

This project is for educational and research purposes. Please respect website terms of service and robots.txt files when using this application.

## ⚠️ Disclaimer

This application extracts publicly available information from websites. Users are responsible for ensuring compliance with website terms of service and applicable laws. The application implements respectful scraping practices with rate limiting and proper user agent headers.