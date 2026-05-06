from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('compose/', views.compose_email, name='compose'),
    path('inbox/', views.inbox_list, name='inbox'),
    path('sent/', views.sent_list, name='sent'),
    path('folders/<str:folder_name>/', views.folder_list, name='folder-list'),
    path('emails/<int:email_id>/', views.email_detail, name='email-detail'),
    path('emails/<int:email_id>/move/', views.move_email, name='move-email'),
    path('emails/<int:email_id>/delete/', views.delete_email, name='delete-email'),
]
