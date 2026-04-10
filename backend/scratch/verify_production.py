import requests
import io

BASE_URL = "https://ghstock-production.up.railway.app"
USERNAME = "krojas"
PASSWORD = "krojas@gh"

def test_production_upload():
    print(f"--- Iniciando prueba en Produccion ({BASE_URL}) ---")
    
    # 1. Login
    print("Iniciando sesion...")
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    try:
        # La ruta correcta es /api/v1/auth/login
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
        response.raise_for_status()
        token = response.json()["access_token"]
        print("Success: Login exitoso.")
    except Exception as e:
        print(f"Error en login: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)
        return

    # 2. Upload
    print("Subiendo archivo de prueba...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    file_content = b"fake image content for cloud test"
    files = {
        "file": ("test_cloud_final.png", io.BytesIO(file_content), "image/png")
    }
    
    try:
        # La ruta es /api/v1/media/upload
        upload_response = requests.post(
            f"{BASE_URL}/api/v1/media/upload",
            headers=headers,
            files=files
        )
        upload_response.raise_for_status()
        data = upload_response.json()
        print("Success: Subida exitosa!")
        print(f"URL devuelta: {data.get('url')}")
        print(f"Almacenamiento usado: {data.get('storage')}")
        
        storage_type = data.get("storage", "").lower()
        if "supabase" in storage_type:
            print("CONFIRMADO: El sistema esta usando Supabase en produccion.")
        else:
            print(f"AVISO: El sistema sigue usando almacenamiento {storage_type.upper()}.")
            
    except Exception as e:
        print(f"Error en subida: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

if __name__ == "__main__":
    test_production_upload()
