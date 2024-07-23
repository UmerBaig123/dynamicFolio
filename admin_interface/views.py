from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import userdata,selected_repos,publication,page_description_text,courses,experience,generalInfo,gitlab_ids,selected_gitlab_repos
import datetime
import os
from dotenv import load_dotenv
# Create your views here.

load_dotenv()
loginUrl = os.environ['ADMINROUTE']
gitlab_api_key = os.environ['GITLABAPITOKEN']
userFullName= ""
if userdata.objects.all().count() != 0:
    userFullName = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name

@login_required(login_url=loginUrl)
def edit_about(request):
    if request.method == 'POST':

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
                myData = userdata(profile_pic=profile_pic,first_name=first_name,last_name=last_name,email_address=email,linkedin_url=linkedin,github_username=github,qualification=qualification,university=university,university_url=universityUrl,summary=summary)
            else:
                myData = userdata(first_name=first_name,last_name=last_name,email_address=email,linkedin_url=linkedin,github_username=github,qualification=qualification,university=university,university_url=universityUrl,summary=summary)
            myData.save()
            return redirect('admin_about')
        myData = userdata.objects.all()[0]
        if request.FILES.get('profile_pic') is not None:
            deletingPic =  myData.profile_pic.path
            if os.path.exists(deletingPic):
                os.remove(deletingPic)
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
        myData.save()
        return render(request, 'edit_about.html',{"userFullName":userFullName,
        "profile_pic":myData.profile_pic,
        "first_name":myData.first_name,
        "last_name":myData.last_name,
        "email":myData.email_address,
        "linkedin":myData.linkedin_url,
        "github":myData.github_username,
        "qualification":myData.qualification,
        "university":myData.university,
        "universityUrl":myData.university_url,
        "summary":myData.summary
        })
    if len(userdata.objects.all()) != 0:
        myData = userdata.objects.all()[0]
        return render(request, 'edit_about.html',{"userFullName":userFullName,
        "profile_pic":myData.profile_pic,
        "first_name":myData.first_name,
        "last_name":myData.last_name,
        "email":myData.email_address,
        "linkedin":myData.linkedin_url,
        "github":myData.github_username,
        "qualification":myData.qualification,
        "university":myData.university,
        "universityUrl":myData.university_url,
        "summary":myData.summary
        })
    return render(request, 'edit_about.html',{"userFullName":userFullName,})
