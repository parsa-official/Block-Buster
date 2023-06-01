from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'job' ,'has_photo')
    search_fields = ['name']
    ordering = ['name']

    def has_photo(self, obj):
        if obj.photo:
            return '✅'
        else:
            return '❌'


admin.site.register(Person, PersonAdmin)
