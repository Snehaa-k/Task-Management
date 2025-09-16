# Task Management System

A comprehensive Django-based task management system with role-based access control, RESTful APIs, and web interface.

## Features

- **Role-based Access Control**: SuperAdmin, Admin, and User roles
- **Task Management**: Create, assign, track, and complete tasks
- **Reporting System**: Task completion reports with worked hours
- **RESTful APIs**: Complete API endpoints for mobile/web integration
- **Web Interface**: Admin panel for task and user management
- **JWT Authentication**: Secure token-based authentication

## Tech Stack

- **Backend**: Django 5.2.6, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT (Simple JWT)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render, Heroku, AWS

## Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/taskmanager.git
cd taskmanager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## API Documentation

### Base URL
```
Development: http://127.0.0.1:8000/api/
Production: https://your-domain.com/api/
```

## Authentication APIs

**POST /api/auth/register/**
Register a new user account in the system. Allows creation of users with different roles (user, admin, superuser).

**POST /api/auth/login/**
Authenticate user credentials and return JWT access and refresh tokens for API access.

**POST /api/token/**
Alternative endpoint to obtain JWT tokens using username and password credentials.

**POST /api/token/refresh/**
Refresh expired JWT access token using the refresh token to maintain user session.

## Task APIs

**GET /api/tasks/**
Retrieve all tasks assigned to the authenticated user. Users see only their tasks, admins see tasks for their managed users, superadmins see all tasks.

**GET /api/tasks/{id}/**
Get detailed information about a specific task including title, description, status, due date, and completion details.

**POST /api/tasks/**
Create a new task and assign it to a user. Only admins and superadmins can create tasks for their managed users.

**PUT /api/tasks/{id}/**
Update task information including status changes, completion reports, and worked hours. Users can update their assigned tasks.

**PATCH /api/tasks/{id}/**
Partially update specific fields of a task without modifying other task properties.

**DELETE /api/tasks/{id}/**
Permanently remove a task from the system. Only superadmins have permission to delete tasks.

## Report APIs

**GET /api/tasks/reports/**
Retrieve completion reports for all finished tasks. Admins see reports for their users, superadmins see all reports.

**GET /api/tasks/{id}/report/**
Get detailed completion report for a specific completed task including worked hours and completion notes.

## Web Interface APIs

**GET /login/**
Display login page for web interface access using session-based authentication.

**POST /login/**
Process login credentials and create user session for web interface access.

**GET /logout/**
End user session and redirect to login page.

**GET /panel/**
Main dashboard showing statistics and navigation based on user role permissions.

## User Management APIs (SuperAdmin Only)

**GET /panel/users/**
Display list of all users in the system with their roles, status, and assigned managers.

**GET /panel/users/create/**
Show form to create a new user with role selection and admin assignment options.

**POST /panel/users/create/**
Process new user creation with specified role and manager assignment.

**GET /panel/users/{id}/edit/**
Display form to edit existing user information including role changes and manager reassignment.

**POST /panel/users/{id}/edit/**
Update user information, role, and manager assignments in the system.

**GET /panel/users/{id}/delete/**
Remove user account from the system permanently.

**GET /panel/users/{id}/assign/**
Show form to assign or reassign a user to a specific admin manager.

**POST /panel/users/{id}/assign/**
Process user assignment to admin manager for task management hierarchy.

## Admin Management APIs (SuperAdmin Only)

**GET /panel/admins/**
Display list of all admin users with their managed user counts and status.

**GET /panel/admins/create/**
Show form to create a new admin user account.

**POST /panel/admins/create/**
Process creation of new admin user with appropriate permissions.

**GET /panel/admins/{id}/edit/**
Display form to edit admin user information and settings.

**POST /panel/admins/{id}/edit/**
Update admin user information and permissions.

**GET /panel/admins/{id}/delete/**
Remove admin user account from the system.

**GET /panel/admins/{id}/demote/**
Convert admin user to regular user role, removing admin privileges.

## Task Management APIs (Admin/SuperAdmin)

**GET /panel/tasks/**
Display list of tasks based on user role - admins see their users' tasks, superadmins see all tasks.

**GET /panel/tasks/create/**
Show form to create new task with user assignment and due date options.

**POST /panel/tasks/create/**
Process new task creation and assignment to specified user.

**GET /panel/tasks/{id}/**
Display detailed view of specific task with all information and status.

**GET /panel/tasks/{id}/edit/**
Show form to edit task details, status, and assignment.

**POST /panel/tasks/{id}/edit/**
Update task information, status, or reassign to different user.

**GET /panel/tasks/{id}/delete/**
Remove task from the system permanently (SuperAdmin only).

## Report Management APIs (Admin/SuperAdmin)

**GET /panel/reports/**
Display list of all completed tasks with their completion reports and worked hours.

**GET /panel/reports/{id}/**
Show detailed completion report for specific task including all completion details.

## User Roles & Permissions

### SuperAdmin
Complete system access including user management, admin management, all task operations, and full reporting capabilities.

### Admin
Can create and manage tasks for assigned users, view completion reports for their users, but cannot manage user accounts or system settings.

### User
Can view assigned tasks via API, update task status, and submit completion reports, but has no web interface access or task creation abilities.

## Authentication

### API Authentication
JWT token required in Authorization header for all protected endpoints.

### Web Authentication
Session-based authentication for web interface with role-based page access control.

## Environment Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Deployment

Supports deployment on Render, Heroku, AWS, and DigitalOcean with proper environment configuration.

