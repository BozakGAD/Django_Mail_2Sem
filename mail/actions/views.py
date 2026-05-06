from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from folders.models import Folder
from users.models import User
from .models import Email


def _create_default_folders(user):
    for system_name, display_name in Folder.SYSTEM_CHOICES:
        Folder.objects.get_or_create(user=user, system_name=system_name, defaults={'name': display_name})


def home(request):
    if request.user.is_authenticated:
        return redirect('inbox')
    return render(request, 'home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('inbox')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        _create_default_folders(user)
        login(request, user)
        messages.success(request, 'Регистрация выполнена успешно')
        return redirect('inbox')
    return render(request, 'register.html', {'form': form})


def password_reset_request_view(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            messages.success(request, 'Запрос на сброс пароля принят. Проверьте вашу почту.')
        else:
            messages.error(request, 'Пользователь с таким email не найден')
        return redirect('login')
    return render(request, 'password_reset_request.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inbox')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('inbox')
    return render(request, 'login.html', {'form': form})


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def compose_email(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        recipient = User.objects.filter(id=recipient_id).first()
        if not recipient:
            messages.error(request, 'Получатель не найден')
            return redirect('compose')
        sender_folder = Folder.objects.get(user=request.user, system_name=Folder.SENT)
        recipient_folder = Folder.objects.get(user=recipient, system_name=Folder.INBOX)
        Email.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=request.POST.get('subject', '').strip(),
            body=request.POST.get('body', '').strip(),
            sender_folder=sender_folder,
            recipient_folder=recipient_folder,
        )
        messages.success(request, 'Письмо отправлено')
        return redirect('sent')
    return render(request, 'compose.html', {'users': users})


@login_required
def inbox_list(request):
    emails = Email.objects.filter(recipient=request.user).select_related('sender', 'recipient_folder')
    return render(request, 'email_list.html', {'emails': emails, 'title': 'Входящие'})


@login_required
def sent_list(request):
    emails = Email.objects.filter(sender=request.user).select_related('recipient', 'sender_folder')
    return render(request, 'email_list.html', {'emails': emails, 'title': 'Исходящие'})


@login_required
def folder_list(request, folder_name):
    emails = Email.objects.filter(recipient=request.user, recipient_folder__system_name=folder_name).select_related('sender', 'recipient_folder')
    return render(request, 'email_list.html', {'emails': emails, 'title': f'Папка: {folder_name}'})


@login_required
def email_detail(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    if email.sender_id != request.user.id and email.recipient_id != request.user.id:
        return HttpResponseForbidden('Доступ запрещен')
    if email.recipient_id == request.user.id and not email.is_read:
        email.is_read = True
        email.save(update_fields=['is_read'])
    return render(request, 'email_detail.html', {'email': email})


@require_POST
@login_required
def move_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    folder_name = request.POST.get('folder')
    target_folder = Folder.objects.filter(user=request.user, system_name=folder_name).first()
    if not target_folder:
        messages.error(request, 'Папка не найдена')
        return redirect('email-detail', email_id=email.id)
    if email.recipient_id == request.user.id:
        email.recipient_folder = target_folder
    elif email.sender_id == request.user.id:
        email.sender_folder = target_folder
    else:
        return HttpResponseForbidden('Доступ запрещен')
    email.save(update_fields=['recipient_folder', 'sender_folder'])
    messages.success(request, 'Письмо перемещено')
    return redirect('email-detail', email_id=email.id)


@require_POST
@login_required
def delete_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    if email.sender_id != request.user.id and email.recipient_id != request.user.id:
        return HttpResponseForbidden('Доступ запрещен')
    email.delete()
    messages.success(request, 'Письмо удалено')
    return redirect('inbox')
