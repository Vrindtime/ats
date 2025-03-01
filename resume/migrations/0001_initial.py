# Generated by Django 5.1.6 on 2025-02-10 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('required_skills', models.JSONField(default=list)),
                ('required_education', models.JSONField(help_text='Stores education key and its aliases')),
                ('required_experience_years', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='resumes/')),
                ('parsed_data', models.JSONField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, help_text='Matching score percentage (0-100)', null=True)),
                ('score_breakdown', models.JSONField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='resume.job')),
                ('test_taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.testtaker')),
            ],
        ),
    ]
