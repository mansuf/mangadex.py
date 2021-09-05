import re
import uuid
from typing import Awaitable, Coroutine, Dict, List, Literal, Union
from datetime import datetime
from .types import *

class BaseRoute:
    BASE = 'https://api.mangadex.org'

    def build_request(self):
        raise NotImplementedError()

class GET:
    method = 'GET'

class POST:
    method = 'POST'

class PUT:
    method = 'PUT'

class DEL:
    method = 'DEL'

class MangaList(BaseRoute, GET):
    def __init__(
        self,
        limit: int = 10,
        offset: int = None,
        title: str = None,
        authors: List[str] = None,
        artists: List[str] = None,
        year: int = None,
        included_tags: List[str] = None,
        included_tags_mode: Literal['AND', 'OR'] = 'AND',
        excluded_tags: List[str] = None,
        excluded_tags_mode: Literal['AND', 'OR'] = 'OR',
        status: Literal[
            MangaStatus.ONGOING,
            MangaStatus.COMPLETED,
            MangaStatus.PAUSED,
            MangaStatus.CANCELLED
        ] = None,
        original_language: List[_mangadex_languages] = None,
        excluded_original_language: List[_mangadex_languages] = None,
        available_original_language: List[_mangadex_languages] = None,
        ids: List[str] = None,
        content_rating: List[Literal[
            ContentRating.SAFE,
            ContentRating.SUGGESTIVE,
            ContentRating.EROTICA,
            ContentRating.PORNOGRAPHIC
        ]] = [ContentRating.SAFE, ContentRating.SUGGESTIVE, ContentRating.EROTICA],
        created_at_since: Union[datetime, str] = None,
        updated_at_since: Union[datetime, str] = None,
        order: MangaListOrder = None,
        includes: List[Literal[
            Relationship.MANGA,
            Relationship.CHAPTER,
            Relationship.COVER_ART,
            Relationship.AUTHOR,
            Relationship.ARTIST,
            Relationship.SCANLATION_GROUP,
            Relationship.TAG,
            Relationship.USER,
            Relationship.CUSTOM_LIST
        ]] = None,
    ) -> None:
        # verify limit
        if not isinstance(limit, int):
            raise ValueError('limit must be int')
        self.limit = limit
        
        # verify offset
        if offset:
            if not isinstance(offset, int):
                raise ValueError('offset must be int')
        self.offset = offset
        
        # verify title
        if title:
            if not isinstance(title, str):
                raise ValueError('title must be str')
        self.title = title

        # verify authors
        if authors:
            if isinstance(authors, list) or isinstance(authors, tuple):
                for pos in range(len(authors)):
                    author = authors[pos]
                    if not isinstance(author, str):
                        raise ValueError('authors[%s] is not str' % pos)
            else:
                raise ValueError('authors must be list or tuple')
        self.authors = authors

        # verify artists
        if artists:
            if isinstance(artists, list) or isinstance(artists, tuple):
                for pos in range(len(artists)):
                    artist = artists[pos]
                    if not isinstance(artist, str):
                        raise ValueError('artists[%s] is not a str' % pos)
            else:
                raise ValueError('artists must be list or tuple')
        self.artists = artists
        
        # verify year
        if year:
            if not isinstance(year, int):
                raise ValueError('year must be int')
        self.year = year

        # verify included_tags
        if included_tags:
            if isinstance(included_tags, list) or isinstance(included_tags, tuple):
                for pos in range(len(included_tags)):
                    included_tag = included_tags[pos]
                    try:
                        uuid.UUID(included_tag, version=4)
                    except ValueError:
                        raise ValueError('included_tags[%s] is not a uuid' % pos) from None
            else:
                raise ValueError('included_tags must be list or tuple')
        self.included_tags = included_tags
        
        # verify included_tags_mode
        if included_tags_mode not in ['AND', 'OR']:
            raise ValueError('included_tags_mode must be "AND" or "OR"')
        self.included_tags_mode = included_tags_mode
        
        # verify excluded_tags
        if excluded_tags:
            if isinstance(excluded_tags, list) or isinstance(excluded_tags, tuple):
                for pos in range(len(excluded_tags)):
                    excluded_tag = excluded_tags[pos]
                    try:
                        uuid.UUID(excluded_tag, version=4)
                    except ValueError:
                        raise ValueError('excluded_tags[%s] is not a uuid' % pos) from None
            else:
                raise ValueError('excluded_tags must be list or tuple')
        self.excluded_tags = excluded_tags
        
        # verify excluded_tags_mode
        if excluded_tags_mode not in ['AND', 'OR']:
            raise ValueError('excluded_tags_mode must be "AND" or "OR"')
        self.excluded_tags_mode = excluded_tags_mode
        
        # verify status
        if status:
            if isinstance(status, MangaStatus):
                pass
            elif isinstance(status, str):
                if status not in list(i.value for i in MangaStatus):
                    raise ValueError('Invalid manga status')
            else:
                raise ValueError('status must be MangaStatus or str')
        self.status = status

        langs = list(i.value for i in MangaDexLanguage)

        # verify original_language
        if original_language:
            if isinstance(original_language, MangaDexLanguage):
                pass
            elif isinstance(original_language, str):
                if original_language not in langs:
                    raise ValueError('Invalid language')
            else:
                raise ValueError('original_language must be MangaDexLanguage or str')
        self.original_language = original_language

        # verify excluded_original_language
        if excluded_original_language:
            if isinstance(excluded_original_language, MangaDexLanguage):
                pass
            elif isinstance(excluded_original_language, str):
                if excluded_original_language not in langs:
                    raise ValueError('Invalid language')
            else:
                raise ValueError('excluded_original_language must be MangaDexLanguage or str')
        self.excluded_original_language = excluded_original_language

        # verify available_original_language
        if available_original_language:
            if isinstance(available_original_language, MangaDexLanguage):
                pass
            elif isinstance(available_original_language, str):
                if available_original_language not in langs:
                    raise ValueError('Invalid language')
            else:
                raise ValueError('available_original_language must be MangaDexLanguage or str')
        self.available_original_language = available_original_language

        # verify ids
        if ids:
            if not isinstance(ids, list):
                raise ValueError('ids must be list or tuple')
            else:
                for pos in range(len(ids)):
                    _id = ids[pos]
                    try:
                        uuid.UUID(_id, version=4)
                    except ValueError:
                        raise ValueError('ids[%s] is not uuid' % _id)
        self.ids = ids

        # verify content_rating
        if isinstance(content_rating, list) or isinstance(content_rating, tuple):
            c_rating_values = list(i.value for i in content_rating)
            for pos in range(len(content_rating)):
                cr = content_rating[pos]
                if isinstance(cr, ContentRating):
                    pass
                elif isinstance(cr, str):
                    if cr not in c_rating_values:
                        raise ValueError('content_rating[%s] is not valid content rating' % pos)
                else:
                    raise ValueError('content_rating must be ContentRating or str')
        else:
            raise ValueError('content_rating must be list or tuple')
        self.content_rating = content_rating

        re_datetime = re.compile(r'^\d{4}-[0-1]\d-([0-2]\d|3[0-1])T([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d$')

        # verify created_at_since
        if created_at_since:
            if isinstance(created_at_since, datetime):
                pass
            elif isinstance(created_at_since, str):
                result = re_datetime.match(created_at_since)
                if not result:
                    raise ValueError('"%s" is not valid datetime string' % result)
            else:
                raise ValueError('created_at_since must be datetime or str')
        self.created_at_since = created_at_since

        # verify updated_at_since
        if updated_at_since:
            if isinstance(updated_at_since, datetime):
                pass
            elif isinstance(updated_at_since, str):
                result = re_datetime.match(updated_at_since)
                if not result:
                    raise ValueError('"%s" is not valid datetime string' % result)
            else:
                raise ValueError('updated_at_since must be datetime or str')
        self.updated_at_since = updated_at_since

        # verify order
        if not isinstance(order, MangaListOrder):
            raise ValueError('order must be a MangaListOrder')
        
        # verify includes
        if includes:
            if isinstance(includes, list) or isinstance(includes, tuple):
                include_values = list(i.value for i in includes)
                for pos in range(len(includes)):
                    include = includes[pos]
                    if isinstance(include, ContentRating):
                        pass
                    elif isinstance(include, str):
                        if include not in include_values:
                            raise ValueError('includes[%s] is not valid content rating' % pos)
                    else:
                        raise ValueError('includes must be ContentRating or str')
            else:
                raise ValueError('includes must be list or tuple')
            self.includes = includes
