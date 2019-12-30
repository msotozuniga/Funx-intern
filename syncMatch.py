import os, time
from syncData.APIExtract import *
from syncData.SyncDb import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Funx.settings")

import django

django.setup()

from synchronize.models import *


def updateDatabase(response):
    delete_keys = ['slug', 'period', 'timestamp', 'datetime', 'championship', 'referee', 'stadium',
                   'local', 'away', 'local_goals', 'local_penalty_goals', 'away_goals', 'away_penalty_goals',
                   'scorer', 'state','actions']
    list = json.loads(response)
    for i in range(len(list)):
        m, create = Match.objects.get_or_create(pk=i, defaults={
            'slug': list[i]['slug'],
            'period': list[i]['period'],
            'duration': list[i]['timestamp'],
            'match_date': datetimeParser(list[i]['datetime'])
        })
        if create:
            championship = list[i]['championship']
            c, dummy = Championship.objects.get_or_create(slug=championship['slug'],
                                                          defaults={'name': championship['name']})
            m.championship = c
            referee = list[i]['referee']
            r, dummy = Referee.objects.get_or_create(name=referee['name'])
            m.referee = r
            stadium = list[i]['stadium']
            s, dummy = Stadium.objects.get_or_create(latitude=stadium['latitude'],
                                                     longitude=stadium['longitude'],
                                                     defaults={
                                                         'slug': stadium['slug'],
                                                         'name': stadium['name'],
                                                         'city': stadium['city'], })
            m.stadium = s
            m.save()

            local = list[i]['local']
            l, dummy = Team.objects.get_or_create(slug=local['slug'],
                                                  defaults={
                                                      'name': local['name'],
                                                      'short_name': local['short_name'],
                                                      'image': local['image']
                                                  })
            away = list[i]['away']
            a, dummy = Team.objects.get_or_create(slug=away['slug'],
                                                  defaults={
                                                      'name': away['name'],
                                                      'short_name': away['short_name'],
                                                      'image': away['image']
                                                  })
            score = Score.objects.create(match=m,
                                         local=l,
                                         away=a,
                                         score_s=list[i]['scorer'],
                                         local_goals=list[i]['local_goals'],
                                         local_penalty=list[i]['local_penalty_goals'],
                                         away_goals=list[i]['away_goals'],
                                         away_penalty=list[i]['away_penalty_goals'])
            e = list[i]['state']

            state = State.objects.create(match=m,
                                         type=e['type'],
                                         name=e['name'])

            for each in list[i]['actions']:
                Action.objects.create(match=m,
                                      url=each['url'],
                                      type=each['type'],
                                      icon=each['icon'])

            entries_to_remove(delete_keys, list[i])
            for key in list[i]:
                if type(list[i][key]) is dict:
                    for each in list[i][key]:
                        MatchData.objects.create(match=m,characteristics=each,status=list[i][key][each])
                else:
                    MatchData.objects.create(match=m, characteristics=key, status=list[i][key])

        pass


cache = ''

while True:
    response = APIExtract().connect().text

    if confirmDifferences(response, cache):
        updateDatabase(response)
    print('loop')
    cache = response
    break
