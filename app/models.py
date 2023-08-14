from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, User, PermissionsMixin
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} {self.surname}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    user_rating = models.IntegerField(default=0)

    @property
    def stars(self):
        return range(self.user_rating)

    @property
    def rating(self):
        return max(0, min(5, self.user_rating))

    @rating.setter
    def rating(self, value):
        self.user_rating = max(0, min(5, value))


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Assignment(models.Model):
    PROGRESS_CHOICES = [(i, str(i)) for i in range(11)]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=0)
    due_date = models.DateField(default=datetime.now() + timedelta(days=7))
    tasks = models.ManyToManyField('Task', related_name='assignments')

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reminder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def time_remaining(self):
        now = timezone.now()
        remaining = self.deadline - now

        if remaining.total_seconds() <= 0:
            return "Reminder Expired"
        else:
            days = remaining.days
            hours, seconds = divmod(remaining.seconds, 3600)
            minutes, _ = divmod(seconds, 60)

            if days == 0:
                if hours == 0:
                    return f"{minutes} minutes"
                else:
                    return f"{hours} hours and {minutes} minutes"
            else:
                return f"{days} days, {hours} hours, and {minutes} minutes"

        time_remaining_text = property(time_remaining)

class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.title
