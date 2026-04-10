"""
Script to seed buildings into production via the API.
Run: python backend/scripts/seed_buildings.py
"""
import requests

API_BASE = "https://ghstock-production.up.railway.app/api/v1"

BUILDINGS = [
    {"name": "Belice",                    "departments_count": 40,  "address": "Jirón Ayacucho 625, Jesús María"},
    {"name": "Boulevard Arequipa",        "departments_count": 56,  "address": "Av. Arequipa N° 4856, Miraflores"},
    {"name": "Brindiris",                 "departments_count": 10,  "address": "Av. General Ernesto Montagne 541, Miraflores"},
    {"name": "EDIFICIO RÚA",              "departments_count": 46,  "address": "AV. ROENTGEN 150, Surquillo"},
    {"name": "GREEN PARK",                "departments_count": 151, "address": "Av. General Santa Cruz 673 - 677, Jesús María"},
    {"name": "La Fontana",                "departments_count": 9,   "address": "Av. La Fontana N° 280, La Molina"},
    {"name": "Los balcones de Santa Cruz","departments_count": 43,  "address": "Calle Santa Cruz N° 653, Jesús María"},
    {"name": "Mar y Vista",               "departments_count": 91,  "address": "Av. Reducto 1583, Miraflores"},
    {"name": "MAYTA CAPAC",               "departments_count": 30,  "address": "Jirón Mayta Capac N° 1324, Jesús María"},
    {"name": "NOVOA",                     "departments_count": 28,  "address": "Jr. Pachacutec 2180, Lince"},
    {"name": "NUEVA AURORA III",          "departments_count": 69,  "address": "AV. BERNALES, SERGIO 460, Miraflores"},
    {"name": "Ramon Ribeyro",             "departments_count": 23,  "address": "Ca. Ramón Ribeyro N° 110, Miraflores"},
    {"name": "REAL 811",                  "departments_count": 64,  "address": "Av. Principal 811, Surquillo"},
    {"name": "SERGIO BERNALES",           "departments_count": 68,  "address": "SERGIO BERNALES N° 528, Surquillo"},
    {"name": "TORRES LUCAS",              "departments_count": 35,  "address": "Avenida Pío XII N° 317 - 319, San Miguel"},
    {"name": "VALENTINA II",              "departments_count": 22,  "address": "Calle Huayna Capac 1175, Jesús María"},
]


def main():
    # Login
    print("Iniciando sesión...")
    resp = requests.post(f"{API_BASE}/auth/login", data={
        "username": "krojas",
        "password": "krojas@gh",
    })
    resp.raise_for_status()
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Sesión iniciada correctamente.\n")

    created = 0
    skipped = 0

    for building in BUILDINGS:
        resp = requests.post(f"{API_BASE}/buildings/", json=building, headers=headers)
        if resp.status_code == 200:
            print(f"  [OK] Creado: {building['name']}")
            created += 1
        elif resp.status_code == 400 and "already exists" in resp.text:
            print(f"  [--] Ya existe: {building['name']}")
            skipped += 1
        else:
            print(f"  [ERR] Error en '{building['name']}': {resp.status_code} {resp.text}")

    print(f"\nResumen: {created} creados, {skipped} ya existían.")


if __name__ == "__main__":
    main()
