from django.db import models
from api.user.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.TextField()
    is_trash = models.BooleanField(default=False)

class Audio(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Sentence(models.Model):
    index = models.IntegerField()
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.IntegerField()
    ended_at = models.IntegerField()
    content = models.TextField()