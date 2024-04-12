import requests
from requests import Response
from bs4 import BeautifulSoup
import io
from django.conf import settings

from logger import build_logger
import json
from PIL import Image

from models import (
    Post, Category, Author, PostAuthor, PostCategory,
    SearchByKeyword, PostSearchByKeywordItem,
    AutoScrap, AutoScrapPostItem, AutoScrapCategoryItem, AutoScrapAuthorItem
)


def clean_text_from_html(*, html_text: str) -> str:
    sep = ' '
    soup = BeautifulSoup(html_text, features="html.parser")
    return sep.join(soup.strings)


class TechCrunchScraperHandler:
    def __init__(self, url_for_scrap, search_url):
        self.authors_list = list()
        self.categories_list = list()
        self.url_for_scrap = url_for_scrap
        self.url_for_search = search_url
        self.logger = build_logger()
        self.request_failed = False

    def build_url_for_scrape(
            self,
            *,
            field: str = '',
            filter_field: str = '?',
            filter_value: str = '',
            data_per_page: str = '',
            page: str = '',
            envelope: str = '',
            embed: str = ''
    ) -> str:
        url_param_dict = {
            "field": field,
            "filter_field": filter_field,
            "filter_value": filter_value,
            "data_per_page": data_per_page,
            "page": page,
            "envelope": envelope,
            "embed": embed
        }
        return self.url_for_scrap.format(**url_param_dict)

    def build_url_for_search(
            self,
            *,
            keyword: str,
            page: int
    ) -> str:
        url_param_dict = {
            "keyword": keyword,
            "page": page,
        }
        return self.url_for_search.format(**url_param_dict)

    def validate_url_and_request(self,
                                 *,
                                 url: str,
                                 for_json: bool = False) -> Response or None:
        self.request_failed = True
        try:
            if for_json:
                response = requests.get(
                    url,
                    headers={'Accept': 'application/json'},
                    timeout=settings.TIME_OUT
                )
            else:
                response = requests.get(url, timeout=settings.TIME_OUT)

            response.raise_for_status()
            # Raises HTTPError for bad responses

            if response.status_code == 200:
                self.request_failed = False
                # Saving first 200 chars for brevity
                self.logger.info(f"Data fetched successfully for "
                                 f"URL: {url}"
                                 )
                return response

        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred for "
                              f"URL {url}: {http_err}"
                              )
            print(f"HTTP error: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Connection error occurred for "
                              f"URL {url}: {conn_err}"
                              )
            print(f"Connection error: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f"Timeout error occurred for "
                              f"URL {url}: {timeout_err}"
                              )
            print(f"Timeout error: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"General error fetching data for "
                              f"URL {url}: {req_err}"
                              )
            print(f"General error fetching data for "
                  f"URL {url}: {req_err}"
                  )
        except Exception as err:
            self.logger.error(f"An error occur {err}")
            print(f"An error occur {err}")

        return None

    def url_request_for_json(self, *, url: str) -> json:
        while 1:
            try:
                response = self.validate_url_and_request(url=url,
                                                         for_json=True)
                if response is not None:
                    return response.json()
                else:
                    raise Exception("No Response is received from the server")
            except Exception as err:
                self.logger.error(f"Request_for_Json_Error!!!:{err}")

    def url_request(self, *, url: str) -> Response:
        while 1:
            try:
                response = self.validate_url_and_request(url=url,
                                                         for_json=False)
                if response is not None:
                    return response
                else:
                    raise Exception("No Response is received from the server")
            except Exception as err:
                self.logger.error(f"Request_for_Json_Error!!!:{err}")

    def download_image(self, *, download_path: str, image_url: str,
                       file_name) -> None:
        image_content = self.url_request(url=image_url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name + '.png'
        with open(file_path, 'wb') as file:
            image.save(fp=file, format="PNG")
        self.logger.info(
            f'Successfully image saved to {file_path} By the name: {file_name}'
        )

    def scrape_author_page_posts(self, *, author_id: str, page: int) -> list:
        posts_list, _ = self.scrape_items_and_parse(
            item_type=settings.ItemTypes.POST.value,
            attribute=settings.ItemAttributeTypes.AUTHOR.value,
            attribute_value=author_id,
            page=page,
        )
        return posts_list

    def scrape_category_page_posts(self, *, category_id: str,
                                   page: int) -> list[Post]:
        posts_list, _ = self.scrape_items_and_parse(
            item_type=settings.ItemTypes.POST.value,
            attribute=settings.ItemAttributeTypes.CATEGORY.value,
            attribute_value=category_id,
            page=page,
        )
        return posts_list

    def scrape_post_with_slug(self, *, post_slug: str) -> Post:
        post, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.POST.value,
            attribute=settings.ItemAttributeTypes.SLUG.value,
            attribute_value=post_slug,
        )
        return post

    def scrape_category_with_slug(self, *, category_slug: str) -> Category:
        category, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.CATEGORY.value,
            attribute=settings.ItemAttributeTypes.SLUG.value,
            attribute_value=category_slug,
        )
        return category

    def scrape_author_with_slug(self, *, author_slug: str) -> Author:
        author, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.AUTHOR.value,
            attribute=settings.ItemAttributeTypes.SLUG.value,
            attribute_value=author_slug,
        )
        return author

    def scrape_post_with_id(self, *, post_id: str) -> Post:
        post, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.POST.value,
            attribute=settings.ItemAttributeTypes.ID.value,
            attribute_value=post_id,
        )
        return post

    def scrape_category_with_id(self, *, category_id: str) -> Category:
        category, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.CATEGORY.value,
            attribute=settings.ItemAttributeTypes.ID.value,
            attribute_value=category_id,
        )

        return category

    def scrape_author_with_id(self, *, author_id: str) -> Author:
        author, _ = self.scrape_items_and_parse(
            single_item=True,
            item_type=settings.ItemTypes.AUTHOR.value,
            attribute=settings.ItemAttributeTypes.ID.value,
            attribute_value=author_id,
        )
        return author

    def parse_post_detail(self, *, post_json: json) -> tuple:
        id_on_techcrunch = post_json['id']
        slug = post_json['slug']
        title = clean_text_from_html(html_text=post_json['title']['rendered'])
        content = clean_text_from_html(
            html_text=post_json['content']['rendered']
        )
        link = post_json['link']
        image_link = post_json['jetpack_featured_media_url']
        self.download_image(download_path='./source/',
                            image_url=image_link,
                            file_name=slug)

        post, _ = Post.objects.get_or_create(
            id_on_techcrunch=id_on_techcrunch,
            slug=slug,
            title=title,
            content=content,
            link=link,
            image_link=image_link,
        )

        categories_id_list = post_json['categories']
        categories_instances = self.parse_post_categories(
            categories_id_list=categories_id_list
        )
        for category in categories_instances:
            PostCategory.objects.get_or_create(post=post, category=category)

        authors_json_list = post_json['_embedded']['authors']
        authors_instances = self.parse_post_authors(
            authors_json_list=authors_json_list
        )
        for author in authors_instances:
            PostAuthor.objects.get_or_create(post=post, author=author)

        return post, authors_instances, categories_instances

    def parse_post_categories(self, *, categories_id_list: list) -> list:
        categories_instances = list()
        for category_id in categories_id_list:
            category = self.scrape_category_with_id(category_id=category_id)
            categories_instances.append(category)
        return categories_instances

    def parse_post_authors(self, *, authors_json_list: list) -> list:
        authors_instances = list()
        for author_json in authors_json_list:
            author = self.parse_author_detail(author_json=author_json)
            authors_instances.append(author)
        return authors_instances

    def scrape_page_categories(self, *, page: int) -> list[Category]:
        categories_list = self.scrape_items_and_parse(
            item_type=settings.ItemTypes.CATEGORY.value,
            page=page,
        )
        return categories_list

    @staticmethod
    def parse_category_detail(*, category_json: json) -> Category:
        id_on_techcrunch = category_json['id']
        slug = category_json['slug']
        post_count = category_json['count']
        name = category_json['name']
        description = category_json['description']
        link = category_json['link']
        category, _ = Category.objects.get_or_create(
            id_on_techcrunch=id_on_techcrunch,
            slug=slug,
            post_count=post_count,
            name=name,
            description=description,
            link=link,
        )
        return category

    @staticmethod
    def parse_author_detail(*, author_json: json) -> Author:
        id_on_techcrunch = author_json['id']
        slug = author_json['slug']
        name = author_json['name']
        description = author_json['description']
        position = author_json['position']
        link = author_json['link']
        avatar_link = '' if not author_json['cbAvatar'] \
            else author_json['cbAvatar']

        author, _ = Author.objects.get_or_create(
            id_on_techcrunch=id_on_techcrunch,
            slug=slug,
            name=name,
            description=description,
            position=position,
            link=link,
            avatar_link=avatar_link,
        )
        return author

    def scrape_items_and_parse(
            self,
            *,
            single_item: bool = False,
            page: int = 0,
            item_type: str,
            attribute: str = '?',
            attribute_value: int or str = '',
            envelop: str = settings.EnvelopeStatuses.TRUE.value,
            embed: str = settings.EmbedStatuses.NONE.value
    ) -> tuple or Category or Author or list:
        if single_item:
            if attribute not in [settings.ItemAttributeTypes.ID.value,
                                 settings.ItemAttributeTypes.SLUG.value]:
                raise Exception('Single item attribute must be "ID" or "SLUG"')

            if item_type == settings.ItemTypes.POST.value:
                embed = settings.EmbedStatuses.TRUE.value
        item_url = self.build_url_for_scrape(
            field=item_type,
            filter_field=attribute,
            filter_value=attribute_value,
            page='' if single_item or page == 0 else f'&page={page}',
            data_per_page='' if single_item else settings.DATA_PER_PAGE,
            envelope='' if single_item else envelop,
            embed=embed
        )
        data_json = self.url_request_for_json(url=item_url)

        # slug search return a list
        if attribute == settings.ItemAttributeTypes.SLUG.value:
            data_json = data_json[0]

        return self.parse_item_detail(data_json=data_json,
                                      item_type=item_type,
                                      single_item=single_item
                                      )

    def parse_item_detail(
            self,
            *,
            data_json: json,
            item_type: str,
            single_item: bool
    ) -> tuple or Category or Author or list:
        if single_item:
            if item_type == settings.ItemTypes.POST.value:
                return self.parse_post_detail(post_json=data_json)
            elif item_type == settings.ItemTypes.CATEGORY.value:
                return self.parse_category_detail(category_json=data_json)
            elif item_type == settings.ItemTypes.AUTHOR.value:
                return self.parse_author_detail(author_json=data_json)
        else:
            data_list = data_json['body']
            items_list = list()
            for data in data_list:
                if item_type == settings.ItemTypes.POST.value:
                    post_categories_authors = self.parse_post_detail(
                        post_json=data)
                    items_list.append(post_categories_authors)
                elif item_type == settings.ItemTypes.CATEGORY.value:
                    category, _ = self.parse_category_detail(
                        category_json=data)
                    items_list.append(category)
                elif item_type == settings.ItemTypes.AUTHOR.value:
                    author, _ = self.parse_author_detail(author_json=data)
                    items_list.append(author)
            return items_list

    def scrape_page_authors(self, *, page: int) -> list[Author]:
        authors_list, _ = self.scrape_items_and_parse(
            item_type=settings.ItemTypes.AUTHOR.value,
            page=page,
        )
        return authors_list

    def search_by_keyword(self, *,
                          search_by_keyword_instance: SearchByKeyword
                          ) -> list[Post]:
        search_items = list()
        for page in range(1, search_by_keyword_instance.page_count + 1):
            search_url = self.build_url_for_search(
                keyword=search_by_keyword_instance.keyword.title,
                page=page
            )
            response = self.url_request(url=search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features='html.parser')
                search_items += self.extract_search_items(
                    search_by_keyword=search_by_keyword_instance,
                    soup=soup
                )
        searched_posts = list()
        for search_item in search_items:
            searched_posts.append(
                self.scrape_post_with_slug(post_slug=search_item.slug)
            )
        return searched_posts

    def extract_search_items(self,
                             *,
                             search_by_keyword: SearchByKeyword,
                             soup: BeautifulSoup
                             ) -> list[PostSearchByKeywordItem]:
        search_items_list = list()
        post_links_list = soup.findAll(name='a', attrs={'class': 'thmb'})
        for post_link in post_links_list:
            link_parts_list = post_link['href'].split('/')
            title = post_link['title']
            slug = link_parts_list[-2]
            search_item = self.parse_search_item(
                search_by_keyword=search_by_keyword,
                title=title,
                slug=slug,
            )
            search_items_list.append(search_item)
        return search_items_list

    @staticmethod
    def parse_search_item(*,
                          search_by_keyword: SearchByKeyword,
                          title: str,
                          slug: str
                          ) -> PostSearchByKeywordItem:
        return PostSearchByKeywordItem(
            search_by_keyword=search_by_keyword,
            title=title,
            slug=slug
        )

    def auto_scrape_posts_with_category(
            self,
            auto_scrap_post_instance: AutoScrapPostItem,
            category_id: str
    ) -> None:
        posts = list()
        end_page = (auto_scrap_post_instance.auto_scrap.page_start +
                    auto_scrap_post_instance.auto_scrap.page_count + 1)
        if end_page > settings.AutoScrapLastPage.POST:
            end_page = settings.AutoScrapLastPage.POST

        for page in range(auto_scrap_post_instance.auto_scrap.page_start,
                          end_page):
            posts += self.scrape_category_page_posts(category_id=category_id,
                                                     page=page)
        auto_scrap_post_instance.categories = posts
        auto_scrap_post_instance.is_scraped = True

    def auto_scrape_categories(
            self,
            auto_scrap_category_instance: AutoScrapCategoryItem,
    ) -> None:
        categories = list()
        end_page = (auto_scrap_category_instance.auto_scrap.page_start +
                    auto_scrap_category_instance.auto_scrap.page_count + 1)
        if end_page > settings.AutoScrapLastPage.CATEGORY:
            end_page = settings.AutoScrapLastPage.CATEGORY

        for page in range(auto_scrap_category_instance.auto_scrap.page_start,
                          end_page):
            categories += self.scrape_page_categories(page=page)
        auto_scrap_category_instance.categories = categories
        auto_scrap_category_instance.is_scraped = True

    def auto_scrape_authors(
            self,
            auto_scrap_author_instance: AutoScrapAuthorItem,
    ) -> None:
        authors = list()
        end_page = (auto_scrap_author_instance.auto_scrap.page_start +
                    auto_scrap_author_instance.auto_scrap.page_count + 1)
        if end_page > settings.AutoScrapLastPage.AUTHOR:
            end_page = settings.AutoScrapLastPage.AUTHOR

        for page in range(auto_scrap_author_instance.auto_scrap.page_start,
                          end_page):
            authors += self.scrape_page_authors(page=page)
        auto_scrap_author_instance.authors = authors
        auto_scrap_author_instance.is_scraped = True

    @staticmethod
    def auto_scrape_items(
            auto_scrap_instance: AutoScrap
    ) -> None:
        auto_scrap_items = list()
        if auto_scrap_instance.field == settings.ItemTypes.POST:
            auto_scrap_post_instance = AutoScrapPostItem(
                auto_scrap=auto_scrap_instance,
            )
            auto_scrap_items.append(auto_scrap_post_instance)
        elif auto_scrap_instance.field == settings.ItemTypes.CATEGORY:
            auto_scrap_category_instance = AutoScrapCategoryItem(
                auto_scrap=auto_scrap_instance,
            )
            auto_scrap_items.append(auto_scrap_category_instance)
        elif auto_scrap_instance.field == settings.ItemTypes.AUTHOR:
            auto_scrap_author_instance = AutoScrapAuthorItem(
                auto_scrap=auto_scrap_instance,
            )
            auto_scrap_items.append(auto_scrap_author_instance)
