from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication, JobSeekerProfile, RecruiterProfile


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


@login_required
def dashboard(request):
    if request.user.user_type == 'jobseeker':
        return render(request, 'dashboard_jobseeker.html')

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'dashboard_recruiter.html', {'jobs': jobs})



@login_required
def profile_redirect(request):
    if request.user.user_type == 'jobseeker':
        return redirect('/jobseeker/profile/')
    return redirect('/recruiter/profile/')


# ---------- JOBSEEKER PROFILE ----------
@login_required
def jobseeker_profile(request):
    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            request.user.profile_image = request.FILES.get('profile_image')
            request.user.save()

        profile.full_name = request.POST['full_name']
        profile.skills = request.POST['skills']
        profile.experience_years = request.POST['experience_years']
        profile.job_type = request.POST['job_type']
        profile.preferred_location = request.POST['preferred_location']
        profile.expected_salary = request.POST['expected_salary']

        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')

        profile.save()
        return redirect('/dashboard/')

    return render(request, 'jobseeker_profile.html', {'profile': profile})


# ---------- RECRUITER PROFILE ----------
@login_required
def recruiter_profile(request):
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.company_name = request.POST['company_name']
        profile.company_description = request.POST['company_description']
        profile.save()
        return redirect('/dashboard/')

    return render(request, 'recruiter_profile.html', {'profile': profile})


@login_required
def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(title__icontains=query)
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if JobApplication.objects.filter(job=job, jobseeker=request.user).exists():
        return redirect('/applied/jobs/')
    JobApplication.objects.create(job=job, jobseeker=request.user)
    return redirect('/applied/jobs/')


@login_required
def applied_jobs(request):
    apps = JobApplication.objects.filter(jobseeker=request.user)
    return render(request, 'applied_jobs.html', {'applications': apps})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    apps = JobApplication.objects.filter(job=job)
    return render(request, 'job_applicants.html', {'applications': apps, 'job': job})


@login_required
def update_application_status(request, app_id, status):
    app = get_object_or_404(JobApplication, id=app_id, job__recruiter=request.user)
    app.status = status
    app.save()
    return redirect(f'/job/{app.job.id}/applicants/')


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    job.delete()
    return redirect('/dashboard/')
