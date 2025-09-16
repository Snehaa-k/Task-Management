from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('tasks/', admin_views.manage_tasks, name='tasks_list'),
    path('tasks/create/', admin_views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', admin_views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', admin_views.task_edit, name='edit_task'),
    path('users/', admin_views.manage_users, name='users_list'),
    path('users/create/', admin_views.create_user, name='create_user'),
    path('users/<int:user_id>/edit/', admin_views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', admin_views.delete_user, name='delete_user'),
    path('admins/', admin_views.manage_admins, name='admins_list'),
    path('admins/create/', admin_views.create_admin, name='admin_create'),
    path('admins/<int:admin_id>/edit/', admin_views.edit_admin, name='admin_edit'),
    path('admins/<int:admin_id>/delete/', admin_views.delete_admin, name='admin_delete'),
    path('admins/<int:admin_id>/demote/', admin_views.demote_admin, name='admin_demote'),
    path('tasks/<int:task_id>/delete/', admin_views.delete_task, name='delete_task'),
    path('reports/', admin_views.reports_list, name='reports_list'),
    path('reports/<int:task_id>/', admin_views.report_detail, name='report_detail'),
    path('users/<int:user_id>/assign/', admin_views.assign_user_to_admin, name='assign_user'),
]
