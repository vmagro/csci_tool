from django.contrib import admin

# Register your models here.

from .models import Student, Repo, Commit, Assignment, Submission, Mutation

admin.site.register(Student)
admin.site.register(Repo)
admin.site.register(Commit)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Mutation)
