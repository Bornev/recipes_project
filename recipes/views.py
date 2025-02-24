"""
Представления для приложения recipes.

Обрабатывает запросы и возвращает ответы (HTML-страницы или перенаправления).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import sample
from .models import Recipe, Category
from .forms import RecipeForm, UserRegisterForm, CategoryForm
from django.db.models import Q

# Главная страница с 5 случайными рецептами
def index(request):
    """
    Отображает главную страницу с 5 случайными рецептами.
    """
    recipes = Recipe.objects.all()  # Получаем все рецепты
    random_recipes = sample(list(recipes), min(5, recipes.count()))  # Выбираем до 5 случайных
    return render(request, 'recipes/index.html', {'recipes': random_recipes})

# Страница подробного просмотра рецепта
def recipe_detail(request, recipe_id):
    """
    Отображает страницу с деталями одного рецепта.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

# Регистрация нового пользователя
def register(request):
    """
    Обрабатывает регистрацию пользователя через форму UserRegisterForm.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Создаём форму с данными из POST-запроса
        if form.is_valid():  # Проверяем валидность данных
            user = form.save()  # Сохраняем пользователя (пароль хешируется в форме)
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')  # Перенаправление на главную
    else:
        form = UserRegisterForm()  # Пустая форма для GET-запроса
    return render(request, 'recipes/register.html', {'form': form})

# Вход пользователя
def user_login(request):
    """
    Обрабатывает вход пользователя через имя и пароль.
    """
    if request.method == 'POST':
        username = request.POST['username']  # Получаем имя пользователя
        password = request.POST['password']  # Получаем пароль
        user = authenticate(request, username=username, password=password)  # Проверка данных
        if user is not None:
            login(request, user)  # Вход, если данные верны
            messages.success(request, 'Вы успешно вошли!')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'recipes/login.html')

# Выход пользователя
def user_logout(request):
    """
    Выполняет выход пользователя из системы.
    """
    logout(request)  # Завершение сессии
    messages.success(request, 'Вы успешно вышли!')
    return redirect('index')  # Перенаправление на главную

# Список рецептов с фильтром по категориям
def recipe_list(request):
    """
    Отображает список всех рецептов с возможностью фильтрации по категории.
    """
    category_id = request.GET.get('category')  # Получаем ID категории из GET-параметра
    recipes = Recipe.objects.all()

    if category_id:
        recipes = recipes.filter(categories__id=category_id)  # Фильтрация по категории

    categories = Category.objects.all()  # Получаем все категории для фильтра
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'categories':
        categories, 'selected_category': category_id})

# Добавление нового рецепта (только для авторизованных)
@login_required
def recipe_create(request):
    """
    Обрабатывает создание нового рецепта через форму RecipeForm.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Форма с данными и файлами
        if form.is_valid():
            recipe = form.save(commit=False)  # Сохраняем без коммита, чтобы добавить автора
            recipe.author = request.user  # Устанавливаем текущего пользователя как автора
            recipe.save()  # Сохраняем рецепт
            print("Выбранные категории:", form.cleaned_data['categories'])
            form.save_m2m()  # Сохраняем связи многие-ко-многим (категории)
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)  # Перенаправление на страницу рецепта
    else:
        form = RecipeForm()  # Пустая форма для GET-запроса
    return render(request, 'recipes/recipe_form.html', {'form': form})

# Редактирование рецепта (только для автора)
@login_required
def recipe_edit(request, recipe_id):
    """
    Обрабатывает редактирование существующего рецепта.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)  # Только автор может редактировать
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Форма с текущими данными
        if form.is_valid():
            form.save()  # Сохраняем изменения
            messages.success(request, 'Рецепт успешно обновлён!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)  # Форма с данными рецепта
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required  # Только авторизованные пользователи
def category_create(request):
    """
    Обрабатывает создание новой категории через форму CategoryForm.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем категорию
            messages.success(request, 'Категория успешно создана!')
            return redirect('recipe_create')  # Перенаправляем на создание рецепта
    else:
        form = CategoryForm()
    return render(request, 'recipes/category_form.html', {'form': form})