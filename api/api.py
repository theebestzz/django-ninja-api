from ninja import NinjaAPI
from .models import Category, Post
from .schema import CategorySchema, PostSchema, CategorySchemaCreate, ErrorSchema
from django.shortcuts import get_object_or_404

app = NinjaAPI()


# Get all categories
@app.get("categories/", response=list[CategorySchema])
def categories(request):
    return Category.objects.all()


# Get category by id
@app.get("categories/get-by-id/{id}/", response=CategorySchema)
def category(request, id: int):
    category = get_object_or_404(Category, id=id)
    return category

# Get category by slug


@app.get("categories/get-by-slug/{slug}/", response=CategorySchema)
def category(request, slug: str):
    category = get_object_or_404(Category, slug=slug)
    return category


# Get all posts
@app.get("posts/", response=list[PostSchema])
def posts(request):
    return Post.objects.all()


# Get post by id
@app.get("posts/get-by-id/{id}/", response=PostSchema)
def post(request, id: int):
    post = get_object_or_404(Post, id=id)
    return post


# Get post by slug
@app.get("posts/get-by-slug/{slug}/", response=PostSchema)
def post(request, slug: str):
    post = get_object_or_404(Post, slug=slug)
    return post


# Create new category
@app.post("categories/create/", response={200: CategorySchema, 400: ErrorSchema})
def create_category(request, payload: CategorySchemaCreate):
    if Category.objects.filter(name=payload.name).exists():
        return 400, {"message": "Category already exists"}

    data = payload.dict()
    category = Category.objects.create(**data)
    return category


@app.post("posts/create/", response={200: PostSchema, 400: ErrorSchema})
def create_post(request, payload: PostSchema):

    if Post.objects.filter(title=payload.title).exists():
        return 400, {"message": "Post already exists"}

    data = payload.dict()
    post = Post.objects.create(**data)
    return post


@app.delete("categories/delete/{id}/", response={200: CategorySchema, 404: ErrorSchema})
def delete_category(request, id: int):

    if (Category.objects.filter(id=id).exists() == False):
        return 404, {"message": "Category does not exist"}

    category = get_object_or_404(Category, id=id)
    category.delete()
    return 200, {"message": "Category deleted"}


@app.delete("posts/delete/{id}/", response={200: PostSchema, 404: ErrorSchema})
def delete_post(request, id: int):

    if (Post.objects.filter(id=id).exists() == False):
        return 404, {"message": "Post does not exist"}

    post = get_object_or_404(Post, id=id)
    post.delete()
    return 200, {"message": "Post deleted"}


@app.put("categories/update/{id}/", response={200: CategorySchema, 404: ErrorSchema})
def update_category(request, id: int, payload: CategorySchemaCreate):
    category = get_object_or_404(Category, id=id)
    category.name = payload.name
    category.slug = payload.slug
    category.save()
    return category


@app.put("posts/update/{id}/", response={200: PostSchema, 404: ErrorSchema})
def update_post(request, id: int, payload: PostSchema):
    post = get_object_or_404(Post, id=id)
    post.title = payload.title
    post.slug = payload.slug
    post.content = payload.content
    post.save()
    return post
