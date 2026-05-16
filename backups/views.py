from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Backup


@login_required
def dashboard(request):

    if request.method == "POST":
        file = request.FILES.get("file")
        name = request.POST.get("name")

        if file and name:
            Backup.objects.create(
                user=request.user,
                name=name,
                file=file,
                size=file.size
            )

        return redirect("dashboard")

    backups = Backup.objects.filter(user=request.user).order_by("-created_at")

    total_backups = backups.count()
    total_size = sum(b.size for b in backups if b.size)
    last_upload = backups.first().created_at if backups.exists() else None

    return render(request, "dashboard.html", {
        "backups": backups,
        "total_backups": total_backups,
        "total_size": total_size,
        "last_upload": last_upload,
    })


@login_required
def delete_backup(request, backup_id):
    backup = get_object_or_404(
        Backup,
        id=backup_id,
        user=request.user
    )

    backup.delete()
    return redirect("dashboard")

