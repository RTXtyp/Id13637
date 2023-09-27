from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=250)
    a = models.CharField(max_length=250)
    b = models.CharField(max_length=250)
    c = models.CharField(max_length=250)
    correct_answer = models.CharField(max_length=250)



