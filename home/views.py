from django.shortcuts import render, HttpResponse
from django import template
from types import SimpleNamespace
import dotenv
import os
from admin_interface.models import userdata, selected_repos,publication,page_description_text,courses,experience,generalInfo,gitlab_ids,selected_gitlab_repos,gs_citation_ids,google_scholar_article,about_me_selected_publications,about_me_selected_gs,news
# Create your views here.
dotenv.load_dotenv()
API_KEY = os.environ['GITLABAPITOKEN']
register = template.Library()
 
def home_page(request):
    userFullName= ""
    animation = False
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
        if userdata.objects.all()[0].onload_animation is True:
            animation = True
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    full_name = ""
    gitlab_id = ""
    if gitlab_ids.objects.all().count() != 0:
        gitlab_id = gitlab_ids.objects.all()[0].gitlab_id
    gitlab_repos = selected_gitlab_repos.objects.all()
    if gitlab_repos.count() == 0:
        gitlab_repos = ""
    else:
        gitlab_repos = [repo.repo_id for repo in selected_gitlab_repos.objects.all()]
        gitlab_repos = ",".join(gitlab_repos)
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    if userdata.objects.all().count() == 0:
        return render(request, 'home.html', {"showNews":showNews,})
    repos = selected_repos.objects.all()
    
    if repos.count() == 0:
        repos = "none"
    else:
        repos = [repo.repo_id for repo in selected_repos.objects.all()]
        repos = ",".join(repos)
    userdata_obj = userdata.objects.all()[0]
    publications =[pub.pub for pub in about_me_selected_publications.objects.all()]
    mynews = news.objects.all().order_by('-news_date')
    return render(request, 'home.html', {"showNews":showNews,"userdata": userdata_obj, "repos": repos,"publications":publications,"full_name":full_name,"api_key":API_KEY,"gitlab_id":gitlab_id,"gitlab_repos":gitlab_repos,'gs_publications':about_me_selected_gs.get_gs_with_pdf_videos(),"news":mynews,"animation":animation})
def repository(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    
    gitlab_id = ""
    if gitlab_ids.objects.all().count() != 0:
        gitlab_id = gitlab_ids.objects.all()[0].gitlab_id
    gitlab_repos = selected_gitlab_repos.objects.all()
    if gitlab_repos.count() == 0:
        gitlab_repos = ""
    else:
        gitlab_repos = [repo.repo_id for repo in selected_gitlab_repos.objects.all()]
        gitlab_repos = ",".join(gitlab_repos)
    description_text = ""
    if page_description_text.objects.filter(page_name="repositories").count() != 0:
        description_text = page_description_text.objects.filter(page_name="repositories")[0]
    github_username = ""
    githubshow = False
    if userdata.objects.all().count() != 0:
        github_username = userdata.objects.all()[0].github_username
        githubshow = userdata.objects.all()[0].showGithubUser

    if selected_repos.objects.all().count() == 0:
        return render(request, 'repository.html', {"showNews":showNews,"repos":"none","github_username":github_username,"description_text":description_text,"full_name":full_name,"gitlab_id":gitlab_id,"gitlab_repos":gitlab_repos,"githubshow":githubshow})
    repos = [repo.repo_id for repo in selected_repos.objects.all()]
    repos = ",".join(repos)
    return render(request, 'repository.html', {"showNews":showNews,"repos":repos,"github_username":github_username,"description_text":description_text,"full_name":full_name,"gitlab_id":gitlab_id,"gitlab_repos":gitlab_repos,"githubshow":githubshow})
def publications(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    page_desc = ""
    if page_description_text.objects.filter(page_name="publications").count() != 0:
        page_desc = page_description_text.objects.filter(page_name="publications")[0]
    publications = publication.objects.all()
    return render(request, 'publications.html', {"showNews":showNews,"publications":publications,"description_text":page_desc,"full_name":full_name,'gs_publications':google_scholar_article.getAllSelectedWithPdf()})
def teachings(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    description_text= ""
    myCourses = courses.objects.all()
    if page_description_text.objects.filter(page_name="teachings").count() != 0:
        description_text = page_description_text.objects.filter(page_name="teachings")[0]
    return render(request, 'teachings.html', {"showNews":showNews,"description": description_text,"courses":myCourses,"full_name":full_name})
def resume(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True 
    education_exp = []
    professional_exp = []
    academic_exp = []   
    award_exp = []   
    showEducation = False
    showProfessional = False
    showAcademic = False
    showAward = False
    myUserdata = ""
    fullName=""
    email=""
    linkedin=""
    if userdata.objects.all().count() != 0:
        myUserdata = userdata.objects.all()[0]
        fullName = myUserdata.first_name + " " + myUserdata.last_name
        email = myUserdata.email_address
        linkedin = myUserdata.linkedin_url
    experience_ids = []
    if experience.objects.all().count() != 0:
        experience_ids = [str(exp.id) for exp in experience.objects.all()]
    experience_ids = ",".join(experience_ids)
    if experience.objects.filter(experience_type="education").count() != 0:
        education_exp = experience.objects.filter(experience_type="education")
        showEducation = True
    if experience.objects.filter(experience_type="professional").count() != 0:
        professional_exp = experience.objects.filter(experience_type="professional")
        showProfessional = True
    if experience.objects.filter(experience_type="academic").count() != 0:
        academic_exp = experience.objects.filter(experience_type="academic")
        showAcademic = True
    if experience.objects.filter(experience_type="award").count() != 0:
        award_exp = experience.objects.filter(experience_type="award")
        showAward = True
    if generalInfo.objects.all().count() != 0:
        myGeneralInfo = generalInfo.objects.all()[0]
        return render(request, 'resume.html',{"showNews":showNews,"experience_ids":experience_ids,"info":myGeneralInfo,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward,"full_name":fullName})
    return render(request, 'resume.html',{"showNews":showNews,"experience_ids":experience_ids,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward,"full_name":fullName})
def news_view_more(request,news_id):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    this_news = news.objects.filter(id=news_id)[0]
    return render(request, "view_news.html",{"news":this_news,"full_name":userFullName,"showNews":True})
def home_news(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    myNews = news.objects.all().order_by('-news_date')
    return render(request, 'news.html', {"news":myNews,"full_name":userFullName,"showNews":True}) 