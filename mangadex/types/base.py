from enum import Enum
from typing import Literal

# Adapted from https://github.com/tachiyomiorg/tachiyomi-extensions/blob/master/src/all/mangadex/src/eu/kanade/tachiyomi/extension/all/mangadex/MangaDexFactory.kt#L54-L95
class MangaDexLanguage(Enum):
    English = 'en'
    Japanese = 'ja'
    Polish = 'pl'
    SerboCroatian = 'sh'
    Dutch = 'nl'
    Italian = 'it'
    Russian = 'ru'
    German = 'de'
    Hungarian = 'hu'
    French = 'fr'
    Finnish = 'fi'
    Vietnamese = 'vi'
    Greek = 'el'
    Bulgarian = 'bg'
    SpanishSpain = 'es'
    PortugueseBrazil = 'pt-br'
    PortuguesePortugal = 'pt'
    Swedish = 'sv'
    Arabic = 'ar'
    Danish = 'da'
    ChineseSimplified = 'zh'
    Bengali = 'bn'
    Romanian = 'ro'
    Czech = 'cs'
    Mongolian = 'mn'
    Turkish = 'tr'
    Indonesian = 'id'
    Korean = 'ko'
    SpanishLTAM = 'es-la'
    Persian = 'fa'
    Malay = 'ms'
    Thai = 'th'
    Catalan = 'ca'
    Filipino = 'tl'
    ChineseTraditional = 'zh-hk'
    Ukrainian = 'uk'
    Burmese = 'my'
    Lithuanian = 'lt'
    Hebrew = 'he'
    Hindi = 'hi'
    Norwegian = 'no'
    Other = None

# For typing
_mangadex_languages: Literal[
    MangaDexLanguage.English,
    MangaDexLanguage.Japanese,
    MangaDexLanguage.Polish,
    MangaDexLanguage.SerboCroatian,
    MangaDexLanguage.Dutch,
    MangaDexLanguage.Italian,
    MangaDexLanguage.Russian,
    MangaDexLanguage.German,
    MangaDexLanguage.Hungarian,
    MangaDexLanguage.French,
    MangaDexLanguage.Finnish,
    MangaDexLanguage.Vietnamese,
    MangaDexLanguage.Greek,
    MangaDexLanguage.Bulgarian,
    MangaDexLanguage.SpanishSpain,
    MangaDexLanguage.PortugueseBrazil,
    MangaDexLanguage.PortuguesePortugal,
    MangaDexLanguage.Swedish,
    MangaDexLanguage.Arabic,
    MangaDexLanguage.Danish,
    MangaDexLanguage.ChineseSimplified,
    MangaDexLanguage.Bengali,
    MangaDexLanguage.Romanian,
    MangaDexLanguage.Czech,
    MangaDexLanguage.Mongolian,
    MangaDexLanguage.Turkish,
    MangaDexLanguage.Indonesian,
    MangaDexLanguage.Korean,
    MangaDexLanguage.SpanishLTAM,
    MangaDexLanguage.Persian,
    MangaDexLanguage.Malay,
    MangaDexLanguage.Thai,
    MangaDexLanguage.Catalan,
    MangaDexLanguage.Filipino,
    MangaDexLanguage.ChineseTraditional,
    MangaDexLanguage.Ukrainian,
    MangaDexLanguage.Burmese,
    MangaDexLanguage.Lithuanian,
    MangaDexLanguage.Hebrew,
    MangaDexLanguage.Hindi,
    MangaDexLanguage.Norwegian,
    MangaDexLanguage.Other
]