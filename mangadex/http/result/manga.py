class MangaListResult(list):
    def __init__(self, data) -> None:
        super().__init__(data.get('data'))
        self._limit = data.get('limit')
        self._offset = data.get('offset')
        self._total = data.get('total')