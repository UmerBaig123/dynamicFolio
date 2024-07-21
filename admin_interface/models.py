from django.db import models
from django.contrib.auth.models import User
import django as django
import datetime
# Create your models here.
class selected_repos(models.Model):
    repo_id = models.CharField(max_length=100)
    def __str__(self):
        return self.repo_id
class page_description_text(models.Model):
    page_name = models.CharField(max_length=100)
    text = models.TextField(default="")
    def __str__(self):
        return self.text
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