from django.contrib import admin
from .models import Note, Audio, Sentence

# Register your models here.
admin.site.register(Note)
admin.site.register(Audio)
admin.site.register(Sentence)