from backend.db.bootstrap import bootstrap_database

if __name__ == "__main__":
    print("Initializing database...")
    bootstrap_database()
    print("Database initialized successfully.")
