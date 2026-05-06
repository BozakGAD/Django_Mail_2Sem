import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from folders.models import Folder
from users.models import User
from .models import Email


def _serialize_email(email, current_user):
    folder = email.recipient_folder if email.recipient_id == current_user.id else email.sender_folder
    return {
        "id": email.id,
        "sender": email.sender.username,
        "recipient": email.recipient.username,
        "subject": email.subject,
        "body": email.body,
        "is_read": email.is_read,
        "created_at": email.created_at.isoformat(),
        "folder": folder.system_name,
    }


@csrf_exempt
@require_POST
def register_view(request):
    payload = json.loads(request.body)
    user = User.objects.create_user(
        username=payload["username"],
        email=payload.get("email", ""),
        password=payload["password"],
    )
    for key, value in Folder.SYSTEM_CHOICES:
        Folder.objects.get_or_create(user=user, system_name=key, defaults={"name": value})
    return JsonResponse({"id": user.id, "username": user.username}, status=201)


@csrf_exempt
@require_POST
def login_view(request):
    payload = json.loads(request.body)
    user = authenticate(request, username=payload.get("username"), password=payload.get("password"))
    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"message": "Logged in"})


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@csrf_exempt
@require_POST
@login_required
def send_email(request):
    payload = json.loads(request.body)
    recipient = User.objects.filter(username=payload.get("recipient")).first()
    if not recipient:
        return JsonResponse({"error": "Recipient not found"}, status=404)
    sender_folder = Folder.objects.get(user=request.user, system_name=Folder.SENT)
    recipient_folder = Folder.objects.get(user=recipient, system_name=Folder.INBOX)
    email = Email.objects.create(
        sender=request.user,
        recipient=recipient,
        subject=payload.get("subject", ""),
        body=payload.get("body", ""),
        sender_folder=sender_folder,
        recipient_folder=recipient_folder,
    )
    return JsonResponse(_serialize_email(email, request.user), status=201)


@require_GET
@login_required
def inbox_list(request):
    emails = Email.objects.filter(recipient=request.user).select_related("sender", "recipient", "recipient_folder")
    return JsonResponse({"results": [_serialize_email(email, request.user) for email in emails]})


@require_GET
@login_required
def sent_list(request):
    emails = Email.objects.filter(sender=request.user).select_related("sender", "recipient", "sender_folder")
    return JsonResponse({"results": [_serialize_email(email, request.user) for email in emails]})


@require_GET
@login_required
def folder_list(request, folder_name):
    emails = Email.objects.filter(
        models.Q(recipient=request.user, recipient_folder__system_name=folder_name)
        | models.Q(sender=request.user, sender_folder__system_name=folder_name)
    ).select_related("sender", "recipient", "recipient_folder", "sender_folder")
    return JsonResponse({"results": [_serialize_email(email, request.user) for email in emails]})


@require_GET
@login_required
def email_detail(request, email_id):
    email = Email.objects.filter(id=email_id).select_related("sender", "recipient", "recipient_folder", "sender_folder").first()
    if not email or (email.sender_id != request.user.id and email.recipient_id != request.user.id):
        return JsonResponse({"error": "Email not found"}, status=404)
    if email.recipient_id == request.user.id and not email.is_read:
        email.is_read = True
        email.save(update_fields=["is_read"])
    return JsonResponse(_serialize_email(email, request.user))


@csrf_exempt
@require_POST
@login_required
def move_email(request, email_id):
    payload = json.loads(request.body)
    target_folder = Folder.objects.filter(user=request.user, system_name=payload.get("folder")).first()
    if not target_folder:
        return JsonResponse({"error": "Folder not found"}, status=404)
    email = Email.objects.filter(id=email_id).first()
    if not email:
        return JsonResponse({"error": "Email not found"}, status=404)
    if email.recipient_id == request.user.id:
        email.recipient_folder = target_folder
    elif email.sender_id == request.user.id:
        email.sender_folder = target_folder
    else:
        return JsonResponse({"error": "No access"}, status=403)
    email.save(update_fields=["recipient_folder", "sender_folder"])
    return JsonResponse(_serialize_email(email, request.user))


@require_POST
@login_required
def delete_email(request, email_id):
    email = Email.objects.filter(id=email_id).first()
    if not email:
        return JsonResponse({"error": "Email not found"}, status=404)
    if email.sender_id == request.user.id or email.recipient_id == request.user.id:
        email.delete()
        return JsonResponse({"message": "Deleted"})
    return JsonResponse({"error": "No access"}, status=403)
