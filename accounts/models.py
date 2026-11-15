from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

CATEGORY_CHOICES = [
    ('general', 'General'),
    ('obc', 'OBC'),
    ('sc', 'SC'),
    ('st', 'ST'),
]

EDUCATION_CHOICES = [
    ('below_10', 'Below 10th'),
    ('10th', '10th Pass'),
    ('12th', '12th Pass'),
    ('graduate', 'Graduate'),
    ('postgraduate', 'Post Graduate'),
]

INDIAN_STATES = [
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('bihar', 'Bihar'),
    ('delhi', 'Delhi'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('west_bengal', 'West Bengal'),
    ('other', 'Other'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    annual_income = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
    state = models.CharField(max_length=30, choices=INDIAN_STATES, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def is_complete(self):
        return all([self.age, self.gender, self.annual_income, self.category, self.state, self.education])
