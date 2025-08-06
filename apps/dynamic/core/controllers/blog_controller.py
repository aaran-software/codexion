from fastapi import APIRouter
from apps.dynamic.core.controllers.dynamic_controller import dynamic_init

router = APIRouter()

# @router.get("/init/blog")
# def setup_blog():
#     # Assuming Blog.json is in `data/`
#     return dynamic_init(name="blog", json_path="data/Blog.json", field_path="blog.blogs.details.fields")

def run_startup_tasks():
    dynamic_init(
        name="blog",
        json_path="data/Blog.json",
        field_path="blog.blogs.details.fields"
    )