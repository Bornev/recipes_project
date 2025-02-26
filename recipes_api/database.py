from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

# Путь к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/user/PycharmProjects/recipes_project/db.sqlite3"

# Создание подключения к базе
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Создание базы для моделей
Base = declarative_base()

# Создание сессии для работы с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Category(Base):
    __tablename__ = "recipes_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)

class Recipe(Base):
    __tablename__ = "recipes_recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    steps = Column(Text)
    cooking_time = Column(Integer)
    image = Column(String)  # Путь к изображению
    ingredients = Column(Text)
    author_id = Column(Integer, ForeignKey("auth_user.id"))

    author = relationship("User", foreign_keys=[author_id])
    categories = relationship("Category", secondary="recipes_recipecategory")

class RecipeCategory(Base):
    __tablename__ = "recipes_recipecategory"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes_recipe.id"))
    category_id = Column(Integer, ForeignKey("recipes_category.id"))