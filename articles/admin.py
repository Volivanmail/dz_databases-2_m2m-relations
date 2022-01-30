from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Tag


class ArticleScopesInlineFormset(BaseInlineFormSet):

    def clean(self):
        for form in self.forms:
            count = 0
            if count > 1:
                raise ValidationError('Основной тег может быть только один')
            elif form.cleaned_data['is_main'] is True:
                count +=1
            else:
                continue
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    extra = 1
    # formset = ArticleScopesInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at']
    inlines = [ArticleScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']