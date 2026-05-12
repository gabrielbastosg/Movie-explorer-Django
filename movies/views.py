from django.shortcuts import render
import requests
from decouple import config
API_KEY = config("TMDB_API_KEY")

# Create your views here.
def home(request):
    query = request.GET.get("q")
    genre_id = request.GET.get("genre")

    # Buscar lista de gêneros
    genres_url = (
        f"https://api.themoviedb.org/3/genre/movie/list"
        f"?api_key={API_KEY}&language=pt-BR"
    )
    genres_response = requests.get(genres_url)
    genres = genres_response.json()["genres"]

    # Escolher qual busca fazer
    if query:
        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}&language=pt-BR&query={query}"
        )
    elif genre_id:
        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={API_KEY}&language=pt-BR&with_genres={genre_id}"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/movie/popular"
            f"?api_key={API_KEY}&language=pt-BR"
        )

    response = requests.get(url)
    data = response.json()
    movies = data["results"]

    return render(request, "movies/home.html", {
        "movies": movies,
        "query": query,
        "genres": genres,
        "selected_genre": genre_id,
    })

def movie_detail(request,movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=pt-BR"
    )

    response = requests.get(url)
    movie = response.json()
    return render(request,"movies/movie_detail.html",{
        "movie":movie,
    })


