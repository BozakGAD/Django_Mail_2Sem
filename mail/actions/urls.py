from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('emails/send/', views.send_email, name='send-email'),
    path('emails/inbox/', views.inbox_list, name='inbox-list'),
    path('emails/sent/', views.sent_list, name='sent-list'),
    path('emails/folder/<str:folder_name>/', views.folder_list, name='folder-list'),
    path('emails/<int:email_id>/', views.email_detail, name='email-detail'),
    path('emails/<int:email_id>/move/', views.move_email, name='move-email'),
    path('emails/<int:email_id>/delete/', views.delete_email, name='delete-email'),
]
