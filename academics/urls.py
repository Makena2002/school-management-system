from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('parents/', views.parent_list, name='parent_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('results/enter/', views.enter_results, name='enter_results'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
    path('my-results/', views.my_results, name='my_results'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/post/', views.post_announcement, name='post_announcement'),
    path('my-children/', views.parent_children, name='parent_children'),
    path('child/<int:student_id>/attendance/', views.child_attendance, name='child_attendance'),
    path('child/<int:student_id>/results/', views.child_results, name='child_results'),
]