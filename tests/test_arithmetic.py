import pytest
from src.arithmetic import generate_arithmetic

def test_easy():
    result = generate_arithmetic("easy")
    items = result[0].split()
    assert items[1] in ('+', '-')

    result = generate_arithmetic("EASY")
    items = result[0].split()
    assert items[1] in ('+', '-')

def test_medium():
    result = generate_arithmetic("medium")
    items = result[0].split()
    assert items[1] in ('+', '-', '*', '/')

def test_hard():
    result = generate_arithmetic("HaRd")
    items = result[0].split()
    assert items[1] in ('+', '-', '*', '/')

def test_invalid():
    with pytest.raises(AssertionError):
        generate_arithmetic("easyy")

    with pytest.raises(AssertionError):
        generate_arithmetic("")

    with pytest.raises(AssertionError):
        generate_arithmetic("1")

    with pytest.raises(AssertionError):
        generate_arithmetic("normal")
