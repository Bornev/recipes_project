from django.contrib import admin
from .models import Category, Recipe, RecipeCategory

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
