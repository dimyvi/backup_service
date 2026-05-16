from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("delete/<int:backup_id>/", views.delete_backup, name="delete_backup"),
]