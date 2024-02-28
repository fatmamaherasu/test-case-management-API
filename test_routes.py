import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_register(client):
    response = client.post("/register",
                        json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"}, 
    )
    assert response.status_code == 201


def test_login(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    response = client.post("/login",
                        json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"}, 
    )
    assert response.status_code == 200


def test_logout(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    response = client.get("logout")
    assert response.status_code == 200


def test_get_all_tests(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_test(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    response = client.post("/create",json={"scenario": "To authenticate a successful user login on Gmail.com", "steps": "The user navigates to Gmail.com. The user enters a registered email address in the email field. The user clicks the ‘Next button. The user enters the registered password.The user clicks Sign In","asset":"Gmail account",
    "asset_id": 3,"test_data":"Legitimate username and password.","actual_results":"As Expected","expected_results": "Once username and password are entered, the web page redirects to the user’s inbox, displaying and highlighting new emails at the top.","status":0})
    assert response.status_code == 201


def test_get_tests_by_asset_id(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/create",json={"scenario": "To authenticate a successful user login on Gmail.com", "steps": "The user navigates to Gmail.com. The user enters a registered email address in the email field. The user clicks the ‘Next button. The user enters the registered password.The user clicks Sign In","asset":"Gmail account",
    "asset_id": 3,"test_data":"Legitimate username and password.","actual_results":"As Expected","expected_results": "Once username and password are entered, the web page redirects to the user’s inbox, displaying and highlighting new emails at the top.","status":0})
    response = client.get("asset/3")
    assert response.status_code == 200


def test_get_test_by_id(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/create",json={"scenario": "To authenticate a successful user login on Gmail.com", "steps": "The user navigates to Gmail.com. The user enters a registered email address in the email field. The user clicks the ‘Next button. The user enters the registered password.The user clicks Sign In","asset":"Gmail account",
    "asset_id": 3,"test_data":"Legitimate username and password.","actual_results":"As Expected","expected_results": "Once username and password are entered, the web page redirects to the user’s inbox, displaying and highlighting new emails at the top.","status":0})
    response = client.get("/1")
    assert response.status_code == 200


def test_edit_test(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/create",json={"scenario": "To authenticate a successful user login on Gmail.com", "steps": "The user navigates to Gmail.com. The user enters a registered email address in the email field. The user clicks the ‘Next button. The user enters the registered password.The user clicks Sign In","asset":"Gmail account",
    "asset_id": 3,"test_data":"Legitimate username and password.","actual_results":"As Expected","expected_results": "Once username and password are entered, the web page redirects to the user’s inbox, displaying and highlighting new emails at the top.","status":0})
    response = client.patch("update/1", json={"status":1})
    assert response.status_code == 200


def test_delete_test(client):
    client.post("/register", json={"name":"Fatma", "email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/login", json={"email": "fatma.maher.elsayed@gmail.com", "password": "myPassword"})
    client.post("/create",json={"scenario": "To authenticate a successful user login on Gmail.com", "steps": "The user navigates to Gmail.com. The user enters a registered email address in the email field. The user clicks the ‘Next button. The user enters the registered password.The user clicks Sign In","asset":"Gmail account",
    "asset_id": 3,"test_data":"Legitimate username and password.","actual_results":"As Expected","expected_results": "Once username and password are entered, the web page redirects to the user’s inbox, displaying and highlighting new emails at the top.","status":0})
    response = client.delete("delete/1")
    assert response.status_code == 200
