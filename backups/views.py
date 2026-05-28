from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.template.defaultfilters import filesizeformat

from .models import Backup, ActivityLog


MAX_STORAGE = 10 * 1024 * 1024 * 1024


@login_required
def dashboard(request):

    backups = Backup.objects.filter(
        user=request.user
    ).order_by("-created_at")

    activities = ActivityLog.objects.filter(
        user=request.user
    ).order_by("-created_at")[:10]

    total_backups = backups.count()

    total_size_raw = backups.aggregate(
        total=Sum("size")
    )["total"] or 0

    total_size = filesizeformat(total_size_raw)

    usage_percent = round(
        (total_size_raw / MAX_STORAGE) * 100,
        1
    )

    last_upload = (
        backups.first().created_at
        if backups.exists()
        else None
    )

    error = None

    if request.method == "POST":

        file = request.FILES.get("file")
        name = request.POST.get("name")

        if file and name:

            if total_size_raw + file.size > MAX_STORAGE:

                error = (
                    "Storage limit exceeded. "
                    "Delete old backups before uploading new files."
                )

            else:

                backup = Backup.objects.create(
                    user=request.user,
                    name=name,
                    file=file,
                    size=file.size
                )

                ActivityLog.objects.create(
                    user=request.user,
                    action="uploaded",
                    filename=backup.name
                )

                return redirect("dashboard")

    return render(request, "dashboard.html", {
        "backups": backups,
        "activities": activities,
        "total_backups": total_backups,
        "total_size": total_size,
        "total_size_raw": total_size_raw,
        "last_upload": last_upload,
        "usage_percent": usage_percent,
        "error": error,
    })


@login_required
def delete_backup(request, backup_id):

    backup = get_object_or_404(
        Backup,
        id=backup_id,
        user=request.user
    )

    # DELETE PHYSICAL FILE
    backup.file.delete(save=False)

    ActivityLog.objects.create(
        user=request.user,
        action="deleted",
        filename=backup.name
    )

    backup.delete()

    return redirect("dashboard")