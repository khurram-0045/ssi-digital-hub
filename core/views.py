from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Session, Registration, TeamMember, Resource, ContactMessage, StudentProfile, Announcement, TaskDuty,ProjectShowcase, GalleryPhoto

def home_view(request):
    sessions_list = Session.objects.filter(status='Upcoming') | Session.objects.filter(status='Reg Open')
    featured_session = sessions_list.order_by('date').first()
    context = {
        'sessions': sessions_list,
        'featured_session': featured_session,
    }
    return render(request, 'core/home.html', context)

def sessions_list_view(request):
    upcoming_sessions = Session.objects.filter(status__in=['Upcoming', 'Reg Open', 'Ongoing']).order_by('date')
    past_sessions = Session.objects.filter(status='Past').order_by('-date')
    
    context = {
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
    }
    return render(request, 'core/sessions.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def team_view(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/team.html', {'team_members': team_members})

def resources_view(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'core/resources.html', {'resources': resources})

def contact_view(request):
    success = False
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )
        success = True

    return render(request, 'core/contact.html', {'success': success})

def register_view(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        university = request.POST.get('university')
        department = request.POST.get('department')
        
        registration = Registration.objects.create(
            session=session,
            full_name=full_name,
            email=email,
            phone=phone,
            university=university,
            department=department
        )
        return render(request, 'core/success.html', {'registration': registration, 'session': session})

    return render(request, 'core/register.html', {'session': session})

def member_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('member_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def member_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        university = request.POST.get('university')
        department = request.POST.get('department')
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            StudentProfile.objects.get_or_create(
                user=user, 
                defaults={'university': university, 'department': department, 'designation': 'SSI Member'}
            )
            login(request, user)
            return redirect('member_dashboard')
    return render(request, 'core/signup.html')

@login_required(login_url='member_login')
def member_dashboard_view(request):
    user_registrations = Registration.objects.filter(email=request.user.email)
    announcements = Announcement.objects.all().order_by('-created_at')
    user_tasks = TaskDuty.objects.filter(assigned_to=request.user)
    
    # Try to fetch team member profile if name matches username or full name
    team_member_profile = TeamMember.objects.filter(name__iexact=request.user.username).first()
    
    context = {
        'user_registrations': user_registrations,
        'announcements': announcements,
        'user_tasks': user_tasks,
        'team_member_profile': team_member_profile,
    }
    return render(request, 'core/dashboard.html', context)

def member_logout_view(request):
    logout(request)
    return redirect('home')

def showcase_view(request):
    projects = ProjectShowcase.objects.all().order_by('-submitted_at')
    return render(request, 'core/showcase.html', {'projects': projects})

def gallery_view(request):
    photos = GalleryPhoto.objects.all().order_by('-event_date', '-uploaded_at')
    return render(request, 'core/gallery.html', {'photos': photos})

@login_required
def submit_project_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tech_stack = request.POST.get('tech_stack')
        project_url = request.POST.get('project_url')
        screenshot = request.FILES.get('screenshot')

        ProjectShowcase.objects.create(
            title=title,
            student=request.user,
            description=description,
            tech_stack=tech_stack,
            project_url=project_url,
            screenshot=screenshot
        )
        return redirect('showcase')
    return render(request, 'core/submit_project.html')