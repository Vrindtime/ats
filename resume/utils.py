# utils.py
import re

def calculate_score(job, resume_data):
    parsed = resume_data.get('parsed', {})
    breakdown = {
        'skills': {'matched': [], 'score': 0},
        'education': {'matched': False, 'score': 0},
        'experience': {'years': 0, 'score': 0},
        'penalties': []
    }

    # Skills - existing correct implementation
    resume_skills = [normalize_skill(s) for s in parsed.get('skills', [])]
    required_skills = [normalize_skill(s) for s in job.required_skills]
    matched_skills = list(set(resume_skills) & set(required_skills))
    breakdown['skills']['matched'] = matched_skills
    breakdown['skills']['score'] = len(matched_skills)/len(required_skills)*100 if required_skills else 100

    # Education - FIXED implementation
    resume_education = [
        normalize_degree(edu.get('degree', '')) 
        for edu in parsed.get('education', [])
    ]
    
    # Normalize job requirements using same method
    required_education = [
        normalize_degree(req_edu)
        for req_edu in job.required_education
    ]
    
    breakdown['education']['matched'] = any(
        edu in required_education
        for edu in resume_education
    )
    breakdown['education']['score'] = 100 if breakdown['education']['matched'] else 0

    # Experience calculation
    # Experience
    total_exp = 0
    for job_entry in parsed.get('employment_history', []):
        try:
            start = int(job_entry.get('start_date', '0000')[:4])
            end = int(job_entry.get('end_date', '0000')[:4]) if job_entry.get('end_date') else 2024
            total_exp += max(0, end - start)
        except ValueError:
            continue
    breakdown['experience']['years'] = total_exp
    req_exp = job.required_experience_years
    breakdown['experience']['score'] = 100 if req_exp == 0 else min((total_exp / req_exp) * 100, 100)
    # Penalties
    if not resume_education and job.required_education:
        breakdown['penalties'].append('Missing education section -20%')
    if not parsed.get('skills'):
        breakdown['penalties'].append('No skills listed -10%')
        
    # Final score
    weighted_total = (
        breakdown['skills']['score'] * 0.5 +
        breakdown['education']['score'] * 0.3 +
        breakdown['experience']['score'] * 0.2
    )
    
    breakdown['total'] = max(0, min(weighted_total, 100))
    return breakdown

def normalize_skill(skill):
    return re.sub(r'[^a-z0-9]', '', skill.lower())

# NEW: Degree normalization matching skill normalization
def normalize_degree(degree):
    return re.sub(r'[^a-z0-9]', '', degree.lower())