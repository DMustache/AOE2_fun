from django.shortcuts import render

from parser.models import PlayersInMatches, Match, Player, Civilization, Teams


def main(request):
    model = Match.objects.order_by('match_datetime_start')
    return render(request, 'main/main.html', {
        'matches': model,
        'players': Player,
        'civs': Civilization,
        'teams': Teams,
        'pim': PlayersInMatches,
    })
