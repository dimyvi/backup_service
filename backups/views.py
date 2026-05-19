from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Backup, ActivityLog


@login_required
def dashboard(request):

    if request.method == "POST":

        file = request.FILES.get("file")
        name = request.POST.get("name")

        if file and name:

            backup = Backup.objects.create(
                user=request.user,
                name=name,
                file=file,
                size=file.size
            )

            # activity log
            ActivityLog.objects.create(
                user=request.user,
                action="uploaded",
                filename=backup.name
            )

        return redirect("dashboard")

    backups = Backup.objects.filter(
        user=request.user
    ).order_by("-created_at")

    activities = ActivityLog.objects.filter(
        user=request.user
    )[:10]

    total_backups = backups.count()

    total_size_bytes = sum(
        b.size for b in backups if b.size
    )

    # format size
    if total_size_bytes >= 1024 ** 3:
        total_size = f"{total_size_bytes / (1024 ** 3):.1f} GB"

    elif total_size_bytes >= 1024 ** 2:
        total_size = f"{total_size_bytes / (1024 ** 2):.1f} MB"

    else:
        total_size = f"{total_size_bytes / 1024:.1f} KB"

    last_upload = (
        backups.first().created_at
        if backups.exists()
        else None
    )

    # 10 GB limit
    storage_limit = 10 * 1024 * 1024 * 1024

    usage_percent = round(
        (total_size_bytes / storage_limit) * 100
    )

    return render(request, "dashboard.html", {
        "backups": backups,
        "activities": activities,
        "total_backups": total_backups,
        "total_size": total_size,
        "last_upload": last_upload,
        "usage_percent": usage_percent,
    })


@login_required
def delete_backup(request, backup_id):

    backup = get_object_or_404(
        Backup,
        id=backup_id,
        user=request.user
    )

    # activity log
    ActivityLog.objects.create(
        user=request.user,
        action="deleted",
        filename=backup.name
    )

    backup.delete()

    return redirect("dashboard")