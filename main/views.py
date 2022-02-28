from django.shortcuts import render

from parser.models import PlayersInMatches, Match, Player, Civilization, Teams, Map


def main(request):
    model = {
        'match': {
            i : 'None'
        } for i in range(Match.objects.get().match_id)
    }
    return render(request, 'main/main.html', model)
