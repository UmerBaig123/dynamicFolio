from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from .models import userdata,selected_repos,publication,page_description_text,courses,experience,generalInfo,gitlab_ids,selected_gitlab_repos,google_scholar_article,gs_citation_ids,about_me_selected_gs,about_me_selected_publications,news
import datetime
import os
from dotenv import load_dotenv
import logging
# Create your views here.
logger = logging.getLogger(__name__)
load_dotenv()
loginUrl = os.environ['ADMINROUTE']
gitlab_api_key = os.environ['GITLABAPITOKEN']
serpapi_key = os.environ['SERPAPIKEY']
@login_required(login_url=loginUrl)
def edit_about(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.method == 'POST':
        showGithubUser = False
        news_view = False
        animation = False
        if request.POST.get('showGithubUser') is not None:
            show = request.POST['showGithubUser']
            if show == "on":
                showGithubUser = True
        if request.POST.get('view_news') is not None:
            news = request.POST['view_news']
            if news == "on":
                news_view = True
        if request.POST.get('animation') is not None:
            anim = request.POST['animation']
            if anim == "on":
                animation = True
        if request.FILES.get('profile_pic') is not None:
            profile_pic = request.FILES['profile_pic']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email_address']
        linkedin = request.POST['linkedin_url']
        github = request.POST['github_username']
        qualification = request.POST['qualification']
        university = request.POST['university']
        universityUrl = request.POST['university_url']
        summary = request.POST['summary']
        if len(userdata.objects.all()) == 0:
            if request.FILES.get('profile_pic') is not None:
                myData = userdata(profile_pic=profile_pic,first_name=first_name,last_name=last_name,email_address=email,linkedin_url=linkedin,github_username=github,qualification=qualification,university=university,university_url=universityUrl,summary=summary,showGithubUser=showGithubUser,view_news=news_view,onload_animation=animation)
            else:
                myData = userdata(first_name=first_name,last_name=last_name,email_address=email,linkedin_url=linkedin,github_username=github,qualification=qualification,university=university,university_url=universityUrl,summary=summary,showGithubUser=showGithubUser,view_news=news_view,onload_animation=animation)
            myData.save()
            return redirect('admin_about')
        myData = userdata.objects.all()[0]
        myData.showGithubUser = showGithubUser
        myData.view_news = news_view
        if request.FILES.get('profile_pic') is not None:
            try:
                deletingPic =  myData.profile_pic.path
                if os.path.exists(deletingPic):
                    os.remove(deletingPic)
            except:
                pass
            myData.profile_pic = profile_pic
        myData.first_name = first_name
        myData.last_name = last_name
        myData.email_address = email
        myData.linkedin_url = linkedin
        myData.github_username = github
        myData.qualification = qualification
        myData.university = university
        myData.university_url = universityUrl
        myData.summary = summary
        myData.onload_animation = animation
        myData.save()
        return redirect ('admin_about')
    if len(userdata.objects.all()) != 0:
        myData = userdata.objects.all()[0]
        return render(request, 'edit_about.html',{"userFullName":userFullName,"showNews":showNews,
        "userdata":myData,
        "profile_pic":myData.profile_pic,
        "first_name":myData.first_name,
        "last_name":myData.last_name,
        "email":myData.email_address,
        "linkedin":myData.linkedin_url,
        "github":myData.github_username,
        "qualification":myData.qualification,
        "university":myData.university,
        "universityUrl":myData.university_url,
        "summary":myData.summary,
        "view_news":myData.view_news,
        "animation":myData.onload_animation,
        })
    return render(request, 'edit_about.html',{"userFullName":userFullName,"showNews":showNews,})
@login_required(login_url=loginUrl)
def edit_repos(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.method == 'POST':
        page_description = request.POST['page_description']
        page_title = "repositories"
        if page_description_text.objects.filter(page_name=page_title).count() != 0:
            myPageDescription = page_description_text.objects.filter(page_name=page_title)[0]
            myPageDescription.text = page_description
            myPageDescription.save()
        else:
            myPageDescription = page_description_text(page_name=page_title,text=page_description)
            myPageDescription.save()
        return redirect('admin_repos')
    page_desc = ""
    gitlab_id = ""
    myGitlabRepos = ""
    if gitlab_ids.objects.all().count() != 0:
        gitlab_id = gitlab_ids.objects.all()[0].gitlab_id
    if selected_gitlab_repos.objects.all().count() != 0:
        myGitlabRepos = [repo.repo_id for repo in selected_gitlab_repos.objects.all()]
        myGitlabRepos = ','.join(myGitlabRepos)
    if page_description_text.objects.filter(page_name="repositories").count() != 0:
        page_desc = page_description_text.objects.filter(page_name="repositories")[0].text
    if len(userdata.objects.all()) != 0:
        myData = userdata.objects.all()[0]
        if len(selected_repos.objects.all()) != 0:
            myRepos = [repo.repo_id for repo in selected_repos.objects.all()]
            myRepos = ','.join(myRepos)
            return render(request, 'edit_repos.html',{"userFullName":userFullName,"showNews":showNews,"username":myData.github_username,"repos":myRepos,"page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})
        return render(request, 'edit_repos.html',{"userFullName":userFullName,"showNews":showNews,"username":myData.github_username,"repos":"none","page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})
    return render(request, 'edit_repos.html',{"userFullName":userFullName,"showNews":showNews,"page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})


def login_admin(request):
    
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.user.is_authenticated:
        return redirect('admin_about')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check if the user exists in the database
        user = authenticate(request, username=username, password=password)
        # If the user exists
        if user is not None:
            login(request, user)
            return redirect('admin_about')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('admin_auth')
    return render(request, 'login.html',{"userFullName":userFullName,"showNews":showNews,})   
class select_repos(APIView):
    def post(self,request): 
        repos = request.data['repos']
        gitlab_repos = request.data['gitlab_repos']
        selected_gitlab_repos.objects.all().delete()
        selected_repos.objects.all().delete()
        for repo in gitlab_repos:
            myRepo = selected_gitlab_repos(repo_id=int(repo))
            myRepo.save()
        for repo in repos:
            myRepo = selected_repos(repo_id=int(repo))
            myRepo.save()
        return Response({"message":"Repos selected successfully","status":200})

@login_required(login_url=loginUrl)
def edit_publications(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.method == 'POST':
        pdfFile = ""
        videoFile = ""
        publication_image = ""
        pref = 0
        if request.POST['preference'] != "":
            pref = request.POST['preference']
        publication_date = datetime.datetime.now()
        title = request.POST['publication_title']
        authors = request.POST['publication_authors']
        description = request.POST['publication_description']
        abstract = request.POST['abs']
        arxiv_url = request.POST['arxiv_url']
        bib = request.POST['bib']
        doi = request.POST['doi']
        if request.POST['publication_date'] != "":
            publication_date = request.POST['publication_date']
        if request.FILES.get('pdf_file') is not None:
            pdfFile = request.FILES['pdf_file']
        if request.FILES.get('video') is not None:
            videoFile = request.FILES['video']
        if request.FILES.get('publication_image') is not None:
            publication_image = request.FILES['publication_image']
        myPublication = publication(doi=doi,title=title,authors=authors,description=description,abs=abstract,arxiv_url=arxiv_url,bib=bib,pdfFile=pdfFile,publication_image=publication_image,publication_date=publication_date,video=videoFile,preference=pref)
        myPublication.save()
        return redirect('admin_publications')
    description = ""
    if page_description_text.objects.filter(page_name="publications").count() != 0:
        description = page_description_text.objects.filter(page_name="publications")[0].text
    publications = publication.objects.all().order_by('-preference')
    gs_articles = google_scholar_article.objects.all()
    aboutme_gs_ids = [ gs.gs.pk for gs in about_me_selected_gs.objects.all()]
    aboutme_pub_ids = [ pub.pub.pk for pub in about_me_selected_publications.objects.all()] 
    return render(request, 'edit_publications.html',{"userFullName":userFullName,"showNews":showNews,"publications":publications,"description":description,"gs_articles_all":gs_articles,"gs_selected":google_scholar_article.getAllSelectedWithPdf(),"aboutme_gs_ids":aboutme_gs_ids,"aboutme_pub_ids":aboutme_pub_ids})
class delete_publication(APIView):
    def post(self,request): 
        publication_id = request.data['publication_id']
        thisPublication = publication.objects.get(id=publication_id)
        # Delete the pdfFile from the system
        try:
            pdf_file_path = thisPublication.pdfFile.path
            image_file_path = thisPublication.publication_image.path
            video_file_path = thisPublication.video.path
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
            if os.path.exists(video_file_path):
                os.remove(video_file_path)
        except:
            pass
        thisPublication.delete()
        return Response({"message":"Publication deleted successfully","status":200})
class select_gs_article(APIView):
    def post(self,request):
        all_articles = google_scholar_article.objects.all()
        for article in all_articles:
            article.isSelected = False
            article.save()
        citation_ids = request.data['citation_ids']
        db_citations = gs_citation_ids.objects.all()
        for id in citation_ids:
            if id not in [ob.citation_id for ob in db_citations]:
                myCitation = gs_citation_ids(citation_id=id)
                myCitation.save()
            thisArticle = google_scholar_article.objects.get(citation_id=id)
            thisArticle.isSelected = True
            thisArticle.save()
        return Response({"message":"Article selected successfully","status":200})
class load_google_scholar_into_db(APIView):
    def post(self,request):
        citation_ids = [ob.citation_id for ob in gs_citation_ids.objects.all()]
        if request.data['gs_id'] is None:
            return Response({"message":"Publication id is required","status":400})
        gs_id = request.data['gs_id']
        google_scholar_article.objects.all().delete()
        url = "https://serpapi.com/search?engine=google_scholar_author&author_id="+gs_id+"&hl=en&api_key="+serpapi_key+"&num=100"
        response = requests.get(url)
        data = response.json()
        if len(data['articles']) == 0 or data['articles'] is None:
            return Response({"message":"No articles found","status":400})
        articles = data['articles']
        for article in articles:
            title = article['title']
            authors = article['authors']
            publication = ""
            if 'publication' in article:
                publication = article['publication']
            year = article['year']
            link = article['link']
            citation_id = article['citation_id']
            isSelected = citation_id in citation_ids
            cited_by = 0
            if 'cited_by' in article and 'value' in article['cited_by'] and article['cited_by']['value'] != "":
                cited_by = article['cited_by']['value']
            myPublication = google_scholar_article(title=title,authors=authors,publication=publication,year=year,link=link,citation_id=citation_id,cited_by=cited_by,isSelected=isSelected)
            myPublication.save()
        return Response({"message":"Google Scholar articles loaded successfully","status":200})
class edit_publication(APIView):
    def post(self,request):
        publication_id = request.data['id']
        title = request.data['title']
        authors = request.data['authors']
        pref = 0
        if request.data['preference'] != "":
            pref = request.data['preference']
        description = request.data['desc']
        abstract = request.data['abs']
        arxiv_url = request.data['arxiv']
        bib = request.data['bib']
        doi = request.data['doi']
        publication_date = request.data['date']
        pdfFile = ""
        publication_image = ""
        video = ""
        if request.FILES.get('pdf') is not None:
            pdfFile = request.FILES['pdf']
        if request.FILES.get('image') is not None:
            publication_image = request.FILES['image']
        if request.FILES.get('video') is not None:
            video = request.FILES['video']
        thisPublication = publication.objects.get(id=publication_id)
        thisPublication.title = title
        thisPublication.authors = authors
        thisPublication.description = description
        thisPublication.abs = abstract
        thisPublication.arxiv_url = arxiv_url
        thisPublication.bib = bib
        thisPublication.doi = doi
        thisPublication.preference = pref
        if pdfFile != "":
            try:
                deletingPdf = thisPublication.pdfFile.path
                if os.path.exists(deletingPdf):
                    os.remove(deletingPdf)
            except:
                pass
            thisPublication.pdfFile = pdfFile
        if publication_image != "":
            try:
                deletingImage = thisPublication.publication_image.path
                if os.path.exists(deletingImage):
                    os.remove(deletingImage)
            except:
                pass
            thisPublication.publication_image = publication_image
        if video != "":
            try:
                deletingVideo = thisPublication.video.path
                if os.path.exists(deletingVideo):
                    os.remove(deletingVideo)
            except:
                pass
            thisPublication.video = video
        if publication_date != "":
            thisPublication.publication_date = publication_date
        thisPublication.save()
        return Response({"message":"Publication edited successfully","status":200})
class add_page_description(APIView):
    def post(self,request):
        page_name = request.data['page_name']
        page_description = request.data['page_description']
        if page_description_text.objects.filter(page_name=page_name).count() != 0:
            myPageDescription = page_description_text.objects.filter(page_name=page_name)[0]
            myPageDescription.text = page_description
            myPageDescription.save()
        else:
            myPageDescription = page_description_text(page_name=page_name,text=page_description)
            myPageDescription.save()
        return Response({"message":"Page description added successfully","status":200})
class edit_course(APIView):
    def post(self,request):
        course_id = request.data['course_id']
        course_year = request.data['course_year']
        course_name = request.data['course_name']
        institution_name = request.data['institution_name']
        role = request.data['role']
        students_level = request.data['students_level']
        hours = request.data['hours']
        thisCourse = courses.objects.get(id=course_id)
        thisCourse.course_year = course_year
        thisCourse.course_name = course_name
        thisCourse.institution_name = institution_name
        thisCourse.role = role
        thisCourse.students_level = students_level
        thisCourse.hours = hours
        thisCourse.save()
        return Response({"message":"Course edited successfully","status":200})
class add_or_edit_gitlabid(APIView):
    def post(self,request):
        my_gitlab_id = int(request.data['gitlab_id'])
        if gitlab_ids.objects.all().count() != 0:
            myData = gitlab_ids.objects.all()[0]
            myData.gitlab_id = my_gitlab_id
            myData.save()
        else:
            myData = gitlab_ids(gitlab_id=my_gitlab_id)
            myData.save()
        return Response({"message":"Gitlab Id added successfully","status":200})
class delete_course(APIView):
    def post(self,request):
        course_id = request.data['course_id']
        thisCourse = courses.objects.get(id=course_id)
        thisCourse.delete()
        return Response({"message":"Course deleted successfully","status":200})
@login_required(login_url=loginUrl)
def teachings(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.method == 'POST':
        course_year = request.POST['course_year']
        course_name = request.POST['course_name']
        institution_name = request.POST['institution_name']
        role = request.POST['role']
        students_level = request.POST['students_level']
        hours = request.POST['hours']
        myCourse = courses(course_year=course_year,course_name=course_name,institution_name=institution_name,role=role,students_level=students_level,hours=hours)
        myCourse.save()
        return redirect('admin_teachings')
    courses_list = courses.objects.all()
    description_text = ""
    if page_description_text.objects.filter(page_name="teachings").count() != 0:
        description_text = page_description_text.objects.filter(page_name="teachings")[0].text
    return render(request, 'edit_teachings.html',{"userFullName":userFullName,"showNews":showNews,"courses":courses_list,"description":description_text})
@login_required(login_url=loginUrl)
def edit_news(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    if request.method == 'POST':
        news_title = request.POST['news_title']
        news_description = request.POST['news_description']
        news_date = datetime.datetime.now()
        if request.POST['news_date'] != "":
            news_date = request.POST['news_date']
        news_image = ""
        if request.FILES.get('news_image') is not None:
            news_image = request.FILES['news_image']
        news_pdf = ""
        if request.FILES.get('news_pdf') is not None:
            news_pdf = request.FILES['news_pdf']
        news_video = "" 
        if request.FILES.get('news_video') is not None:
            news_video = request.FILES['news_video']
        
        if request.POST.get('news_id') is not None:
            myNews = news.objects.get(id=request.POST['news_id'])
            if news_title != "":
                myNews.title = news_title
            if news_description != "":
                myNews.news_description = news_description
            if news_date != "":    
                myNews.news_date = news_date
            if news_image != "":
                try:
                    deletingImage = myNews.image.path
                    if os.path.exists(deletingImage):
                        os.remove(deletingImage)
                except:
                    pass
                myNews.image = news_image
            if news_pdf != "":
                try:
                    deletingPdf = myNews.pdf.path
                    if os.path.exists(deletingPdf):
                        os.remove(deletingPdf)
                except:
                    pass
                myNews.pdf = news_pdf
            if news_video != "":
                try:
                    deletingVideo = myNews.video.path
                    if os.path.exists(deletingVideo):
                        os.remove(deletingVideo)
                except:
                    pass
                myNews.video = news_video
        else: 
            myNews = news(title=news_title,news_description=news_description,news_date=news_date,image=news_image,pdf=news_pdf,video=news_video)
        myNews.save()
        return redirect('admin_news')
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    return render(request, 'edit_news.html',{"userFullName":userFullName,"showNews":showNews,"all_news":news.objects.all()})
class add_pdf_to_gs(APIView):
    def post(self,request):
        citation_id = request.data['citation_id']
        pdf = request.FILES['pdf']
        myCitation = gs_citation_ids.objects.get(citation_id=citation_id)
        oldpdf = myCitation.pdf
        if oldpdf != "":
            try:
                deletingPdf = oldpdf.path
                if os.path.exists(deletingPdf):
                    os.remove(deletingPdf)
            except:
                pass
        myCitation.pdf = pdf
        myCitation.save()
        return Response({"message":"PDF added successfully","status":200})
class select_for_about_me(APIView): 
    def post(self,request):
        selected_publications = request.data['selected_publications']
        selected_gs = request.data['selected_gs']
        about_me_selected_publications.objects.all().delete()
        about_me_selected_gs.objects.all().delete()
        for publ in selected_publications:
            myPublication = publication.objects.get(id=int(publ))
            myPub = about_me_selected_publications(pub=myPublication)
            myPub.save()
        for gs in selected_gs:
            myGoogleScholar = google_scholar_article.objects.get(id=int(gs))
            myGs = about_me_selected_gs(gs=myGoogleScholar)
            myGs.save()
        return Response({"message":"Selected successfully","status":200})
class add_video_to_gs(APIView):
    def post(self,request):
        citation_id = request.data['citation_id']
        video = request.FILES['video']
        myCitation = gs_citation_ids.objects.get(citation_id=citation_id)
        oldvideo = myCitation.video
        if oldvideo != "":
            try:
                deletingVideo = oldvideo.path
                if os.path.exists(deletingVideo):
                    os.remove(deletingVideo)
            except:
                pass
        myCitation.video = video
        myCitation.save()
        return Response({"message":"Video added successfully","status":200})
@login_required(login_url=loginUrl)
def edit_resume(request):
    userFullName= ""
    if userdata.objects.all().count() != 0:
        userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    
    showNews = False
    if userdata.objects.all().count() != 0:
        if userdata.objects.all()[0].view_news is True:
            showNews = True
    if request.method == 'POST':
        cv = ""
        if request.FILES.get('cv') is not None:
            cv = request.FILES['cv']
        if generalInfo.objects.all().count() != 0:
            myGeneralInfo = generalInfo.objects.all()[0]
            if request.FILES.get('cv') is not None:
                try:
                    deletingCv = myGeneralInfo.cv.path
                    if os.path.exists(deletingCv):
                        os.remove(deletingCv)
                except:
                    pass
                myGeneralInfo.cv = cv
            myGeneralInfo.save()
            return redirect('admin_resume')
        myGeneralInfo = generalInfo(cv=cv)
        myGeneralInfo.save()
        return redirect('admin_resume')
    education_exp = []
    professional_exp = []
    academic_exp = []   
    award_exp = []   
    showEducation = False
    showProfessional = False
    showAcademic = False
    showAward = False
    myUserdata = ""
    fullName = ""
    email = ""
    linkedin = ""
    if userdata.objects.all().count()!= 0:
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
        return render(request, 'edit_resume.html',{"userFullName":userFullName,"showNews":showNews,"experience_ids":experience_ids,"info":myGeneralInfo,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
    return render(request, 'edit_resume.html',{"userFullName":userFullName,"showNews":showNews,"experience_ids":experience_ids,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
class deleteNews(APIView):
    def post(self,request):
        news_id = request.data['news_id']
        thisNews = news.objects.get(id=news_id)
        if thisNews.image != "":
            try:
                deletingImage = thisNews.image.path
                if os.path.exists(deletingImage):
                    os.remove(deletingImage)
            except:
                pass
        if thisNews.pdf != "":
            try:
                deletingPdf = thisNews.pdf.path
                if os.path.exists(deletingPdf):
                    os.remove(deletingPdf)
            except:
                pass
        if thisNews.video != "":
            try:
                deletingVideo = thisNews.video.path
                if os.path.exists(deletingVideo):
                    os.remove(deletingVideo)
            except:
                pass
        thisNews.delete()
        return Response({"message":"News deleted successfully","status":200})