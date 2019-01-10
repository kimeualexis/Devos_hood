from django.contrib import admin
from .models import Question, Comment, Quote

admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Quote)
