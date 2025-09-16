from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Task
from .forms import TaskForm, UserForm, AdminForm

User = get_user_model()

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('login')
    
    if request.user.is_superuser:
        tasks_count = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
    else:
        tasks_count = Task.objects.filter(assigned_to__admin=request.user).count()
        completed_tasks = Task.objects.filter(status='completed', assigned_to__admin=request.user).count()
    
    context = {
        'user': request.user,
        'tasks_count': tasks_count,
        'users_count': User.objects.count(),
        'admins_count': User.objects.filter(role='admin').count(),
        'completed_tasks': completed_tasks,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def manage_tasks(request):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('login')
    
    if request.user.is_superuser:
        tasks = Task.objects.all()
    elif getattr(request.user, 'role', None) == 'admin':
        tasks = Task.objects.filter(assigned_to__admin=request.user)
    else:
        tasks = Task.objects.none()
    
    return render(request, 'admin/tasks_list.html', {'tasks': tasks})

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    users = User.objects.all()
    return render(request, 'admin/users_list.html', {'users': users})

@login_required
def create_task(request):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return render(request, '403.html')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully')
            return redirect('tasks_list')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'admin/task_form.html', {'form': form})

@login_required
def create_user(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST.get('password')
        if form.is_valid() and password:
            user = form.save(commit=False)
            user.set_password(password)
            
            # Handle superuser creation
            if form.cleaned_data['role'] == 'superuser':
                user.is_superuser = True
                user.is_staff = True
                user.role = 'admin'  # Set role to admin for consistency
            
            user.save()
            role_name = 'SuperUser' if user.is_superuser else user.get_role_display()
            messages.success(request, f'{role_name} created successfully')
            return redirect('users_list')
    else:
        form = UserForm()
    
    return render(request, 'admin/user_form.html', {'user_form': form})

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle superuser role changes
            if form.cleaned_data['role'] == 'superuser':
                user.is_superuser = True
                user.is_staff = True
                user.role = 'admin'
            else:
                user.is_superuser = False
                user.is_staff = False
            
            user.save()
            role_name = 'SuperUser' if user.is_superuser else user.get_role_display()
            messages.success(request, f'{role_name} updated successfully')
            return redirect('users_list')
    else:
        form = UserForm(instance=user_obj)
        # Set initial role value for superusers
        if user_obj.is_superuser:
            form.initial['role'] = 'superuser'
    
    return render(request, 'admin/user_form.html', {'user_form': form})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    # Prevent self-deletion
    if user_obj.id == request.user.id:
        messages.error(request, 'You cannot delete yourself')
        return redirect('users_list')
    
    role_display = 'SuperUser' if user_obj.is_superuser else user_obj.get_role_display()
    user_obj.delete()
    messages.success(request, f'{role_display} deleted successfully')
    return redirect('users_list')

@login_required
def task_detail(request, task_id):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'admin/task_detail.html', {'task': task})

@login_required
def task_edit(request, task_id):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return render(request, '403.html')
    
    task = get_object_or_404(Task, id=task_id)
    
    # Admin can only edit tasks assigned to their users
    if request.user.role == 'admin' and task.assigned_to.admin != request.user:
        return render(request, '403.html')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'admin/task_form.html', {'form': form, 'task': task})

@login_required
def manage_admins(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    admins = User.objects.filter(role='admin')
    return render(request, 'admin/admins_list.html', {'admins': admins})

@login_required
def reports_list(request):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('login')
    
    if request.user.is_superuser:
        completed_tasks = Task.objects.filter(status='completed')
    else:
        completed_tasks = Task.objects.filter(status='completed', assigned_to__admin=request.user)
    
    total_hours = sum(task.worked_hours for task in completed_tasks)
    
    return render(request, 'admin/reports_list.html', {
        'completed_tasks': completed_tasks,
        'total_hours': total_hours
    })

@login_required
def report_detail(request, task_id):
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id, status='completed')
    return render(request, 'admin/report_detail.html', {'task': task})

@login_required
def create_admin(request):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    if request.method == 'POST':
        form = AdminForm(request.POST)
        password = request.POST.get('password')
        if form.is_valid() and password:
            user = form.save(commit=False)
            user.role = 'admin'
            user.set_password(password)
            user.save()
            messages.success(request, 'Admin created successfully')
            return redirect('admins_list')
    else:
        form = AdminForm()
    
    return render(request, 'admin/admin_form.html', {'admin_form': form})

@login_required
def edit_admin(request, admin_id):
    if not request.user.is_superuser:
        return redirect('login')
    
    admin_obj = get_object_or_404(User, id=admin_id, role='admin')
    if request.method == 'POST':
        form = UserForm(request.POST, instance=admin_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin updated successfully')
            return redirect('admins_list')
    else:
        form = UserForm(instance=admin_obj)
    
    return render(request, 'admin/user_form.html', {'user_form': form})

@login_required
def delete_admin(request, admin_id):
    if not request.user.is_superuser:
        return redirect('login')
    
    admin_obj = get_object_or_404(User, id=admin_id, role='admin')
    admin_obj.delete()
    messages.success(request, 'Admin deleted successfully')
    return redirect('admins_list')

@login_required
def demote_admin(request, admin_id):
    if not request.user.is_superuser:
        return redirect('login')
    
    admin_obj = get_object_or_404(User, id=admin_id, role='admin')
    admin_obj.role = 'user'
    admin_obj.save()
    messages.success(request, 'Admin demoted to user successfully')
    return redirect('admins_list')

@login_required
def delete_task(request, task_id):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully')
    return redirect('tasks_list')

@login_required
def assign_user_to_admin(request, user_id):
    if not request.user.is_superuser:
        return render(request, '403.html')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        if admin_id:
            admin_obj = get_object_or_404(User, id=admin_id, role='admin')
            user_obj.admin = admin_obj
            user_obj.save()
            messages.success(request, f'User {user_obj.username} assigned to {admin_obj.username}')
        else:
            user_obj.admin = None
            user_obj.save()
            messages.success(request, f'User {user_obj.username} unassigned from admin')
        return redirect('users_list')
    
    admins = User.objects.filter(role='admin')
    return render(request, 'admin/assign_user.html', {
        'user_obj': user_obj,
        'admins': admins
    })
