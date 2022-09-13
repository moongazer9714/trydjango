from django.urls import path
from .views import (recipe_list_view,
                    recipe_detail_view,
                    recipe_create_view,
                    recipe_update_view,
                    recipe_delete_view,
                    )

app_name = "recipes"

urlpatterns = [
    path('', recipe_list_view, name="recipe_list"),
    path('detail/<slug:slug>/', recipe_detail_view, name="recipe_detail"),
    path('create/', recipe_create_view, name="recipe_create"),
    path('edit/<int:pk>/', recipe_update_view, name="recipe_update"),
    path('delete/<slug:slug>/', recipe_delete_view, name="recipe_delete"),
]
