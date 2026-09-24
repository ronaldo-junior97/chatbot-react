import pytest

from app.tools.addition_tool import add
from app.tools.division_tool import divide
from app.tools.multiplication_tool import multiply
from app.tools.subtraction_tool import subtract


def test_add():
    assert add(5, 4) == 9


def test_subtract():
    assert subtract(9, 2) == 7


def test_multiply():
    assert multiply(2, 3) == 6


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        divide(10, 0)