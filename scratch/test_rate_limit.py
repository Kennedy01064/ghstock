import requests
import time

def test_login_rate_limit():
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {"username": "admin", "password": "wrongpassword"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Testing Rate Limit on /login...")
    for i in range(15):
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 429:
            print(f"[{i+1}] SUCCESS: Rate limit triggered (429)! Message: {response.json().get('detail')}")
            return
        elif response.status_code == 401:
            print(f"[{i+1}] Allowed (401 Unauthorized as expected)")
        else:
            print(f"[{i+1}] Unexpected status code: {response.status_code}")
        time.sleep(0.1)
    
    print("WARNING: Rate limit was never triggered after 15 requests.")

if __name__ == "__main__":
    test_login_rate_limit()
