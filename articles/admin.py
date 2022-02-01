from pprint import pprint

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Tag


class ArticleScopesInlineFormset(BaseInlineFormSet):

    def clean(self):
        count = False
        for form in self.forms:
            if bool(form.cleaned_data) is True:
                if count is False and form.cleaned_data['is_main'] is True:
                    count = True
                elif count is True and form.cleaned_data['is_main'] is True:
                    if form.cleaned_data['is_main'] is True:
                        raise ValidationError('Основной тег может быть только один')
                else:
                    continue
            else:
                return super().clean()





class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    extra = 1
    formset = ArticleScopesInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'published_at')
    list_display_links = ('title', 'text')
    inlines = [ArticleScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
