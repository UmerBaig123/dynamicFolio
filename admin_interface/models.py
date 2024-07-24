from django.db import models
from django.contrib.auth.models import User
import django as django
import datetime
# Create your models here.
class selected_repos(models.Model):
    repo_id = models.CharField(max_length=100)
    def __str__(self):
        return self.repo_id
class selected_gitlab_repos(models.Model):
    repo_id = models.CharField(max_length=100)
    def __str__(self):
        return self.repo_id
class page_description_text(models.Model):
    page_name = models.CharField(max_length=100)
    text = models.TextField(default="")
    def __str__(self):
        return self.text
class gitlab_ids(models.Model):
    gitlab_id = models.CharField(max_length=100)
    def __str__(self):
        return self.gitlab_id
class userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    profile_pic = models.ImageField(upload_to="images",blank=True,default="",null=True)
    first_name = models.CharField(max_length=100,default="First Name")
    last_name = models.CharField(max_length=100,default="Last Name")
    github_username = models.CharField(max_length=100,default="Github Username")
    linkedin_url = models.URLField(default="https://linkedin.com")
    email_address = models.EmailField(default="example@email.com")
    qualification = models.TextField(default="Qualification")
    university = models.TextField(default="University")
    university_url = models.URLField(default="https://university.com")
    view_news = models.BooleanField(default=True)
    summary = models.TextField(default="Summary")
    def __str__(self):
        return self.user.username
class publication(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_image = models.ImageField(upload_to='publication_images', blank=True,default="")
    title = models.CharField(max_length=100,default="Title")
    authors = models.CharField(max_length=100,default="Authors")
    description = models.TextField(default="Description")
    abs = models.TextField(default="Abstract")
    arxiv_url = models.URLField(default="https://arxiv.org/pdf/")
    bib = models.TextField(default="BibTex")
    pdfFile = models.FileField(upload_to='publication_pdfs',default="", blank=True)
    doi = models.CharField(max_length=100,default="")
    publication_date = models.DateField(default=django.utils.timezone.now)
    def __str__(self):
        return self.title
    def isDoi(self):
        return self.doi != ""
class news(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    news_date = models.DateField()
    news_description = models.TextField()
    def __str__(self):
        return self.title
class courses(models.Model):
    course_year = models.IntegerField()
    course_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    students_level = models.CharField(max_length=100)
    hours = models.IntegerField()
    def __str__(self):
        return self.course_name
class generalInfo(models.Model):
    date_of_birth = models.DateField(default=django.utils.timezone.now)
    languages = models.TextField(default="Languages")
    cv = models.FileField(upload_to='cv',default="", blank=True)
    phone = models.CharField(max_length=100,default="Phone")
    hobbies = models.TextField(default="")
class experience(models.Model):
    experience_from_year = models.IntegerField()
    experience_to_year = models.IntegerField()
    experience_name = models.CharField(max_length=100,default="")
    experience_type = models.CharField(max_length=100,default="")
    experience_place = models.CharField(max_length=100,default="")
    experience_location = models.CharField(max_length=100,default="")
    experience_description = models.TextField(default="")
    def __str__(self):
        return self.experience_name
class google_scholar_article(models.Model):
    title = models.CharField(max_length=100,default="")
    authors = models.TextField(default="")
    publication = models.TextField(default="")
    year = models.IntegerField(null=True)
    cited_by = models.IntegerField(null=True,blank=True)
    citation_id = models.CharField(max_length=100,default="")
    isSelected = models.BooleanField(default=False)
    link = models.URLField(default="")
    def getAllSelectedWithPdf():
        if google_scholar_article.objects.filter(isSelected=True).count() == 0 or google_scholar_article.objects.filter(isSelected=True) is None:
            return []
        else:
            articles = google_scholar_article.objects.filter(isSelected=True)
            article_pdf = []
            for article in articles:
                thisTitle = article.title
                thisAuthors = article.authors
                thisPublication = article.publication
                thisYear = article.year
                thisCitedBy = article.cited_by
                thisCitationId = article.citation_id
                thisLink = article.link
                thisPdf = gs_citation_ids.objects.filter(citation_id=thisCitationId)[0].pdf
                dictionary = {
                    "title":thisTitle,
                    "authors":thisAuthors,
                    "publication":thisPublication,
                    "year":thisYear,
                    "cited_by":thisCitedBy,
                    "citation_id":thisCitationId,
                    "link":thisLink,
                    "pdf":thisPdf
                }
                article_pdf.append(dictionary)
            return article_pdf
    def __str__(self):
        return self.title
class gs_citation_ids(models.Model):
    citation_id = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='gs_pdfs',default="", blank=True)
    def __str__(self):
        return self.citation_id