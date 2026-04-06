import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from typing import Dict, List, Tuple

class RateLimiter:
    """
    A simple in-memory sliding window rate limiter.
    Stores timestamps of requests for each bucket (e.g., IP or user).
    """
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.history: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        # Clean up old timestamps
        expiry = now - self.window_seconds
        self.history[key] = [t for t in self.history[key] if t > expiry]
        
        if len(self.history[key]) < self.requests_limit:
            self.history[key].append(now)
            return True
        return False

# Global limiters
# 10 login attempts per 1 minute per IP
login_limiter = RateLimiter(requests_limit=10, window_seconds=60)

async def check_login_rate_limit(request: Request):
    """
    Dependency to protect the login endpoint.
    Uses the client host (IP) as the bucket key.
    """
    client_ip = request.client.host if request.client else "unknown"
    if not login_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )
