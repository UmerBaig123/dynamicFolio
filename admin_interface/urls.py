from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_admin, name='admin_auth'),
    path('select_repos/', views.select_repos.as_view(), name='repos_select'),
    path('about/', views.edit_about, name='admin_about'),
    path('repos/', views.edit_repos, name='admin_repos'),
    path('teachings/', views.teachings, name='admin_teachings'),
    path('publications/', views.edit_publications, name='admin_publications'),
    path('delete_publications/', views.delete_publication.as_view(), name='delete_publication'),
    path('edit_publications/', views.edit_publication.as_view(), name='edit_publication'),
    path('add_description/', views.add_page_description.as_view(), name='add_page_description'),
    path('delete_course/', views.delete_course.as_view(), name='delete_course'),
    path('edit_course/', views.edit_course.as_view(), name='edit_course'),
    path('resume/', views.edit_resume, name='admin_resume'),
    path('add_experience/', views.add_experience.as_view(), name='add_experience'),
    path('edit_experience/', views.edit_experience.as_view(), name='edit_experience'),
    path('delete_experience/', views.delete_experience.as_view(), name='delete_experience'),
    path('add_gitlab/', views.add_or_edit_gitlabid.as_view(), name='add_gitlab'),
    path('add_google_scholar/', views.load_google_scholar_into_db.as_view(), name='add_gs'),
    path('select_google_scholar/', views.select_gs_article.as_view(), name='select_gs'),
    path('add_pdf_to_gs/', views.add_pdf_to_gs.as_view(), name='add_pdf'),
    path('add_video_to_gs/', views.add_video_to_gs.as_view(), name='add_video'),
    path('select_for_about_me/', views.select_for_about_me.as_view(), name='select_aboutme'),
    path('delete_news/', views.deleteNews.as_view(), name='delete_news'),
    path('news/', views.edit_news, name='admin_news'),

]