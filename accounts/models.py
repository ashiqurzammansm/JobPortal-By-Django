from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('jobseeker', 'Job Seeker'),
    )
    display_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, default='')
    company_description = models.TextField(default='')


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, default='')
    skills = models.TextField(default='')
    experience_years = models.IntegerField(default=0)
    job_type = models.CharField(max_length=50, default='Remote')
    preferred_location = models.CharField(max_length=150, default='Worldwide')
    expected_salary = models.CharField(max_length=100, default='Negotiable')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    openings = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField()


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(default=timezone.now)
