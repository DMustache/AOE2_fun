from django.contrib import admin

from parser.models import *

admin.site.register(
    [
        Player,
        Civilization,
        PlayersInMatches,
        Teams,
        Colors,
        Match,
        MatchTag,
        MatchTagging,
        Map,
        MapTag,
        MapTagging,
    ]
)
