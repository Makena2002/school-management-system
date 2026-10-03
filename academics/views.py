from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Student, Teacher, ClassRoom, Subject, Attendance, Result, Announcement, Parent


def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


def is_teacher(user):
    return user.is_authenticated and user.role == 'TEACHER'


def is_student(user):
    return user.is_authenticated and user.role == 'STUDENT'


def is_parent(user):
    return user.is_authenticated and user.role == 'PARENT'


@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.select_related('user', 'classroom').all()
    return render(request, 'academics/student_list.html', {'students': students})


@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.select_related('user').prefetch_related('subjects').all()
    return render(request, 'academics/teacher_list.html', {'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def classroom_list(request):
    classrooms = ClassRoom.objects.select_related('class_teacher__user').all()
    return render(request, 'academics/classroom_list.html', {'classrooms': classrooms})


@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})


@login_required
@user_passes_test(is_admin)
def parent_list(request):
    parents = Parent.objects.select_related('user').prefetch_related('children__user').all()
    return render(request, 'academics/parent_list.html', {'parents': parents})


@login_required
@user_passes_test(is_teacher)
def mark_attendance(request):
    teacher = Teacher.objects.get(user=request.user)
    classroom = ClassRoom.objects.filter(class_teacher=teacher).first()

    if not classroom:
        messages.error(request, "You are not assigned as a class teacher for any classroom.")
        return render(request, 'academics/mark_attendance.html', {'students': []})

    students = Student.objects.filter(classroom=classroom).select_related('user')
    today = timezone.now().date()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status, 'marked_by': teacher}
                )
        messages.success(request, "Attendance marked successfully.")
        return redirect('mark_attendance')

    return render(request, 'academics/mark_attendance.html', {'students': students, 'today': today})


@login_required
@user_passes_test(is_teacher)
def enter_results(request):
    teacher = Teacher.objects.get(user=request.user)
    subjects = teacher.subjects.all()
    term = "Term 1 2026"

    if not subjects:
        messages.error(request, "You are not assigned to any subjects.")
        return render(request, 'academics/enter_results.html', {'students': [], 'subjects': []})

    students = Student.objects.select_related('user', 'classroom').all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        subject = subjects.filter(id=subject_id).first()
        if subject:
            for student in students:
                score = request.POST.get(f'score_{student.id}')
                if score:
                    Result.objects.update_or_create(
                        student=student,
                        subject=subject,
                        term=term,
                        defaults={'score': score, 'recorded_by': teacher}
                    )
            messages.success(request, "Results saved successfully.")
        return redirect('enter_results')

    return render(request, 'academics/enter_results.html', {
        'students': students,
        'subjects': subjects,
        'term': term,
    })


@login_required
@user_passes_test(is_student)
def my_attendance(request):
    student = Student.objects.get(user=request.user)
    records = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'academics/my_attendance.html', {'records': records})


@login_required
@user_passes_test(is_student)
def my_results(request):
    student = Student.objects.get(user=request.user)
    records = Result.objects.filter(student=student).select_related('subject').order_by('-term')
    return render(request, 'academics/my_results.html', {'records': records})


@login_required
def announcement_list(request):
    announcements = Announcement.objects.select_related('posted_by').all()
    return render(request, 'academics/announcement_list.html', {'announcements': announcements})


@login_required
@user_passes_test(is_admin)
def post_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if title and message:
            Announcement.objects.create(title=title, message=message, posted_by=request.user)
            messages.success(request, "Announcement posted.")
            return redirect('announcement_list')
    return render(request, 'academics/post_announcement.html')


@login_required
@user_passes_test(is_parent)
def parent_children(request):
    parent = Parent.objects.get(user=request.user)
    children = parent.children.select_related('user', 'classroom').all()
    return render(request, 'academics/parent_children.html', {'children': children})


@login_required
@user_passes_test(is_parent)
def child_attendance(request, student_id):
    parent = Parent.objects.get(user=request.user)
    student = get_object_or_404(parent.children, id=student_id)
    records = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'academics/child_attendance.html', {'records': records, 'student': student})


@login_required
@user_passes_test(is_parent)
def child_results(request, student_id):
    parent = Parent.objects.get(user=request.user)
    student = get_object_or_404(parent.children, id=student_id)
    records = Result.objects.filter(student=student).select_related('subject').order_by('-term')
    return render(request, 'academics/child_results.html', {'records': records, 'student': student})