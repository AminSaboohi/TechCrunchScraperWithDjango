from celery import shared_task
from . import constances

from .scraper_handler import TCScraperHandler

from .models import (SearchByKeyword, Keyword,
                     PostSearchByKeywordItem,
                     PostSearchDailyItem)


@shared_task()
def techcrunch_search_by_keyword_task(
        keyword,
        page_count=constances.DEFAULT_SEARCH_PAGE_COUNT,
):
    print(
        f'techcrunch_search_by_keyword_task => {keyword} Started1222')

    keyword, _ = Keyword.objects.get_or_create(
        title=keyword,
    )
    scraper_handler = TCScraperHandler(
        url_for_scrap=constances.URL_FOR_SCRAPE,
        search_url=constances.SEARCH_URL,
    )

    search_by_keyword, _ = SearchByKeyword.objects.get_or_create(
        keyword=keyword,
        page_count=page_count,
    )

    scraped_item_count = scraper_handler.search_by_keyword(
        search_by_keyword_instance=search_by_keyword
    )

    print(
        f'techcrunch_search_by_keyword_task => {keyword}finished')

    return {
        'keyword': keyword.title,
        'page_count': page_count,
        'scraped_item_count': scraped_item_count,
        'status': 'finished',
    }


@shared_task()
def techcrunch_scrape_remain_search_item():
    print('techcrunch_scrape_remain_post_search_item => Started')

    remain_post_search_items = PostSearchByKeywordItem.objects.filter(
        is_scraped=False,
        is_active=True,
    ).all()

    scraper_handler = TCScraperHandler(
        url_for_scrap=constances.URL_FOR_SCRAPE,
        search_url=constances.SEARCH_URL,
    )

    new_scraped_item = list()
    for remain_post_search_item in remain_post_search_items:
        try:
            post, categories, authors = scraper_handler.scrape_post_with_slug(
                post_slug=remain_post_search_item.slug
            )
            remain_post_search_item.post = post
            remain_post_search_item.is_scraped = True
            remain_post_search_item.save()
            new_scraped_item.append(remain_post_search_item)
        except Exception as e:
            remain_post_search_item.fail_count += 1
            remain_post_search_item.save()
            print(f'Error-{remain_post_search_item.fail_count}', e)
            if remain_post_search_item.fail_count > constances.MAX_FAIL_COUNT:
                remain_post_search_item.is_active = False
                remain_post_search_item.save()
            continue

    print(new_scraped_item)

    print('techcrunch_scrape_remain_post_search_item => finished')

    return {
        'new_scraped_item_count': len(new_scraped_item),
        'status': 'finished',
    }


@shared_task()
def techcrunch_scrape_daily_item():
    print('techcrunch_scrape_remain_daily_item => Started')
    scraper_handler = TCScraperHandler(
        url_for_scrap=constances.URL_FOR_SCRAPE,
        search_url=constances.SEARCH_URL,
    )

    scraper_handler.daily_search()
    daily_items = PostSearchDailyItem.objects.filter(
        is_scraped=False,
        is_active=True,
    ).all()
    new_items = list()
    for daily_item in daily_items:
        try:
            post, categories, authors = scraper_handler.scrape_post_with_slug(
                post_slug=daily_item.slug
            )
            daily_item.post = post
            daily_item.is_scraped = True
            daily_item.save()
            new_items.append(daily_item)
        except Exception as e:
            daily_item.fail_count += 1
            daily_item.save()
            print(f'Error-{daily_item.fail_count}', e)
            if daily_item.fail_count > constances.MAX_FAIL_COUNT:
                daily_item.is_active = False
                daily_item.save()
            continue

    print(new_items)

    print('techcrunch_scrape_remain_book_search_item => finished')

    return {
        'new_scraped_item_count': len(new_items),
        'status': 'finished',
    }


@shared_task()
def techcrunch_scrape_remain_auto_scrap_item():
    pass

# celery -A techcrunch_scraper_with_django worker -l INFO -P eventlet
# celery -A techcrunch_scraper_with_django beat --loglevel=INFO
