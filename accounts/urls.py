from django.urls import path
from .views import (
    register, login_view, logout_view,
    dashboard, profile_redirect,
    recruiter_profile, jobseeker_profile,
    post_job, job_list, apply_job,
    applied_jobs, job_applicants
)

urlpatterns = [
    path('', dashboard),
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard),
    path('profile/', profile_redirect),
    path('recruiter/profile/', recruiter_profile),
    path('jobseeker/profile/', jobseeker_profile),
    path('job/post/', post_job),
    path('jobs/', job_list),
    path('job/apply/<int:job_id>/', apply_job),
    path('applied/jobs/', applied_jobs),
    path('job/<int:job_id>/applicants/', job_applicants),
]
