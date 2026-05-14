from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('favorite/<int:movie_id>/',views.add_favorite, name="add_favorite"),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/remove/<int:movie_id>/', views.remove_favorite, name='remove_favorite'),
]