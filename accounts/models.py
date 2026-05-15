from django.contrib.auth.models import AbstractUser
from django.db import models
 
 
class User(AbstractUser):
    """
    Custom user model. Always use get_user_model() to reference this,
    never import directly. AUTH_USER_MODEL = 'accounts.User' in settings.
    """
 
    STUDENT = "student"
    COMPANY = "company"
    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (COMPANY, "Company"),
    ]
 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    headline = models.CharField(max_length=140, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=160, blank=True)
    website = models.URLField(blank=True)
 
    # Student-specific fields
    university = models.CharField(max_length=255, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    major = models.CharField(max_length=255, blank=True)
    skills = models.CharField(
        max_length=512, blank=True, help_text="Comma-separated list of skills"
    )
 
    # Company-specific fields
    company_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
 
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
 
    def is_student(self):
        return self.role == self.STUDENT
 
    def is_company(self):
        return self.role == self.COMPANY
 
    def __str__(self):
        return f"{self.username} ({self.role})"