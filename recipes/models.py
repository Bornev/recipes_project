"""
Модели данных для приложения recipes.

Описывает структуру таблиц в базе данных для хранения рецептов, категорий и их связей.
"""

from django.db import models
from django.contrib.auth.models import User  # Встроенная модель пользователя Django

# Модель категории рецептов
class Category(models.Model):
    """
    Категория рецептов (например, "Десерты", "Супы").
    """
    name = models.CharField(
        max_length=100,           # Максимальная длина названия — 100 символов
        unique=True,              # Название должно быть уникальным
        verbose_name="Название"
    )

    def __str__(self):
        """
        Строковое представление объекта (отображается в админке и консоли).
        """
        return self.name

    class Meta:
        verbose_name = "Категория"         # Название модели в единственном числе
        verbose_name_plural = "Категории"

# Модель рецепта
class Recipe(models.Model):
    """
    Рецепт блюда с основными данными: название, описание, шаги, время, изображение и т.д.
    """
    title = models.CharField(
        max_length=200,           # Максимальная длина названия — 200 символов
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание"   # Поле для описание блюда
    )
    steps = models.TextField(
        verbose_name="Шаги приготовления"  # Поле для шагов рецепта
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Время в минутах",       # Подсказка в админке
        verbose_name="Время приготовления"
    )
    image = models.ImageField(
        upload_to='recipes/',              # Папка для загрузки изображений
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    author = models.ForeignKey(
        User,                              # Связь с моделью User (автор рецепта)
        on_delete=models.CASCADE,          # Удаление рецепта при удалении пользователя
        verbose_name="Автор"
    )
    categories = models.ManyToManyField(
        Category,                          # Связь многие-ко-многим с категориями
        through='RecipeCategory',          # Через связующую таблицу
        verbose_name="Категории"
    )
    ingredients = models.TextField(
        blank=True,
        help_text="Список ингредиентов",
        verbose_name="Ингредиенты"
    )

    def __str__(self):
        """
        Строковое представление рецепта (название).
        """
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

# Связующая таблица для отношения многие-ко-многим между Recipe и Category
class RecipeCategory(models.Model):
    """
    Связь между рецептом и категорией (например, "Торт" — "Десерты").
    """
    recipe = models.ForeignKey(
        Recipe,                            # Связь с рецептом
        on_delete=models.CASCADE,          # Удаление связи при удалении рецепта
        verbose_name="Рецепт"
    )
    category = models.ForeignKey(
        Category,                          # Связь с категорией
        on_delete=models.CASCADE,          # Удаление связи при удалении категории
        verbose_name="Категория"
    )

    def __str__(self):
        """
        Строковое представление связи (например, "Торт - Десерты").
        """
        return f"{self.recipe} - {self.category}"

    class Meta:
        verbose_name = "Связь рецепта и категории"
        verbose_name_plural = "Связи рецептов и категорий"
        unique_together = ('recipe', 'category')  # Уникальность связки рецепт-категория