from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard),

    path('profile/', profile_redirect),
    path('jobseeker/profile/', jobseeker_profile),
    path('recruiter/profile/', recruiter_profile),

    path('jobs/', job_list),
    path('job/apply/<int:job_id>/', apply_job),
    path('applied/jobs/', applied_jobs),

    path('job/<int:job_id>/applicants/', job_applicants),
    path('application/<int:app_id>/<str:status>/', update_application_status),
    path('job/delete/<int:job_id>/', delete_job),
]
