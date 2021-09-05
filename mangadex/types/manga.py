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

class MangaListOrder:
    def __init__(
        self,
        title: Literal['asc', 'desc'] = None,
        year: Literal['asc', 'desc'] = None,
        created_at: Literal['asc', 'desc'] = None,
        updated_at: Literal['asc', 'desc'] = None, 
        latest_uploaded_chapter: Literal['asc', 'desc'] = 'desc',
        followed_count: Literal['asc', 'desc'] = None,
        relevance: Literal['asc', 'desc'] = None
    ) -> None:
        params = {}
        
        if title:
            params['title'] = title
        
        if year:
            params['year'] = year

        if created_at:
            params['createdAt'] = created_at

        if updated_at:
            params['updatedAt'] = updated_at
        
        if latest_uploaded_chapter:
            params['latestUploadedChapter'] = latest_uploaded_chapter

        if followed_count:
            params['followedCount'] = followed_count
        
        if relevance:
            params['relevance'] = relevance

        self.params = params

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