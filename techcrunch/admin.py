from django.contrib import admin
from django.contrib.admin import register

from .models import (
    Author, Category, Post, PostAuthor, PostCategory,
    Keyword, SearchByKeyword, PostSearchByKeywordItem,
    AutoScrap, AutoScrapPostItem, AutoScrapCategoryItem, AutoScrapAuthorItem
)


def make_activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


def make_deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


class BaseAdmin(admin.ModelAdmin):
    actions = (make_activate, make_deactivate)


@register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ('id',
                    'name',
                    'description',
                    'position',
                    'link',
                    'avatar_image',
                    'slug',
                    'is_active',
                    'created_at',
                    'updated_at')
    list_display_links = ('id', 'name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('id',
                    'name',
                    'description',
                    'link',
                    'slug',
                    'is_active',
                    'created_at',
                    'updated_at')
    list_display_links = ('id', 'name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('id',
                    'title',
                    'content',
                    'link',
                    'slug',
                    'is_active',
                    'created_at',
                    'updated_at')
    list_display_links = ('id', 'title')
    list_filter = (
        'is_active', 'created_at', 'updated_at',
    )
    list_editable = ('is_active',)


@register(PostAuthor)
class PostAuthorAdmin(BaseAdmin):
    list_display = ('id', 'post', 'author',
                    'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'post')
    list_filter = ('is_active', 'created_at', 'updated_at', 'post', 'author')
    list_editable = ('is_active',)


@register(PostCategory)
class PostCategoryAdmin(BaseAdmin):
    list_display = ('id', 'post', 'category',
                    'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'post')
    list_filter = ('is_active', 'created_at', 'updated_at', 'post', 'category')
    list_editable = ('is_active',)


@register(Keyword)
class KeywordAdmin(BaseAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(SearchByKeyword)
class SearchByKeywordAdmin(BaseAdmin):
    list_display = ('id', 'keyword', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'keyword')
    list_filter = ('is_active', 'created_at', 'updated_at', 'keyword')
    list_editable = ('is_active',)


@register(PostSearchByKeywordItem)
class PostSearchByKeywordItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'search_by_keyword',
        'post',
        'is_scraped',
        'slug',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'search_by_keyword')
    list_filter = (
        'is_active', 'is_scraped', 'created_at', 'updated_at',
        'search_by_keyword',
        'post')
    list_editable = ('is_active',)


@register(AutoScrap)
class AutoScrapAdmin(BaseAdmin):
    list_display = (
        'id',
        'field',
        'page_count',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'field')
    list_filter = (
        'field', 'is_active', 'created_at', 'updated_at', )
    list_editable = ('is_active',)


@register(AutoScrapPostItem)
class AutoScrapPostItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'auto_scrap',
        'is_scraped',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'auto_scrap')
    list_filter = (
        'is_active', 'is_scraped', 'created_at', 'updated_at',)
    list_editable = ('is_active',)


@register(AutoScrapCategoryItem)
class AutoScrapCategoryItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'auto_scrap',
        'is_scraped',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'auto_scrap')
    list_filter = (
        'is_active', 'is_scraped', 'created_at', 'updated_at',)
    list_editable = ('is_active',)


@register(AutoScrapAuthorItem)
class AutoScrapAuthorItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'auto_scrap',
        'is_scraped',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'auto_scrap')
    list_filter = (
        'is_active', 'is_scraped', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
