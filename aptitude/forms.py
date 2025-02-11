from django.forms import inlineformset_factory
from django.forms import  ModelForm,ChoiceField,RadioSelect,NullBooleanField,BooleanField
from .models import AptitudeQuestions, Choice, AptitudeCategory


class AptitudeQuestionForm(ModelForm):
    class Meta:
        model = AptitudeQuestions
        fields=['text','category']

class ChoiceForm(ModelForm):
    is_correct = NullBooleanField(
        widget=RadioSelect(choices=[(True, "Correct")]),
        required=False  # Allow deselection if needed
    )
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']


def get_choice_formset(extra):
    return inlineformset_factory(
        AptitudeQuestions,
        Choice,
        form=ChoiceForm,
        extra=extra,  # Dynamically set extra fields
        can_delete=False
    )

class AptitudeCategoryForm(ModelForm):
    class Meta:
        model = AptitudeCategory
        fields = '__all__'
