from typing import Literal, Union
from ..types import MangaDexLanguage

# For typing 
_mangalist_order = Literal['asc', 'desc']

class MangaListOrder:
    def __init__(
        self,
        title: _mangalist_order = None,
        year: _mangalist_order = None,
        created_at: _mangalist_order = None,
        updated_at: _mangalist_order = None, 
        latest_uploaded_chapter: _mangalist_order = 'desc',
        followed_count: _mangalist_order = None,
        relevance: _mangalist_order = None
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

class MangaTitles:
    def __init__(self, title: str, language: MangaDexLanguage = MangaDexLanguage.English) -> None:
        self.titles = {language: title}

    def add_title(self, title: str, language: MangaDexLanguage):
        self.titles[language] = title
    
    def getvalue(self):
        titles = {}
        for lang, title in self.titles.items():
            titles[lang.value] = title
        return titles

class MangaDescriptions:
    def __init__(self, desc: str, language: MangaDexLanguage = MangaDexLanguage.English) -> None:
        self.descriptions = {language: desc}
    
    def add_description(self, desc: str, language: MangaDexLanguage):
        self.descriptions[language] = desc

    def getvalue(self):
        descriptions = {}
        for lang, desc in self.descriptions:
            descriptions[lang.value] = desc
        return descriptions

class MangaLinks:
    def __init__(self) -> None:
        self.links = {}
    