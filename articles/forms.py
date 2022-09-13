from django import forms
from .models import Article


class _ArticleCreateForm(forms.Form):
    title = forms.CharField(max_length=222)
    content = forms.CharField(max_length=222)


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['slug']
