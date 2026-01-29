from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import RecruiterProfile, JobSeekerProfile, Job, JobApplication

User = get_user_model()

def register(request):
    if request.method == 'POST':
        if request.POST.get('password') == request.POST.get('confirm_password'):
            User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                email=request.POST.get('email'),
                display_name=request.POST.get('display_name'),
                user_type=request.POST.get('user_type')
            )
            return redirect('/login/')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def profile_redirect(request):
    return redirect('/jobseeker/profile/' if request.user.user_type == 'jobseeker' else '/recruiter/profile/')


@login_required(login_url='/login/')
def jobseeker_profile(request):
    if request.method == 'POST':
        JobSeekerProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'full_name': request.POST.get('full_name'),
                'skills': request.POST.get('skills'),
                'experience_years': request.POST.get('experience_years'),
                'job_type': request.POST.get('job_type'),
                'preferred_location': request.POST.get('preferred_location'),
                'expected_salary': request.POST.get('expected_salary'),
                'resume': request.FILES.get('resume')
            }
        )
        return redirect('/dashboard/')
    return render(request, 'jobseeker_profile.html')


@login_required(login_url='/login/')
def recruiter_profile(request):
    if request.method == 'POST':
        RecruiterProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'company_name': request.POST.get('company_name'),
                'company_description': request.POST.get('company_description')
            }
        )
        return redirect('/dashboard/')
    return render(request, 'recruiter_profile.html')


@login_required(login_url='/login/')
def post_job(request):
    if request.method == 'POST':
        Job.objects.create(
            recruiter=request.user,
            title=request.POST.get('title'),
            openings=request.POST.get('openings'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            skills=request.POST.get('skills')
        )
        return redirect('/dashboard/')
    return render(request, 'post_job.html')


@login_required(login_url='/login/')
def job_list(request):
    return render(request, 'job_list.html', {'jobs': Job.objects.all()})


@login_required(login_url='/login/')
def apply_job(request, job_id):
    JobApplication.objects.get_or_create(
        job=Job.objects.get(id=job_id),
        jobseeker=request.user
    )
    return redirect('/applied/jobs/')


@login_required(login_url='/login/')
def applied_jobs(request):
    applications = JobApplication.objects.filter(jobseeker=request.user)
    return render(request, 'applied_jobs.html', {'applications': applications})


@login_required(login_url='/login/')
def job_applicants(request, job_id):
    job = Job.objects.get(id=job_id, recruiter=request.user)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applicants.html', {'job': job, 'applications': applications})


@login_required(login_url='/login/')
def dashboard(request):
    if request.user.user_type == 'jobseeker':
        try:
            JobSeekerProfile.objects.get(user=request.user)
        except:
            return redirect('/profile/')
        jobs = Job.objects.all()
        return render(request, 'dashboard_jobseeker.html', {'jobs': jobs})

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'dashboard_recruiter.html', {'jobs': jobs})
