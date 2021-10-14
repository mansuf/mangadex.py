from .types.manga import Title

class Manga:
    def __init__(self, data, http) -> None:
        self._id = data.get('id')
        self._type = data.get('type')
        self._http = http
        self._data = data.get('attributes')

        self.title = Title(self._data.get('title'))
        self.alternative_titles = [Title(i) for i in self._data.get('altTitles')]
    
    def __repr__(self) -> str:
        return '<Manga title="%s">' % (
            self.title
        )