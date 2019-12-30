from django.contrib import admin

# Register your models here.
from synchronize.models import *

admin.site.register(Match)
admin.site.register(Team)
admin.site.register(MatchData)
admin.site.register(Score)
admin.site.register(Championship)
admin.site.register(State)
admin.site.register(Referee)
admin.site.register(Action)
admin.site.register(Stadium)