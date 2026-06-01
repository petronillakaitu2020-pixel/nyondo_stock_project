from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    Custom user model for Nyondo Hardware system
    """
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('stock', 'Stock Personnel'),
        ('sales', 'Sales Personnel'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales')
    nin = models.CharField(max_length=14, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex=r'^(07|03)\d{8}$', message="Enter a valid Ugandan phone number (07XXXXXXXX or 03XXXXXXXX)")                                                                     
        ],
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.username} ({self.role})"