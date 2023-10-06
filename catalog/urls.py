from django.urls import path
from catalog import views

app_name = 'catalog'
urlpatterns = [
    path('api/genre/', views.GenreAPIView.as_view(), name='genre-list'),
    path('api/genre/<int:pk>/', views.GenreAPIView.as_view(), name='genre_by_id'),
    path('api/catalog/', views.BookAPIView.as_view(), name='book-list'),
    # path('api/catalog/<int:pk>/', views.BookIdAPIView.as_view()),
    path('api/book/<int:pk>/', views.BookDetailAPIView.as_view(), name='book_by_id'),
    path('api/book/<int:pk>/review/', views.BookReviewAPIView.as_view(), name='book-review'),
    path('api/search/', views.SearchAPIView.as_view(), name="search"),
    path('api/book/popular/', views.BookPopularAPIView.as_view(), name="book_popular"),
]
