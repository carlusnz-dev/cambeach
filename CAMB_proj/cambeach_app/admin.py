from django.contrib import admin
from .models import Category, Tournament

# Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    list_filter = ('genre',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tournament)