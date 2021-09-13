from enum import Enum
from typing import Literal, NamedTuple

class MangaStatus(Enum):
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

class _MangaLink:
    def __init__(self, key, url, full_url=True) -> None:
        self.key = key
        self.url = url
        self.full_url = full_url

    def build_url(self, id_or_slug: str):
        pass

class MangaLink(Enum):
    AniList = _MangaLink('al', 'https://anilist.co/manga/{}', False)
    AnimePlanet = _MangaLink('ap', 'https://www.anime-planet.com/manga/{}', False)
    BookWalker = _MangaLink('bw', '	https://bookwalker.jp/{}', False)
    Mangaupdates = _MangaLink('mu', 'https://www.mangaupdates.com/series.html?id={}', False)
    Novelupdates = _MangaLink('nu', 'https://www.novelupdates.com/series/{}', False)