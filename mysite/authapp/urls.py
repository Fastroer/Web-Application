from django.urls import path
from .views import ProfileView, SignOutView, SignInView, SignUpView, ChangePasswordView, AvatarView

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', SignOutView.as_view(), name='sign-out'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('profile/password', ChangePasswordView.as_view(), name='change-password'),
    path('profile/avatar', AvatarView.as_view()),
]
