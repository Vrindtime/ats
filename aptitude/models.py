# from aptitude.models
from django.db import models
from home.models import TestTaker

# Create your models here.
class AptitudeCategory(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class AptitudeQuestions(models.Model):
    text = models.TextField()
    category = models.ForeignKey(AptitudeCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(AptitudeQuestions, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class AptitudeResponse(models.Model):
    test_taker = models.ForeignKey(TestTaker,on_delete=models.CASCADE)
    selected_answer = models.ManyToManyField(Choice)  # If using the Choice model
    # to store the score only
    score = models.IntegerField()
    # to Store *score* for each category
    score_category = models.JSONField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_taker.id}"