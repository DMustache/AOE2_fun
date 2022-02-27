from django.contrib import admin

from parser.models import *

admin.site.register(
    [
        Player,
        Civilization,
        PlayersInMatches,
        Teams,
        Match,
        MatchTag,
        MatchTagging,
        Map,
    ]
)
