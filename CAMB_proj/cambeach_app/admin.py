from django.contrib import admin
from .models import Category, Tournament, Team, Match, Group

# Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    list_filter = ('genre',)
    search_fields = ('name',)
    
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'local', 'organization', 'start_date', 'end_date')
    list_filter = ('organization',)
    search_fields = ('name', 'local', 'start_date', 'end_date')
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'category')
    list_filter = ('tournament', 'category')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team)
admin.site.register(Group, GroupAdmin)
admin.site.register(Match)