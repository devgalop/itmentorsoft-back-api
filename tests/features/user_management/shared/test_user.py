import pytest

from src.features.user_management.shared.user import User, UserStatus, UserRole


@pytest.fixture
def active_admin_user():
    sample_pass = "hashed"
    return User(
        username="alice",
        email="alice@example.com",
        name="Alice Smith",
        password_hashed=sample_pass,
        status=UserStatus.ACTIVE,
        role=UserRole.ADMIN,
    )


@pytest.fixture
def inactive_student_user():
    sample_pass = "hashed"
    return User(
        username="bob",
        email="bob@example.com",
        name="Bob Johnson",
        password_hashed=sample_pass,
        status=UserStatus.INACTIVE,
        role=UserRole.STUDENT,
    )


@pytest.fixture
def suspended_user():
    sample_pass = "hashed"
    return User(
        username="charlie",
        email="charlie@example.com",
        name="Charlie Brown",
        password_hashed=sample_pass,
        status=UserStatus.SUSPENDED,
        role=UserRole.USER,
    )


def test_is_active_returns_true_when_status_is_active(active_admin_user: User):
    assert active_admin_user.is_active() is True


def test_is_active_returns_false_when_status_is_inactive(inactive_student_user: User):
    assert inactive_student_user.is_active() is False


def test_is_active_returns_false_when_status_is_suspended(suspended_user: User):
    assert suspended_user.is_active() is False


def test_is_admin_returns_true_when_role_is_admin(active_admin_user: User):
    assert active_admin_user.is_admin() is True


def test_is_admin_returns_false_when_role_is_student(inactive_student_user: User):
    assert inactive_student_user.is_admin() is False


def test_deactivate_sets_status_to_inactive(active_admin_user: User):
    active_admin_user.deactivate()
    assert active_admin_user.status == UserStatus.INACTIVE


def test_suspend_sets_status_to_suspended(active_admin_user: User):
    active_admin_user.suspend()
    assert active_admin_user.status == UserStatus.SUSPENDED


def test_set_role_id_assigns_role_id_to_user(active_admin_user: User):
    active_admin_user.set_role_id("role-123")
    assert active_admin_user.role_id == "role-123"
