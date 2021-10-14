import uuid
from enum import Enum
from .base import MangaDexLanguage
from ..errors import ConverterError

class Status(Enum):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    PAUSED = 'hiatus'
    CANCELLED = 'cancelled'

class ContentRating(Enum):
    SAFE = 'safe'
    SUGGESTIVE = 'suggestive'
    EROTICA = 'erotica'
    PORNOGRAPHIC = 'pornographic'

class PublicationDemographic(Enum):
    SHOUJO = 'shoujo'
    SHOUNEN = 'shounen'
    JOSEI = 'josei'
    SEINEN = 'seinen'
    NONE = 'none'

class Relationship(Enum):
    MANGA = 'manga'
    CHAPTER = 'chapter'
    COVER_ART = 'cover_art'
    AUTHOR = 'author'
    ARTIST = 'artist'
    SCANLATION_GROUP = 'scanlation_group'
    TAG = 'tag'
    USER = 'user'
    CUSTOM_LIST = 'custom_list'

class LinkData:
    int_conv = lambda x: str(int(x))

    # Each REFS (References) has key, name, url, and converters
    REFS = [
        [
            'al',
            'AniList',
            'https://anilist.co/manga/{}',
            [int_conv]
        ],
        [
            'ap',
            'AnimePlanet',
            'https://www.anime-planet.com/manga/{}',
            [str]
        ],
        [
            'bw',
            'BookWalker',
            'https://bookwalker.jp/{}',
            [
                lambda x: 'series/%s' % int(x), # If integer, then the url path will be extended to series
                lambda x: str(uuid.UUID(x, version=4)) # Make sure we check valid UUID
            ]
        ],
        [
            'mu',
            'Mangaupdates',
            'https://www.mangaupdates.com/series.html?id={}',
            [int_conv]
        ],
        [
            'nu',
            'Novelupdates',
            'https://www.novelupdates.com/series/{}',
            [str]
        ],
        [
            'kt',
            'Kitsu',
            'https://kitsu.io/api/edge/manga{}',
            [
                lambda x: '/%s' % int_conv(x),
                lambda x: '?filter[slug]=%s' % x
            ]
        ],
        [
            'amz',
            'Amazon',
            '{}',
            [str]
        ],
        [
            'ebj',
            'eBookJapan',
            '{}',
            [str]
        ],
        [
            'mal',
            'MyAnimeList',
            'https://myanimelist.net/manga/{}',
            [int_conv]
        ],
        [
            'cdj',
            'CDJapan',
            '{}',
            [str]
        ],
        [
            'raw',
            'Raw', # We don't know the source is, so we leave it empty
            '{}',
            [str]
        ],
        [
            'engtl',
            'English Licensed', # We don't know the source is, so we leave it empty
            '{}',
            [str]
        ]
    ]

    def __init__(self, site, slug_or_id) -> None:
        for key, name, url, converters in self.REFS:
            if key == site:
                break
        
        self.name = name
        self.key_site = key
        self.slug_or_id = slug_or_id
        
        exceptions = []
        for converter in converters:
            try:
                self.url = url.format(converter(slug_or_id))
            except Exception as e:
                exceptions.append(e)
        if exceptions:
            raise ConverterError('converter is failing, %s' % exceptions)

    def __str__(self) -> str:
        return '<MangaLinkData source="%s" link="%s">' % (
            self.name,
            self.url
        )

    def get_link(self) -> str:
        return self.url

class Title:
    def __init__(self, data) -> None:
        lang = list(data.keys())[0]
        self.language = MangaDexLanguage(lang)
        self.title = data.get(lang)

    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return self.title