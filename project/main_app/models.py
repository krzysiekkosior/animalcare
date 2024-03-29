from django.db import models

from accounts.models import CustomUser


class Case(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='cases')
    TYPES = [
        (0, "Poszukiwany / Poszukiwana"),
        (1, "Znaleziony / Znaleziona")
    ]
    type = models.IntegerField(choices=TYPES, default=1)
    place = models.CharField(max_length=80)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    STATUSES = [
        (0, "Otwarte"),
        (1, "Zakończone")
    ]
    status = models.IntegerField(choices=STATUSES, default=0)

    def __str__(self):
        return f'{self.date} - {self.place}'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='comments')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


class CasePhoto(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField()


class Observed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='observed')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='observed')
