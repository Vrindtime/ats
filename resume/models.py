# models.py
from django.db import models
from home.models import TestTaker

class Job(models.Model):
    title = models.CharField(max_length=200)
    required_skills = models.JSONField(default=list)
    required_education = models.JSONField(
        help_text="Stores education key and its aliases"
    )
    required_experience_years = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resume(models.Model):
    test_taker = models.ForeignKey(TestTaker, on_delete=models.CASCADE)
    job = models.ForeignKey(  # Add this field
        Job, 
        on_delete=models.CASCADE,  # Delete resumes when job is deleted
        related_name='resumes'
    )
    file = models.FileField(upload_to='resumes/')
    parsed_data = models.JSONField(null=True, blank=True)
    score = models.FloatField(  # Add this field
        null=True, 
        blank=True, 
        help_text="Matching score percentage (0-100)"
    )
    score_breakdown = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.job.title}): ID: {self.test_taker.id}"

EDUCATION_CHOICES = [
    ('bca', 'BCA - Bachelor of Computer Applications (B.C.A, BCA, Bachelors in Computer Applications)'),
    ('mca', 'MCA - Master of Computer Applications (M.C.A, MCA, Masters in Computer Applications)'),
    ('btech', 'B.Tech - Bachelor of Technology (B.Tech, BTech, Bachelors in Technology)'),
    ('mtech', 'M.Tech - Master of Technology (M.Tech, MTech, Masters in Technology)'),
    ('be', 'BE - Bachelor of Engineering (B.E, BE, Bachelors in Engineering)'),
    ('me', 'ME - Master of Engineering (M.E, ME, Masters in Engineering)'),
    ('bsc_cs', 'B.Sc Computer Science (B.Sc CS, BSc CS, Bachelor of Science in Computer Science)'),
    ('bsc_it', 'B.Sc Information Technology (B.Sc IT, BSc IT, Bachelor of Science in IT)'),
    ('msc_cs', 'M.Sc Computer Science (M.Sc CS, MSc CS, Master of Science in Computer Science)'),
    ('msc_it', 'M.Sc Information Technology (M.Sc IT, MSc IT, Master of Science in IT)'),
    ('bba', 'BBA - Bachelor of Business Administration (B.B.A, BBA, Bachelors in Business Administration)'),
    ('mba', 'MBA - Master of Business Administration (M.B.A, MBA, Masters in Business Administration)'),
    ('bcom', 'B.Com - Bachelor of Commerce (B.Com, BCom, Bachelors in Commerce)'),
    ('mcom', 'M.Com - Master of Commerce (M.Com, MCom, Masters in Commerce)'),
    ('bca_ai', 'BCA AI - Bachelor of Computer Applications in AI (BCA AI, BCA in Artificial Intelligence)'),
    ('btech_ai', 'B.Tech AI - Bachelor of Technology in Artificial Intelligence (B.Tech AI, BTech AI, Bachelors in AI)'),
    ('btech_ds', 'B.Tech Data Science (B.Tech DS, BTech DS, Bachelor of Technology in Data Science)'),
    ('bsc_ds', 'B.Sc Data Science (B.Sc DS, BSc DS, Bachelor of Science in Data Science)'),
    ('btech_cyber', 'B.Tech Cyber Security (B.Tech Cyber Security, BTech Cyber Security, Bachelor of Technology in Cyber Security)'),
    ('bsc_cyber', 'B.Sc Cyber Security (B.Sc Cyber Security, BSc Cyber Security, Bachelor of Science in Cyber Security)'),
    ('bba_it', 'BBA IT - Bachelor of Business Administration in Information Technology (BBA IT, BBA in IT)'),
    ('mba_it', 'MBA IT - Master of Business Administration in Information Technology (MBA IT, MBA in IT)'),
]
