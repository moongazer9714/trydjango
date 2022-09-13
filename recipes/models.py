from django.db import models
# from .validators import validator_of_units
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    tag = models.CharField(max_length=21)
    slug = models.SlugField(max_length=221, unique=True, null=True, blank=True)

    def __str__(self):
        return self.tag

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.tag)
    #     super().save(*args, **kwargs)


class Recipe(Timestamp):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=221, unique=True, null=True, blank=True)
    recipe_name = models.CharField(max_length=221)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.recipe_name


# def recipe_pre_save(instance, sender, *args, **kwargs):
#     if instance.slug is None:
#         instance.slug = slugify(instance.name)
#
#
# pre_save.connect(recipe_pre_save, sender=Recipe)


def recipe_post_save(instance, sender, created, *args, **kwargs):
    if created:
        if instance.slug is None:
            instance.slug = slugify(instance.recipe_name)
            instance.save()


post_save.connect(recipe_post_save, sender=Recipe)


class RecipeIngredient(Timestamp):
    UNITS = (
        (0, 'kg'),
        (1, 'l'),
        (2, 'sht'),
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=221, help_text="Kichikroq yoz")
    quantity = models.FloatField()
    # unit = models.CharField(max_length=21, validators=[validator_of_units])
    unit = models.IntegerField(choices=UNITS, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
