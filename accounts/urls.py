from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logoutView, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path("ticket_list/", views.ticket_list, name="ticket_list"),
    path('create_ticket/', views.create_ticket, name='create_ticket'),

    path('ticket_detail/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket_delete/<int:pk>/', views.ticket_delete, name='ticket_delete'),
    path('ticket_edit/<int:pk>/', views.ticket_edit, name='ticket_edit'),

    path('add_company/', views.add_company, name='add_company'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]