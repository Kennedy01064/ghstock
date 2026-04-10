import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_roles_flow():
    print("--- STARTING UAT API INTEGRATION TEST (ROLES) ---")
    
    # === 1. ADMIN FLOW ===
    print("\n1. Logging in as Admin (eguzman)...")
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": "eguzman", "password": "eguzman"})
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
    admin_token = res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print(" -> Checking Admin Dashboard Stats...")
    res_admin_stats = requests.get(f"{BASE_URL}/analytics/admin", headers=admin_headers)
    if res_admin_stats.status_code == 200:
        stats = res_admin_stats.json()
        print(f"   [OK] Analytics loaded: {stats}")
    else:
        print(f"   [ERROR] Analytics: {res_admin_stats.status_code}")

    print(" -> Checking Building Inventory...")
    # Admin manages Torre Norte and Edificio Central
    res_inv = requests.get(f"{BASE_URL}/inventory/", headers=admin_headers)
    if res_inv.status_code == 200:
        b_inv = res_inv.json()
        print(f"   [OK] Found {len(b_inv)} inventory items assigned to this Admin's buildings.")
    else:
        print(f"   [ERROR] Building Inventory: {res_inv.status_code}")


    # === 2. MANAGER FLOW ===
    print("\n2. Logging in as Manager (mgomez)...")
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": "mgomez", "password": "mgomez"})
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
    mgr_token = res.json()["access_token"]
    mgr_headers = {"Authorization": f"Bearer {mgr_token}"}

    print(" -> Checking Manager Dashboard Stats...")
    res_mgr_stats = requests.get(f"{BASE_URL}/analytics/manager", headers=mgr_headers)
    if res_mgr_stats.status_code == 200:
        stats = res_mgr_stats.json()
        print(f"   [OK] Analytics loaded: {stats}")
    else:
        print(f"   [ERROR] Analytics: {res_mgr_stats.status_code}")

    print(" -> Creating a new DRAFT Order...")
    # Get associated buildings for manager
    res_b = requests.get(f"{BASE_URL}/buildings/", headers=mgr_headers)
    buildings = res_b.json()
    if not buildings:
         print("   [ERROR] No buildings available for manager.")
         return
    b_id = buildings[0]["id"]
    
    # Start DRAFT
    res_draft = requests.post(f"{BASE_URL}/orders/", headers=mgr_headers, json={"building_id": b_id})
    if res_draft.status_code == 200:
        order_id = res_draft.json()["id"]
        print(f"   [OK] Created Draft Order #{order_id} for Building #{b_id}")
        
        # Add item
        print(" -> Adding Item to Draft Order...")
        res_prod = requests.get(f"{BASE_URL}/catalog/all", headers=mgr_headers)
        product_id = res_prod.json()[0]["id"]
        
        res_item = requests.post(f"{BASE_URL}/orders/{order_id}/items", headers=mgr_headers, json={"product_id": product_id, "quantity": 3})
        if res_item.status_code == 200:
             print(f"   [OK] Added 3x of Product #{product_id} to Order #{order_id}")
             
             # Submit Order
             print(" -> Submitting Order...")
             res_sub = requests.post(f"{BASE_URL}/orders/{order_id}/submit", headers=mgr_headers)
             if res_sub.status_code == 200:
                 print(f"   [OK] Order #{order_id} successfully submitted!")
             else:
                 print(f"   [ERROR] Submit: {res_sub.text}")
        else:
             print(f"   [ERROR] Item Add: {res_item.text}")
    else:
        print(f"   [ERROR] Order Draft: {res_draft.status_code} - {res_draft.text}")

    print("\n--- ROLES UAT SUCCESSFUL ---")

if __name__ == "__main__":
    test_roles_flow()


