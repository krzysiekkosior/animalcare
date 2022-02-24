from django.contrib import admin

from main_app.models import Case, CasePhoto, Comment, Observed

admin.site.register(Case)
admin.site.register(CasePhoto)
admin.site.register(Comment)
admin.site.register(Observed)
