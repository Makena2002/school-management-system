# School Management System

A Django-based web application for managing school operations across three roles: Admin, Teacher, and Student.

## Features

- **Role-based authentication** — single login system with Admin, Teacher, and Student roles
- **Admin**: manage students, teachers, classrooms, and subjects
- **Teacher**: mark daily attendance for their assigned classroom, enter student results per subject/term
- **Student**: view their own attendance history and academic results

## Tech Stack

- Python 3.12
- Django 6.1
- Django REST Framework (installed for future API expansion)
- Bootstrap 5 (via CDN)
- SQLite (default development database)

## Project Structure

- `accounts/` — custom User model with role field (Admin/Teacher/Student), dashboard view
- `academics/` — core models (ClassRoom, Subject, Teacher, Student, Attendance, Result) and all role-based views
- `templates/` — Django templates, organized by app

## Setup Instructions

1. Clone the repository and navigate into the project folder
2. Create and activate a virtual environment: