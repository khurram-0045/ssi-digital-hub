from django.db import models

class Session(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Reg Open', 'Registration Open'),
        ('Ongoing', 'Ongoing'),
        ('Past', 'Past / Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255, default="Google Meet")
    speaker_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    
    # Media & Learning Materials (Managed from Admin Panel)
    thumbnail = models.ImageField(upload_to='session_thumbnails/', blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True, help_text="YouTube or Google Drive link to recorded session")
    slides_file = models.FileField(upload_to='session_slides/', blank=True, null=True, help_text="PDF or PPT slides")

    def __str__(self):
        return self.title

class Registration(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    university = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    registration_id = models.CharField(max_length=50, unique=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_id:
            import random
            self.registration_id = f"SSI-2026-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.registration_id}"

class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order sequence")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.role}"

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('Cheat Sheet', 'Cheat Sheet'),
        ('Code Template', 'Code Template'),
        ('Study Notes', 'Study Notes'),
        ('Configuration', 'Configuration File'),
        ('External Link', 'External Link'),
    ]

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('Cheat Sheet', 'Cheat Sheet'),
        ('Code Template', 'Code Template'),
        ('Study Notes', 'Study Notes'),
        ('Configuration', 'Configuration File'),
        ('External Link', 'External Link'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Study Notes')
    thumbnail = models.ImageField(upload_to='resource_thumbnails/', blank=True, null=True, help_text="Optional small thumbnail image")
    file = models.FileField(upload_to='resources_files/', blank=True, null=True)
    external_url = models.URLField(blank=True, null=True, help_text="Optional link if resource is online")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"    

from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=50, blank=True, null=True)
    university = models.CharField(max_length=150, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=100, default='Community Member', help_text="e.g. President, QA Lead, Member")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.designation})"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskDuty(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', help_text="Select member to assign this task")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} -> {self.assigned_to.username}"

class ProjectShowcase(models.Model):
    title = models.CharField(max_length=200)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    tech_stack = models.CharField(max_length=150, help_text="e.g. Python, Next.js, Django")
    project_url = models.URLField(blank=True, null=True, help_text="GitHub or Live Demo link")
    screenshot = models.ImageField(upload_to='project_screenshots/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.student.username}"   
    
class GalleryPhoto(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Hands-on Networking Workshop at NUST")
    image = models.ImageField(upload_to='gallery/')
    event_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
   