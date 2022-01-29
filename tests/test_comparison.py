import pytest

from plaseerausbotti.model import _is_similar

@pytest.mark.parametrize(
    "groups,expected",
    [(['Gang gang'] * 2, True),
     (['Gang gang', 'Jengi jengi'], False),
     (['Gang gang', 'Gang gnag'], True)]
)
def test_similarity(groups, expected):
    assert _is_similar(*groups) == expected