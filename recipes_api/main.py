from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine, get_db
from .database import Recipe, Category, RecipeCategory
from pydantic import BaseModel

# Создание таблиц (если они ещё не созданы)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Модели Pydantic для валидации данных
class RecipeCreate(BaseModel):
    title: str
    description: str
    steps: str
    cooking_time: int
    ingredients: str
    categories: list[int]  # Список ID категорий


class RecipeUpdate(BaseModel):
    description: str | None = None
    steps: str | None = None
    ingredients: str | None = None
    categories: list[int] | None = None


# Операции чтения (Read)
@app.get("/recipes/")
async def get_all_recipes(db: Session = Depends(get_db)):
    """
    Получение всех рецептов.
    """
    recipes = db.query(Recipe).all()
    return recipes


@app.get("/recipes/{recipe_title}")
async def get_recipe_by_title(recipe_title: str, db: Session = Depends(get_db)):
    """
    Получение рецепта по названию.
    """
    recipe = db.query(Recipe).filter(Recipe.title == recipe_title).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe


@app.get("/recipes/ingredient/{ingredient}")
async def get_recipes_by_ingredient(ingredient: str, db: Session = Depends(get_db)):
    """
    Получение всех рецептов с указанным ингредиентом.
    """
    recipes = db.query(Recipe).filter(Recipe.ingredients.ilike(f"%{ingredient}%")).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="Рецепты не найдены")
    return recipes


@app.get("/recipes/category/{category_id}")
async def get_recipes_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Получение всех рецептов указанной категории.
    """
    recipes = db.query(Recipe).join(RecipeCategory).join(Category).filter(Category.id == category_id).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="Рецепты не найдены")
    return recipes


# Дополнительный запрос (по автору)
@app.get("/recipes/author/{author_id}")
async def get_recipes_by_author(author_id: int, db: Session = Depends(get_db)):
    """
    Получение всех рецептов указанного автора.
    """
    recipes = db.query(Recipe).filter(Recipe.author_id == author_id).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="Рецепты не найдены")
    return recipes


# Операции создания (Create)
@app.post("/recipes/")
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Добавление нового рецепта.
    """
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        steps=recipe.steps,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Добавление категорий
    for category_id in recipe.categories:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        recipe_category = RecipeCategory(recipe_id=new_recipe.id, category_id=category_id)
        db.add(recipe_category)
    db.commit()

    return new_recipe


# Операции обновления (Update)
@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe_update: RecipeUpdate, db: Session = Depends(get_db)):
    """
    Редактирование рецепта.
    """
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    if recipe_update.description is not None:
        db_recipe.description = recipe_update.description
    if recipe_update.steps is not None:
        db_recipe.steps = recipe_update.steps
    if recipe_update.ingredients is not None:
        db_recipe.ingredients = recipe_update.ingredients

    if recipe_update.categories is not None:
        # Удаляем старые связи
        db.query(RecipeCategory).filter(RecipeCategory.recipe_id == recipe_id).delete()
        # Добавляем новые
        for category_id in recipe_update.categories:
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(status_code=404, detail="Категория не найдена")
            recipe_category = RecipeCategory(recipe_id=recipe_id, category_id=category_id)
            db.add(recipe_category)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe