import re
import uuid

from typing import List, Literal, Union
from datetime import datetime
from .base import * 
from ..types import *
from ..utils import *

__all__ = (
    'MangaList',
)

class MangaList(GET):
    path = '/manga'

    def __init__(
        self,
        limit,
        offset,
        title,
        authors,
        artists,
        year,
        included_tags,
        included_tags_mode,
        excluded_tags,
        excluded_tags_mode,
        status,
        original_language,
        excluded_original_language,
        available_translated_language,
        ids,
        content_rating,
        created_at_since,
        updated_at_since,
        order,
        includes,
    ) -> None:
        # verify limit
        if not isinstance(limit, int):
            raise ValueError('limit must be int')
        elif limit > 100 or limit <= 0:
            raise ValueError('limit range must from 1 to 100')
        self.limit = limit
        
        # verify offset
        if offset:
            if not isinstance(offset, int):
                raise ValueError('offset must be int')
            elif offset <= 0:
                raise ValueError('offset cannot lower than 0')
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
            if isinstance(status, Status):
                pass
            elif isinstance(status, str):
                if status not in list(i.value for i in Status):
                    raise ValueError('Invalid manga status')
            else:
                raise ValueError('status must be MangaStatus or str')
        self.status = status

        langs = list(i.value for i in MangaDexLanguage)

        # verify original_language
        if original_language:
            if isinstance(original_language, list) or isinstance(original_language, tuple):
                for pos in range(len(original_language)):
                    lang = original_language[pos]
                    if isinstance(lang, MangaDexLanguage):
                        pass
                    elif isinstance(lang, str):
                        if lang not in langs:
                            raise ValueError('original_language[%s] is not valid language' % pos)
                    else:
                        raise ValueError('original_language[%s] must be MangaDexLanguage or str' % pos)
            else:
                raise ValueError('original_language must be tuple or list')
        self.original_language = original_language

        # verify excluded_original_language
        if excluded_original_language:
            if isinstance(excluded_original_language, list) or isinstance(excluded_original_language, tuple):
                for pos in range(len(excluded_original_language)):
                    lang = excluded_original_language[pos]
                    if isinstance(lang, MangaDexLanguage):
                        pass
                    elif isinstance(lang, str):
                        if lang not in langs:
                            raise ValueError('excluded_original_language[%s] is not valid language' % pos)
                    else:
                        raise ValueError('excluded_original_language[%s] must be MangaDexLanguage or str' % pos)
            else:
                raise ValueError('excluded_original_language must be tuple or list')
        self.excluded_original_language = excluded_original_language

        # verify available_translated_language
        if available_translated_language:
            if isinstance(available_translated_language, list) or isinstance(available_translated_language, tuple):
                for pos in range(len(available_translated_language)):
                    lang = available_translated_language[pos]
                    if isinstance(lang, MangaDexLanguage):
                        pass
                    elif isinstance(lang, str):
                        if lang not in langs:
                            raise ValueError('available_translated_language[%s] is not valid language' % pos)
                    else:
                        raise ValueError('available_translated_language[%s] must be MangaDexLanguage or str' % pos)
            else:
                raise ValueError('available_translated_language must be tuple or list')
        self.available_translated_language = available_translated_language

        # verify ids
        if ids:
            if not isinstance(ids, list):
                raise ValueError('ids must be list or tuple')
            else:
                if len(ids) > 100:
                    raise ValueError('ids cannot be more than 100')
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
        if order:
            if not isinstance(order, MangaListOrder):
                raise ValueError('order must be a MangaListOrder')
        self.order = order
        
        # verify includes
        if includes:
            if isinstance(includes, list) or isinstance(includes, tuple):
                include_values = list(i.value for i in includes)
                for pos in range(len(includes)):
                    include = includes[pos]
                    if isinstance(include, Relationship):
                        pass
                    elif isinstance(include, str):
                        if include not in include_values:
                            raise ValueError('includes[%s] is not valid Relationship' % pos)
                    else:
                        raise ValueError('includes[%s] must be Relationship or str' % pos)
            else:
                raise ValueError('includes must be list or tuple')
        self.includes = includes

    def build_request(self) -> dict:
        request_param = super().build_request(self.path)
        param = {}
        request_param['params'] = param

        param['limit'] = self.limit

        if self.offset:
            param['offset'] = self.offset
        
        if self.title:
            param['title'] = self.title
        
        if self.authors:
            param['authors[]'] = self.authors
        
        if self.artists:
            param['artists[]'] = self.artists

        if self.year:
            param['year'] = self.year
        
        if self.included_tags:
            param['includedTags[]'] = self.included_tags

        param['includedTagsMode'] = self.included_tags_mode

        if self.excluded_tags:
            param['excludedTags[]'] = self.excluded_tags
        
        param['excludedTagsMode'] = self.excluded_tags_mode

        if self.status:
            param['status[]'] = self.status
        
        original_lang = []
        if self.original_language:
            for lang in self.original_language:
                if isinstance(lang, MangaDexLanguage):
                    original_lang.append(lang.value)
                else: # str instance
                    original_lang.append(lang)
            param['originalLanguage[]'] = original_lang

        excluded_original_lang = []
        if self.excluded_original_language:
            for lang in self.excluded_original_language:
                if isinstance(lang, MangaDexLanguage):
                    excluded_original_lang.append(lang.value)
                else: # str instance
                    excluded_original_lang.append(lang)
            param['excludedOriginalLanguage[]'] = self.excluded_original_language
        
        available_translated_lang = []
        if self.available_translated_language:
            for lang in self.available_translated_language:
                if isinstance(lang, MangaDexLanguage):
                    available_translated_lang.append(lang.value)
                else:
                    available_translated_lang.append(lang)
            param['availableTranslatedLanguage[]'] = self.available_translated_language
        
        if self.ids:
            param['ids[]'] = self.ids
        
        content_ratings = []
        for content_rating in self.content_rating:
            if isinstance(content_rating, ContentRating):
                content_ratings.append(content_rating.value)
            else: # str instance
                content_ratings.append(content_rating)
        param['contentRating[]'] = content_ratings

        if self.created_at_since:
            if isinstance(self.created_at_since, datetime):
                created_at_since = self.created_at_since.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                created_at_since = self.created_at_since
            param['createdAtSince'] = created_at_since
        
        if self.updated_at_since:
            if isinstance(self.updated_at_since, datetime):
                updated_at_since = self.updated_at_since.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                updated_at_since = self.updated_at_since
            param['updatedAtSince'] = updated_at_since
        
        if self.order:
            param['order'] = self.order.params
        
        includes = []
        if self.includes:
            for include in includes:
                if isinstance(include, Relationship):
                    includes.append(include.value)
                else: # str instance
                    includes.append(include)
            param['includes[]'] = includes

        return request_param

class CreateManga(POST, RequireLogin):
    def __init__() -> None:
        raise NotImplementedError