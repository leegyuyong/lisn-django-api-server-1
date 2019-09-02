from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=320)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete=models.PROTECT, null=True) # Note 테이블에 Directory 연결, Directory 삭제되도 Note 삭제 안됨
    title = models.CharField(max_length=200)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
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

class Directory(models.Model):                                  # Directory DB 추가
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)