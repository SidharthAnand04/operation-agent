# MovieMingle

MovieMingle is a Flask-based movie recommendation platform where users can create, share, and explore movie lists.

## Features
- Public movie lists
- IMDB API integration
- AI-powered recommendations
- Responsive design

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python run.py`

## Configuration
- Edit `config.py` for API keys and Redis configuration.
- Use a `.env` file to securely manage sensitive information with `python-dotenv`.

## Scalability
- Plan to migrate data from CSV to a relational database using SQLAlchemy models as the application grows.
- Consider using PostgreSQL or similar databases for production.