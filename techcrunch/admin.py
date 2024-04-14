from django.contrib import admin
from django.contrib.admin import register
from .constances import TEXT_SHOW_MAX_SIZE
from django.http import HttpResponseRedirect
from django.conf import settings
import zipfile
import os

from .models import (
    Author, Category, Post, PostAuthor, PostCategory,
    Keyword, SearchByKeyword, PostSearchByKeywordItem, PostSearchDailyItem,
    AutoScrap, AutoScrapPostItem, AutoScrapCategoryItem, AutoScrapAuthorItem,
)
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html


def make_activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


def make_deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author


@admin.action(description='Export selected items to ZIP')
def export_as_zip(modeladmin, request, queryset):
    resource = PostResource()
    dataset = resource.export(queryset)
    html_content = dataset.html

    html_file_path = os.path.join(settings.MEDIA_ROOT, 'exported_data.html')
    with open(html_file_path, 'w') as file:
        file.write(html_content)

    zip_path = os.path.join(settings.MEDIA_ROOT, 'exported_data.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(html_file_path, os.path.basename(html_file_path))
        for obj in queryset:
            if obj.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(obj.image))
                zipf.write(image_path, os.path.basename(image_path))

    return HttpResponseRedirect(settings.MEDIA_URL + 'exported_data.zip')


class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = (make_activate, make_deactivate, export_as_zip)


@register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ('id',
                    'name',
                    'image_tag',
                    'short_description',
                    'position',
                    'link',
                    'slug',
                    'is_active',
                    'created_at',
                    'updated_at')
    list_display_links = ('id', 'name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)

    def image_tag(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" width="50" height="auto"/>'
        )

    image_tag.short_description = 'Image'

    def short_description(self, obj):
        return obj.description[:TEXT_SHOW_MAX_SIZE] + '...' \
            if len(obj.description) > TEXT_SHOW_MAX_SIZE else obj.description

    short_description.short_description = 'Description'


@register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('id',
                    'name',
                    'short_description',
                    'link',
                    'slug',
                    'is_active',
                    'created_at',
                    'updated_at')
    list_display_links = ('id', 'name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)

    def short_description(self, obj):
        return obj.description[:TEXT_SHOW_MAX_SIZE] + '...' \
            if len(obj.description) > TEXT_SHOW_MAX_SIZE else obj.description

    short_description.short_description = 'Description'


@register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('id',
                    'title',
                    'image_tag',
                    'short_content',
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

    def image_tag(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" width="50" height="auto"/>'
        )

    image_tag.short_description = 'Image'

    def short_content(self, obj):
        return obj.content[:TEXT_SHOW_MAX_SIZE] + '...' \
            if len(obj.content) > TEXT_SHOW_MAX_SIZE else obj.content

    short_content.short_description = 'Content'


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
        'fail_count',
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


@register(PostSearchDailyItem)
class PostSearchDailyItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'fail_count',
        'post',
        'is_scraped',
        'slug',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id',)
    list_filter = (
        'is_active', 'is_scraped', 'created_at', 'updated_at', 'post')
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
        'field', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)


@register(AutoScrapPostItem)
class AutoScrapPostItemAdmin(BaseAdmin):
    list_display = (
        'id',
        'fail_count',
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
        'fail_count',
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
        'fail_count',
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
