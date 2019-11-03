from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=320)
    picture_url = models.CharField(max_length=320, null=True)              # Google 서버에 저장된

class Directory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.TextField()
    is_trash = models.BooleanField(default=False)
    edit_user = models.IntegerField(null=True)

class Audio(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.IntegerField(default=0)

class Sentence(models.Model):
    index = models.IntegerField()
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.IntegerField()
    ended_at = models.IntegerField()
    content = models.TextField()

class Share(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)