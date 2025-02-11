# forms.py
from django import forms
import csv
from io import StringIO
from .models import Job, EDUCATION_CHOICES, Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

class JobForm(forms.ModelForm):
    required_skills = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, "Machine Learning", AWS',
            'class': 'skill-input'
        }),
        help_text="Enter skills separated by commas. Use quotes for multi-word skills."
    )
    
    education_choice = forms.ChoiceField(
        label="Required Education",
        choices=EDUCATION_CHOICES,
        help_text="Select standardized education level"
    )

    class Meta:
        model = Job
        fields = ['title', 'required_skills', 'education_choice', 
                'required_experience_years', 'is_active']
        exclude = ['required_education']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Editing existing job
            # Convert existing list to comma-separated string for editing
            if isinstance(self.instance.required_skills, list):
                self.initial['required_skills'] = ', '.join(self.instance.required_skills)
            else:
                self.initial['required_skills'] = ''

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # SAFEST SKILL PROCESSING (works for all input types)
        skills_str = str(self.cleaned_data['required_skills'])
        reader = csv.reader(StringIO(skills_str))
        skills = [s.strip() for row in reader for s in row if s.strip()]
        
        # Simple deduplication without changing case
        seen = set()
        instance.required_skills = []
        for skill in skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                instance.required_skills.append(skill)

        # Original education handling remains unchanged
        education_map = {
            'bca': ['bca', 'b.c.a', 'bachelor of computer applications'],
            'btech': ['b.tech', 'btech', 'bachelor of technology'],
            'mca': ['mca', 'm.c.a', 'master of computer applications']
        }
        instance.required_education = education_map.get(
            self.cleaned_data['education_choice'], 
            [self.cleaned_data['education_choice']]
        )

        if commit:
            instance.save()
        return instance