# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ResumeForm, JobForm
from .models import Resume, Job 
from .utils import calculate_score
from home.models import TestTaker
import requests
from django.contrib.auth.decorators import login_required
import environ, os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize `environ`
env = environ.Env()

# Load .env file
env.read_env(os.path.join(BASE_DIR, ".env"))  # Load .env from project root

def upload_resume(request):
    test_taker_id = request.session.get('test_taker_id')
    test_taker = TestTaker.objects.get(id=test_taker_id)

    # Fetch API from .env
    api_key = env('RESUME_PARSER_API_KEY')
    print(f"Bearer {api_key}")
    if not api_key:
        raise ValueError("RESUME_PARSER_API_KEY environment variable is not set")

    if request.method == 'POST':
        try:
            job_id = request.POST.get('job_id')
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return render(request, 'resume/upload_resume.html',{'form': ResumeForm(), 'error': 'Invalid job selected'})

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)  # Don't save yet
            resume.test_taker = test_taker
            resume.job = job  # Assign the job to resume



            # API Call
            try:
                files = {"file": resume.file.open()}
                response = requests.post(
                    "https://resumeparser.app/resume/parse",
                    headers = {"Authorization": f"Bearer {api_key}"},
                    files=files
                )
                response.raise_for_status()  # Raise error for bad status
            except requests.RequestException as e:
                form.add_error(None, f"API Error: {str(e)}")
                return render(request, 'resume/upload_resume.html', {'form': form})

            # Parse and save data
            parsed_data = response.json()
            resume.parsed_data = parsed_data

            # Calculate score
            resume.score_breakdown = calculate_score(job, parsed_data)
            resume.score = resume.score_breakdown['total']
            resume.save()

            return redirect('personality_test')
    else:
        # GET request - show form with active jobs
        # test_taker_id = session.get('')
        active_jobs = Job.objects.filter(is_active=True)
        form = ResumeForm()
    test_taker_id = request.session.get('test_taker_id','Null')

    context={
        'test_taker_id': test_taker_id,
        'form': form,
        'active_jobs': active_jobs,  # Pass jobs to template
    }
    return render(request, 'resume/upload_resume.html', context)


def resume_detail(request, resume_id):
    if request.GET.get('resume_id'):
        resume_id = request.GET.get('resume_id')
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'resume/resume_detail.html', {'resume': resume})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resume_dashboard')  # Redirect to upload page
    else:
        form = JobForm()
    
    return render(request, 'resume/add_job.html', {'form': form})

@login_required
def resume_dashboard(request):
    resume = Resume.objects.all().values()
    # need to send id,name,score,job posting,uploaded date
    # but they are in parsed form in table so cant sent them all directly
    context={
        'jobs':resume
    }
    return render(request,'dashboard.html',context)

@login_required
def delete_resume(request,id):
    resume = get_object_or_404(Resume,id=id)
    resume.delete()
    return redirect('resume_dashboard')
