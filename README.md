# Fridge App API

A FastAPI-based REST API for a fridge inventory management application. It provides CRUD operations for tracking food products and includes an AI-powered recipe generation feature that suggests creative recipes based on available ingredients.

## Key Features

- Full CRUD operations for product inventory management
- Soft delete support (products are marked as discarded rather than permanently deleted)
- AI-powered recipe generation using OpenAI's GPT-4o model
- Supabase backend for data persistence
- CORS enabled for cross-origin requests

## Installation

1. Clone or download this repository into your desired directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon/public key
   - `OPENAI_API_KEY` - Your OpenAI API key (for recipe generation)
6. Run the development server: `fastapi dev main.py`
7. The API will be available at `http://localhost:8000`

## Key Endpoints

| Method | Endpoint | Description |
| :------| :-------- | :---------- |
| `GET` | `/products` | List all active (non-discarded) products |
| `GET` | `/products/{id}` | Get a specific product by ID |
| `POST` | `/products` | Create a new product |
| `PUT` | `/products/{id}` | Update an existing product |
| `DELETE` | `/products/{id}` | Soft delete a product (marks as discarded) |
| `POST` | `/products/recipes` | Generate recipes from a list of products |

## Requirements

- Python 3.13+
- FastAPI
- Supabase
- OpenAI
- Pydantic

### Environment Variables

| Variable | Description |
| :-------- | :---------- |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon/public key |
| `OPENAI_API_KEY` | OpenAI API key for recipe generation |

## File Structure

- `main.py` - FastAPI application entry point with CORS middleware and router setup
- `routes/products.py` - Product API endpoints and AI recipe generation logic
- `models/products.py` - Pydantic models for product data validation
- `db/__init__.py` - Supabase client initialization
- `tests/products/` - Test suite for product endpoints
- `Dockerfile` - Docker container configuration
- `requirements.txt` - Python dependencies

### Database Schema (Supabase)

The `products` table should have the following columns:
- `id` (integer, primary key)
- `name` (text)
- `type` (text)
- `quantity` (integer)
- `store` (text)
- `stock_location` (text)
- `discarded_at` (timestamp with timezone, nullable - used for soft delete)
- `created_at` (timestamp with timezone, auto-generated)

## Docker Deployment

The project includes a Dockerfile for containerized deployment:

```bash
docker build -t fridge-app-api .
docker run -p 8080:8080 fridge-app-api
```

The API will be available at `http://localhost:8080`.

## Usage Example

### Create a product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Eggs", "type": "dairy", "quantity": 12, "store": "Whole Foods", "stock_location": "fridge"}'
```

### Get all products
```bash
curl http://localhost:8000/products
```

### Generate recipes
```bash
curl -X POST http://localhost:8000/products/recipes \
  -H "Content-Type: application/json" \
  -d '["eggs", "tomatoes", "onions", "chicken"]'
```

## Support

For issues or contributions, please refer to the project's development guidelines or contact the development team.
