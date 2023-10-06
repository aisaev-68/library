from django.urls import path


from account.views import CheckAuthenticationAPI, AccountUserAPIView, UserProfileAPIView, UserAvatarAPIView, UserPasswordChangeView

app_name = 'account'
urlpatterns = [
    path('api/account/', AccountUserAPIView.as_view()),
    path('api/profile/', UserProfileAPIView.as_view()),
    path('api/profile/avatar/', UserAvatarAPIView.as_view()),
    path('api/profile/password/', UserPasswordChangeView.as_view(), name='user-password-change'),
    path('api/check-authentication/', CheckAuthenticationAPI.as_view(), name='check_authentication_api'),
]

