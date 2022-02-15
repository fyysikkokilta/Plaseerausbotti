import csv
from dataclasses import dataclass
from queue import LifoQueue
from typing import List, Set

import networkx as nx
import numpy as np
from thefuzz import fuzz


@dataclass(frozen=True, order=True)
class Person:
    """ Immutable class to model a person in the sitsit.

    Args:
        name: Name of the person
        group: Name(s) of the group, or people, the person wants to sit next to.

    """
    name: str
    group: str = None


firstname_keywords = {'etunimi', 'firstname', 'first', 'given'}
surname_keywords = {'sukunimi', 'surname', 'last', 'family'}
group_keywords = {'pöytäseuratoive', 'pöytäseuruetoive', 'pöytäseura', 'group', 'sit', 'avec'}


def _compare_keywords(header: str, keywords: Set[str]):
    """ Split header by spaces and check if in keywords. """
    return any((p in keywords for p in header.lower().split()))


def _select_keyword(headers: List[str], keywords: Set[str]):
    """ Select header matches a keyword. """
    i = [_compare_keywords(h, keywords) for h in headers]
    return headers[np.where(i)[0][0]]


def read_csv(filename: str):
    """ Read ``.csv`` file from `Ilmomasiina <https://github.com/fyysikkokilta/ilmomasiina>`_.

    Args:
        filename: Path to the ``.csv``

    Returns:
        List[People]: list of the people at the sitsit as :class:`Person`.

    """
    people = []
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        headers = list(next(csv_reader).keys())  # get headers from first row
        print(headers, '\n\n')
        firstname = _select_keyword(headers, firstname_keywords)
        surname = _select_keyword(headers, surname_keywords)
        group = _select_keyword(headers, group_keywords)

        csv_file.seek(0)  # roll back to first row
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            info = {
                'name': f"{row[firstname]} {row[surname]}",
                'group': row[group]
            }
            people.append(Person(**info))

    return people


def _is_similar(group1: str, group2: str):
    """ Tell whether strings are similar using Levenshtein Distance.

    Args:
        group1: group to compare as string
        group2: the other group to compare as string

    Returns:
        bool: True or False

    """
    return fuzz.ratio(group1, group2) > 87  # threshold can still be hand-tuned


def _common_friends(person: Person, people: List[Person]):
    """ Retrieve people that have a similar group.

    TODO handle when group is just names.

    Args:
        person: Person for which to find common friends
        people: List of people to retrieve similar groups from

    Returns:
        List[Person]: list of friends as people

    """
    friends = []
    for p in people:
        if person.name != p.name and _is_similar(person.group, p.group):
            friends.append(p)
    return friends


def initialise_tables(tables_text: str, people: List[Person]):
    """ Return list of np.array with people initialised with corresponding IDs

    Args:
        tables_text: Given as, e.g., ``"60 60 60"``.

    Returns:
        tables: Tables as 2xN np.array with IDs corresponding to people
        id_people_map: IDs mapped to people
    """
    table_sizes = map(int, tables_text.split())
    tables = [np.zeros([table_size // 2, 2], dtype=int) for table_size in table_sizes]

    id_people_map = dict(enumerate(people, 1))
    people_id_map = {p: i for i, p in id_people_map.items()}
    friends_map = {p: _common_friends(p, people) for p in people}

    cluster_sizes = [len(e) for e in friends_map.values()]
    people_clustered = [p for _, p in sorted(zip(cluster_sizes, friends_map.keys()))]
    table_splits = np.cumsum([t.size for t in tables])[:-1] - 1

    for table, people_in_table in zip(tables, np.split(people_clustered, table_splits)):

        stack = LifoQueue()
        for person in reversed(people_in_table):
            stack.put(person)

        i = 0
        processed = set()
        while not stack.empty():
            person = stack.get()
            if person not in processed:
                table[i // 2, i % 2] = people_id_map[person]

                for f in friends_map[person]:
                    stack.put(f)

                processed.add(person)
                i += 1

    return tables, id_people_map


def plot_graph(people: List[Person]):
    """ Return simple graph plot with groups as clusters
    """
    # TODO make graph nicer
    g = nx.Graph()
    g.add_nodes_from([(p.name, {'group': p.group}) for p in people])
    for person, friends in zip(people, [_common_friends(p, people) for p in people]):
        g.add_edges_from([(person.name, f.name) for f in friends])

    nx.draw(g, with_labels=True, font_weight='bold')
