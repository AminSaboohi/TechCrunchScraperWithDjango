from enum import Enum

TEXT_SHOW_MAX_SIZE = 100
TIME_OUT = 30
DATA_PER_PAGE = '&per_page=100'
DEFAULT_SEARCH_PAGE_COUNT = 5
MAXIMUM_SEARCH_PAGE_COUNT = 100
IMAGE_FORMAT = '.png'
MAX_FAIL_COUNT = 2

BASE_URL = 'https://www.techcrunch.com/'
JSON_PATH = 'wp-json/wp/v2/'
URL_FOR_SCRAPE = (BASE_URL + JSON_PATH + '{field}{filter_field}{filter_value}'
                                         '{data_per_page}'
                                         '{page}'
                                         '{envelope}'
                                         '{embed}'
                  )

SEARCH_BASE_URL = 'https://search.techcrunch.com/'
SEARCH_URL = (SEARCH_BASE_URL + 'search?p={keyword}&b={page}1')


class ItemTypes(Enum):
    POST = 'posts'
    CATEGORY = 'categories'
    AUTHOR = 'users'


class ItemAttributeTypes(Enum):
    ID = '/'
    SLUG = '?slug='
    CATEGORY = '?categories='
    NONE = ''


class EnvelopeStatuses(Enum):
    TRUE = '&_envelope=true'
    FALSE = '&_envelope=false'


class EmbedStatuses(Enum):
    TRUE = '&_embed=true'
    FALSE = '&_embed=false'
    NONE = ''


class AutoScrapLastPage(Enum):
    POST = 499
    CATEGORY = 3
    AUTHOR = 7
