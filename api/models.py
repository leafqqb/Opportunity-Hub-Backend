from datetime import date

from django.conf import settings
from django.db import models


class Opportunity(models.Model):
    INTERNSHIP = "Internship"
    SCHOLARSHIP = "Scholarship"
    COMPETITION = "Competition"
    COOP = "COOP"
    BOOTCAMP = "Bootcamp"
    VOLUNTEERING = "Volunteering"
    PROGRAM = "Program"

    OPPORTUNITY_TYPE_CHOICES = [
        (INTERNSHIP, "Internship"),
        (SCHOLARSHIP, "Scholarship"),
        (COMPETITION, "Competition"),
        (COOP, "COOP"),
        (BOOTCAMP, "Bootcamp"),
        (VOLUNTEERING, "Volunteering"),
        (PROGRAM, "Program"),
    ]

    title = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255)
    description = models.TextField()
    opportunity_type = models.CharField(
        max_length=32,
        choices=OPPORTUNITY_TYPE_CHOICES,
        default=INTERNSHIP,
    )
    category = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    external_url = models.URLField()
    application_deadline = models.DateField(null=True, blank=True)

    # Optional enrichment fields shown in the Figma detail page
    is_paid = models.BooleanField(null=True, blank=True)   # True/False/None (not applicable)
    is_urgent = models.BooleanField(default=False)
    major = models.CharField(max_length=255, blank=True)   # target major(s)
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opportunities",
    )

    # Soft-delete / admin control: admins can deactivate spam listings
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"

    @property
    def is_expired(self):
        """True when the deadline has passed. Computed, never stored."""
        if self.application_deadline:
            return self.application_deadline < date.today()
        return False

    @property
    def status(self):
        if not self.is_active:
            return "inactive"
        if self.is_expired:
            return "expired"
        return "active"

    def __str__(self):
        return f"{self.title} @ {self.organization_name}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sort by nearest deadline for the Deadline Tracker feature
        ordering = ["opportunity__application_deadline"]
        unique_together = [["user", "opportunity"]]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f"{self.user.username} → {self.opportunity.title}"