from fastapi.testclient import TestClient
import warnings

warnings.filterwarnings("ignore")


def test_create_new_user(client: TestClient, data_user_su):
    response = client.post("/register/", json=data_user_su)
    assert response.status_code == 200
    assert response.json()["username"] == "dima"
    assert response.json()["first_name"] == "string"
    assert response.json()["email"] == "user@example.com"
    assert response.json()["is_active"] is True
    assert response.json()["is_staff"] is True
    assert response.json()["is_superuser"] is True


def test_login_for_access_token(client: TestClient, request_data_auth_su):
    response = client.post("/auth/", data=request_data_auth_su)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(client: TestClient):
    invalid_request = {"username": "dima", "password": "badpassword"}
    response = client.post("/auth/", data=invalid_request)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_user_salary(client: TestClient, request_data_auth_su):
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "dima"
    assert response.json()["first_name"] == "string"
    assert response.json()["email"] == "user@example.com"
    assert response.json()["rate_an_hour"] == 500
    assert response.json()["date_increased"] == "2023-06-11"
    assert response.json()["is_active"] is True


def test_get_users_list(
    client: TestClient,
    request_data_auth_su,
    data_new_user: dict,
    data_new_user1: dict,
):
    client.post("/register/", json=data_new_user)
    client.post("/register/", json=data_new_user1)
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        params={"skip": 0, "limit": 100},
    )
    assert response.status_code == 200
    users = response.json()["users"]
    assert len(users) == 3
    assert users[1]["username"] == "ivan"
    assert users[2]["username"] == "ivan1"
    assert users[1]["first_name"] == "istring"
    assert users[2]["first_name"] == "istring1"
    assert users[1]["last_name"] == "istring"
    assert users[2]["last_name"] == "istring1"
    assert users[1]["email"] == "ivan@example.com"
    assert users[2]["email"] == "ivan1@example.com"
    current_user = response.json()["current_user"]
    assert current_user["username"] == "dima"
    assert current_user["email"] == "user@example.com"
    assert current_user["is_superuser"] is True


def test_get_users_list_not_access(
    client: TestClient,
    request_data_auth_user: dict,
):
    response = client.post("/auth/", data=request_data_auth_user)
    token = response.json()["access_token"]
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        params={"skip": 0, "limit": 100},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No access"


def test_get_user_for_update_salary(
    client: TestClient, request_data_auth_su, data_new_user: dict
):

    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    response = client.get(
        f"/users/{user_name}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_updated = response.json()["user_for_update"]
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    assert user_updated["rate_an_hour"] == 500
    assert user_updated["date_increased"] == "2023-10-11"
    assert user_updated["is_active"] is True
    current_user = response.json()["current_user"]
    assert current_user["username"] == "dima"
    assert current_user["email"] == "user@example.com"
    assert current_user["rate_an_hour"] == 500
    assert current_user["is_superuser"] is True


def test_get_user_for_update_salary_no_access(
    client: TestClient, request_data_auth_user: dict, data_new_user1: dict
):
    response = client.post("/auth/", data=request_data_auth_user)
    token = response.json()["access_token"]
    user_name = data_new_user1["username"]
    response = client.get(
        f"/users/{user_name}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No access"


def test_update_user_salary(
    client: TestClient,
    request_data_auth_su,
    data_new_user: dict,
    data_update_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    response = client.put(
        f"/users/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_update_new_user,
    )
    assert response.status_code == 200
    user_updated = response.json()["user_updated"]
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    assert user_updated["rate_an_hour"] == 1000
    assert user_updated["date_increased"] == "2024-10-11"
    assert user_updated["is_active"] is True
    current_user = response.json()["current_user"]
    assert current_user["username"] == "dima"
    assert current_user["email"] == "user@example.com"
    assert current_user["rate_an_hour"] == 500
    assert current_user["is_superuser"] is True


def test_update_user_salary_no_access(
    client: TestClient,
    request_data_auth_user,
    data_new_user: dict,
    data_update_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_user)
    token = response.json()["access_token"]
    response = client.put(
        f"/users/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_update_new_user,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No access"


def test_upgrade_user_permission(
    client: TestClient,
    request_data_auth_su,
    data_new_user: dict,
    data_update_new_user: dict,
    data_downgrade_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    # up access
    response = client.put(
        f"/users/upgrade/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_update_new_user,
    )
    assert response.status_code == 200
    user_updated = response.json()["user_updated"]
    assert user_updated["is_staff"] is True
    assert user_updated["is_superuser"] is False
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    # downgrade access
    response = client.put(
        f"/users/upgrade/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_downgrade_new_user,
    )
    user_updated = response.json()["user_updated"]
    assert user_updated["is_staff"] is False
    assert user_updated["is_superuser"] is False
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    current_user = response.json()["current_user"]
    assert current_user["username"] == "dima"
    assert current_user["is_superuser"] is True


def test_upgrade_user_permission_no_access(
    client: TestClient,
    request_data_auth_user,
    data_new_user: dict,
    data_update_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_user)
    token = response.json()["access_token"]

    response = client.put(
        f"/users/upgrade/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_update_new_user,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No access, only admin"


def test_update_active_deactive(
    client: TestClient,
    request_data_auth_su,
    data_new_user: dict,
    data_update_new_user: dict,
    data_downgrade_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_su)
    token = response.json()["access_token"]
    # block user
    response = client.put(
        f"/users/activation/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_downgrade_new_user,
    )
    user_updated = response.json()["user_updated"]
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    assert user_updated["is_active"] is False
    # unblock user
    response = client.put(
        f"/users/activation/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_update_new_user,
    )
    user_updated = response.json()["user_updated"]
    assert user_updated["username"] == "ivan"
    assert user_updated["email"] == "ivan@example.com"
    assert user_updated["is_active"] is True
    current_user = response.json()["current_user"]
    assert current_user["username"] == "dima"
    assert current_user["is_superuser"] is True


def test_update_active_deactive_no_access(
    client: TestClient,
    request_data_auth_user,
    data_new_user: dict,
    data_update_new_user: dict,
    data_downgrade_new_user: dict,
):
    user_name = data_new_user["username"]
    response = client.post("/auth/", data=request_data_auth_user)
    token = response.json()["access_token"]
    response = client.put(
        f"/users/activation/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data_downgrade_new_user,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No access, only admin"
