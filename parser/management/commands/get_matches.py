from abc import ABC
from datetime import datetime
from time import sleep

import django.db.utils

from parser.models import PlayersInMatches, Match, Player, Map, Civilization, Teams
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
import requests


def fill_link(url, args):
    for elem in args.keys():
        url = url.replace(f'{elem}=', f'{elem}={args.get(elem)}')
    return url


def find_max_started(data):
    return max([data[i]['started'] for i in data.keys()])

def get_matches_history():
    url = r'https://aoe2.net/api/matches?game=aoe2de&count=&since='

    tmp = requests.get(r'https://aoe2.net/api/strings?game=aoe2de&language=en').json()
    info = {name: {
        tmp[name][i]['id'] if tmp[name] != 'language' else '': tmp[name][i]['string'] if tmp[name] != 'language' else ''
        for i in range(len(tmp[name]))
    } for name in list(tmp.keys())[1:]}
    del tmp

    data = {}
    since = 0
    url_tmp = fill_link(url, {'count': 1, 'started': since})
    api_data = requests.get(url_tmp).json()
    for elem in range(len(api_data)):
        data[len(data) + 1] = api_data[elem]

    length = len(data)
    while find_max_started(data) != since:
        tmp = requests.get(fill_link(url, {'count': 999, 'started': find_max_started(data)})).json()
        since = find_max_started(data)

        for elem in range(len(tmp)):
            data[len(data) + 1] = tmp[elem]

        print(f'{since} time pass. {len(data) - length} rows added')
        length = len(data)
        sleep(3)
    del since, length

    print('filter_started')
    for map_id in info['map_type']:
        Map.objects.update_or_create(
            map_id=map_id,
            map_name=info['map_type'][map_id],
        )

    for civ_id in info['civ']:
        Civilization.objects.update_or_create(
            civilization_id=civ_id,
            civilization_name=info['civ'][civ_id],
            civilization_meta='None',
        )

    for i in data.keys():
        if not data[i]['cheats'] and data[i]['ranked']:
            Match.objects.update_or_create(
                match_name=data[i]['name'],
                match_uuid=data[i]['match_uuid'],
                match_datetime_start=make_aware(datetime.utcfromtimestamp(data[i]['started'])),
                match_duration=make_aware(datetime.utcfromtimestamp(data[i]['finished'] - data[i]['started'])),
                match_map=Map.objects.get(map_id=data[i]['map_type']),
                match_team_win=data[i]['players'][0]['team'] if data[i]['players'][0]['won'] else int(abs(data[i]['players'][0]['won'] - 1))
            )

            for player_id in range(len(data[i]['players'])):
                if data[i]['players'][player_id]['name'] is None:
                    data[i]['players'][player_id]['name'] = 'Bot'
                    print('Bot hound')

                try:
                    Player.objects.update_or_create(
                        player_name=data[i]['players'][player_id]['name'],
                        player_rating=data[i]['players'][player_id]['rating'],
                        player_api_id=data[i]['players'][player_id]['profile_id'],
                        defaults={
                            'player_rating': data[i]['players'][player_id]['rating']
                        }
                    )
                except django.db.utils.IntegrityError:
                    Player.objects.filter(player_name=data[i]['players'][player_id]['name']).update(
                        player_rating=data[i]['players'][player_id]['rating']
                    )

                Teams.objects.update_or_create(
                    team_name=data[i]['players'][player_id]['team'],
                )
                PlayersInMatches.objects.create(
                    pim_match_id=Match.objects.get(
                        match_name=data[i]['name'],
                        match_uuid=data[i]['match_uuid'],
                        match_datetime_start=make_aware(datetime.utcfromtimestamp(data[i]['started'])),
                    ),

                    pim_player_id=Player.objects.get(
                        player_name=data[i]['players'][player_id]['name']),

                    pim_civilization_id=Civilization.objects.get(
                        civilization_name=info['civ'][data[i]['players'][player_id]['civ']]
                    ),

                    pim_team_id=Teams.objects.get(team_name=data[i]['players'][player_id]['team'])
                )
                print('player ', player_id, data[i]['players'][player_id]['name'])

            print(f'{i} match done')

    print('Done')


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        get_matches_history()
