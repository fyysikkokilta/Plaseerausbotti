import pytest

from plaseerausbotti.model import plot_graph, initialise_tables


def test_csv_loads(people):
    assert people


def test_plot_graph(people):
    plot_graph(people)


@pytest.mark.parametrize(
    "tables_text",
    [('28'),
     ('14 14'),
     ('14 8 6')]
)
def test_initialise_tables(tables_text, people):
    tables, _ = initialise_tables(tables_text, people)
    assert all((table != 0).any() for table in tables)


@pytest.mark.parametrize(
    "tables_text",
    [('0'),
     ('27'),
     ('14 8 2')]
)
def test_initialise_tables_fails_with_less_space(tables_text, people):
    with pytest.raises(IndexError, match='out of bounds'):
        assert initialise_tables(tables_text, people)