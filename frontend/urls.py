from django.urls import path, re_path
from django.views.generic import TemplateView
from account.views import RegisterView, MyLoginView, MyLogoutView


name = 'frontend'
urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html"), name='index'),
    path('account/', TemplateView.as_view(template_name="frontend/account.html"), name='account'),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html"), name='catalog'),
    path('catalog/<int:pk>/', TemplateView.as_view(template_name="frontend/catalog.html"), name='catalog_by_id'),
    path('book/<int:pk>/', TemplateView.as_view(template_name="frontend/book_detail.html"), name='book-detail'),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html"), name='profile'),
    path('book-list/', TemplateView.as_view(template_name="frontend/book-list.html"), name='book-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
