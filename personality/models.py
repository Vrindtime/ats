# personality/models.py
from django.db import models
from home.models import TestTaker

# To manage categories ["Openness", "Conscientiousness"]
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)   # e.g., "Openness", "Conscientiousness"

    def __str__(self):
        return self.text[:50]  # Show first 50 characters in admin


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    score = models.IntegerField()  # e.g., 1-5 (1 being the lowest and 5 being the highest)

    def __str__(self):
        return f"{self.text} (Score: {self.score})"

# ------------------------------------------------------------------------------  #

# The UserResponse model holds the granular data (each answer),
# while the Result model holds the computed summary.
# This separation makes it easier to recalculate scores
# if your scoring logic ever changes and avoids redundancy.

#To store the user input (each question with its answer that the user inputed)
class PersonalityUserResponse(models.Model):
    test_taker = models.ForeignKey(TestTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.question}"

# to store the score of a user
class PersonalityResult(models.Model):
    test_taker = models.OneToOneField(TestTaker, on_delete=models.CASCADE)
    scores = models.JSONField()  # Stores scores for each category, e.g., {"Openness": 3.5, "Conscientiousness": 4.2}
    total_score = models.FloatField(default=0)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test_taker.id}"

