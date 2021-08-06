from plaseerausbotti.model import plot_graph


def test_csv_loads(people):
    assert people


def test_plot_graph(people):
    plot_graph(people)
    # plt.savefig('temp.png', dpi=300)
