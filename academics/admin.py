from django.contrib import admin
from .models import ClassRoom, Subject, Teacher, Student, Parent, Attendance, Result, Announcement

admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Attendance)
admin.site.register(Result)
admin.site.register(Announcement)