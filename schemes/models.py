from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

SCHEME_CATEGORY_CHOICES = [
    ('education', 'Education'),
    ('health', 'Health'),
    ('agriculture', 'Agriculture'),
    ('housing', 'Housing'),
    ('employment', 'Employment'),
    ('social_welfare', 'Social Welfare'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class Scheme(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SCHEME_CATEGORY_CHOICES)
    organization = models.CharField(max_length=200)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    max_income = models.PositiveIntegerField(null=True, blank=True)
    eligible_genders = models.CharField(
        max_length=50, blank=True,
        help_text='Comma-separated: male,female,other. Leave blank for all.'
    )
    eligible_categories = models.CharField(
        max_length=50, blank=True,
        help_text='Comma-separated: general,obc,sc,st. Leave blank for all.'
    )
    min_education = models.CharField(max_length=20, choices=[
        ('', 'Any'),
        ('below_10', 'Below 10th'),
        ('10th', '10th Pass'),
        ('12th', '12th Pass'),
        ('graduate', 'Graduate'),
        ('postgraduate', 'Post Graduate'),
    ], blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_schemes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Scheme.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class SchemeApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
    reason = models.TextField(help_text='Why do you want to apply for this scheme?')
    admin_remarks = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'scheme']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} - {self.scheme.name}"
