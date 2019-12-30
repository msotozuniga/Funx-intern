from syncData.SyncDb import *
from syncMatch import updateDatabase
from synchronize.models import *
from django.test import TestCase


class syncDataTest(TestCase):
    def setUp(self):
        self.old = 'test'
        self.newCorrect = 'test'
        self.newWrong = 'tes'
        self.time = nextIteration()
        f = open('syncData/data.json','r')
        if f.mode == 'r':
            self.data = f.read()



    def test_confirmDifferences(self):
        one = confirmDifferences(self.newCorrect, self.old)
        two = confirmDifferences(self.newWrong, self.old)
        three = confirmDifferences(self.newCorrect, self.newWrong)
        self.assertFalse(one)
        self.assertTrue(two)
        self.assertTrue(three)

    def test_nextIteration(self):
        self.assertTrue(self.time > 0)
        self.assertTrue(self.time < 86400)

    def test_updateDatabase(self):
        updateDatabase(self.data)
        self.assertEquals(len(Match.objects.all()),5)
        self.assertEquals(len(MatchData.objects.all()), 34)
        self.assertEquals(len(Stadium.objects.all()),1)
        self.assertEquals(len(Championship.objects.all()),1)
        self.assertEquals(len(Team.objects.all()),5)
        self.assertEquals(len(Referee.objects.all()), 5)
        self.assertEquals(len(Action.objects.all()), 10)
        self.assertEquals(len(State.objects.all()),5)
        self.assertEquals(len(Score.objects.all()),5)
        changes = Match.objects.get(pk=0)
        changes.period='Fecha X'
        changes.save()
        Match.objects.create(slug='test',match_date=datetime.now(),duration=500,period='test')
        self.assertEquals(changes.period , 'Fecha X')
        updateDatabase(self.data)

        self.assertEquals(Match.objects.get(pk=0).period, 'Fecha 15')
        self.assertEquals(len(Match.objects.all()),5)