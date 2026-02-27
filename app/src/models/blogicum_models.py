"""Файл с моделями приложения."""
from datetime import datetime
from typing import Optional


class BaseModel:
    """Класс базовой модели с универсальными параметрами."""

    def __init__(self):
        """Метод инициализации."""
        self.id: Optional[int] = None
        self.is_published: bool = True
        self.created_at: datetime = datetime.now()


class Category(BaseModel):
    """Модель категории поста."""

    def __init__(self, title: str, description: str, slug: str):
        """Метод инициализации."""
        super().__init__()
        self.title = title
        self.description = description
        self.slug = slug


class Location(BaseModel):
    """Модель места публикации."""

    def __init__(self, name: str):
        """Метод инициализации."""
        super().__init__()
        self.name = name


class Post(BaseModel):
    """Модель поста."""

    def __init__(
        self,
        title: str,
        text: str,
        pub_date: datetime,
        author_id: int,
        location_id: Optional[int] = None,
        category_id: Optional[int] = None,
        image: Optional[str] = None,
    ):
        """Метод инициализации."""
        super().__init__()
        self.title = title
        self.text = text
        self.pub_date = pub_date
        self.author_id = author_id
        self.location_id = location_id
        self.category_id = category_id
        self.image = image


class Comment(BaseModel):
    """Модель комментария."""

    def __init__(self, post_id: int, author_id: int, text: str):
        """Метод инициализации."""
        super().__init__()
        self.post_id = post_id
        self.author_id = author_id
        self.text = text


class User(BaseModel):
    """Модель пользователя."""

    def __init__(self, username, email, password, first_name, second_name):
        """Метод инициализации."""
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.second_name = second_name
