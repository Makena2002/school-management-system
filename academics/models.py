from django.db import models
from django.conf import settings


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)  # e.g. "Form 2 East"
    class_teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='classroom_led'
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student, related_name='parents', blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)  # e.g. "Term 1 2026"
    score = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'subject', 'term')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.term}: {self.score}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title