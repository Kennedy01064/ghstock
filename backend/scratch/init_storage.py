import requests
import sys

URL = "https://mmlheqsgcbbakhknpjbk.supabase.co/storage/v1/bucket"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tbGhlcXNnY2JiYWtoa25wamJrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc3MTYyNywiZXhwIjoyMDkxMzQ3NjI3fQ.HxGlHPDmWrpZGtWQlOXt5Tw4Oi95frV4gbO-eufOilI"

headers = {
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

payload = {
    "id": "stock-media",
    "name": "stock-media",
    "public": True,
    "file_size_limit": 52428800, # 50MB
    "allowed_mime_types": ["image/png", "image/jpeg", "image/webp", "image/gif"]
}

def create_bucket():
    print(f"Intentando crear bucket 'stock-media'...")
    response = requests.post(URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Success: Bucket created.")
    elif response.status_code == 409:
        print("Info: Bucket already exists.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_bucket()
