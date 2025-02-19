from django.contrib import admin
from src.knowledge.models import Category, Tag, Article, Glossary
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):
    """Form for connecting ckeditor to Article model"""
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published', 'date_creation')
    list_filter = ('author', 'category', 'published')
    filter_horizontal = ('glossary',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    """Glossary"""
    pass


admin.site.register(Tag)
