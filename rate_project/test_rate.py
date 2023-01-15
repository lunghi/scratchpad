import pytest

from rate_project.rate import Rate, datetime, active_rate_amount, offer_start_rate, Amount


@pytest.fixture
def rate_matrix():
    return (_ for _ in [
        Rate(datetime(2022, month=11, day=1), datetime(2022, month=12, day=30), Amount("4.99"), 0),
        Rate(datetime(2022, month=12, day=31), datetime(2023, month=11, day=1), Amount("5.99"), 0),
        Rate(datetime(2023, month=11, day=2), datetime(2023, month=11, day=10), Amount("6.99"), 2),
        Rate(datetime(2023, month=11, day=2), datetime(2023, month=11, day=10), Amount("7.56"), 1),
        Rate(datetime(2023, month=12, day=12), datetime(2030, month=12, day=31), Amount("8.99"), 0),
    ])


@pytest.fixture
def empty_rate_matrix():
    return list()


def test_active_rate_amount(rate_matrix):
    assert active_rate_amount(rate_matrix, datetime(2022, month=11, day=3)) == Amount("4.99")


def test_priority_rate(rate_matrix):
    assert active_rate_amount(rate_matrix, datetime(2023, month=11, day=4)) == Amount("6.99")


def test_missing_rate(rate_matrix):
    assert active_rate_amount(rate_matrix, datetime(2023, month=12, day=5)) is None


def test_offer_start_rate(rate_matrix):
    assert offer_start_rate(rate_matrix, datetime(2019, month=10, day=4)) == Amount("5.99")


def test_active_rate_empty_matrix(empty_rate_matrix):
    assert active_rate_amount(empty_rate_matrix, datetime(2022, month=11, day=3)) is None
