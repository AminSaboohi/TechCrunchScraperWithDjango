from abc import abstractmethod
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe


# Create your models here.
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
                                        verbose_name="Title",
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
    avatar_link = models.CharField(max_length=250,
                                   blank=False,
                                   null=False,
                                   verbose_name="Position"
                                   )
    avatar_image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return f'Author: {self.name}, {self.position}'

    def img_preview(self):  # new
        return mark_safe(
            '<img src = "{url}" width = "{width}" height="{height}"/>'.format(
                url=self.avatar_image.url,
                width=300,
                height=300,
            )
        )


class Category(BaseModel):
    id_on_techcrunch = models.CharField(max_length=20,
                                        blank=False,
                                        null=False,
                                        verbose_name="Title",
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
    categories = models.ManyToManyField(
        Category,
        related_name='posts',
        on_delete=models.CASCADE
    )
    authors = models.ManyToManyField(
        Author,
        related_name='posts',
        on_delete=models.CASCADE
    )
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
                            blank=False,
                            null=False,
                            verbose_name="Link",
                            )
    image_link = models.CharField(max_length=250,
                                  blank=False,
                                  null=False,
                                  verbose_name="Image link",
                                  )
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post: {self.title}'

    def img_preview(self):  # new
        return mark_safe(
            '<img src = "{url}" width = "{width}" height="{height}"/>'.format(
                url=self.image.url,
                width=300,
                height=300,
            )
        )


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
                                on_delete=models.CASCADE
                                )
    page_count = models.IntegerField(
        default=settings.TECH_CRUNCH_DEFAULT_SEARCH_PAGE_COUNT,
        blank=False,
        null=False,
        verbose_name="Page count",
    )

    class Meta:
        verbose_name = 'Search By Keyword'
        verbose_name_plural = 'Search By Keywords'

    def __str__(self):
        return f'{self.keyword.title}: {self.page_count}'
