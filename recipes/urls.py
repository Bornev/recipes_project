"""
URL-маршруты для приложения recipes.

Связывает URL-адреса с функциональными представлениями из views.py.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # Страница подробного просмотра рецепта
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

    # Регистрация пользователя
    path('register/', views.register, name='register'),

    # Вход пользователя
    path('login/', views.user_login, name='login'),

    # Выход пользователя
    path('logout/', views.user_logout, name='logout'),

    # Создание нового рецепта
    path('recipe/create/', views.recipe_create, name='recipe_create'),

    # Редактирование рецепта
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),

    path('recipes/', views.recipe_list, name='recipe_list'),
]