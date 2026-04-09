import httpx

def test_pdf():
    with httpx.Client() as client:
        r_login = client.post("http://127.0.0.1:5000/auth/login", data={"username": "superadmin", "password": "password"})
        
        valid_batch_id = 1
        print(f"Testing with valid_batch_id: {valid_batch_id}")
        
        r1 = client.get(f"http://127.0.0.1:5000/dispatch/batch/{valid_batch_id}/export/consolidated", follow_redirects=False)
        print("Consolidated Export Status:", r1.status_code)
        if r1.status_code in (301, 302):
            print("Redirect Location:", r1.headers.get("location"))
        
        r2 = client.get(f"http://127.0.0.1:5000/dispatch/batch/{valid_batch_id}/export/buildings", follow_redirects=False)
        print("Buildings Export Status:", r2.status_code)
        if r2.status_code in (301, 302):
            print("Redirect Location:", r2.headers.get("location"))

if __name__ == "__main__":
    test_pdf()
