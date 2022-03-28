"""Test sample."""


# content of test_sample.py
def func(name_x):
    return name_x + 1


def test_answer():
    assert func(4) == 5
