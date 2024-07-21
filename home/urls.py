
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_page, name='home'),
    path('repositories/', views.repository, name='home_repos'),
    path('publications/', views.publications, name='home_publications'),
    path('teachings/', views.teachings, name='home_teachings'),
    path('resume/', views.resume, name='home_resume'),
]
