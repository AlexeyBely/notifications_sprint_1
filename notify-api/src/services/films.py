import aiohttp
from urllib.parse import urlencode

from core.config import settings


class MovieFilms():
    """Read films from movies service."""

    def __init__(self):
        pass

    async def read_info_films(self) -> list | None:
        """Reading and organizing films."""
        movie_films = await self._read_movie_films()
        return movie_films        

    async def _read_movie_films(self) -> list:
        async with aiohttp.ClientSession() as session:
            query = urlencode({'page': 1,
                               'size': 4,
                               'sort': 'imdb_rating:desc'})
            url = f'{settings.api_films_url}?{query}'
            async with session.get(url) as response:
                data_films = await response.json()
            films = data_films['data']
            film_info = []

            for film in films:
                id_film = film['id']
                url = f'{settings.api_films_url}{id_film}'
                async with session.get(url) as response:
                    data_film = await response.json()
                info = {
                    'title': data_film['title'],
                    'description': data_film['description'],
                    'genre': data_film['genre'],
                    'rating': data_film['imdb_rating'],
                }    
                film_info.append(info)
        return film_info 
    

def get_movie_films_service() -> MovieFilms:
    """interface and movie service connectivity."""
    return MovieFilms()