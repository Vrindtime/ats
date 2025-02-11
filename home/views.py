from django.contrib.auth.decorators import login_required
from django.dispatch.dispatcher import NONE_ID
from django.shortcuts import render, redirect, get_object_or_404
from .models import TestTaker
# from personality.models import Result
from resume.models import Resume
from personality.models import PersonalityResult
from aptitude.models import AptitudeResponse
import uuid



# Create your views here.
def home(request):
    test_taker_id = request.session.get('test_taker_id',None)
    return render(request,'home/homepage.html',{'test_taker_id': test_taker_id })

def start_test(request):
    # Create a new TestTaker
    test_taker = TestTaker.objects.create()

    # Store the unique ID in the session
    request.session['test_taker_id'] = str(test_taker.id)

    # Redirect to the test page
    return redirect('upload_resume')

@login_required
def delete_user(request,id):
    get_object_or_404(TestTaker,id=id)
    return redirect('admin_dashboard')


# A button to clear cache for testing purposes
def clear_cache(request):
    request.session.flush()  # Clear the session
    return redirect('home')


def result(request):

    # test_taker = TestTaker.objects.get(id=test_taker_id)
    if request.GET:
        test_taker_id = request.GET.get('resume_id')
        test_taker = get_object_or_404(TestTaker, id=test_taker_id)
    else:
        test_taker_id = request.session.get('test_taker_id')
        test_taker = get_object_or_404(TestTaker, id=test_taker_id)

    # Fetching results for personality test, aptitude, and resume
    personality_result = PersonalityResult.objects.filter(test_taker=test_taker).first()
    aptitude_result = AptitudeResponse.objects.filter(test_taker=test_taker).first()
    resume = Resume.objects.filter(test_taker=test_taker).first()


    job={
        'title': resume.job.title,
        'experience': resume.job.required_experience_years,
    }

    # Parsed Resume Data (if available)
    parsed_data = resume.parsed_data if resume and resume.parsed_data else {}

    # Extracting Scores
    personality_score = personality_result.total_score if personality_result else 0
    aptitude_score = aptitude_result.score if aptitude_result else 0
    resume_score = resume.score if resume.score else 0

    # Normalize personality and aptitude scores (assuming both are out of 10)
    max_personality = 10
    max_aptitude = 10
    normalized_personality = (personality_score / max_personality) * 100  # Convert to percentage
    normalized_aptitude = (aptitude_score / max_aptitude) * 100  # Convert to percentage

    # Calculate the overall score as the average of the three percentages
    overall_score = (resume_score + normalized_personality + normalized_aptitude) / 3

    # Approval Status (pending / failed / approved)
    approved = test_taker.approved

    context = {
        "test_taker": test_taker_id,
        "parsed_data": parsed_data,
        'job':job,
        "applied_on": resume.uploaded_at,
        "resume_score": resume_score,
        "personality_score": personality_score,
        "aptitude_score": aptitude_score,
        "overall_score": overall_score,
        "approved": approved,
    }

    return render(request, "home/result.html", context)
