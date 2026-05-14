from django.conf import settings
from django.db import models


class Profile(models.Model):
    STUDENT = 'student'
    COMPANY = 'company'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (COMPANY, 'Company'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    headline = models.CharField(max_length=140, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=160, blank=True)
    website = models.URLField(blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    university = models.CharField(max_length=255, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    skills = models.CharField(max_length=512, blank=True, help_text='Comma-separated skills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Opportunity(models.Model):
    INTERNSHIP = 'Internship'
    SCHOLARSHIP = 'Scholarship'
    FELLOWSHIP = 'Fellowship'
    JOB = 'Job'
    COURSE = 'Course'
    EVENT = 'Event'
    GRANT = 'Grant'
    OTHER = 'Other'

    OPPORTUNITY_TYPE_CHOICES = [
        (INTERNSHIP, 'Internship'),
        (SCHOLARSHIP, 'Scholarship'),
        (FELLOWSHIP, 'Fellowship'),
        (JOB, 'Job'),
        (COURSE, 'Course'),
        (EVENT, 'Event'),
        (GRANT, 'Grant'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255)
    description = models.TextField()
    opportunity_type = models.CharField(max_length=32, choices=OPPORTUNITY_TYPE_CHOICES, default=OTHER)
    category = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    external_url = models.URLField()
    application_deadline = models.DateField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.organization_name}"


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['user', 'opportunity']]

    def __str__(self):
        return f"{self.user.username} bookmarked {self.opportunity.title}"
