from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator




class EntityType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=200)
    entity_type = models.ForeignKey(EntityType, on_delete=models.PROTECT, related_name='entities')
    description = models.TextField()
    image = models.ImageField(upload_to='entity_images/', null=True, blank=True)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    director_name = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    upvotes = models.IntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_from_application = models.BooleanField(default=False)

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    def __str__(self):
        return self.name

class Upvote(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='entity_upvotes')
    name = models.CharField(max_length=100, blank=True, default='Anonymous')
    role = models.CharField(max_length=100, blank=True)
    reason = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('entity', 'ip_address')

    def __str__(self):
        return f"Upvote for {self.entity.name} by {self.name}"
    


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    name = models.CharField(max_length=200)
    entity_type = models.ForeignKey(EntityType, on_delete=models.PROTECT, related_name='applications')
    description = models.TextField()
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applicant_name = models.CharField(max_length=100, null=True)
    applicant_role = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    



class VisitorApplication(models.Model):
    APPLICATION_TYPES = (
        ('visit', 'Visit'),
        ('internship', 'Internship'),
        ('job', 'Job'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='visitor_applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    application_type = models.CharField(max_length=10, choices=APPLICATION_TYPES)
    message = models.TextField()
    cv = models.FileField(upload_to='visitor_cvs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}'s {self.get_application_type_display()} application for {self.entity.name}"