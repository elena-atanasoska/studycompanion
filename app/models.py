from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    user_rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return max(0, min(5, self._rating))

    @rating.setter
    def rating(self, value):
        self._rating = max(0, min(5, value))
