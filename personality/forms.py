# personality/forms.py
from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'})
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'score']