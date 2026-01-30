from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),

    path('dashboard/', views.dashboard),

    path('profile/', views.profile_redirect),
    path('jobseeker/profile/', views.jobseeker_profile),
    path('recruiter/profile/', views.recruiter_profile),

    path('jobs/', views.job_list),
    path('job/apply/<int:job_id>/', views.apply_job),
    path('applied/jobs/', views.applied_jobs),

    path('job/post/', views.post_job),
    path('job/edit/<int:job_id>/', views.edit_job),
    path('job/delete/<int:job_id>/', views.delete_job),

    path('job/<int:job_id>/applicants/', views.job_applicants),
]
