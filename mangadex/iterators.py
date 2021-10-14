import asyncio
from typing import List
from .manga import Manga

# According to https://api.mangadex.org/docs.html#section/Result-Limit
RESULT_LIMIT_MANGA = 10000

class MangaIterator:
    def __init__(self, **kwargs) -> None:
        self._limit = kwargs.pop('limit')
        self._http = kwargs.pop('http')
        self._offset = 0
        self._kwargs = kwargs
        self._queue = asyncio.Queue()

    def __aiter__(self) -> "MangaIterator":
        return self
    
    async def __anext__(self) -> Manga:
        if self._queue.empty():
            await self._fill_data()
        
        try:
            return self._queue.get_nowait()
        except asyncio.QueueEmpty:
            raise StopAsyncIteration()

    async def flatten(self) -> List[Manga]:
        mangas = []
        while True:
            try:
                manga = await self.__anext__()
            except StopAsyncIteration:
                return mangas
            else:
                mangas.append(manga)

    async def _fill_data(self):
        if self._limit > 0:
            kwargs = self._kwargs.copy()
            limit = self._limit if self._limit <= 100 else 100
            kwargs['limit'] = limit
            kwargs['offset'] = self._offset

            data = await self._http.manga_list(**kwargs)
            if data:
                self._limit -= limit
                self._offset += limit
                for item in data:
                    await self._queue.put(Manga(item, self._http))