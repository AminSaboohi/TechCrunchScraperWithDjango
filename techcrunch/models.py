from abc import abstractmethod

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import mark_safe
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
import os

# Create your models here.
User = get_user_model()


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        abstract = True

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('Implement __str__ method')


class Author(BaseModel):
    id_on_techcrunch = models.CharField(max_length=20,
                                        blank=False,
                                        null=False,
                                        verbose_name="ID on Techcrunch",
                                        )
    slug = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Slug"
                            )
    name = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Name"
                            )
    description = models.TextField(blank=False,
                                   null=False,
                                   verbose_name="Description"
                                   )
    position = models.CharField(max_length=250,
                                blank=False,
                                null=False,
                                verbose_name="Position"
                                )
    link = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Link"
                            )
    image_link = models.URLField(max_length=250,
                                 blank=False,
                                 null=False,
                                 verbose_name="Position"
                                 )
    image = models.ImageField(upload_to='images/',
                              default=f'{slug}.png',
                              blank=True, )

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return f'Author: {self.name}, {self.position}'

    def get_remote_image(self):
        if self.image_link and not self.image:
            img_temp = NamedTemporaryFile(delete=True)

            fd = os.open(f"image_{self.pk}.png", os.O_RDWR)
            print("Blocking Mode:", os.get_blocking(fd))
            blocking = False
            os.set_blocking(fd, blocking)
            print("Blocking mode changed")
            print("Blocking Mode:", os.get_blocking(fd))

            # close the file descriptor

            img_temp.write(urlopen(self.image_link).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}.png", File(img_temp), save=True)
            self.save()
            os.close(fd)

    def img_preview(self):  # new
        return mark_safe(f'<img src="/images/{self.image}"'
                         f'" width="150" height="150" />')

    img_preview.short_description = 'Image'


class Category(BaseModel):
    id_on_techcrunch = models.CharField(max_length=20,
                                        blank=False,
                                        null=False,
                                        verbose_name="ID on Techcrunch",
                                        )
    slug = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Slug"
                            )
    name = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Name"
                            )
    post_count = models.CharField(max_length=250,
                                  blank=False,
                                  null=False,
                                  verbose_name="Post count"
                                  )
    description = models.TextField(blank=False,
                                   null=False,
                                   verbose_name="Description"
                                   )
    link = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Link"
                            )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Category: {self.name}'


class Post(BaseModel):
    id_on_techcrunch = models.CharField(max_length=20,
                                        blank=False,
                                        null=False,
                                        verbose_name="ID on Techcrunch",
                                        )
    title = models.CharField(max_length=250,
                             blank=False,
                             null=False,
                             verbose_name="Title",
                             )
    slug = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Slug",
                            )
    content = models.TextField(blank=False,
                               null=False,
                               verbose_name="Content",
                               )
    link = models.CharField(max_length=250,
                            blank=True,
                            null=False,
                            verbose_name="Link",
                            )
    image_link = models.URLField(max_length=250,
                                 blank=True,
                                 null=False,
                                 verbose_name="Image link",
                                 )
    image = models.ImageField(upload_to='images/',
                              default=f'image.png',
                              blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post: {self.title}'


class PostCategory(BaseModel):
    post = models.ForeignKey(Post,
                             related_name='post_categories',
                             on_delete=models.CASCADE,
                             verbose_name="Post",
                             )
    category = models.ForeignKey(Category,
                                 related_name='post_categories',
                                 on_delete=models.CASCADE,
                                 verbose_name="Category",
                                 )

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return f'{self.post.title}({self.category.name})'


class PostAuthor(BaseModel):
    post = models.ForeignKey(Post,
                             related_name='post_authors',
                             on_delete=models.CASCADE,
                             verbose_name="Post"
                             )
    author = models.ForeignKey(Author,
                               related_name='post_authors',
                               on_delete=models.CASCADE,
                               verbose_name="Author"
                               )

    class Meta:
        verbose_name = 'Post Author'
        verbose_name_plural = 'Post Authors'

    def __str__(self):
        return f'{self.post.title}({self.author.name})'


class Keyword(BaseModel):
    title = models.CharField(max_length=250,
                             blank=False,
                             null=False,
                             verbose_name="Keyword",
                             )

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

    def __str__(self):
        return self.title


class SearchByKeyword(BaseModel):
    keyword = models.ForeignKey(Keyword,
                                related_name='searches',
                                on_delete=models.CASCADE,
                                verbose_name="Keyword",
                                )
    page_count = models.IntegerField(
        default=settings.DEFAULT_SEARCH_PAGE_COUNT,
        blank=False,
        null=False,
        verbose_name="Page count",
    )

    class Meta:
        verbose_name = 'Search By Keyword'
        verbose_name_plural = 'Search By Keywords'

    def __str__(self):
        return f'searches {self.keyword.title}: {self.page_count}'


class PostSearchByKeywordItem(BaseModel):
    search_by_keyword = models.ForeignKey(
        SearchByKeyword,
        related_name='post_search_by_keyword_items',
        on_delete=models.CASCADE,
        verbose_name="Search By Keyword",
    )
    post = models.ForeignKey(
        Post,
        related_name='post_search_by_keyword_items',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Post",
    )
    slug = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Slug",
                            )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )
    fail_count = models.IntegerField(default=0,
                                     blank=False,
                                     null=False,
                                     verbose_name="Fail count",
                                     )

    class Meta:
        verbose_name = 'Post Search By Keyword Item'
        verbose_name_plural = 'Post Search By Keyword Items'

    def __str__(self):
        return f'Post Search By Keyword : slug = {self.slug}'


