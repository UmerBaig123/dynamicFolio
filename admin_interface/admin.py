from django.contrib import admin
from .models import userdata,selected_repos,publication,experience,generalInfo,google_scholar_article,gs_citation_ids
# Register your models here
# admin.site.register(userdata)
admin.site.register(selected_repos)
admin.site.register(generalInfo)
admin.site.register(publication)
admin.site.register(experience)
admin.site.register(google_scholar_article)
admin.site.register(gs_citation_ids)