@login_required(login_url=loginUrl)
def edit_repos(request):
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
            return render(request, 'edit_repos.html',{"userFullName":userFullName,"username":myData.github_username,"repos":myRepos,"page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})
        return render(request, 'edit_repos.html',{"userFullName":userFullName,"username":myData.github_username,"repos":"none","page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})
    return render(request, 'edit_repos.html',{"userFullName":userFullName,"page_desc":page_desc,"gitlab_id":gitlab_id,"gitlab_repos":myGitlabRepos,"api_key":gitlab_api_key})


def login_admin(request):
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
    return render(request, 'login.html',{"userFullName":userFullName,})   
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
    if request.method == 'POST':
        pdfFile = ""
        publication_image = ""
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
        if request.FILES.get('publication_image') is not None:
            publication_image = request.FILES['publication_image']
        myPublication = publication(doi=doi,title=title,authors=authors,description=description,abs=abstract,arxiv_url=arxiv_url,bib=bib,pdfFile=pdfFile,publication_image=publication_image,publication_date=publication_date)
        myPublication.save()
        return redirect('admin_publications')
    description = ""
    if page_description_text.objects.filter(page_name="publications").count() != 0:
        description = page_description_text.objects.filter(page_name="publications")[0].text
    publications = publication.objects.all()
    return render(request, 'edit_publications.html',{"userFullName":userFullName,"publications":publications,"description":description})
class delete_publication(APIView):
    def post(self,request):
        publication_id = request.data['publication_id']
        thisPublication = publication.objects.get(id=publication_id)
        # Delete the pdfFile from the system
        try:
            pdf_file_path = thisPublication.pdfFile.path
            image_file_path = thisPublication.publication_image.path
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
        except:
            pass
        thisPublication.delete()
        return Response({"message":"Publication deleted successfully","status":200})
class edit_publication(APIView):
    def post(self,request):
        publication_id = request.data['id']
        title = request.data['title']
        authors = request.data['authors']
        description = request.data['desc']
        abstract = request.data['abs']
        arxiv_url = request.data['arxiv']
        bib = request.data['bib']
        doi = request.data['doi']
        publication_date = request.data['date']
        pdfFile = ""
        publication_image = ""
        if request.FILES.get('pdf') is not None:
            pdfFile = request.FILES['pdf']
        if request.FILES.get('image') is not None:
            publication_image = request.FILES['image']
        thisPublication = publication.objects.get(id=publication_id)
        thisPublication.title = title
        thisPublication.authors = authors
        thisPublication.description = description
        thisPublication.abs = abstract
        thisPublication.arxiv_url = arxiv_url
        thisPublication.bib = bib
        thisPublication.doi = doi
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
class add_experience(APIView):
    def post(self,request):
        experience_type = request.data['experience_type']
        experience_name = request.data['experience_name']
        experience_place = request.data['experience_place']
        experience_location = request.data['experience_location']
        experience_from_year = request.data['experience_from_year']
        experience_to_year = request.data['experience_to_year']
        experience_description = request.data['experience_description']
        myExperience = experience(experience_type=experience_type,experience_name=experience_name,experience_place=experience_place,experience_from_year=experience_from_year,experience_to_year=experience_to_year,experience_description=experience_description,experience_location=experience_location)
        myExperience.save()
        return Response({"message":"Experience added successfully","status":200})
class edit_experience(APIView):
    def post(self,request):
        experience_id = request.data['experience_id']
        experience_name = request.data['experience_name']
        experience_place = request.data['experience_place']
        experience_location = request.data['experience_location']
        experience_from_year = request.data['experience_from_year']
        experience_to_year = request.data['experience_to_year']
        experience_description = request.data['experience_description']
        thisExperience = experience.objects.get(id=experience_id)
        thisExperience.experience_name = experience_name
        thisExperience.experience_place = experience_place
        thisExperience.experience_location = experience_location
        thisExperience.experience_from_year = experience_from_year
        thisExperience.experience_to_year = experience_to_year
        thisExperience.experience_description = experience_description
        thisExperience.save()
        return Response({"message":"Experience edited successfully","status":200})
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
class delete_experience(APIView):
    def post(self,request):
        experience_id = request.data['experience_id']
        thisExperience = experience.objects.get(id=experience_id)
        thisExperience.delete()
        return Response({"message":"Experience deleted successfully","status":200})
class delete_course(APIView):
    def post(self,request):
        course_id = request.data['course_id']
        thisCourse = courses.objects.get(id=course_id)
        thisCourse.delete()
        return Response({"message":"Course deleted successfully","status":200})
@login_required(login_url=loginUrl)
def teachings(request):
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
    return render(request, 'edit_teachings.html',{"userFullName":userFullName,"courses":courses_list,"description":description_text})

@login_required(login_url=loginUrl)
def edit_resume(request):
    if request.method == 'POST':
        dob = datetime.datetime.now()
        language = request.POST['languages']
        cv = ""
        phone = request.POST['phone']
        hobbies = request.POST['hobbies']
        if request.FILES.get('cv') is not None:
            cv = request.FILES['cv']
        if generalInfo.objects.all().count() != 0:
            myGeneralInfo = generalInfo.objects.all()[0]
            if request.POST['date_of_birth'] != "":
                dob = request.POST['date_of_birth']
                myGeneralInfo.date_of_birth = dob
            if request.FILES.get('cv') is not None:
                try:
                    deletingCv = myGeneralInfo.cv.path
                    if os.path.exists(deletingCv):
                        os.remove(deletingCv)
                except:
                    pass
                myGeneralInfo.cv = cv
            myGeneralInfo.languages = language
            myGeneralInfo.phone = phone
            myGeneralInfo.hobbies = hobbies
            myGeneralInfo.save()
            return redirect('admin_resume')
        myGeneralInfo = generalInfo(date_of_birth=dob,languages=language,cv=cv,phone=phone,hobbies=hobbies)
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
        return render(request, 'edit_resume.html',{"userFullName":userFullName,"experience_ids":experience_ids,"info":myGeneralInfo,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
    return render(request, 'edit_resume.html',{"userFullName":userFullName,"experience_ids":experience_ids,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
