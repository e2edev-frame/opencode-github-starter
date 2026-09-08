"""Tests for the calc module."""

from calc import add, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(4, 5) == 20


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5


def test_divide():
    assert divide(6, 3) == 2.0
    assert divide(7, 2) == 3.5
    assert divide(-6, 3) == -2.0
    assert divide(0, 5) == 0.0

    import pytest

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)
