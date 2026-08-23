from django.contrib import admin
from .models import Session, Registration, TeamMember, Resource, ContactMessage, StudentProfile, Announcement, TaskDuty,ProjectShowcase, GalleryPhoto

admin.site.register(Session)
admin.site.register(Registration)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    search_fields = ('name', 'role')
    list_editable = ('order',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')    

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'sent_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    list_filter = ('sent_at',)   

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'university', 'department')
    list_filter = ('designation', 'university')
    search_fields = ('user__username', 'user__email', 'designation')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')

@admin.register(TaskDuty)
class TaskDutyAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description')

@admin.register(ProjectShowcase)
class ProjectShowcaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'tech_stack', 'submitted_at')
    search_fields = ('title', 'student__username', 'tech_stack')
    list_filter = ('submitted_at',) 

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'uploaded_at')
    search_fields = ('title', 'description')
    list_filter = ('event_date',)      