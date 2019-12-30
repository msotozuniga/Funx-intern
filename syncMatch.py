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
                   'scorer', 'state', 'actions']
    list = json.loads(response)
    for i in range(len(list)):
        m, create = Match.objects.get_or_create(pk=i, defaults={
            'slug': list[i]['slug'],
            'period': list[i]['period'],
            'duration': list[i]['timestamp'],
            'match_date': datetimeParser(list[i]['datetime'])
        })
        championship = list[i]['championship']
        referee = list[i]['referee']
        stadium = list[i]['stadium']
        local = list[i]['local']
        away = list[i]['away']
        estate = list[i]['state']
        if create:
            c, dummy = Championship.objects.get_or_create(slug=championship['slug'],
                                                          defaults={'name': championship['name']})
            m.championship = c
            r, dummy = Referee.objects.get_or_create(name=referee['name'])
            m.referee = r
            s, dummy = Stadium.objects.get_or_create(latitude=stadium['latitude'],
                                                     longitude=stadium['longitude'],
                                                     defaults={
                                                         'slug': stadium['slug'],
                                                         'name': stadium['name'],
                                                         'city': stadium['city'], })
            m.stadium = s
            m.save()

            l, dummy = Team.objects.get_or_create(slug=local['slug'],
                                                  defaults={
                                                      'name': local['name'],
                                                      'short_name': local['short_name'],
                                                      'image': local['image']
                                                  })

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

            state = State.objects.create(match=m,
                                         type=estate['type'],
                                         name=estate['name'])

            for each in list[i]['actions']:
                Action.objects.create(match=m,
                                      url=each['url'],
                                      type=each['type'],
                                      icon=each['icon'])

            entries_to_remove(delete_keys, list[i])
            for key in list[i]:
                if type(list[i][key]) is dict:
                    for each in list[i][key]:
                        MatchData.objects.create(match=m, characteristics=each, status=list[i][key][each])
                else:
                    MatchData.objects.create(match=m, characteristics=key, status=list[i][key])
        else:
            m.slug = list[i]['slug']
            m.period = list[i]['period']
            m.duration = list[i]['timestamp']
            m.match_date = datetimeParser(list[i]['datetime'])
            m.save()
            c = m.championship
            c.name = championship['name']
            c.slug = championship['slug']
            c.save()
            r = m.referee
            r.name = referee['name']
            r.save()
            s = m.stadium
            s.name = stadium['name']
            s.slug = stadium['slug']
            s.city = stadium['city']
            s.latitude = stadium['latitude']
            s.longitude = stadium['longitude']
            oldscore = Score.objects.get(match=m)
            l = oldscore.local
            l.slug = local['slug']
            l.name = local['name']
            l.short_name = local['short_name']
            l.image = local['image']
            l.save()
            a = oldscore.away
            a.slug = away['slug']
            a.name = away['name']
            a.short_name = away['short_name']
            a.image = away['image']
            a.save()
            oldscore.local_goals = list[i]['local_goals']
            oldscore.local_penalty = list[i]['local_penalty_goals']
            oldscore.away_goals = list[i]['away_goals']
            oldscore.away_penalty = list[i]['away_penalty_goals']
            oldscore.score_s = list[i]['scorer']
            oldscore.save()
            oldstate = State.objects.get(match=m)
            oldstate.name = estate['name']
            oldstate.type = estate['type']
            oldstate.save()
            actions_list = Action.objects.filter(match=m)
            for j in range(len(actions_list)):
                actions_list[j].type = list[i]['actions'][j]['type']
                actions_list[j].icon = list[i]['actions'][j]['icon']
                actions_list[j].url = list[i]['actions'][j]['url']
                actions_list[j].save()
            entries_to_remove(delete_keys, list[i])
            for key in list[i]:
                if type(list[i][key]) is dict:
                    for each in list[i][key]:
                        d, fabricate = MatchData.objects.get_or_create(match=m, characteristics=each,
                                                                       defaults={'status': list[i][key][each]})
                        if not fabricate:
                            d.status = list[i][key][each]
                else:
                    d, fabricate = MatchData.objects.get_or_create(match=m, characteristics=key,
                                                                   defaults={'status': list[i][key]})
                    if not fabricate:
                        d.status = list[i][key]

    return


cache = ''

while True:
    response = APIExtract().connect().text

    if confirmDifferences(response, cache):
        updateDatabase(response)
    print('loop')
    cache = response
    break
