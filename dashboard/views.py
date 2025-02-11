import json
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, IntegerField, CharField
from django.shortcuts import render, get_object_or_404,redirect
from home.models import TestTaker
from resume.models import Resume
from aptitude.models import AptitudeResponse
from personality.models import PersonalityResult

@login_required
def admin_dashboard(request):
    # Subquery to get the latest parsed_data for each test_taker
    parsed_data_subquery = Subquery(
        Resume.objects.filter(test_taker=OuterRef('pk'))
        .values('parsed_data')[:1],  # Get the first parsed_data entry
        output_field=CharField()
    )

    resume_id_subquery = Subquery(
        Resume.objects.filter(test_taker=OuterRef('pk'))
        .values('id')[:1],
        output_field=IntegerField()
    )
    
    # Subqueries to get the latest scores
    resume_score_subquery = Subquery(
        Resume.objects.filter(test_taker=OuterRef('pk'))
        .values('score')[:1], 
        output_field=IntegerField()
    )

    aptitude_score_subquery = Subquery(
        AptitudeResponse.objects.filter(test_taker=OuterRef('pk'))
        .values('score')[:1],
        output_field=IntegerField()
    )

    personality_score_subquery = Subquery(
        PersonalityResult.objects.filter(test_taker=OuterRef('pk'))
        .values('total_score')[:1],
        output_field=IntegerField()
    )

    # Query TestTakers with subqueries
    test_takers = TestTaker.objects.annotate(
        resume_id = resume_id_subquery,
        resume_score=resume_score_subquery,
        aptitude_score=aptitude_score_subquery,
        personality_score=personality_score_subquery,
        parsed_data=parsed_data_subquery 
    )

    # Process JSON manually after querying the database
    for test_taker in test_takers:
        parsed_json = json.loads(test_taker.parsed_data) if test_taker.parsed_data else {}
        test_taker.extracted_name = parsed_json.get("parsed", {}).get("name", "Unknown")

    context = {
        'test_takers': test_takers
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def approve_view(request,id):
    test_taker = get_object_or_404(TestTaker,id=id)
    test_taker.approved = "approved"
    test_taker.save()
    return redirect('admin_dashboard')

@login_required
def reject_view(request,id):
    test_taker = get_object_or_404(TestTaker,id=id)
    test_taker.approved = "rejected"
    test_taker.save()
    return redirect('admin_dashboard')