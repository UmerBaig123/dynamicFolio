from django.shortcuts import render
from types import SimpleNamespace
from admin_interface.models import userdata, selected_repos,publication,page_description_text,courses,experience,generalInfo
# Create your views here.
def home_page(request):
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    if userdata.objects.all().count() == 0:
        return render(request, 'home.html', {})
    repos = selected_repos.objects.all()
    if repos.count() == 0:
        repos = "none"
    else:
        repos = [repo.repo_id for repo in selected_repos.objects.all()]
        repos = ",".join(repos)
    userdata_obj = userdata.objects.all()[0]
    publications = publication.objects.all()
    return render(request, 'home.html', {"userdata": userdata_obj, "repos": repos,"publications":publications,"full_name":full_name})
def repository(request):
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    description_text = ""
    if page_description_text.objects.filter(page_name="repositories").count() != 0:
        description_text = page_description_text.objects.filter(page_name="repositories")[0]
    github_username = ""
    if userdata.objects.all().count() != 0:
        github_username = userdata.objects.all()[0].github_username
    if selected_repos.objects.all().count() == 0:
        return render(request, 'repository.html', {"repos":"none","github_username":github_username,"description_text":description_text,"full_name":full_name})
    repos = [repo.repo_id for repo in selected_repos.objects.all()]
    repos = ",".join(repos)
    return render(request, 'repository.html', {"repos":repos,"github_username":github_username,"description_text":description_text,"full_name":full_name})
def publications(request):
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    page_desc = ""
    if page_description_text.objects.filter(page_name="publications").count() != 0:
        page_desc = page_description_text.objects.filter(page_name="publications")[0]
    publications = publication.objects.all()
    return render(request, 'publications.html', {"publications":publications,"description_text":page_desc,"full_name":full_name})
def teachings(request):
    full_name = ""
    if userdata.objects.all().count() != 0:
        full_name = userdata.objects.all()[0].first_name + " " + userdata.objects.all()[0].last_name
    description_text= ""
    myCourses = courses.objects.all()
    if page_description_text.objects.filter(page_name="teachings").count() != 0:
        description_text = page_description_text.objects.filter(page_name="teachings")[0]
    return render(request, 'teachings.html', {"description": description_text,"courses":myCourses,"full_name":full_name})
def resume(request):
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
        return render(request, 'resume.html',{"experience_ids":experience_ids,"info":myGeneralInfo,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
    return render(request, 'resume.html',{"experience_ids":experience_ids,"education":education_exp,"professional":professional_exp,"academic":academic_exp,"awards":award_exp,"fullname":fullName,"email":email,"linkedin":linkedin,"showEducation":showEducation,"showProfessional":showProfessional,"showAcademic":showAcademic,"showAward":showAward})
