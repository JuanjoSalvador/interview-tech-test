from api.auth.views import LoginView
from api.router.api_route import APIRoute
from app.movies.views import MoviesView

URLS = [
    APIRoute("/login", LoginView),
    APIRoute("/api/v1/movies/", MoviesView),
    APIRoute("/api/v1/movies/{movie_id}/", MoviesView),
]