class PostSearchDailyItem(BaseModel):
    post = models.ForeignKey(
        Post,
        related_name='post_search_daily_items',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Post",
    )
    slug = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Slug",
                            )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )
    fail_count = models.IntegerField(default=0,
                                     blank=False,
                                     null=False,
                                     verbose_name="Fail count",
                                     )

    class Meta:
        verbose_name = 'Post Search Daily Item'
        verbose_name_plural = 'Post Search Daily Items'

    def __str__(self):
        return f'Post Search Daily : slug = {self.slug}'


class AutoScrap(BaseModel):
    field = models.CharField(max_length=250,
                             blank=False,
                             null=False,
                             verbose_name="field",
                             )
    page_start = models.IntegerField(
        default=1,
        blank=False,
        null=False,
        verbose_name="Page count",
    )
    page_count = models.IntegerField(
        default=settings.DEFAULT_SEARCH_PAGE_COUNT,
        blank=False,
        null=False,
        verbose_name="Page count",
    )

    class Meta:
        verbose_name = 'Auto scrap'
        verbose_name_plural = 'Auto scrap'

    def __str__(self):
        return f'Auto scrape {self.field}'


class AutoScrapPostItem(BaseModel):
    auto_scrap = models.ForeignKey(
        AutoScrap,
        related_name='auto_scrap_post_items',
        on_delete=models.CASCADE,
        verbose_name="Auto Scrap",
    )
    posts = models.ManyToManyField(
        Post,
        related_name='auto_scrap_category_items',
        blank=True,
        verbose_name='Posts'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )
    fail_count = models.IntegerField(default=0,
                                     blank=False,
                                     null=False,
                                     verbose_name="Fail count",
                                     )

    class Meta:
        verbose_name = 'Auto Scrap Post Item'
        verbose_name_plural = 'Auto Scrap Post Items'

    def __str__(self):
        return (f'Auto Scrap Post : field = {self.auto_scrap.field} ,'
                f' {self.auto_scrap.page_count}pages')


class AutoScrapCategoryItem(BaseModel):
    auto_scrap = models.ForeignKey(
        AutoScrap,
        related_name='auto_scrap_category_items',
        on_delete=models.CASCADE,
        verbose_name="Auto Scrap"
    )
    categories = models.ManyToManyField(
        Category,
        related_name='auto_scrap_category_items',
        blank=True,
        verbose_name='Categories'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )
    fail_count = models.IntegerField(default=0,
                                     blank=False,
                                     null=False,
                                     verbose_name="Fail count",
                                     )

    class Meta:
        verbose_name = 'Auto Scrap Category Item'
        verbose_name_plural = 'Auto Scrap Category Items'

    def __str__(self):
        return (f'Auto Scrap Category : field = {self.auto_scrap.field} ,'
                f' {self.auto_scrap.page_count}pages')


class AutoScrapAuthorItem(BaseModel):
    auto_scrap = models.ForeignKey(
        AutoScrap,
        related_name='auto_scrap_author_items',
        on_delete=models.CASCADE,
        verbose_name='Auto Scrap'
    )
    authors = models.ManyToManyField(
        Author,
        related_name='auto_scrap_author_items',
        blank=True,
        verbose_name='Authors'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )
    fail_count = models.IntegerField(default=0,
                                     blank=False,
                                     null=False,
                                     verbose_name="Fail count",
                                     )

    class Meta:
        verbose_name = 'Auto Scrap Author Item'
        verbose_name_plural = 'Auto Scrap Author Items'

    def __str__(self):
        return (f'Auto Scrap Author : field = {self.auto_scrap.field} ,'
                f' {self.auto_scrap.page_count}pages')
