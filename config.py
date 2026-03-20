import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-default-key'
    # Use SQLite as fallback for development if DATABASE_URL is not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///stock.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
