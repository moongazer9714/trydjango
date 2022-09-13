from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .models import Recipe, Tag, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm


def recipe_list_view(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, 'recipes/list.html', context)


def recipe_detail_view(request, slug=None):
    recipe = None
    if slug is not None:
        recipe = Recipe.objects.get(slug=slug)
    context = {'recipe': recipe}
    return render(request, 'recipes/detail.html', context)


@login_required
def recipe_create_view(request):
    form = RecipeForm()
    FormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=3)
    qs = RecipeIngredient.objects.none()
    formset = FormSet(queryset=qs)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = FormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user_id = request.user.id
            recipe.save()
            form.save_m2m()

            for form in formset:
                obj = form.save(commit=False)
                if form.cleaned_data.get('name') and form.cleaned_data.get('quantity'):
                    obj.recipe_id = recipe.id
                    obj.save()
            return redirect('recipes:recipe_list')
    context = {"form": form, 'formset': formset}
    return render(request, 'recipes/create.html', context)


def recipe_update_view(request, pk):
    obj = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=obj)
    FormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=3)
    qs = RecipeIngredient.objects.filter(recipe_id=pk)
    formset = FormSet(queryset=qs)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=obj)
        formset = FormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()

            for form in formset:
                obj2 = form.save(commit=False)
                if form.cleaned_data.get('name') and form.cleaned_data.get('quantity'):
                    obj2.recipe_id = obj.id
                    obj2.save()
            return redirect('recipes:recipe_detail', obj.slug)
    context = {"form": form, "formset": formset}
    return render(request, 'recipes/create.html', context)


def recipe_delete_view(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes:recipe_list')
    context = {"recipe": recipe}
    return render(request, 'recipes/delete.html', context)
