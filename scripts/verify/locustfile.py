import os
import random

from locust import HttpUser, between, task


NORMAL_USER_CREDENTIALS = [
    (
        os.getenv("LOCUST_NORMAL_USER_1", "admin_juan"),
        os.getenv("LOCUST_NORMAL_PASS_1", "password123"),
    ),
    (
        os.getenv("LOCUST_NORMAL_USER_2", "admin_maria"),
        os.getenv("LOCUST_NORMAL_PASS_2", "password123"),
    ),
]
MANAGER_USERNAME = os.getenv("LOCUST_MANAGER_USER", "superboss")
MANAGER_PASSWORD = os.getenv("LOCUST_MANAGER_PASS", "password123")


class AuthenticatedUser(HttpUser):
    abstract = True
    wait_time = between(1, 3)

    username: str | None = None
    password: str | None = None
    access_token: str | None = None
    auth_headers: dict[str, str]

    def login(self, username: str, password: str) -> None:
        with self.client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
            name="POST /api/v1/auth/login",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"login failed: {response.status_code} {response.text}")
                return

            payload = response.json()
            token = payload.get("access_token")
            if not token:
                response.failure("login failed: missing access_token")
                return

            self.username = username
            self.password = password
            self.access_token = token
            self.auth_headers = {"Authorization": f"Bearer {token}"}
            response.success()


class ConserjeUser(AuthenticatedUser):
    weight = 4

    def on_start(self) -> None:
        username, password = random.choice(NORMAL_USER_CREDENTIALS)
        self.login(username, password)

    @task
    def browse_products_and_submit_order(self) -> None:
        if not self.access_token:
            return

        with self.client.get(
            "/api/v1/catalog/?limit=20",
            headers=self.auth_headers,
            name="GET /api/v1/catalog/",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"catalog failed: {response.status_code} {response.text}")
                return
            products = response.json()
            if len(products) < 2:
                response.failure("catalog failed: fewer than 2 products returned")
                return
            response.success()

        with self.client.get(
            "/api/v1/buildings/",
            headers=self.auth_headers,
            name="GET /api/v1/buildings/",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"buildings failed: {response.status_code} {response.text}")
                return
            buildings = response.json()
            if not buildings:
                response.failure("buildings failed: no assigned buildings returned")
                return
            building_id = random.choice(buildings)["id"]
            response.success()

        with self.client.post(
            "/api/v1/orders/",
            headers=self.auth_headers,
            json={"building_id": building_id},
            name="POST /api/v1/orders/",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"create order failed: {response.status_code} {response.text}")
                return
            order = response.json()
            order_id = order["id"]
            response.success()

        selected_products = random.sample(products, 2)
        for product in selected_products:
            with self.client.post(
                f"/api/v1/orders/{order_id}/items",
                headers=self.auth_headers,
                json={
                    "product_id": product["id"],
                    "quantity": random.randint(1, 3),
                },
                name="POST /api/v1/orders/{id}/items",
                catch_response=True,
            ) as response:
                if response.status_code != 200:
                    response.failure(f"add item failed: {response.status_code} {response.text}")
                    return
                response.success()

        with self.client.post(
            f"/api/v1/orders/{order_id}/submit",
            headers=self.auth_headers,
            name="POST /api/v1/orders/{id}/submit",
            catch_response=True,
        ) as response:
            if response.status_code not in (200, 400):
                response.failure(f"submit order failed: {response.status_code} {response.text}")
                return
            response.success()


class GerenteUser(AuthenticatedUser):
    weight = 1

    def on_start(self) -> None:
        self.login(MANAGER_USERNAME, MANAGER_PASSWORD)

    @task
    def view_cached_analytics_dashboard(self) -> None:
        if not self.access_token:
            return

        with self.client.get(
            "/api/v1/analytics/superadmin",
            headers=self.auth_headers,
            name="GET /api/v1/analytics/superadmin",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"analytics failed: {response.status_code} {response.text}")
                return
            response.success()
