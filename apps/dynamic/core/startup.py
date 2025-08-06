# app/core/startup.py

from apps.dynamic.core.controllers.dynamic_controller import dynamic_init  # Adjust path accordingly

def run_startup_tasks():
    dynamic_init(
        name="blog",
        json_path="data/Blog.json",
        field_path="blog.blogs.details.fields"
    )

    # Add other dynamic_init calls here if needed
