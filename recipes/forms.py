"""
Формы для приложения recipes.

Содержит формы для работы с рецептами и регистрацией пользователей.
"""

from django import forms
from django.contrib.auth.models import User
from .models import Recipe

# Форма для добавления и редактирования рецептов
class RecipeForm(forms.ModelForm):
    """
    Форма, связанная с моделью Recipe.
    Используется для создания и редактирования рецептов.
    """
    class Meta:
        model = Recipe  # Связь с моделью Recipe
        fields = [
            'title',
            'description',
            'steps',
            'cooking_time',
            'image',
            'ingredients',
            'categories',
        ]
        widgets = {
            # Настройка виджетов для текстовых полей
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'steps': forms.Textarea(attrs={'rows': 10, 'cols': 50}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'categories': forms.CheckboxSelectMultiple(),  # Множественный выбор категорий
        }
        labels = {
            # Человекочитаемые подписи для полей
            'title': 'Название рецепта',
            'description': 'Описание блюда',
            'steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления (в минутах)',
            'image': 'Изображение блюда',
            'ingredients': 'Список ингредиентов',
            'categories': 'Категории рецепта',
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы: настройка стилей или дополнительных параметров.
        """
        super().__init__(*args, **kwargs)
        # Добавляем CSS-классы для стилизации
        for field in self.fields:
            if field != 'categories':  # Исключаем категории
                self.fields[field].widget.attrs.update({'class': 'form-control'})


# Форма для регистрации нового пользователя
class UserRegisterForm(forms.ModelForm):
    """
    Форма для регистрации пользователей с проверкой пароля.
    """
    password = forms.CharField(
        widget=forms.PasswordInput,  # Поле ввода пароля (скрывает символы)
        label="Пароль"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,  # Повторный ввод пароля
        label="Подтверждение пароля"
    )

    class Meta:
        model = User  # Связь с моделью User
        fields = ['username', 'email', 'password']  # Поля формы
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Проверка данных формы: совпадение паролей.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data

    def save(self, commit=True):
        """
        Сохранение пользователя с хешированием пароля.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Хеширование пароля
        if commit:
            user.save()
        return user