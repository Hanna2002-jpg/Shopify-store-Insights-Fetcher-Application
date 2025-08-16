# Shopify-store-Insights-Fetcher-Application


# Shopify Brand Insights API

![Python](https://img.shields.io/badge/python-3.13-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

## Overview

**Shopify Brand Insights API** is a Python-based project that extracts and stores Shopify brand information from website URLs. It provides a FastAPI backend with MySQL database integration and includes a test script for validating the service. This tool is designed to be scalable, allowing batch extraction for multiple websites while handling duplicates and database errors gracefully.

---

## Features

- **FastAPI Backend**: `/api/extract` endpoint for extracting brand information.  
- **Database Integration**: MySQL via SQLAlchemy ORM for persistent storage.  
- **Robust Service Layer**: `ShopifyInsightsService` handles data fetching, insertion, and error handling.  
- **Test Script**: `test_service.py` validates the service functionality.  
- **Dependencies**: BeautifulSoup4, Requests, LXML for web scraping and parsing.  
- **Error Handling**: Gracefully handles duplicate entries and database connection issues.

---

## Folder Structure

```

shopify-brand-insights/
│
├─ api/
│   ├─ **init**.py
│   └─ routes.py
│
├─ core/
│   ├─ **init**.py
│   └─ db.py
│
├─ models/
│   ├─ **init**.py
│   ├─ db\_models.py
│   └─ schemas.py
│
├─ services/
│   ├─ **init**.py
│   └─ insights\_service.py
│
├─ test\_service.py
├─ main.py
└─ requirements.txt

````

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/shopify-brand-insights.git
cd shopify-brand-insights
````

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Database Setup

1. Create a MySQL database:

```sql
CREATE DATABASE shopify_insights;
USE shopify_insights;
```

2. Update `core/db.py` with your MySQL credentials:

```python
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Koloth@2002@localhost/shopify_insights"
```

3. Make sure SQLAlchemy tables are created (if using `Base.metadata.create_all(engine)`).

---

## Running the FastAPI Server

```bash
python main.py
```

* The server will run at: `http://127.0.0.1:8000`
* Root endpoint:

```http
GET http://127.0.0.1:8000/
```

Response:

```json
{"message":"✅ API Running. Use POST /api/extract"}
```

---

## API Usage

### **POST /api/extract**

**Request Body:**

```json
{
  "website_url": "https://example.com"
}
```

**Curl Example:**

```bash
curl -X POST "http://127.0.0.1:8000/api/extract" \
-H "Content-Type: application/json" \
-d '{"website_url":"https://example.com"}'
```

**Response Example:**

```json
{
  "brand_name": "Example Brand",
  "website_url": "https://example.com"
}
```

---

## Testing the Service

`test_service.py` validates the `ShopifyInsightsService` class.

```bash
python test_service.py
```

**Expected Output:**

```
=== TESTING SHOPIFY INSIGHTS SERVICE ===
Testing service...
✅ Service imported successfully
Result type: <class 'dict'>
Result keys: ['brand_name', 'website_url']
✅ Service returned success
Brand name: Example Brand
Description: None
✅ Service test completed!
```

---

## Dependencies

* Python 3.13
* FastAPI
* Uvicorn
* SQLAlchemy
* MySQL Connector Python
* BeautifulSoup4
* Requests
* LXML

Install all dependencies via:

```bash
pip install fastapi uvicorn sqlalchemy mysql-connector-python beautifulsoup4 requests lxml
```

---

## Notes

* Make sure `services/__init__.py` and `api/__init__.py` exist, even if empty.
* Handle port conflicts on Windows (`WinError 10048`) by killing the previous process:

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

* To run on a different port:

```bash
uvicorn main:app --reload --port 8001
```

---

## Future Improvements

* Batch extraction for multiple Shopify URLs.
* More detailed brand insights (products, categories, reviews).
* Logging and monitoring for large-scale data collection.
* Dockerization for easy deployment.

---

## License

MIT License © \[HANNA ANSAR]


