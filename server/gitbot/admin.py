from django.contrib import admin

# Register your models here.

from .models import Student, Repo, Commit, Assignment

admin.site.register(Student)
admin.site.register(Repo)
admin.site.register(Commit)
admin.site.register(Assignment)
