from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication, JobSeekerProfile, RecruiterProfile


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                display_name=request.POST['display_name'],
                user_type=request.POST['user_type']
            )
            return redirect('/login/')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def dashboard(request):
    if request.user.user_type == 'jobseeker':
        return render(request, 'dashboard_jobseeker.html')

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'dashboard_recruiter.html', {'jobs': jobs})


@login_required(login_url='/login/')
def profile_redirect(request):
    if request.user.user_type == 'jobseeker':
        return redirect('/jobseeker/profile/')
    return redirect('/recruiter/profile/')


@login_required(login_url='/login/')
def recruiter_profile(request):
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.company_name = request.POST['company_name']
        profile.company_description = request.POST['company_description']
        profile.save()
        return redirect('/dashboard/')

    return render(request, 'recruiter_profile.html', {'profile': profile})


@login_required(login_url='/login/')
def jobseeker_profile(request):
    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.full_name = request.POST['full_name']
        profile.skills = request.POST['skills']
        profile.experience_years = request.POST['experience_years']
        profile.save()
        return redirect('/dashboard/')

    return render(request, 'jobseeker_profile.html', {'profile': profile})


@login_required(login_url='/login/')
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required(login_url='/login/')
def post_job(request):
    if request.method == 'POST':
        Job.objects.create(
            recruiter=request.user,
            title=request.POST['title'],
            description=request.POST['description']
        )
        return redirect('/dashboard/')
    return render(request, 'post_job.html')


@login_required(login_url='/login/')
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.save()
        return redirect('/dashboard/')

    return render(request, 'edit_job.html', {'job': job})


@login_required(login_url='/login/')
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    job.delete()
    return redirect('/dashboard/')


@login_required(login_url='/login/')
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if not JobApplication.objects.filter(job=job, jobseeker=request.user).exists():
        JobApplication.objects.create(job=job, jobseeker=request.user)

    return redirect('/applied/jobs/')


@login_required(login_url='/login/')
def applied_jobs(request):
    applications = JobApplication.objects.filter(jobseeker=request.user)
    return render(request, 'applied_jobs.html', {'applications': applications})


@login_required(login_url='/login/')
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applicants.html', {
        'job': job,
        'applications': applications
    })
