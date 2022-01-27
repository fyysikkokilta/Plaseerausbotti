import csv
from dataclasses import dataclass
from typing import List, Set

import networkx as nx
import numpy as np
from thefuzz import fuzz


@dataclass
class Person:
    """ Class to model a person in the sitsit.

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
    with open(filename, mode='r') as csv_file:
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
            friends.append((person.name, p.name))
    return friends


def plot_graph(people):
    # TODO make graph nicer
    g = nx.Graph()
    g.add_nodes_from([(p.name, {'group': p.group}) for p in people])
    for friends in [_common_friends(p, people) for p in people]:
        g.add_edges_from(friends)

    nx.draw(g, with_labels=True, font_weight='bold')
