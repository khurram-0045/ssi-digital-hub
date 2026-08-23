from django.urls import path
from .views import (
    home_view, sessions_list_view, register_view, about_view, 
    team_view, resources_view, contact_view, 
    member_login_view, member_signup_view, member_dashboard_view, member_logout_view,showcase_view, gallery_view,submit_project_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('sessions/', sessions_list_view, name='sessions_list'),
    path('about/', about_view, name='about'),
    path('team/', team_view, name='team'),
    path('resources/', resources_view, name='resources'),
    path('contact/', contact_view, name='contact'),
    path('register/<int:session_id>/', register_view, name='register_session'),
    path('login/', member_login_view, name='member_login'),
    path('signup/', member_signup_view, name='member_signup'),
    path('dashboard/', member_dashboard_view, name='member_dashboard'),
    path('logout/', member_logout_view, name='member_logout'),
    path('showcase/', showcase_view, name='showcase'),
    path('gallery/', gallery_view, name='gallery'),
    path('showcase/submit/', submit_project_view, name='submit_project'),

]