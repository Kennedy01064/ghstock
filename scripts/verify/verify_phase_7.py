import os
import sys
import uuid
import time
import importlib
from fastapi.testclient import TestClient

# Ensure backend is in path
sys.path.append(os.getcwd())

def test_production_hardening():
    print("Testing production hardening...")
    os.environ["ENVIRONMENT"] = "production"
    os.environ["SECRET_KEY"] = "your-secret-key-for-dev"
    
    try:
        # Reloading config should trigger validation error
        import backend.core.config as config
        importlib.reload(config)
        print("FAILED: Production booted with insecure key!")
    except ValueError as e:
        print(f"PASSED: Caught insecure key in production: {e}")
    finally:
        # Restore local environment
        os.environ["ENVIRONMENT"] = "local"
        import backend.core.config as config
        importlib.reload(config)

def test_request_correlation():
    print("\nTesting request correlation...")
    from backend.main import app
    client = TestClient(app)
    
    response = client.get("/")
    request_id = response.headers.get("X-Request-ID")
    if request_id:
        print(f"PASSED: Found X-Request-ID: {request_id}")
    else:
        print("FAILED: X-Request-ID header missing")

def test_rate_limiting():
    print("\nTesting login rate limiting...")
    from backend.main import app
    client = TestClient(app)
    
    # Attempt 11 logins (limit is 10 per minute)
    for i in range(12):
        response = client.post("/api/v1/auth/login", data={"username": "test", "password": "wrong"})
        if response.status_code == 429:
            print(f"PASSED: Received 429 Too Many Requests after {i+1} attempts")
            return
    print(f"FAILED: Did not receive 429 after 12 attempts. Last status: {response.status_code}")

def test_audit_logging():
    print("\nTesting audit logging (checking console/mock)...")
    from backend.services.audit_service import audit_service
    from backend.core.config import settings
    
    settings.AUDIT_LOG_ENABLED = True
    
    try:
        audit_service.log_event(
            operation="TEST_AUDIT",
            actor_id=1,
            payload={"test": "data"}
        )
        print("PASSED: Audit event logged without error")
    except Exception as e:
        print(f"FAILED: Audit logging crashed: {e}")

if __name__ == "__main__":
    test_audit_logging()
    test_request_correlation()
    test_production_hardening()
    test_rate_limiting()
