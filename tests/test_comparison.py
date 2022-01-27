import pytest

from plaseerausbotti.model import _is_similar

@pytest.mark.parametrize(
    "input,expected",
    [(['Gang gang'] * 2, True),
     (['Gang gang', 'Jengi jengi'], False),
     (['Gang gang', 'Gang gnag'], True)]
)
def test_similarity(input, expected):
    assert _is_similar(*input) == expected