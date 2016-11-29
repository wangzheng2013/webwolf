from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=18)
    password = models.CharField(max_length=18)
    email = models.EmailField()
    nickname = models.CharField(max_length=20)
    age = models.SmallIntegerField(default=0)
    gender = models.CharField(choices=(('Male', 'man'), ('Female', 'woman'), ('Unknown', 'secret'),), max_length=8, default='Unknown')
    introduction = models.TextField(max_length=200, blank=True)
    credit = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

