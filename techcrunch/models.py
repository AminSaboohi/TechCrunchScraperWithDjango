from abc import abstractmethod
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

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
    user = models.ForeignKey(User,
                             related_name='searches',
                             on_delete=models.PROTECT,
                             verbose_name="User",
                             )
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
        return f'{self.user} searches {self.keyword.title}: {self.page_count}'


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

    class Meta:
        verbose_name = 'Post Search By Keyword Item'
        verbose_name_plural = 'Post Search By Keyword Items'

    def __str__(self):
        return f'Post Search By Keyword : slug = {self.slug}'


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
        verbose_name='Posts'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
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
        verbose_name='Categories'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
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
        verbose_name='Authors'
    )
    is_scraped = models.BooleanField(default=False,
                                     blank=False,
                                     null=False,
                                     verbose_name="Is scraped",
                                     )

    class Meta:
        verbose_name = 'Auto Scrap Author Item'
        verbose_name_plural = 'Auto Scrap Author Items'

    def __str__(self):
        return (f'Auto Scrap Author : field = {self.auto_scrap.field} ,'
                f' {self.auto_scrap.page_count}pages')
