# Quick Start Guide

## Prerequisites
- Python
- MySQL Server
- Git

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Create the `canteen` MySQL database
5. Configure `.streamlit/secrets.toml`
6. Run the application

## Run the Application

streamlit run src/app.py

The application will be available at:
http://localhost:8501

## Troubleshooting

### MySQL Connection Error
- Make sure MySQL is running.
- Check the database credentials in `.streamlit/secrets.toml`.

### Missing Python Package
Run:

pip install -r requirements.txt
