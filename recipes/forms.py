from django import forms
from django.forms import ModelForm
from .models import Recipe, RecipeIngredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
        exclude = ['slug', 'user', 'is_active']


class RecipeIngredientForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']

