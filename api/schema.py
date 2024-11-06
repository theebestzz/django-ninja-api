from ninja import ModelSchema, Schema
from .models import Category, Post


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class PostSchema(ModelSchema):
    category: CategorySchema | None = None

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'category')


class CategorySchemaCreate(Schema):
    name: str
    slug: str | None = None


class PostSchemaCreate(Schema):
    title: str
    slug: str | None = None
    content: str
    category: int


class ErrorSchema(Schema):
    message: str
