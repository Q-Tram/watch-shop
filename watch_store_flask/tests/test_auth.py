from app.models.user import User


def test_password_hashing(app):
    """Test that passwords are stored as secure hashes, never plain text."""
    with app.app_context():
        user = User.find_by_email("customer@gmail.com")
        assert user is not None
        assert user.password != "customerpassword123"
        assert user.password.startswith("scrypt:") or user.password.startswith("pbkdf2:")
        assert user.check_password("customerpassword123") is True
        assert user.check_password("wrongpassword") is False


def test_user_registration(client, app):
    """Test user registration flow."""
    response = client.post(
        "/register",
        data={
            "fullName": "Le Thi Mai",
            "email": "mai@gmail.com",
            "password": "mypassword123",
            "confirm_password": "mypassword123",
            "phone": "0987654321",
            "address": "12 Tran Phu, Da Nang",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"\xc4\x90\xc4\x83ng k\xc3\xbd t\xc3\xa0i kho\xe1\xba\xa3n th\xc3\xa0nh c\xc3\xb4ng" in response.data or b"th\xc3\xa0nh c\xc3\xb4ng" in response.data

    with app.app_context():
        user = User.find_by_email("mai@gmail.com")
        assert user is not None
        assert user.fullName == "Le Thi Mai"
        assert user.role == "customer"


def test_registration_duplicate_email(client):
    """Test duplicate email rejection during registration."""
    response = client.post(
        "/register",
        data={
            "fullName": "Duplicate User",
            "email": "customer@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    assert b"Email n\xc3\xa0y \xc4\x91\xc3\xa3 \xc4\x91\xc6\xb0\xe1\xbb\xa3c s\xe1\xbb\xad d\xe1\xbb\xa5ng" in response.data


def test_login_success(client):
    """Test successful login."""
    response = client.post(
        "/login",
        data={"email": "customer@gmail.com", "password": "customerpassword123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"\xc4\x90\xc4\x83ng nh\xe1\xba\xadp th\xc3\xa0nh c\xc3\xb4ng" in response.data


def test_login_wrong_password(client):
    """Test login with incorrect password."""
    response = client.post(
        "/login",
        data={"email": "customer@gmail.com", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert b"M\xe1\xba\xadt kh\xe1\xba\xa9u kh\xc3\xb4ng ch\xc3\xadnh x\xc3\xa1c" in response.data


def test_login_locked_account(client, app):
    """Test that locked accounts cannot log in."""
    with app.app_context():
        user = User.find_by_email("customer@gmail.com")
        User.toggle_lock(user.id)  # Lock account

    response = client.post(
        "/login",
        data={"email": "customer@gmail.com", "password": "customerpassword123"},
        follow_redirects=True,
    )
    assert b"T\xc3\xa0i kho\xe1\xba\xa3n c\xe1\xbb\xa7a b\xe1\xba\xa1n \xc4\x91\xc3\xa3 b\xe1\xbb\x8b kh\xc3\xb3a" in response.data


def test_logout(auth_client):
    """Test logout flow."""
    response = auth_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"b\xe1\xba\xa1n \xc4\x91\xc3\xa3 \xc4\x91\xc4\x83ng xu\xe1\xba\xa5t" in response.data.lower()

