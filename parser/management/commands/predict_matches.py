from abc import ABC

import pickle, sklearn

from parser.models import PlayersInMatches, Match, Player, Map, Civilization, Teams
from django.core.management import BaseCommand


def predict_matches():
    with open(r'parser/management/commands/data/linear_model.h5', 'rb') as model_file:
        model = pickle.load(model_file)
    print(model.predict([[1, 1, 1, 1, 1, 1, 1]]))


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        predict_matches()
