import os

import pytest

from plaseerausbotti.model import read_csv


@pytest.fixture
def people():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory to that of this file
    return read_csv('generic_sitsit.csv')
