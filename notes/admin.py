from django.contrib import admin

# Register your models here.

from .models import Note

'''
# Shorter Way:
admin.site.register(Note)
'''

'''Another way to register'''
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass
